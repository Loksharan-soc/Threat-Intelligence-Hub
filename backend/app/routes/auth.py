# ===============================
# auth.py - User Authentication Routes
# ===============================

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
#from app.db import users_collection
from ..db import users_collection

# Blueprint for auth routes
auth_bp = Blueprint("auth", __name__)

# ===============================
# User Registration
# ===============================
@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
    
    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Insert user into MongoDB
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password_hash": password_hash
    })

    return jsonify({"message": "User registered successfully"}), 201

# ====================
# User Login
# ====================
@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Incorrect password"}), 401


    print("Session before login:", session.get("user"))

    # ✅ Create session
    session["user"] = {"username": user["username"], "email": user["email"]}
    session.permanent = True
    print("Session user:", session.get("user"))
    
    return jsonify({"success": True, "user": session["user"]}), 200

# ===============================
# Update User Profile (Username + Email)
# ===============================
@auth_bp.route("/api/auth/update", methods=["POST"])
def update_profile():
    user_session = session.get("user")
    if not user_session:
        print(session.get("user"))
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    new_username = data.get("username")
    new_email = data.get("email")

    if not new_username or not new_email:
        return jsonify({"error": "Username and email are required"}), 400

    old_email = user_session.get("email")
    if not old_email:
        return jsonify({"error": "Session missing email"}), 400

    update_fields = {}
    if new_username: update_fields["username"] = new_username
    if new_email: update_fields["email"] = new_email

    try:
        result = users_collection.update_one(
            {"email": old_email},
            {"$set": update_fields}
        )
        if result.matched_count == 0:
            return jsonify({"error": "User not found in DB"}), 404
    except Exception as e:
        print("DEBUG: MongoDB update error:", e)
        return jsonify({"error": "Server error while updating profile"}), 500

    # Fetch updated user info
    updated_user = users_collection.find_one(
        {"email": new_email},
        {"_id": 0, "password_hash": 0}
    )

    # Update session
    session["user"] = updated_user
    return jsonify({"message": "Profile updated", "user": updated_user}), 200


# ===============================
# Change User Password
# ===============================
@auth_bp.route("/api/auth/change-password", methods=["POST"])
def change_password():
    

    user_session = session.get("user") #{'username': 'user3', 'email': 'user3@gmail.com'} #
    print("Session user:", user_session)
    if not user_session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json
    current_pw = data.get("currentPassword")
    new_pw = data.get("newPassword")

    if not current_pw or not new_pw:
        return jsonify({"success": False, "message": "Both current and new passwords are required"}), 400

    user = users_collection.find_one({"email": user_session["email"]})
    if not user or not check_password_hash(user["password_hash"], current_pw):
        return jsonify({"success": False, "message": "Incorrect current password"}), 401

    try:
        users_collection.update_one(
            {"email": user_session["email"]},
            {"$set": {"password_hash": generate_password_hash(new_pw)}}
        )
    except Exception as e:
        print("DEBUG: MongoDB update error:", e)
        return jsonify({"success": False, "message": "Server error while updating password"}), 500

    return jsonify({"success": True, "message": "Password changed successfully"}), 200

# ===============================
# Delete User Account
# ===============================
@auth_bp.route("/api/auth/delete", methods=["POST"])
def delete_account():
    user_session = session.get("user")


    if not user_session:
        return jsonify({"message": "Unauthorized"}), 401

    email = user_session.get("email")
    if not email:
        return jsonify({"message": "User email not found in session"}), 400

    try:
        result = users_collection.delete_one({"email": email})
    except Exception as e:
        print("DEBUG: Mongo deletion error:", e)
        return jsonify({"message": "Server error while deleting account"}), 500

    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404

    session.pop("user", None)
    return jsonify({"message": "Account deleted successfully"}), 200


# ===============================
# Logout
# ===============================
@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    print("Session user logout :", session.get("user"))

    session.pop("user", None)  # Remove user from session

    return jsonify({"message": "Logged out successfully"}), 200


# ===============================
# Session Test (Debug)
# ===============================
@auth_bp.route("/api/session-test")
def session_test():
    print("Session:", session.get("user"))
    return jsonify({"user": session.get("user")})

