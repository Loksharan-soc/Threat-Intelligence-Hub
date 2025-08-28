from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# ---------------------------
# MongoDB configuration
# ---------------------------

# Replace these with your actual Atlas credentials
MONGO_USER = "your_atlas_username"
MONGO_PASS = "your_atlas_password"
MONGO_CLUSTER = "ac-slaydsl-shard-00-00.sc6ymra.mongodb.net"  # primary host from Atlas
MONGO_DBNAME = "tihub_db"

# MongoDB URI
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_CLUSTER}/"
    f"{MONGO_DBNAME}?retryWrites=true&w=majority"
)

# Create client with lazy connection (won't attempt handshake until first query)
client = MongoClient(
    MONGO_URI,
    connect=False,                  # lazy connect to prevent Gunicorn crash
    tls=True,                       # enable TLS/SSL
    tlsAllowInvalidCertificates=True  # bypass SSL handshake issues
)

# Database and collections
db = client[MONGO_DBNAME]
users_collection = db["users"]
# Add more collections here if needed

# Test connection (only if you want to check at startup)
try:
    client.admin.command("ping")
    print("⚡ MongoDB client created. Connection will be tested on first query.")
except ConnectionFailure:
    print("❌ MongoDB connection failed. Will retry on first query.")
