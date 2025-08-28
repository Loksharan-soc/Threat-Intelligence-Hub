# backend/db.py
from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- MongoDB connection ----------------
MONGO_USER = "cyberdev"
MONGO_PASS = "cyberdev@123"
MONGO_DB = "threat_hub"

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Direct host connection (replace with your cluster hosts)
MONGO_URI = (
    f"mongodb://{MONGO_USER}:{password}@"
    "ac-slaydsl-shard-00-00.sc6ymra.mongodb.net:27017,"
    "ac-slaydsl-shard-00-01.sc6ymra.mongodb.net:27017,"
    "ac-slaydsl-shard-00-02.sc6ymra.mongodb.net:27017/"
    f"{MONGO_DB}?ssl=true&authSource=admin&retryWrites=true&w=majority"
)

# Mongo client & collections
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]

print("⚡ MongoDB client created. Connection will be tested on first query.")
