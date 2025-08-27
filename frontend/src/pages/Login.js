import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/Login.css";

axios.defaults.withCredentials = true; // store session cookie

// Use environment variable for API base URL
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Username and password are required");
      return;
    }

    try {
      const response = await axios.post(
        `${API_URL}/api/login`,
        { username, password },
        { withCredentials: true }
      );

      console.log("Backend response:", response.data);

      if (response.data.success) {
        localStorage.setItem("loggedIn", "true");
        localStorage.setItem("user", JSON.stringify(response.data.user));
        navigate("/dashboard");
      } else {
        setError(response.data.error || "Login failed");
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error || err.response.data.message || "Server error");
      } else {
        setError("Server error. Try again later.");
      }
    }
  };

  const handleRegister = () => navigate("/register");

  return (
    <div className="login-page">
      <h1 className="app-title">Threat Intelligence Hub</h1>
      <div className="login-wrapper">
        <div className="login-container">
          <h2>Welcome</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Login</button>
            {error && <p className="error">{error}</p>}
          </form>
          <button className="register-btn" onClick={handleRegister}>
            Create Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
