from typing import Tuple, Optional
from app.core.database import db
from app.models.session import Session

def create_session(data: dict, username: str) -> Tuple[Optional[Session], Optional[str]]:
    """
    Create and save a poker session.

    Args:
        data (dict): Session data containing buy_in, buy_out, times, etc.
        username (str): Associated username for the session

    Returns:
        Tuple[Optional[Session], Optional[str]]: (Session object, error message)
            - On success: (Session, None)
            - On failure: (None, error_message)
    """
    try:
        new_session = Session(
            username=username,
            buy_in=data.get('buy_in'),
            buy_out=data.get('buy_out'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            title=data.get('title'),
            caption=data.get('caption'),
            images=data.get('images'),
            public=data.get('public'),
            blinds=data.get('blinds'),
            ante=data.get('ante')
        )
        db.session.add(new_session)
        db.session.commit()
        return new_session, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)