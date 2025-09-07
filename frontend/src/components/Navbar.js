import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Navbar.css";




// const API_URL = process.env.REACT_APP_API_URL;
// const API_URL ="http://localhost:5000";
const API_URL ="https://tihub.onrender.com";


const Navbar = () => {
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

 // Logout function
 const handleLogout = async () => {
    try {
      const response = await fetch(`${API_URL}/api/logout`, {
        method: "POST",
        credentials: "include", // send session cookie
      });

      if (response.ok) {
        localStorage.removeItem("loggedIn");
        localStorage.removeItem("user");
        navigate("/login");
      }
    } catch (error) {
      console.error("Logout failed:", error);
      alert("Server error while logging out");
    }
  };



  return (
    <nav className="navbar">
      <div className="navbar-logo" onClick={() => navigate("/dashboard")}>
        Threat Intel Hub
      </div>

      <div
        className={`navbar-links ${isMobileMenuOpen ? "open" : ""}`}
      >
        <button onClick={() => navigate("/dashboard")}>Dashboard</button>
        <button onClick={() => navigate("/profile")}>Profile</button>
        <button onClick={() => navigate("/settings")}>Settings</button>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div
        className="mobile-menu-icon"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        &#9776; {/* hamburger icon */}
      </div>
    </nav>
  );
};

export default Navbar;
