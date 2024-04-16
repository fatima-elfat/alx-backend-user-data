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
        Task 4. Define which routes don't need authentication.
        returns False - path and excluded_paths
        """
        if path is not None and excluded_paths is not None:
            for ex_path in excluded_paths:
                ex_path = ex_path.strip()
                if ex_path[-1] in ['*', '/']:
                    if path == ex_path[0:-1]:
                        return False
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
