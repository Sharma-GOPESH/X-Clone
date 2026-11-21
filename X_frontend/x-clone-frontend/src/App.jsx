import React from "react"
import Register_user from "./Components/Register_user"
import "./Components/Register_users.css";
import "./Components/home.css"
import "./Components/login_user.css"
import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import Login_user from "./Components/Login_user";
import Home_feed from "./Components/Home_feed_page.jsx";
import Home from "./Components/home.jsx";
import "./Components/Home_feed.css"

const API_URL = "http://localhost:8000"

function App() {
 return(
    <>
    <Routes>
        <Route path="/" element={<Home/>}></Route>
        <Route path="/login" element={<Login_user/>}></Route>
        <Route path="/Register_user" element={<Register_user/>}></Route>
        <Route path="/home_feed" element={<Home_feed/>}></Route>
    </Routes>
    
    </>
 )
}
export default App