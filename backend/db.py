# backend/db.py
from pymongo import MongoClient
from urllib.parse import quote_plus

# ----- MongoDB credentials -----
MONGO_USER = "loksharan"           # your username
MONGO_PASS = "SuperSecret123!"     # your password with special characters
MONGO_HOSTS = "ac-slaydsl-shard-00-00.sc6ymra.mongodb.net:27017," \
              "ac-slaydsl-shard-00-01.sc6ymra.mongodb.net:27017," \
              "ac-slaydsl-shard-00-02.sc6ymra.mongodb.net:27017"
MONGO_DB = "tihub"                 # your DB name
REPLICA_SET = "ac-slaydsl-shard-0" # your Atlas replica set name

# ----- URL-encode username & password -----
user_enc = quote_plus(MONGO_USER)
pass_enc = quote_plus(MONGO_PASS)

# ----- Build the URI -----
MONGO_URI = (
    f"mongodb://{user_enc}:{pass_enc}@{MONGO_HOSTS}/"
    f"{MONGO_DB}?ssl=true&replicaSet={REPLICA_SET}&authSource=admin&retryWrites=true&w=majority"
)

# ----- Connect to MongoDB -----
try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,  # needed for Render SSL
        serverSelectionTimeoutMS=10000      # 10s timeout
    )
    print("⚡ MongoDB client created. Connection will be tested on first query.")
except Exception as err:
    print("❌ MongoDB connection failed:", err)
    raise err

# ----- Collections -----
db = client[MONGO_DB]
users_collection = db["users"]
