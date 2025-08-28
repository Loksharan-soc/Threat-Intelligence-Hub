# backend/db.py
import os
from urllib.parse import quote_plus
from pymongo import MongoClient, errors

# ---------------- MongoDB connection ----------------
MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")      # default for local dev
MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")  # default for local dev
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"

# ---------------- Mongo Client ----------------
try:
    client = MongoClient(
        MONGO_URI,
        tls=True,                       # enforce TLS
        tlsAllowInvalidCertificates=True,  # temporarily bypass cert validation on Render
        serverSelectionTimeoutMS=10000   # 10s timeout
    )
    # Test the connection
    client.server_info()
    print("✅ MongoDB connected successfully")
except errors.ServerSelectionTimeoutError as err:
    print("❌ MongoDB connection failed:", err)
    raise err

# ---------------- Database & Collections ----------------
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]
