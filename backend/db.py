# backend/db.py
from pymongo import MongoClient
from urllib.parse import quote_plus

# ---------------- MongoDB connection ----------------
# Hardcoded credentials
MONGO_USER = "cyberdev"
MONGO_PASS = "cyberdev@123"
MONGO_CLUSTER = "intelhub.sc6ymra.mongodb.net"
MONGO_DB = "threat_hub"

# Encode password for special characters
password = quote_plus(MONGO_PASS)

# Connection URI
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=intelhub"

# Mongo client & collections
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)  # Add TLS bypass for Render SSL issues
db = client[MONGO_DB]
users_collection = db["users"]
threats_collection = db["threats"]

print("⚡ MongoDB client created. Connection will be tested on first query.")
