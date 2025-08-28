from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os

from .auth import auth_bp

def create_app():
    # Absolute path from current working directory (Render-friendly)
    static_path = os.path.join(os.getcwd(), "frontend", "dist")
    app = Flask(__name__, static_folder=static_path, static_url_path="")

    # Config
    app.config['SECRET_KEY'] = "supersecretkey"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Enable sessions and CORS
    Session(app)
    CORS(app, origins=["https://tihub.onrender.com"], supports_credentials=True)


    # Register blueprints
    app.register_blueprint(auth_bp)  # /api/login, etc.

    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        full_path = os.path.join(app.static_folder, path)
        if path != "" and os.path.exists(full_path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
