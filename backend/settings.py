# backend/settings.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .db import users_collection  # Import from db.py

# ------------------- Blueprint -------------------
# All routes under /api/settings
settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")

# ------------------- GET API KEYS -------------------
@settings_bp.route("/api-keys", methods=["GET"])
@jwt_required()
def get_api_keys():
    """
    Fetch all API keys for the logged-in user.
    """
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"apiKeys": user.get("apiKeys", [])}), 200


# ------------------- ADD API KEY -------------------
@settings_bp.route("/api-keys", methods=["POST"])
@jwt_required()
def add_api_key():
    """
    Add a new API key for a threat source.
    Expects JSON: { "service": { "name": "...", "apiKey": "..." } }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    service = data.get("service")

    if not service or "name" not in service or "apiKey" not in service:
        return jsonify({"message": "Invalid service data"}), 400

    # Push new API key into user's apiKeys array
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"apiKeys": service}}
    )

    # Return updated API keys
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return jsonify({"apiKeys": user.get("apiKeys", [])}), 200


# ------------------- DELETE API KEYS -------------------
@settings_bp.route("/api-keys", methods=["DELETE"])
@jwt_required()
def delete_api_keys():
    """
    Delete selected API keys for the logged-in user.
    Expects JSON: { "keys": [ { "name": "...", "apiKey": "..." }, ... ] }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    keys_to_remove = data.get("keys")

    if not keys_to_remove or not isinstance(keys_to_remove, list):
        return jsonify({"message": "No keys provided"}), 400

    # Pull each key from user's apiKeys array
    for key in keys_to_remove:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"apiKeys": key}}
        )

    # Return updated API keys
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return jsonify({"apiKeys": user.get("apiKeys", [])}), 200
