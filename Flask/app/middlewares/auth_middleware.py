from functools import wraps
from flask import request, jsonify, g, current_app
from app.utils.token import decode_token

def token_required(f):
    """
        Purpose: Wraps a route to make sure a token is associated with the request
        Expects: Token in header
        Returns: Payload(Username) associated with token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Parse auth_header for token
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        # Returns error if token doesnt exist
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        # Decode token to retrieve payload
        payload = decode_token(token)
        if payload is None:
            return jsonify({"message": "Token is invalid or expired!"}), 401
        
        # Attach token payload to the global context
        g.token_payload = payload
        return f(*args, **kwargs)
    
    return decorated