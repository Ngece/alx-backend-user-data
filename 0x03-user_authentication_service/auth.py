#!/usr/bin/env python3
"""Auth module to interact with the authentication database."""
import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4

def _hash_password(password: str) -> bytes:
    """Hashes password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID"""
    return str(uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
            
    def register_user(self ,email: str, password: str) -> User:
        """Registers a new user"""
        db = DB()
        try:
            user = db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = db.add_user(email, hashed_password)
            return useralx-backend-user-data/0x03-user_authentication_service/user.py