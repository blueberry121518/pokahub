import os
from dotenv import load_dotenv

def generate_token(username):
    # Retrieve secret key
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Generate token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {"username": username, "exp": expiration_time},
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


