from flask import Blueprint, request, jsonify
import Flask.app.services.user_service

user_bp = Blueprint("user", __name__)

user_services = app.services.user_service

@user_bp.route("/create", methods=["POST"])
def user_create():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Delegate user creation to the service.
    user, error = user_services.create_user(username, password)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "User successfully created!"}), 201

@user_bp.route("/login", methods=["POST"])
def user_login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Delegate authentication to the service.
    token, error = user_services.authenticate_user(username, password)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "User authenticated and logged in!", "token": token}), 200