from flask import Flask
from app.core.config import Config
from app.core.database import db 
from app.routes import user_bp, session_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database with app
    db.init_app(app)

    # Import and register Blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(session_bp, url_prefix='/session')

    return app