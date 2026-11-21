import React, { useState } from "react"
import {NavLink } from "react-router"
import { useNavigate } from "react-router-dom";
import "./login_user.css"

function Login_user(){
     const navigate = useNavigate();
     const [form , setform] = useState({"email":"", "password":""})
     const [have_token , sethave_token] = useState(false)
 const handle_change =(e)=>{
       setform({...form, [e.target.name]:e.target.value})
    }  

const user_login =async(e)=>{
     e.preventDefault();
    try{
     const res = await fetch("http://127.0.0.1:8000/user_login",{
        method: "POST",
        headers : { "Content-Type": "application/json" },
        body : JSON.stringify(form)
     })
    const data = await res.json()
    if (!res.ok){
        if (Array.isArray(data.detail)) {
                for (let i = 0; i < data.detail.length; i++) {
                    if(data.detail[i]["type"]=="value_error"){
                        alert("Enter Correct Email")
                    } 
                    else if(data.detail[i]["loc"][1]=="password"){
                        alert("Password Must have Atleast 8 characters!!")
                    }               
                }
            }
        else{
            alert("Madrchod Kabhi sign in nhi kiya kahin?")
            return;
        }
    }
     sethave_token(true)
     localStorage.removeItem("token")
     localStorage.setItem("token", data)
     navigate("/home_feed")
    }
    catch(err){
      alert(err)
      return;
    }

}
       return(
        <>
    <form onSubmit={user_login}>      
    <div id="main">
        <h1 id="header_title">See What's Happening</h1>
        <h4 id="heading">Sign in</h4>
        <div id="login-email">
            <input type="text" id="inpt_email" value={form.email}  name="email" onChange={handle_change} placeholder=" " required></input>
            <label htmlFor="inpt_email">Email</label>      
       </div>
       <div id="login-pass">
        <input type="text" id="inpt_pass" name="password"  value={form.password} onChange={handle_change} placeholder=" " required></input>
         <label htmlFor="inpt_pass">Password</label>       
       </div>
       <button  type="submit" id="Submit_button">Continue</button>
       <div id="login_box">
        <h5>Do not have an account?</h5>
        <NavLink id="sign_up" to="/Register_user">Sign Up</NavLink>
        </div>       
    </div>
    
    </form>
        </>
       )
}

export default Login_user