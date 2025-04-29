from flask import Flask
from app.core.config import Config
from app.core.database import db 
from app.routes import user_bp, session_bp

def create_app() -> Flask:
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(session_bp, url_prefix='/session')

    return app