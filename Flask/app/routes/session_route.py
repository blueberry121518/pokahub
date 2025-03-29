from flask import Blueprint, request, jsonify, g
from Flask.app.schemas.session_schema import SessionSchemas
import Flask.app.services.session_service
from Flask.app.middlewares.auth_middleware import token_required

session_bp = Blueprint("sessions", __name__)

session_service = Flask.app.schemas.session_schema

@session_bp.route("/create", methods=["POST"])
@token_required # Checks for valid token
def create_session_route():
    """
        Purpose: Enters a new poker session into database
        Expects: Session details and a corresponding user
        Returns: Saved session details and success or error message
    """

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
    username = token_payload.get("sub")  

    # Uses services to create session in database
    session_obj, error = session_service.create_session(data, username)
    if error:
        return jsonify({"message": error}), 400

    # Dump session object and return
    result = schema.dump(session_obj)
    return jsonify({"message": "Session created successfully", "session": result}), 201