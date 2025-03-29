import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def generate_token(username):
    """
    Purpose: Generate a JWT token
    Input: A specific username
    Output: JWT token string
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
    Purpose: Decode a JWT token

    Input: JWT token string
    Output: Decoded payload if token is valid
            None if error is present
    """
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token