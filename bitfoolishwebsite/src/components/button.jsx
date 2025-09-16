function MyButton(){
  const name = "Jim"
  return (
    <div>
      <button>I am a button called {name}</button>
      <button onClick={
        ()=>{
          alert("Hello")
        }  
      }>Click me</button>
    </div>
  );
}

export default MyButton;