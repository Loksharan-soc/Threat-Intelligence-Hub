from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# -------------------------------
# MongoDB credentials (hardcoded)
# -------------------------------
MONGO_URI = "mongodb+srv://<username>:<password>@ac-slaydsl-shard-00-00.sc6ymra.mongodb.net/?retryWrites=true&w=majority"

# -------------------------------
# MongoClient setup (lazy connect)
# -------------------------------
# connect=False ensures the client doesn't try to connect immediately at import
client = MongoClient(
    MONGO_URI,
    tls=True,  # enable TLS
    tlsAllowInvalidCertificates=True,  # ignore invalid certs
    connect=False,  # do NOT connect at startup
    serverSelectionTimeoutMS=10000  # 10 second timeout
)

# -------------------------------
# Database & Collection
# -------------------------------
db = client["tihub"]  # your DB name
users_collection = db["users"]

# -------------------------------
# Optional test function (lazy connection)
# -------------------------------
def test_connection():
    try:
        # First query triggers connection & handshake
        client.admin.command("ping")
        print("⚡ MongoDB connection successful!")
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ MongoDB connection failed: {e}")

# You can call test_connection() in run.py or Flask startup if you want
