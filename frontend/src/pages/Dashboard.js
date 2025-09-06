import React, { useState, useEffect } from "react";
import axios from "axios"; 
import "../styles/Dashboard.css"; 
import sampleThreats from '../data/sampleThreats.json';
import { useNavigate, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Dashboard = () => {
  const [threatsData, setThreatsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterType, setFilterType] = useState("");

  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.clear();
    localStorage.clear();
    navigate("/login");
  };

  // Fetch threats
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/threats")
      .then(response => {
        setThreatsData(response.data); 
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching threats:", err);
        setThreatsData(sampleThreats);
        setError(true);
        setLoading(false);
      });
  }, []);

  // Filter and search
  const filteredThreats = threatsData.filter(threat => {
    const matchesSearch = threat.indicator.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType ? threat.type.toLowerCase() === filterType.toLowerCase() : true;
    return matchesSearch && matchesFilter;
  });

  // Export CSV
  const handleExport = () => {
    const csvRows = [
      ["Type", "Indicator", "Severity", "MITRE Mapping"],
      ...filteredThreats.map(t => [t.type, t.indicator, t.severity, t.mitre])
    ];
    const csvContent = csvRows.map(e => e.join(",")).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "threats_export.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  // Login check
  const loggedIn = localStorage.getItem("loggedIn");
  if (!loggedIn) {
    return <Navigate to="/login" />;
  }

  return (
    <div className="dashboard-container" style={{ marginTop: "60px" }}>
      <Navbar />

      <div className="dashboard-main">
        <h1>Dashboard</h1>
        <p>Welcome to your Threat Intelligence Hub!</p>

        <div className="cards-container">
          <div className="card">
            <input 
              type="text" 
              placeholder="Search by indicator..." 
              value={searchTerm} 
              onChange={e => setSearchTerm(e.target.value)} 
            />
          </div>
          <div className="card">
            <select value={filterType} onChange={e => setFilterType(e.target.value)}>
              <option value="">Filter by Type</option>
              <option value="IP">IP</option>
              <option value="URL">URL</option>
              <option value="File Hash">Hash</option>
            </select>
          </div>
          <div className="card">
            <button onClick={handleExport}>Export CSV</button>
          </div>
        </div>

        {loading ? (
          <p>Loading threat data...</p>
        ) : (
          <>
            <table className="threat-table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Indicator</th>
                  <th>Severity</th>
                  <th>MITRE Mapping</th>
                </tr>
              </thead>
              <tbody>
                {filteredThreats.map((threat, index) => (
                  <tr key={index}>
                    <td>{threat.type}</td>
                    <td>{threat.indicator}</td>
                    <td>{threat.severity}</td>
                    <td>{threat.mitre}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {error && <p style={{color: "red"}}>Failed to fetch live data, using local sample.</p>}
          </>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default Dashboard;
