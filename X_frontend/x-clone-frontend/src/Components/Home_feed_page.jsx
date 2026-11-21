import React from "react";
import { useState , useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Home_feed.css"
import search from "./Search-icon.png"

function Home_feed(){
    const navigate = useNavigate();
const [feed , setfeed] = useState([])
const[loading, setloading] = useState(true)

useEffect(()=> {
async function get_post(){
    try{
    const All_token = localStorage.getItem("token")

    if(!All_token){
        alert("Please Sign_up or Sign_in")
        navigate("/login")
        return;
    }
              
    const res = await fetch("http://127.0.0.1:8000/feed", {
        headers: { Authorization: `Bearer ${All_token}` }
    })
    const data = await res.json()
    console.log(data)
    if(!res.ok){
         if (typeof data.detail === "string") {
                alert("detail ke upr")
                console.log(data)
                alert(data.detail);
                navigate("/login")
                return;
         }
        else {
                alert("Something went wrong");
                navigate("/login")
                return;
            }  
    }
    setfeed(data)
    setloading(false)
}
    catch(err){
        alert("something went wrong , please try again!!")
        return;
    }
}
    get_post()
},[]
);

    return(
        <>

        <div id="feed">
        <div id="header"> 
            <label htmlFor="search-icon">
            <h1 id="x" >X</h1>
            <div id="search">
            <input type="text" id="search_label" placeholder=" "></input>
            <label htmlFor="search__label" ><img id="search-icon" src={search}></img></label>
            </div>
            </label> 
             </div>
             <hr id="line"></hr>
            <div id="All_posts">
        {feed.map(f => (
            <div className="post" key={f.id}>
             <div className="username">@{f.username}</div>
             <div className="post_body">{f.post_body}</div>
             <div className="like">{f.likes}</div>
             <div className="posting_time">{f.posted_at}</div>   
            </div>
        ))}
        </div>
        </div>
        </>
    )

}
export default Home_feed