# backend/db.py
from pymongo import MongoClient
from urllib.parse import quote_plus

# ----------------------------
# Hardcoded credentials
# ----------------------------
USERNAME = "YOUR_USERNAME"  # replace with your MongoDB username
PASSWORD = "YOUR_PASSWORD"  # replace with your MongoDB password
CLUSTER = "ac-slaydsl"      # your cluster prefix
DB_NAME = "tihub"           # database name

# Escape username and password
USERNAME_ESC = quote_plus(USERNAME)
PASSWORD_ESC = quote_plus(PASSWORD)

# MongoDB URI
MONGO_URI = f"mongodb+srv://{USERNAME_ESC}:{PASSWORD_ESC}@{CLUSTER}.sc6ymra.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

# ----------------------------
# Lazy client creation function
# ----------------------------
_client = None
_db = None

def get_db():
    global _client, _db
    if _client is None:
        # Create client lazily (after fork, for Gunicorn)
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000,  # 10s timeout
            tls=True,
            tlsAllowInvalidCertificates=True  # bypass SSL handshake issues
        )
        _db = _client[DB_NAME]
        print("⚡ MongoDB client created. Connection will be tested on first query.")
    return _db

# ----------------------------
# Collections
# ----------------------------
def get_users_collection():
    return get_db()["users"]

users_collection = get_users_collection()
