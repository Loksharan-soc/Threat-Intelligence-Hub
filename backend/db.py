# backend/db.py
import os
from pymongo import MongoClient
from urllib.parse import quote_plus
import sys

# ---------------- MongoDB connection ----------------
MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")      # local default
MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")  # local default
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"

# Detect if running on Render
ON_RENDER = os.environ.get("RENDER", None) is not None

# Mongo client & collections
try:
    if ON_RENDER:
        # Render often has SSL handshake issues; temporarily bypass cert verification
        client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsAllowInvalidCertificates=True,
            serverSelectionTimeoutMS=5000
        )
    else:
        # Local development: normal connection
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

    # Test connection
    client.admin.command("ping")
    print("✅ MongoDB connected successfully")

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# Database & collections
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]
