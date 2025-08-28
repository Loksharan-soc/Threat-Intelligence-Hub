# backend/db.py
import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# -------------------- MONGODB CONFIG --------------------
# Use environment variables for credentials
MONGO_USER = os.getenv("MONGO_USER", "your_username")
MONGO_PASS = os.getenv("MONGO_PASS", "your_password")
MONGO_DB = os.getenv("MONGO_DB", "your_database")
MONGO_HOST = os.getenv("MONGO_HOST", "cluster0.mongodb.net")

# Encode username and password safely for the URI
MONGO_USER_ESCAPED = quote_plus(MONGO_USER)
MONGO_PASS_ESCAPED = quote_plus(MONGO_PASS)

# Full connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER_ESCAPED}:{MONGO_PASS_ESCAPED}@{MONGO_HOST}/{MONGO_DB}?retryWrites=true&w=majority"

# -------------------- CONNECT TO MONGO --------------------
try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,  # Render containers sometimes require this
        serverSelectionTimeoutMS=10000     # 10s timeout
    )
    # Try a quick server call to verify connection
    client.server_info()
    print("✅ MongoDB connected successfully")
except ConnectionFailure as err:
    print(f"❌ MongoDB connection failed: {err}")
    raise err

# -------------------- DATABASE AND COLLECTIONS --------------------
db = client[MONGO_DB]
users_collection = db["users"]
