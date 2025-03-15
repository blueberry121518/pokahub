from flask import Flask
from ..config import Config
from .database import db  # Import database instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database with app
    db.init_app(app)

    # Import and register Blueprints
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    return app