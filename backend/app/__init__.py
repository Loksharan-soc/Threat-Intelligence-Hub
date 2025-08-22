from flask import Flask, send_from_directory
from .config import Config
from .extensions import login_manager
from .routes import auth, iocs, feeds, dashboard
from flask_cors import CORS
from datetime import timedelta
from flask_session import Session


def create_app():
    # ---------------- Flask app initialization ----------------
    app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")

    # ---------------- Load config ----------------
    app.config.from_object(Config)

    # ---------------- Secret Key ----------------
    app.secret_key = Config.SECRET_KEY

    # ---------------- Session config ----------------
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"   # ✅ required for cross-origin
    app.config['SESSION_COOKIE_SECURE'] = False      # ✅ keep False on localhost (True in prod HTTPS)


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
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"] )

    # ---------------- Serve React frontend ----------------
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_react(path):
        if path and (app.static_folder / path).exists():
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app
