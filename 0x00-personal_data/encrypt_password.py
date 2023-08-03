#!/usr/bin/env python3
"""A module containing functions that encrypt passwords"""

import bcrypt

def hash_password(password: str) -> bytes:
    """A function that returns a salted, hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """A function that checks if a password is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
