#!/usr/bin/env python3
""" Auth module"""

from flask import request
from typing import List, TypeVar
from os import getenv

""" Auth class"""
class Auth:
    """Auth class for managing API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path and excluded paths       
        Args:
            path (str): The request path.
            excluded_paths (List[str]): List of paths that are excluded from authentication.     
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        
        """ Ensure slash tolerance"""
        path = path.rstrip('/') + '/'
        
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                prefix = excluded_path[:-1]
                if path.startswith(prefix):
                    return False
            elif path == excluded_path:
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
        if 'Authorization' not in request.headers:
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

    def session_cookie(self, request=None):
        """ Session Cookie
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))

