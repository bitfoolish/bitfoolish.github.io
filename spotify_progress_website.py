import os
from dotenv import load_dotenv, dotenv_values 
import string, secrets, hashlib, base64
import urllib.parse, webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import sys
import json

load_dotenv() 
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
redir_url = os.getenv("redirect_url", "http://127.0.0.1:8080/callback")
liked_songs_playlist_url = os.getenv("liked_songs_playlist_url", "https://api.spotify.com/v1/me/tracks?limit=50")
completed_playlist_id = os.getenv("COMPLETED_PLAYLIST_ID")


if not CLIENT_ID or not completed_playlist_id:
    print("Missing required environment variables.")
    sys.exit(1)

captured_code = "N/A"

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        if "code" in params:
            captured_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
    
    def log_message(self, format, *args):
        return

server = HTTPServer(("127.0.0.1", 8080), CallbackHandler)


def gen_code_verifier():
    alphabet = string.ascii_letters + string.digits
    code_verifier = ''.join(secrets.choice(alphabet) for _ in range(64))
    return code_verifier

# hash via SHA-256
def gen_code_challenge(code_verifier):
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
    return code_challenge

code_verifier = gen_code_verifier()
code_challenge = gen_code_challenge(code_verifier)
scope = "user-library-read playlist-read-private"

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "scope": scope,
    "code_challenge_method": "S256",
    "code_challenge": code_challenge,
    "redirect_uri": redir_url,
}

base_auth_url = "https://accounts.spotify.com/authorize"
auth_url = f"{base_auth_url}?{urllib.parse.urlencode(params)}"

webbrowser.open(auth_url)
server.handle_request()

if not captured_code or captured_code == "N/A":
    print("Failed to capture authorisation code.")
    sys.exit(1)

print("Captured authorisation code successfully.")

## exchange code for access token
token_url = "https://accounts.spotify.com/api/token"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {
    'client_id': CLIENT_ID,
    'grant_type': 'authorization_code',
    'code': captured_code,
    'redirect_uri': redir_url,
    'code_verifier': code_verifier
}
x = requests.post(token_url, headers=headers, data=payload)
data = x.json()
access_token = data.get("access_token")
refresh_token = data.get("refresh_token")

headers = {"Authorization": f"Bearer {access_token}"}

songs_assigned = set() # track IDs of songs inside liked
total_tracks = 0
total_assgn_tracks = 0

completed_playlist_url = f"https://api.spotify.com/v1/playlists/{completed_playlist_id}/items?limit=100"
while completed_playlist_url:
    res = requests.get(completed_playlist_url, headers=headers).json()
    if "items" not in res:
        print("Error fetching playlist: ", res)
        break

    for item in res["items"]:
        track = item.get("item")
        if track:
            songs_assigned.add(track.get("id"))
    completed_playlist_url = res.get("next")

print("Assigned songs length: ", len(songs_assigned))

while liked_songs_playlist_url:
    res = requests.get(liked_songs_playlist_url, headers=headers).json()
    
    if "items" not in res:
        print("Error:", res)
        break
        
    for item in res["items"]:
        track = item.get("track")
        if track:
            total_tracks += 1
            if (track.get("id")) in songs_assigned:
                total_assgn_tracks += 1
    liked_songs_playlist_url = res.get("next")  # Pagination to fetch all liked songs


print(f"Total Liked Songs: {total_tracks}")
try:
    completion_pcntg = (total_assgn_tracks / total_tracks) * 100
    print(f"Completion Percentage: {completion_pcntg:.2f}%")
    stats = {
        "total_liked": total_tracks,
        "total_assigned": total_assgn_tracks,
        "percentage": round(completion_pcntg, 2),
    }
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("Saved stats to stats.json")
except ZeroDivisionError:
    print("Error: 0 tracks have been assigned to done")