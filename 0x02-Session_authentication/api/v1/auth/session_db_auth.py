#!/usr/bin/env python3
""" Module of Session DB Authentication"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta

""" Session DB Authentication"""
class SessionDBAuth(SessionExpAuth):
    """ Session DB Authentication class"""
    def create_session(self, user_id: str = None) -> str:
        """ Create session ID
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for Session ID
        """
        if session_id is None or type(session_id) != str:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        if created_at is None:
            return None
        expired_time = created_at + timedelta(seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy Session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        user_session = UserSession.search({'session_id': session_cookie})
        if len(user_session) == 0:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True