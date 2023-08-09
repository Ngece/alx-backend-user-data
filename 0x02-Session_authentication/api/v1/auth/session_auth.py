#!/usr/bin/env python3
""" Module of Session Authentication"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid
from os import getenv

""" Session Authentication"""
class SessionAuth(Auth):
    """ Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session ID
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for Session ID
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """ Current User
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

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
        del self.user_id_by_session_id[session_cookie]
        return True

    def session_cookie(self, request=None):
        """ Session Cookie
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
    