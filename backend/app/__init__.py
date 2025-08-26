from flask import Flask, send_from_directory
from .config import Config
from .extensions import login_manager
from .routes import auth, iocs, feeds, dashboard
from flask_cors import CORS
from datetime import timedelta
from flask_session import Session
import os


def create_app():
    # ---------------- Flask app initialization ----------------
# Absolute path to frontend/dist
    # __file__ is backend/app/__init__.py
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes to backend/
    project_root = os.path.dirname(repo_root)  # goes to repo root
    frontend_dist = os.path.join(project_root, 'frontend', 'dist')  # correct path

    
    if not os.path.exists(frontend_dist):
        raise RuntimeError(f"React dist folder not found at {frontend_dist}")
    
    app = Flask(__name__, static_folder=frontend_dist, static_url_path='')
    # ---------------- Load config ----------------
    app.config.from_object(Config)

    # ---------------- Secret Key ----------------
    app.secret_key = Config.SECRET_KEY

    # ---------------- Session config ----------------
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"   # ✅ required for cross-origin
    app.config['SESSION_COOKIE_SECURE'] = False   # ✅ keep False on localhost (True in prod HTTPS)


    Session(app)  # This initializes filesystem-backed sessions

 
    # ---------------- Initialize extensions ----------------
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"   # ✅ make sure redirect works if not logged in

    # ---------------- Register blueprints ----------------
    app.register_blueprint(auth.auth_bp)
   # app.register_blueprint(iocs.iocs_bp)
    #app.register_blueprint(feeds.feeds_bp)
    #app.register_blueprint(dashboard.dashboard_bp)


    # ---------------- Enable CORS ----------------
    CORS(app, supports_credentials=True )

    # ---------------- Serve React frontend ----------------
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        
        file_path = os.path.join(app.static_folder, path)

        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # register blueprints and initialize extensions here
    return app
