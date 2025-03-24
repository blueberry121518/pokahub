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

def verify_token(token, expected_username):
    """
    Verify and decode a JWT token, ensuring that the token's subject matches the expected username.
    """

    # Attempts to decode the token
        # If the token is expired or doesn't exist, or the username doesn't match, return None
        # Else return the corresponding decoded payload
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

        if payload.get("sub") != expected_username:
            return None  # Token valid but does not belong to the expected user
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token