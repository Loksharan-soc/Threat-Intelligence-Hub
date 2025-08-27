from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os

from .auth import auth_bp

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist"), static_url_path="")
    
    # Config
    app.config['SECRET_KEY'] = "supersecretkey"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    
    Session(app)
    CORS(app, supports_credentials=True)

    # Register auth blueprint
    app.register_blueprint(auth_bp)  # now /api/login will work

    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
