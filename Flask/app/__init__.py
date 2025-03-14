from flask import Flask
from Flask.app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register Blueprints (routes)
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    return app