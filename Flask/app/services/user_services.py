import mysql.connector
import os
from dotenv import load_dotenv

def database_initiate():
    load_dotenv()

    return mysql.connector.connect(
        host = "localhost",
        user = "blueberry@%",
        password = os.getenv("DATABASE_PASSWORD"),
        database = "poker"
    )

def database_session_upload(user_id, buy_in, buy_out, start_time, end_time, big_blind, small_blind, title, notes, images):
    # Initiate connections
    connection = database_initiate()
    cursor = connection.cursor()

    # Insert session
    query = """
        INSERT INTO sessions (user_id, buy_in, buy_out, start_time, end_time, big_blind, small_blind, title, notes, images, likes, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, [])
    """
    values = [user_id, buy_in, buy_out, start_time, end_time, big_blind, small_blind, title, notes, images]
    cursor.execute(query, values)
    connection.commit()

    # Close connections
    cursor.close()
    connection.close()

    return

def database_user_create(username, password_hash):
    # Initiate connections
    connection = database_initiate()
    cursor = connection.cursor()

    # Insert session
    query = """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
    """
    values = [username, password_hash]
    cursor.execute(query, values)
    connection.commit()

    # Close connections
    cursor.close()
    connection.close()

def database_user_authentication(username, password_hash) -> bool:
    # Initiate connections
    connection = database_initiate()
    cursor = connection.cursor()

    # Retrieve password_hash
    query = """
        SELECT * FROM sessions WHERE username = %s
    """
    cursor.execute(query, (username, ))
    saved_password_hash = cursor.fetchall()["password_hash"]

    # Close connections
    cursor.close()
    connection.close()

    # Validate user and return result
    if saved_password_hash == password_hash:
        return True
    else:
        return False

def database_user_exists(username) -> bool:
    # Initiate connections
    connection = database_initiate()
    cursor = connection.cursor()

    # Check for existing username
    query = """
        SELECT COUNT(*) FROM poker_sessions WHERE username = %s;
    """
    cursor.execute(query, (username, ))
    existing = cursor.fetchone()[0]

    # Close connections
    cursor.close()
    connection.close()

    # Return result
    if existing == 1:
        return True
    else:
        return False
    
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



    




