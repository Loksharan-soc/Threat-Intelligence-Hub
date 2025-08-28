# backend/db.py
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- MongoDB connection ----------------

# Use full MONGO_URI from environment (recommended for Render)
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    # fallback for local development
    MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")
    MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")
    MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")

    user = quote_plus(MONGO_USER)
    password = quote_plus(MONGO_PASS)
    MONGO_URI = f"mongodb+srv://{user}:{password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=intelhub"

# Database name
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Decide if we are on Render (production) or local dev
IS_RENDER = os.environ.get("RENDER") == "true"  # Render sets this automatically

# Connect to MongoDB
if IS_RENDER:
    # On Render: enforce TLS/SSL (Atlas requires TLS 1.2+)
    client = MongoClient(
        MONGO_URI,
        tls=True,                   # enable TLS
        tlsAllowInvalidCertificates=False,  # verify server certificate
        serverSelectionTimeoutMS=5000
    )
else:
    # Local dev: plain connection
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# Test connection
try:
    client.server_info()
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

# Get DB and collections
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]
