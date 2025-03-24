from datetime import datetime, timezone
from app.core.database import db

class User(db.Model):
    __tablename__ = 'user'

    # Use username as the primary key, ensuring it's unique and not nullable.
    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    
    # User's chosen displayname
    display_name = db.Column(db.String(80), nullable=False)
    
    # Store the hashed password.
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Use a timezone-aware current time for created_at.
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.username} ({self.displayname})>"