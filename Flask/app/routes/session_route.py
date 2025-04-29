from flask import Blueprint, request, jsonify, g
from app.schemas.session_schema import SessionSchema
from app.services import session_service
from app.middlewares.auth_middleware import token_required

session_bp = Blueprint("session", __name__)

@session_bp.route("/create", methods=["POST"])
@token_required
def create_session_route():
    """
    Create a new poker session.

    Requires: Valid JWT token in Authorization header
    Request body: JSON with session details (see SessionSchema)
    
    Returns:
        201: Session created successfully
        400: Invalid input data
        401: Invalid or missing token
    """
    schema = SessionSchema()
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No input data provided"}), 400

    errors = schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    username = g.token_payload.get("sub")
    session_obj, error = session_service.create_session(data, username)
    
    if error:
        return jsonify({"message": error}), 400

    result = schema.dump(session_obj)
    return jsonify({
        "message": "Session created successfully",
        "session": result
    }), 201

@session_bp.route("/stats", methods=["GET"])
@token_required # Checks for valid token
def fetch_stats_route():
    """
        Purpose: Fetches user stats
        Expects: Corresponding user token
        Returns: A list of cleaned session data

        Notes: We want to return a list of pure data so that the front end only has what it really needs
                Session history can be a link to user's own profile
                Trend Chart: Y-Axis: [(Blinds), (Cash)] X-Axis: [(Time), (Session), (Hours)][This can have a range associated]
                Need to return a list that can easily be used to display these stats: Big Blind, Profit, Time, Hours
                Other stats: This will be based on the range associated with the trend chart - 
                            Average profit([Blinds], [Cash]) / If time, do by session
                            
                            

    """

    

    # Use schema to validate output
    # Return schema

