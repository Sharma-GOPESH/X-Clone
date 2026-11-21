import React from "react";
import {NavLink} from "react-router"
import "./home.css"
function Home(){
    return(
        <>
         <div id="wlcm">
        <h1 id="home">Welcome</h1>
        <div id="user-page">
            <NavLink to="/Register_user" id="nav-1">Sign-up</NavLink>
            <NavLink to="/login" id="nav-1">Sign-in</NavLink>
        </div>
        </div>
        </>
    )
}

export default Home