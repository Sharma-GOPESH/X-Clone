import React from "react"
import Register_user from "./Components/Register_user"
import Login_use from "./Components/Login_user";
import "./Components/Register_users.css";
import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router";
import Login_user from "./Components/Login_user";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
 return(
    <>
    <Routes>
        <Route path="/login" element={<Login_user/>}></Route>
        <Route path="/Register_user" element={<Register_user/>}></Route>
    </Routes>
    
    </>
 )
}
export default App