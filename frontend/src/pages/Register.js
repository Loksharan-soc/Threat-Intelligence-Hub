import React, { useState } from "react";
import axios from "axios";
import "../styles/Register.css";


// const API_URL = process.env.REACT_APP_API_URL;
// const API_URL ="http://localhost:5000";
const API_URL ="https://tihub.onrender.com";


const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(`${API_URL}/api/register`, {
        username,
        email,
        password,
      });

      setMessage(response.data.message);
      // Clear fields on success
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (err) {
      // Display backend error message
      if (err.response && err.response.data && err.response.data.error) {
        setMessage(err.response.data.error);
      } else {
        setMessage("Registration failed.");
      }
    }
  };

  return (
    <div className="register-page">
      <h1>Threat Intelligence Hub</h1>
    <div className="register-container">
      <h2>Create Account</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
    </div>

  );
};

export default Register;
