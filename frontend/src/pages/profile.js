import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Profile.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";


// const API_URL = process.env.REACT_APP_API_URL;
// const API_URL ="http://localhost:5000";
const API_URL ="https://tihub.onrender.com"; 



const Profile = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({ username: "", email: "" });

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      const parsedUser = JSON.parse(storedUser);
      setUser(parsedUser);
      setFormData({ username: parsedUser.username, email: parsedUser.email });
    } else navigate("/login");
  }, [navigate]);

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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
  // Use current user values if input fields are empty
  const updatedUsername = formData.username.trim() || user.username;
  const updatedEmail = formData.email.trim() || user.email;

  try {
    const response = await fetch(`${API_URL}/api/auth/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: updatedUsername,
        email: updatedEmail,
      }),
      credentials: "include",
    });

    const data = await response.json();
    console.log("Update response:", data); // debug

    if (response.ok) {
      setUser(data.user);
      localStorage.setItem("user", JSON.stringify(data.user));
      setIsEditing(false);
      alert("Profile updated successfully!");
    } else {
      alert(data.error || data.message || "Error updating profile");
    }
  } catch (error) {
    console.error("Update failed:", error);
    alert("Server error while updating profile");
  }
};

  if (!user) return null;

  return (
    <div className="profile-page" style={{ marginTop: "60px" }}>
      <Navbar />
      <h1>Profile</h1>
      <div className="profile-container">
        {isEditing ? (
          <>
            <label>
              Username:
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
              />
            </label>
            <label>
              Email:
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </label>
            <button onClick={handleSave}>Save</button>
            <button onClick={() => setIsEditing(false)}>Cancel</button>
          </>
        ) : (
          <>
            <p>
              <strong>Username:</strong> {user.username}
            </p>
            <p>
              <strong>Email:</strong> {user.email}
            </p>
          {/*  <button onClick={() => setIsEditing(true)}>Edit Profile</button>*/}
          </>
        )}
        <button onClick={handleLogout}>Logout</button>
      </div>
      <Footer />
    </div>
  );
};

export default Profile;
