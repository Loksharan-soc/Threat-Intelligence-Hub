# backend/db.py
import os
from pymongo import MongoClient

# ---------------- MongoDB connection ----------------
# Get URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set!")

# Mongo client & collections
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client.get_default_database()  # automatically uses DB from URI
users_collection = db["users"]
threats_collection = db["threats"]

print("⚡ MongoDB client created. Connection will be tested on first query.")
