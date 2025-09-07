from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import users_collection, threats_collection

settings_bp = Blueprint("settings", __name__)

# -------------------- Helper --------------------
def get_current_user():
    """Return current user from session, or None if not logged in."""
    if "user" in session:
        username = session["user"]["username"]
        user = users_collection.find_one({"username": username})
        return user
    return None

# -------------------- Change Password --------------------
@settings_bp.route("/api/settings/change-password", methods=["POST"])
def change_password():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"error": "Both current and new passwords required"}), 400

    if not check_password_hash(current_user["password_hash"], current_password):
        return jsonify({"error": "Current password incorrect"}), 401

    users_collection.update_one(
        {"username": current_user["username"]},
        {"$set": {"password_hash": generate_password_hash(new_password)}}
    )

    return jsonify({"success": True, "message": "Password changed successfully"}), 200

# -------------------- Add Service / API Key --------------------
@settings_bp.route("/api/settings/add-service", methods=["POST"])
def add_service():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    service_name = data.get("name")
    api_key = data.get("apiKey", "")

    if not service_name:
        return jsonify({"error": "Service name required"}), 400

    threats_collection.update_one(
        {"user_id": str(current_user["_id"])},
        {"$push": {"services": {"name": service_name, "apiKey": api_key}}},
        upsert=True
    )
    return jsonify({"success": True, "message": f"{service_name} added successfully"}), 200

# -------------------- Remove Service --------------------
@settings_bp.route("/api/settings/remove-service", methods=["POST"])
def remove_service():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    service_name = data.get("name")
    if not service_name:
        return jsonify({"error": "Service name required"}), 400

    threats_collection.update_one(
        {"user_id": str(current_user["_id"])},
        {"$pull": {"services": {"name": service_name}}}
    )
    return jsonify({"success": True, "message": f"{service_name} removed successfully"}), 200

# -------------------- Get Services --------------------
@settings_bp.route("/api/settings/get-services", methods=["GET"])
def get_services():
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401

    user_services = threats_collection.find_one({"user_id": str(current_user["_id"])}) or {}
    return jsonify({"success": True, "apiKeys": user_services.get("services", [])}), 200
