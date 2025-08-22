import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/profile";
import Settings from "./pages/settings";


import "./styles/App.css";

// Protected route wrapper
const ProtectedDashboard = () => {
  const loggedIn = localStorage.getItem("loggedIn") === "true";
  return loggedIn ? <Dashboard /> : <Navigate to="/" />;
};

function App() {
  return (
    
    <Routes>
      <Route path="/" element={<Login />} />        {/* Default page */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/settings" element={<Settings />} />

      <Route path="/dashboard" element={<ProtectedDashboard />} />  {/* Use protected wrapper */}
      
    </Routes>
  );
}

export default App;
