#!/usr/bin/env python3
"""
Task 6. Basic auth.
Task 7. Basic - Base64 part.
Task 8. Basic - Base64 decode.
Task 9. Basic - User credentials.
Task 10. Basic - User object.
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    class BasicAuth that inherits from Auth.
    """

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        returns the Base64 part of the Authorization header for a Basic Auth:
        Return None if authorization_header is None
        Return None if authorization_header is not a string
        Return None if authorization_header doesn’t
            start by Basic (with a space at the end).
        Otherwise, return the value after Basic (after the space)
        You can assume authorization_header contains only one Basic
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Task 8. Basic - Base64 decode.
        returns the decoded value of a Base64
        string base64_authorization_header:
            Return None if base64_authorization_header is None
            Return None if base64_authorization_header is not a string
            Return None if base64_authorization_header is not a
                valid Base64 - you can use try/except
            Otherwise, return the decoded value as UTF8 string
                you can use decode('utf-8')
        """
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            b = b64decode(base64_authorization_header.encode(
                "utf-8"))
            r = b.decode("utf-8")
        except Exception:
            return None
        return r

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Task 9. Basic - User credentials.
        returns the user email and password from the Base64 decoded value.
            This method must return 2 values
            Return None, None if d.._b..._a..._h... is None
            Return None, None if d.._b..._a..._h... is not a string
            Return None, None if d.._b..._a..._h... doesn’t contain :
            Otherwise, return the user email and the user password
                these 2 values must be separated by a :
            You can assume d.._b..._a..._h... will contain only one :
        """

        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        a, b = decoded_base64_authorization_header.split(':', 1)
        return a, b

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Task 10. Basic - User object.
        returns the User instance based on his email and password.
            Return None if user_email is None or not a string
            Return None if user_pwd is None or not a string
            Return None if your database (file) doesn’t contain
                any User instance with email equal to user_email
                you should use the class method search of the User
                to lookup the list of users based on their email.
                Don’t forget to test all cases:
                “what if there is no user in DB?”, etc.
            Return None if user_pwd is not the password of
            the User instance found - you must use
            the method is_valid_password of User
            Otherwise, return the User instance
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
