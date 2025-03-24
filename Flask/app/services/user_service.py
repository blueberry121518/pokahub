from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.core.database import db
from app.utils.token import generate_token

def create_user(username, password):
    """
    Creates a new user if the username does not already exist.
    Returns a tuple: (User object or None, error message or None).
    """
    # Check if the username is already taken.
    if User.query.filter_by(username=username).first():
        return None, "Username already exists!"
    
    # Hash the password.
    password_hash = generate_password_hash(password)
    
    # Create a new user instance.
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return new_user, None

def authenticate_user(username, password):
    """
    Authenticates a user by username and password.
    Returns a tuple: (token or None, error message or None).
    """
    # Retrieve the user by username.
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, "Username doesn't exist!"
    
    # Verify the password.
    if check_password_hash(user.password_hash, password):
        # Generate a token using the user's username.
        token = generate_token(user.username)
        return token, None
    else:
        return None, "Invalid password!"