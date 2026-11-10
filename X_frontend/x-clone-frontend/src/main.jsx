import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import "./Components/Register_users.css";
import "@fontsource-variable/inter"
import App from './App.jsx'
import { BrowserRouter, Routes, Route } from "react-router";

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
  <StrictMode>
    <App />
  </StrictMode>
  </BrowserRouter>,
)