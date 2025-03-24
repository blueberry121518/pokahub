import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def generate_token(username):
    """
    Generate a JWT token for the given username.
    """

    # Current time
    now = datetime.now(timezone.utc)

    # Token payload: Holds username for identification verification
    payload = {
        "sub": username,               
        "iat": now,                      
        "exp": now + timedelta(hours=24) 
    }

    # Creates the token by hashing the payload
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    return token

def decode_token(token):
    """
    Decode a JWT token.
    
    Attempts to decode the token using the secret key from the current Flask app.
    Returns the decoded payload if the token is valid.
    Returns None if the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token