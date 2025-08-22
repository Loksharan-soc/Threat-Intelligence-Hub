Threat Intelligence Hub (TIH) Web App

A full-stack Threat Intelligence Hub web application built with React (frontend) and Flask + MongoDB (backend). The platform aggregates, visualizes, and manages cybersecurity threat intelligence, including IPs, domains, file hashes, and attack indicators.  

It is designed as a portfolio project to demonstrate full-stack development, session management, and cybersecurity concepts.

---

Features

- User Authentication
  - Secure registration and login with password hashing.
  - Session-based login using Flask sessions.
- Profile Management
  - View and update username.
  - Logout with session clearing.
- Threat Intelligence Management
  - Store and view indicators of compromise (IOCs).
  - Tag and categorize threats.
  - Map threats to MITRE ATT&CK techniques.
- Frontend
  - React with functional components and hooks.
  - User-friendly dashboard and forms.
  - Persistent login using localStorage.
- Backend
  - Flask RESTful API with CORS support for React frontend.
  - MongoDB for storing users and threat data.
  - Secure session management with SECRET_KEY.

---

Tech Stack

- Frontend: React, React Router, Axios, CSS
- Backend: Flask, Flask-Login, Flask-CORS
- Database: MongoDB Atlas
- Security: Password hashing with Werkzeug, session-based authentication

---

Folder Structure

tih-webapp/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── config.py          # App configuration
│   │   ├── extensions.py      # Flask extensions
│   │   ├── routes/
│   │   │   ├── auth.py        # Auth routes
│   │   │   ├── iocs.py        # Threat intelligence routes
│   │   │   └── ... 
│   │   └── db.py              # MongoDB connection
│   └── run.py                 # Run Flask server
│
├── frontend/
│   ├── src/
│   │   ├── components/        # Navbar, Footer, etc.
│   │   ├── pages/             # Login, Profile, Dashboard
│   │   ├── styles/            # CSS files
│   │   └── App.js
│   └── package.json
│
└── README.md

---

Installation & Setup

Backend

1. Create a virtual environment:

python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

2. Install dependencies:

pip install -r requirements.txt

3. Configure MongoDB credentials in db.py.

4. Run the Flask server:

python run.py

Frontend

1. Navigate to frontend folder:

cd frontend

2. Install dependencies:

npm install

3. Start the React dev server:

npm start

The app will run on http://localhost:3000 and connect to Flask backend on http://127.0.0.1:5000.

---

Usage

1. Register a new user.
2. Login to the dashboard.
3. View and edit your profile.
4. Add, view, and manage threat intelligence entries.
5. Logout securely to clear your session.

---

Future Improvements

- JWT-based authentication for stateless sessions.
- Role-based access control (admin vs user).
- Advanced threat dashboards with charts and graphs.
- Integration with OSINT feeds and APIs.
- MITRE ATT&CK mapping for automated threat classification.

---

License

This project is for educational and portfolio purposes.
