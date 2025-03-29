from flask import Blueprint, request, jsonify
import app.services.user_service

user_bp = Blueprint("user", __name__)

user_service = app.services.user_service

@user_bp.route("/create", methods=["POST"])
def user_create():
    """
        Purpose: Create a new user with username and password
        Expects: Unique username and password
        Returns: Success or error message
    """
    # Retrieve data
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Verify that username and password is included
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Delegate the creation of user to user_service
    user, error = user_service.create_user(username, password)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "User successfully created!"}), 201

@user_bp.route("/login", methods=["POST"])
def user_login():
    """
        Purpose: Logs the user in if credentials are correct
        Expects: Username and corresponding password
        Returns: Token and success message if the credentials are correct
                 Error message if not
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    # Delegate authentication to the service.
    token, error = user_service.authenticate_user(username, password)
    if error:
        return jsonify({"message": error}), 400

    return jsonify({"message": "User authenticated and logged in!", "token": token}), 200