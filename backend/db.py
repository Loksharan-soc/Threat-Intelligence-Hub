# backend/db.py
import os
from pymongo import MongoClient

# ---------------- MongoDB connection ----------------

# Prefer a full connection string from environment (for Render / production)
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    # fallback for local dev
    from urllib.parse import quote_plus
    MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")
    MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")
    MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
    MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

    password = quote_plus(MONGO_PASS)
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=intelhub"
else:
    # If full URI provided, get DB name separately
    MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Connect
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB]

# Collections
users_collection = db["users"]
threats_collection = db["threats"]
