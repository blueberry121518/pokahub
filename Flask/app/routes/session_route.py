from flask import Blueprint, request, jsonify, g
from Flask.app.schemas.session_schema import SessionSchemas
from Flask.app.services.session_service import create_session
from Flask.app.middlewares.auth_middleware import token_required

session_bp = Blueprint("sessions", __name__)

@session_bp.route("/create", methods=["POST"])
@token_required # Checks for valid token
def create_session_route():

    # Initiate schema to format input data
    schema = SessionSchemas()

    # Retrieves data 
    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    # Uses schema to validate data
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Retrieve username from the token payload 
    token_payload = g.get('token_payload')
    username = token_payload.get("sub")  # Assumes token's 'sub' claim stores the username

    # Uses services to create session in database
    session_obj, error = create_session(data, username)
    if error:
        return jsonify({"message": error}), 400

    # Optionally, dump the session object using the same schema.
    result = schema.dump(session_obj)
    return jsonify({"message": "Session created successfully", "session": result}), 201