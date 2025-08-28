# backend/db.py
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- MongoDB connection ----------------
MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")
MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Encode username & password for special characters
username = quote_plus(MONGO_USER)
password = quote_plus(MONGO_PASS)

# Connection URI
MONGO_URI = f"mongodb+srv://{username}:{password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=intelhub"

# Mongo client & collections
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]
