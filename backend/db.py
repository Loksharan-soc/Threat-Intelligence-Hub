# backend/db.py
import os
import re
from urllib.parse import quote_plus
from pymongo import MongoClient

# ---------------- MongoDB connection ----------------
MONGO_URI_RAW = os.environ.get("MONGO_URI")  # raw URI from Render env

if not MONGO_URI_RAW:
    raise Exception("MONGO_URI environment variable not set!")

# Extract password from URI and encode it
# Expected format: mongodb+srv://username:password@cluster/...
match = re.match(r"(mongodb(?:\+srv)?://[^:]+:)([^@]+)(@.+)", MONGO_URI_RAW)
if not match:
    raise Exception("MONGO_URI format invalid!")

encoded_password = quote_plus(match[2])
MONGO_URI = f"{match[1]}{encoded_password}{match[3]}"

# Create MongoDB client
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

# Use default database from URI if specified
db = client.get_default_database()

# Collections
users_collection = db["users"]
threats_collection = db["threats"]

print("⚡ MongoDB client created. Connection will be tested on first query.")
