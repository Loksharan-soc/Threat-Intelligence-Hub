import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Settings.css";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import axios from "axios";
axios.defaults.withCredentials = true; // set globally or per request

/**
 * Settings Page Component
 * -----------------------
 * Allows the user to:
 * - Change password
 * - Add/remove API keys for threat sources
 * - Enable 2FA
 * - Delete account
 */

const API_URL = process.env.REACT_APP_API_URL;


const Settings = () => {
  const navigate = useNavigate();

  // -------------------- User State --------------------
  const [user, setUser] = useState(null);

  // -------------------- Password State --------------------
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [passwordData, setPasswordData] = useState({ currentPassword: "", newPassword: "" });
  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [isSavingPassword, setIsSavingPassword] = useState(false); // disable save button while request

  // -------------------- API Keys State --------------------
  const services = [
    "VirusTotal",
    "AbuseIPDB",
    "HybridAnalysis",
    "AlienVault",
    "ThreatCrowd",
    "MISP",
    "OpenAI",
    "OTX",
    "Custom"
  ];
  const [selectedService, setSelectedService] = useState("");
  const [customService, setCustomService] = useState({ name: "", apiKey: "" });
  const [apiKeys, setApiKeys] = useState([]);
  const [selectedApiIndexes, setSelectedApiIndexes] = useState([]);

  // -------------------- Two-Factor Authentication --------------------
  const [twoFAEnabled, setTwoFAEnabled] = useState(false);
  const [twoFAMethod, setTwoFAMethod] = useState("");

  // -------------------- Account Deletion --------------------
  const [deleting, setDeleting] = useState(false);

  // -------------------- Load user & API keys on mount --------------------
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) setUser(JSON.parse(storedUser));
    else navigate("/login");

    const storedApiKeys = localStorage.getItem("apiKeys");
    if (storedApiKeys) setApiKeys(JSON.parse(storedApiKeys));
  }, [navigate]);

  // ==================== HANDLERS ====================

  /** Handle password change */
  const handlePasswordChange = async () => {
    const current = passwordData.currentPassword.trim();
    const newP = passwordData.newPassword.trim();

    if (!current || !newP) {
      setPasswordMessage("Both fields are required.");
      setPasswordError(true);
      return;
    }

    setIsSavingPassword(true);
    setPasswordMessage("");

    try {
      const response = await axios.post(
        `${API_URL}/api/auth/change-password`,
        { currentPassword: current, newPassword: newP },
        { withCredentials: true }
      );

      if (response.status === 200 && response.data.success) {
        setPasswordMessage("Password changed successfully!");
        setPasswordError(false);
        setPasswordData({ currentPassword: "", newPassword: "" });
        setIsChangingPassword(false);
      } else {
        setPasswordMessage(response.data.message || "Error changing password");
        setPasswordError(true);
      }
    } catch (err) {
      console.error(err);
      setPasswordMessage("Server error while changing password");
      setPasswordError(true);
    } finally {
      setIsSavingPassword(false);
      setTimeout(() => setPasswordMessage(""), 5000); // auto-clear message
    }
  };

  /** Handle account deletion */
  const handleDeleteAccount = async () => {
    if (deleting) return;
    if (!window.confirm("Are you sure you want to delete your account?")) return;

    setDeleting(true);
    try {
      const response = await axios.post(
        `${API_URL}/api/auth/delete`,
        {},
        { withCredentials: true }
      );
      const data = response.data;

      if (response.status === 200) {
        alert(data.message);
        localStorage.removeItem("loggedIn");
        localStorage.removeItem("user");
        navigate("/login");
      } else {
        alert(data.message || "Error deleting account");
      }
    } catch (err) {
      console.error("Delete account error:", err);
      alert("Could not connect to server. Try again later.");
    } finally {
      setDeleting(false);
    }
  };

  /** Add a new threat source / API key */
  const handleAddService = () => {
    if (!selectedService) return;

    let newService;
    if (selectedService === "Custom") {
      if (!customService.name || !customService.apiKey) {
        alert("Enter both service name and API key");
        return;
      }
      newService = customService;
    } else {
      if (!customService.apiKey) {
        alert("Enter API key for the selected service");
        return;
      }
      newService = { name: selectedService, apiKey: customService.apiKey };
    }

    const updatedKeys = [...apiKeys, newService];
    setApiKeys(updatedKeys);
    localStorage.setItem("apiKeys", JSON.stringify(updatedKeys));

    setSelectedService("");
    setCustomService({ name: "", apiKey: "" });
  };

  /** Remove selected API keys */
  const handleRemoveSelectedApi = () => {
    if (selectedApiIndexes.length === 0) return;

    const updatedKeys = apiKeys.filter((_, i) => !selectedApiIndexes.includes(i));
    setApiKeys(updatedKeys);
    localStorage.setItem("apiKeys", JSON.stringify(updatedKeys));
    setSelectedApiIndexes([]);
  };

  /** Enable 2FA */
  const handle2FA = (method) => {
    setTwoFAMethod(method);
    setTwoFAEnabled(true);
    alert(`2FA enabled with ${method}`);
  };

  // ==================== RENDER ====================
  return (
    <div className="settings-page" style={{ marginTop: "60px" }}>
      <Navbar />
      <h1>Settings</h1>
      <div className="settings-container">

        {/* Password Change */}
        <section className="card">
          <h2>Change Password</h2>
          {isChangingPassword ? (
            <>
              <input
                type="password"
                placeholder="Current Password"
                value={passwordData.currentPassword}
                onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
              />
              <input
                type="password"
                placeholder="New Password"
                value={passwordData.newPassword}
                onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
              />
              <button onClick={handlePasswordChange} disabled={isSavingPassword}>
                {isSavingPassword ? "Saving..." : "Save Password"}
              </button>
              <button onClick={() => { setIsChangingPassword(false); setPasswordMessage(""); }}>Cancel</button>
              {passwordMessage && (
                <p style={{ color: passwordError ? "red" : "green" }}>{passwordMessage}</p>
              )}
            </>
          ) : (
            <button onClick={() => setIsChangingPassword(true)}>Change Password</button>
          )}
        </section>

        {/* Add / Manage API Keys */}
        <section className="card">
          <h2>Add Threat Source / API Key</h2>
          <div className="service-input">
            <select value={selectedService} onChange={(e) => setSelectedService(e.target.value)}>
              <option value="">Select Service</option>
              {services.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>

            {selectedService && selectedService !== "Custom" && (
              <input
                type="text"
                placeholder="Enter API Key"
                value={customService.apiKey}
                onChange={(e) => setCustomService({ ...customService, apiKey: e.target.value })}
              />
            )}

            {selectedService === "Custom" && (
              <>
                <input
                  type="text"
                  placeholder="Service Name"
                  value={customService.name}
                  onChange={(e) => setCustomService({ ...customService, name: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="API Key"
                  value={customService.apiKey}
                  onChange={(e) => setCustomService({ ...customService, apiKey: e.target.value })}
                />
              </>
            )}

            <button onClick={handleAddService}>Add Service</button>
          </div>
        </section>

        {/* API Keys List */}
        {apiKeys.length > 0 && (
          <section className="card api-list-card">
            <h2>Added Services / API Keys</h2>
            <ul className="api-list">
              {apiKeys.map((s, i) => {
                const isSelected = selectedApiIndexes.includes(i);
                return (
                  <li
                    key={i}
                    className={isSelected ? "selected" : ""}
                    onClick={() => {
                      if (isSelected) setSelectedApiIndexes(selectedApiIndexes.filter(idx => idx !== i));
                      else setSelectedApiIndexes([...selectedApiIndexes, i]);
                    }}
                  >
                    {s.name} - {s.apiKey || <em>API key not set</em>}
                  </li>
                );
              })}
            </ul>
            {selectedApiIndexes.length > 0 && (
              <button className="remove-btn" onClick={handleRemoveSelectedApi}>
                Remove Selected Service(s)
              </button>
            )}
          </section>
        )}

        {/* Two-Factor Authentication */}
        <section className="card">
          <h2>Two-Factor Authentication</h2>
          <button onClick={() => handle2FA("Google Authenticator")}>Enable Google Authenticator</button>
          <button onClick={() => handle2FA("Gmail OTP")}>Enable Gmail OTP</button>
          {twoFAEnabled && <p>2FA Enabled via {twoFAMethod}</p>}
        </section>

        {/* Danger Zone */}
        <section className="card">
          <h2>Danger Zone</h2>
          <button onClick={handleDeleteAccount} className="delete-btn" disabled={deleting}>
            {deleting ? "Deleting..." : "Delete Account"}
          </button>
        </section>

      </div>
      <Footer />
    </div>
  );
};

export default Settings;
