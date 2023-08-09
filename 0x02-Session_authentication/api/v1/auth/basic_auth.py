#!/usr/bin/env python3
""" BasicAuth module"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User

class BasicAuth(Auth):
    """BasicAuth class for managing the API authentication"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header
        Args:
            authorization_header (str): The Authorization header.
        Returns:
            str: The Base64 part of the Authorization header.
        """
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode a Base64 string
        Args:
            base64_authorization_header (str): The Base64 string.
        Returns:
            str: The decoded value.
        """
        if base64_authorization_header is None or type(base64_authorization_header) is not str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract the user credentials from a decoded Base64 string
        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string.
        Returns:
            tuple: The user email and password.
        """
        if decoded_base64_authorization_header is None or type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Return the User instance based on his email and password
        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.
        Returns:
            TypeVar('User'): The User instance.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Overload Auth and retrieve the User instance for a request
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): The User instance.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_b64_auth_header = self.decode_base64_authorization_header(b64_auth_header)
        if decoded_b64_auth_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_b64_auth_header)
        if user_credentials is None:
            return None
        user = self.user_object_from_credentials(user_credentials[0], user_credentials[1])
        return user
    