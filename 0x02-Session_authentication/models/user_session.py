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