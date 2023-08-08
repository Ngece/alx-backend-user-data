#!/usr/bin/env python3
"""Authentication Module
This module provides a class for handling authentication related tasks.
"""

from flask import request
from typing import List, TypeVar, Optional
from os import getenv
class auth:
    """Authentication class
    This class provides methods for handling authentication tasks.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required
        Args:
            path (str): The request path.
            excluded_paths (List[str]): List of paths that are excluded from authentication.
        Returns:
            bool: True if authentication is required, False if excluded.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        return True
            
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
