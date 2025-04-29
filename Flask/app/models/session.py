import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import List
from app.core.database import db

class Session(db.Model):
    """
    Represents a poker session in the database.
    
    Attributes:
        session_id (str): Unique identifier for the session
        username (str): Associated user's username
        buy_in (Decimal): Amount bought in
        buy_out (Decimal): Amount cashed out
        start_time (datetime): Session start time
        end_time (datetime): Session end time
        title (str): Session title
        caption (str): Session description or notes
        images (List[str]): URLs of associated images
        public (bool): Whether session is publicly visible
        blinds (List[Decimal]): List of blind amounts
        ante (Decimal): Ante amount if any
        created_at (datetime): Record creation timestamp
    """
    __tablename__ = 'session'
    
    # Unique session identifier using UUID
    session_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Username associated with the session, with a foreign key constraint referencing users.username
    username = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    
    # Monetary values using DECIMAL(10,2)
    buy_in = db.Column(db.Numeric(10, 2), nullable=False)
    buy_out = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Start and end times (application logic should round these to 1-minute intervals)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    # Title for session
    title = db.Column(db.String(255), nullable=False)
    
    # Longer text for posting captions or personal notes
    caption = db.Column(db.Text, nullable=True)
    
    # URL for an uploaded image 
    images = db.Column(db.JSON, nullable=True)
    
    # Public status
    public = db.Column(db.Boolean, nullable=False, default=True)
    
    # Blinds stored as up to 3 numbers (to 2 decimals) in sorted order; stored in JSON format
    blinds = db.Column(db.JSON)
    
    # Ante value: one number up to 2 decimals; can be null
    ante = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Auto-generated timestamp for record creation
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __repr__(self) -> str:
        return f"<Session {self.session_id} by {self.username}>"