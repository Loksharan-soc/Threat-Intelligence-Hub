from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import users_collection

auth_bp = Blueprint("auth", __name__)

# -------------------- REGISTER --------------------
@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # Check if username or email already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 409

    password_hash = generate_password_hash(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password_hash": password_hash
    })

    return jsonify({"message": "User registered successfully"}), 201


# -------------------- LOGIN --------------------
@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.get("password_hash", ""), password):
        return jsonify({"error": "Incorrect password"}), 401

    session["user"] = {"username": user["username"], "email": user["email"]}
    session.permanent = True

    return jsonify({"success": True, "user": session["user"]}), 200


# -------------------- LOGOUT --------------------
@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"}), 200


# -------------------- EDIT PROFILE --------------------
@auth_bp.route("/api/auth/update", methods=["POST"])
def update_profile():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Username and email required"}), 400

    current_user = session["user"]

    # Check if new username/email is taken by others
    if users_collection.find_one({"username": username, "username": {"$ne": current_user["username"]}}):
        return jsonify({"error": "Username already taken"}), 409
    if users_collection.find_one({"email": email, "email": {"$ne": current_user["email"]}}):
        return jsonify({"error": "Email already taken"}), 409

    users_collection.update_one(
        {"username": current_user["username"]},
        {"$set": {"username": username, "email": email}}
    )

    # Update session
    session["user"]["username"] = username
    session["user"]["email"] = email

    return jsonify({"message": "Profile updated successfully", "user": session["user"]}), 200


# -------------------- CHANGE PASSWORD --------------------
@auth_bp.route("/api/auth/change-password", methods=["POST"])
def change_password():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"error": "Both current and new passwords required"}), 400

    current_user = users_collection.find_one({"username": session["user"]["username"]})
    if not current_user or not check_password_hash(current_user["password_hash"], current_password):
        return jsonify({"error": "Current password incorrect"}), 401

    new_hash = generate_password_hash(new_password)
    users_collection.update_one(
        {"username": session["user"]["username"]},
        {"$set": {"password_hash": new_hash}}
    )

    return jsonify({"success": True, "message": "Password changed successfully"}), 200


# -------------------- DELETE ACCOUNT --------------------
@auth_bp.route("/api/auth/delete", methods=["POST"])
def delete_account():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    username = session["user"]["username"]
    users_collection.delete_one({"username": username})
    session.pop("user", None)

    return jsonify({"success": True, "message": "Account deleted successfully"}), 200
