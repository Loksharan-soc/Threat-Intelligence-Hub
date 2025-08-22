#db.py
from pymongo import MongoClient
from urllib.parse import quote_plus

username = "cyberdev"
password = quote_plus("cyberdev@123")  # encode special characters like @
cluster = "intelhub.sc6ymra.mongodb.net"

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=intelhub"

client = MongoClient(MONGO_URI)
db = client["threat_hub"]
users_collection = db["users"]
threats_collection = db["threats"]
