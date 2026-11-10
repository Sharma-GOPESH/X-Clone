import React from "react"
import {NavLink } from "react-router"

function Login_user(){
       return(
        <>
            <form>      
    <div id="main">
        <h1 id="header_title">See What's Happening</h1>
        <h4 id="heading">Login</h4>
        <div id="email">
            <input type="text" id="inpt_email" placeholder="Email"></input>
       </div>
       <div id="pass">
        <input type="text" id="inpt_pass" placeholder="Password"></input>
       </div>
       <button  type="submit" id="Submit_buttpn">Continue</button>
       <div id="login_box">
        <h5>Do not have an account?</h5>
        <NavLink to="/Register_user">Register Yourself</NavLink>
        </div>       
    </div>
    
    </form>
        </>
       )
}

export default Login_user