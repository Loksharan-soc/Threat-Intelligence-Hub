# backend/db.py
from pymongo import MongoClient
from urllib.parse import quote_plus
from pymongo.errors import ServerSelectionTimeoutError

# -----------------------------
# MongoDB Atlas credentials
# -----------------------------
USERNAME = "your_db_username"
PASSWORD = "your_db_password"
CLUSTER  = "ac-slaydsl-shard-00-00.sc6ymra.mongodb.net"
DB_NAME  = "tihub"

# URL-encode username and password
USERNAME_ENC = quote_plus(USERNAME)
PASSWORD_ENC = quote_plus(PASSWORD)

# Build the MongoDB connection URI
MONGO_URI = f"mongodb+srv://{USERNAME_ENC}:{PASSWORD_ENC}@{CLUSTER}/{DB_NAME}?retryWrites=true&w=majority"

# Connect with SSL enabled and allow invalid certs for Render
client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=10000  # 10s timeout
)

# Select database and collections
db = client[DB_NAME]
users_collection = db["users"]
ioc_collection   = db["iocs"]

# Test the connection immediately
try:
    # The ismaster command is cheap and does not require auth
    client.admin.command("ping")
    print("✅ MongoDB connection successful!")
except ServerSelectionTimeoutError as err:
    print("❌ MongoDB connection failed:", err)
    raise

print("⚡ MongoDB client created. Connection tested at startup.")
