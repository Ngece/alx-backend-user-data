from flask import request
from typing import List, TypeVar

class Auth:
    """Auth class for managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path and excluded paths       
        Args:
            path (str): The request path.
            excluded_paths (List[str]): List of paths that are excluded from authentication.       
        Returns:
            bool: False (authentication is not required for now).
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header from the request       
        Args:
            request: The Flask request object.       
        Returns:
            str: The value of the Authorization header.
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user
        Args:
            request: The Flask request object.   
        Returns:
            TypeVar('User'): The current user object.
        """
        return None
