import os

class Config:
    # ---------------- Secret Key ----------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")

    # ---------------- MongoDB URI ----------------
    # Optionally, you can point to a single env var like MONGO_URI
    MONGO_URI = os.environ.get("MONGO_URI")
    # If using individual variables, you can construct it in db.py instead

    # ---------------- Flask-Session ----------------
    SESSION_TYPE = "filesystem"       # simplest for dev, good for small apps
    SESSION_PERMANENT = True          # permanent session controlled by lifetime
    SESSION_USE_SIGNER = True         # signs cookies to prevent tampering
    SESSION_FILE_DIR = os.path.join(os.getcwd(), "flask_session")
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds

    # ---------------- Cookies / CORS ----------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"    # allows React frontend to send cookies
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"  # True in prod
