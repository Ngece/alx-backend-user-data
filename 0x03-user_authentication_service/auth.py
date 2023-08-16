#!/usr/bin/env python3
"""Auth module to interact with the authentication database."""

from sqlalchemy.exc import NoResultFound
from db import DB
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hashes password"""
    import bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())