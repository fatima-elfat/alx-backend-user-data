#!/usr/bin/env python3
"""
Task 6. Basic auth.
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    class BasicAuth that inherits from Auth.
    For the moment this class will be empty.
    """
