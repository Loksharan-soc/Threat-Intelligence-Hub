import React from "react";
import "../styles/Footer.css";

const Footer = () => {
  const year = new Date().getFullYear(); // dynamic year

  return (
    <footer className="footer">
      <p>© {year} Threat Intelligence Hub. All rights reserved.</p>
      <p>
        Developed by Loksharan | 
        <a href="https://github.com/loksharan-soc" target="_blank" rel="noreferrer"> GitHub</a> | 
        <a href="https://linkedin.com/in/loksharan" target="_blank" rel="noreferrer"> LinkedIn</a>
      </p>
    </footer>
  );
};

export default Footer;
