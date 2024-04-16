#!/usr/bin/env python3
"""
Task 3. Auth class.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ a class to manage the API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns False - path and excluded_paths
        will be used later, now, you don’t need to take care of them.
        """
        if path is not None and excluded_paths is not None:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        that returns None - request will be the Flask request object.
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None - request will be the Flask request object.
        """
        return None
