from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os

# Import blueprints
from .auth import auth_bp
from .threats import threats_bp  # ✅ Added registration

def create_app():
    # Set frontend dist path relative to project root
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

    app = Flask(
        __name__,
        static_folder=frontend_dist,
        static_url_path=""
    )

    # Config
    app.config['SECRET_KEY'] = "supersecretkey"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    Session(app)
    CORS(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp)     # /api/login
    app.register_blueprint(threats_bp)  # /api/threats

    # Serve React frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        file_path = os.path.join(app.static_folder, path)
        if path != "" and os.path.exists(file_path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
