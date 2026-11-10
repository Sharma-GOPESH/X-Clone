import React from "react"
import { useState } from "react"
import './Register_users.css'
import { BrowserRouter, Routes, Route,NavLink } from "react-router"

function Register_user(){
     const [Form , setForm] = useState({"email":"", "password":"", "username":""})
      const [Response, setResponse] = useState("")

    const handle_change =(e)=>{
       setForm({...Form, [e.target.name]:e.target.value})
    }  
    const sent_data = async() =>{
      const res = await fetch("http://127.0.0.1:8000/users",{
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body : JSON.stringify(Form)
      }).then(res => res.json())
      .then(data => setResponse(data))
      .catch(err =>console.error(err))
    }  
return(
    <>
    <form onSubmit={sent_data}>      
    <div id="main">
        <h1 id="header_title">See What's Happening</h1>
        <h4 id="heading">Register Yourself</h4>
        <div id="email">
            <input type="text" name="email" onChange={handle_change} id="inpt_email" placeholder="Email"></input>
       </div>
       <div id="username">
        <input type="text" name="username" onChange={handle_change} id="inpt_usrnm" placeholder="Username"></input>
       </div>
       <div id="pass">
        <input type="text" name="password" onChange={handle_change} id="inpt_pass" placeholder="Password"></input>
       </div>
       <button  type="submit" id="Submit_buttpn">Continue</button>
       <div id="login_box">
        <h5>Already have an account?</h5>
        <NavLink to="/login">Login</NavLink>
        </div>       
    </div>
    
    </form>
    </>
)

}

export default Register_user