import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    MONGO_URI = os.environ.get("MONGO_URI")

    # Flask-Session configuration
    SESSION_TYPE = "filesystem"   # ✅ simplest option for dev
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_FILE_DIR = os.path.join(os.getcwd(), "flask_session")  # folder to store session files

    # CORS + Cookie config
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # set True in production
