import NavbarTop from "./components/Navbar";
import { Outlet } from "react-router-dom";

export function Layout(){
    return(
        <>
            <NavbarTop/>
            <main>
                <Outlet/>
            </main>
        </>
    )
}