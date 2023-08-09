#!/usr/bin/env python3
""" User session model"""

from models.base import Base

""" User session model"""
class UserSession(Base):
    """ User session model"""
    def __init__(self, *args: list, **kwargs: dict):
        """ Constructor"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def to_dict(self) -> dict:
        """ Dictionary representation of User Session"""
        dictionary = super().to_dict()
        dictionary['user_id'] = self.user_id
        dictionary['session_id'] = self.session_id
        return dictionary
    
    def save(self):
        """ Save the instance to the database"""
        from models import db_session
        db_session.add(self)
        db_session.commit()
