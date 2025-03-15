from flask import Blueprint, jsonify
import database_functions
import functions


user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/session/upload")
def session_upload():
    # Load session data
    data = request.json 

    # Check for required fields
    required_fields = ["user_id", "buy_in", "buy_out", "start_time", "is_public", "big_blind", "small_blind"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    # Parse images (allowing up to 3)
    images = data.get("images", [])
    if not isinstance(images, list) or len(images) > 3:
        return jsonify({"message": "Invalid images field: must be a list with up to 3 image URLs"}), 400

    # Add session
    database_functions.database_session_upload(
        user_id=data.get("user_id"),
        buy_in=data.get("buy_in"),  
        buy_out=data.get("buy_out"),  
        start_time=data.get("start_time"),
        end_time=data.get("end_time"),
        big_blind=data.get("big_blind"),
        small_blind=data.get("small_blind"),
        title=data.get("title"),
        notes=data.get("notes"),
        images=images  
    )
    return jsonify({"message": "Poker session uploaded successfully!"})

@user_bp.route("/user/create")
def user_create():
    # Retrieve username and password
    data = request.json
    username = data["username"]
    password_hash = data["password_hash"]

    # Check if username already exists
    exists = database_functions.database_user_exists(username)
    if exists:
        return jsonify({"message":"Username already exists!"}), 400
    
    # Add new user to database
    database_functions.database_user_create(username, password_hash)
    return jsonify({"message":"User successfully created!"}), 200

@user_bp.route("/user/login")
def user_login():
    # Retrieve username and password
    data = request.json
    username = data["username"]
    password_hash = data["password_hash"]

    # Check if username exists
    exists = database_functions.database_user_exists(username)
    if not exists:
        return jsonify({"message":"Username doesn't exist!"}), 400
    
    # Authenticate user
    authenticated = database_functions.database_user_authentication(username, password_hash)
    if authenticated:
        token = functions.generate_token(username)
        return jsonify({"message":"User authenticated and logged in!", "token":token}), 200
    else:
        return jsonify({"message":"Password doesn't exist!"}), 400