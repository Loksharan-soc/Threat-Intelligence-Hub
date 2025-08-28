# backend/db.py
import os
from urllib.parse import quote_plus
from pymongo import MongoClient

# ---------------- MongoDB connection ----------------
MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")
MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority"

# ---------------- Mongo Client ----------------
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,  # allow Render to bypass TLS validation
    serverSelectionTimeoutMS=10000
)

# ---------------- Database & Collections ----------------
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]

print("⚡ MongoDB client created. Connection will be tested on first query.")
