# backend/db.py
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- MongoDB connection ----------------
MONGO_USER = os.environ.get("MONGO_USER", "cyberdev")       # default for local dev
MONGO_PASS = os.environ.get("MONGO_PASS", "cyberdev@123")   # default for local dev
MONGO_CLUSTER = os.environ.get("MONGO_CLUSTER", "intelhub.sc6ymra.mongodb.net")
MONGO_DB = os.environ.get("MONGO_DB", "threat_hub")

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Connection URI (explicitly includes DB)
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{password}"
    f"@{MONGO_CLUSTER}/{MONGO_DB}?retryWrites=true&w=majority&appName=intelhub"
)

# Mongo client & collections
client = MongoClient(MONGO_URI)
db = client.get_database()  # gets the DB from URI directly
users_collection = db["users"]
threats_collection = db["threats"]
