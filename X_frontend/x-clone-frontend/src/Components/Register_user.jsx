import { useState } from "react"
import './Register_users.css'
import { NavLink } from "react-router"
import { useNavigate } from "react-router-dom";
function Register_user(){
    const navigate = useNavigate();
     const [Form , setForm] = useState({"email":"", "password":"", "username":""})
    const [success , setsuccess] = useState("")

    const handle_change =(e)=>{
       setForm({...Form, [e.target.name]:e.target.value})
    }  
    const sent_data = async(e) =>{
      e.preventDefault();
      setsuccess("")
      try{
      const res = await fetch("http://127.0.0.1:8000/users",{
        method : "POST",
        headers : { "Content-Type": "application/json" },
        body : JSON.stringify(Form)
      })
      const data = await res.json()
      
      if (!res.ok) {
            if (typeof data.detail === "string") {
                alert(data.detail);                     
            } else if (Array.isArray(data.detail)) {
                for (let i = 0; i < data.detail.length; i++) {
                    if(data.detail[i]["type"]=="value_error"){
                        alert("Enter Correct Email")
                    } 
                    else if(data.detail[i]["loc"][1]=="password"){
                        alert("Password Must have Atleast 8 characters!!")
                    }
                    else if(data.detail[i]["loc"][1]=="username"){
                        alert("Username Must have Atleast 6 characters!!")
                    }                      
                }
            } else {
                alert("Something went wrong");
            }
            return;
        }
        setsuccess("Account created successfully!");
        localStorage.removeItem("token")
        localStorage.setItem("token", data)
        navigate("/home_feed")
      
    }
    catch(err){
    alert("something went wrong")
    return;
    }
    }
return(
    <>
    <form className="page" onSubmit={sent_data}>      
    <div id="main">
        <h1 id="header_title">See What's Happening</h1>
        <div id="sign-up">
        <h4 id="heading">Sign Up</h4>
        <div id="email">
            <input type="text" name="email"  value={Form.email} onChange={handle_change} id="inpt_email" placeholder=" " required></input>
             <label htmlFor="inpt_email">Email</label>
       </div>
       <div id="username">
        <input type="text" name="username" value={Form.username} onChange={handle_change} id="inpt_usrnm" placeholder=" " required></input>
        <label htmlFor="inpt_usrnm">Username</label>
       </div>
       <div id="pass">
        <input type="text" name="password" value={Form.password} onChange={handle_change} id="inpt_pass" placeholder=" " required></input>
       <label htmlFor="inpt_pass">Password</label>
       </div>
       </div>
       <button  type="submit" id="Submit_button">Continue</button>
       <div id="login_box">
        <h5>Already have an account?</h5>
        {success && <p className="success_msg">{success}</p>}
        <NavLink id="sign-in" to="/login">Sign in</NavLink>
        </div>       
    </div>
    
    </form>
    </>
)

}

export default Register_user

