from app.core.database import db
from Flask.app.models.session import Sessions

def create_session(data, username):
    """
    Purpose: Creates and save a poker session
    Input: Session data and associated username
    Output: Created session if successful
            None if unsucceessful
    """
    try:
        new_session = Sessions(
            username=username,
            buy_in=data.get('buy_in'),
            buy_out=data.get('buy_out'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            title=data.get('title'),
            caption=data.get('caption'),
            image_url=data.get('image_url'),
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