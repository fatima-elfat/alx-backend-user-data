#!/usr/bin/env python3
"""
0x01
    Task 3. Auth class.
0x02
    Task 4. Session cookie.
"""
from flask import request
from os import getenv
from typing import List, TypeVar
import re


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
                if path == ex_path:
                    return False
                if ex_path[-1] in ['/']:
                    if path == ex_path[0:-1]:
                        return False
                if ex_path[-1] in ['*']:
                    if re.match(ex_path[0:-1], path):
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

    def session_cookie(self, request=None):
        """
        Task 4. Session cookie.
        returns a cookie value from a request:
            Return None if request is None
            Return the value of the cookie named _my_session_id from
                request - the name of the cookie must be defined
                by the environment variable SESSION_NAME.
            You must use .get() built-in for accessing the cookie
                in the request cookies dictionary.
            You must use the environment variable SESSION_NAME
                to define the name of the cookie used for the Session ID.
        """
        if request is not None:
            SESSION_NAME = getenv("SESSION_NAME")
            if SESSION_NAME is None:
                return None
            return request.cookies.get(SESSION_NAME)
