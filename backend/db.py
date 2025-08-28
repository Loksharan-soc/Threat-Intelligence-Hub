# backend/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env (optional, mainly for local development)
load_dotenv()

# MongoDB connection string (full URI, not SRV)
# Example format:
# mongodb://username:password@host1:27017,host2:27017,host3:27017/dbname?ssl=true&replicaSet=atlas-xxxx-shard-0&authSource=admin&retryWrites=true&w=majority
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,  # enable TLS
        tlsAllowInvalidCertificates=True,  # Atlas cert issues sometimes in cloud containers
        serverSelectionTimeoutMS=10000  # 10s timeout
    )
    # Attempt to get server info to test connection
    client.server_info()
    print("✅ MongoDB connection successful")
except Exception as err:
    print("❌ MongoDB connection failed:", err)
    raise err

# Access the database and collection
db = client.get_default_database()  # uses DB specified in URI
users_collection = db["users"]
