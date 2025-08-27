# backend/app/extensions.py
from flask_login import LoginManager

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Optional: endpoint for login redirects
