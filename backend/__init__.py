# backend/__init__.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os

# ------------------- Import Blueprints -------------------
from .auth import auth_bp
from .settings import settings_bp
from .threats import threats_bp


# ------------------- JWT -------------------
from flask_jwt_extended import JWTManager


def create_app():
    """
    Create and configure the Flask app.
    Sets up sessions, CORS, JWT, and registers blueprints.
    Serves the React frontend from /frontend/dist.
    """
    # Absolute path to React build folder (frontend/dist)
    static_path = os.path.join(os.getcwd(), "frontend", "dist")
    app = Flask(__name__, static_folder=static_path, static_url_path="")

    # ------------------- Flask Config -------------------
    app.config['SECRET_KEY'] = "supersecretkey"  # Flask session secret
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # ------------------- JWT Config -------------------
    # Used by flask_jwt_extended for @jwt_required and access tokens
    app.config['JWT_SECRET_KEY'] = "another_super_secret_key"
    jwt = JWTManager(app)

    # ------------------- Enable CORS & Sessions -------------------
    Session(app)
    CORS(app, supports_credentials=True)

    # ------------------- Register Blueprints -------------------
    # Auth routes: /api/auth/*
    app.register_blueprint(auth_bp)
    # Settings routes: /api/settings/*
    app.register_blueprint(settings_bp)
    app.register_blueprint(threats_bp)  # /api/threats



    # ------------------- Serve React Frontend -------------------
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        """
        Serve static files from the React build folder.
        If path exists, serve that file; otherwise, serve index.html.
        """
        full_path = os.path.join(app.static_folder, path)
        if path != "" and os.path.exists(full_path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
