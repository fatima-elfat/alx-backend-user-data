#!/usr/bin/env python3
"""
Task 4. Hash password.
Task 5. Register user.
Task 8. Credentials validation.
Task 9. Generate UUIDs.
Task 10. Get session ID.
Task 12. Find user by session ID.
Task 13. Destroy session.
Task 16. Generate reset password token.
Task 18. Update password.
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> str:
    """
    takes in a password string arguments and returns bytes.
    The returned bytes is a salted hash of the input password,
    hashed with bcrypt.hashpw.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    function should return a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        take mandatory email and password string arguments
        and return a User object.
        If a user already exist with the passed email, raise a
        ValueError with the message User <user's email> already exists.
        If not, hash the password with _hash_password, save the user
        to the database using self._db and return the User object.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hash = _hash_password(password)
            return self._db.add_user(email, hash)
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Try locating the user by email. If it exists, check the password
        with bcrypt.checkpw. If
        it matches return True. In any other case, return False.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed = user.hashed_password
            encoded = password.encode()
        except NoResultFound:
            return False
        if bcrypt.checkpw(encoded, hashed):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        find the user corresponding to the email, generate a
        new UUID and store it in the database
        as the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            uuid_ = _generate_uuid()
            self._db.update_user(user.id, session_id=uuid_)
        except NoResultFound:
            return None
        return uuid_

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
        returns the corresponding User or None.
        If the session ID is None or no user is found,
        return None. Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user’s session ID to None.
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and update the user’s
        reset_token database field. Return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
            tkn = _generate_uuid()
            self._db.update_user(user.id, reset_token=tkn)
        except NoResultFound:
            raise ValueError
        return tkn

    def update_password(self, reset_token: str, password: str) -> None:
        """
        find the corresponding user. If it does not exist,
        raise a ValueError exception.
        Otherwise, hash the password and update
        the user’s hashed_password field with
        the new hashed password and the reset_token
        field to None.
        """
        if reset_token is not None or password is not None:
            try:
                u = self._db.find_user_by(reset_token=reset_token)
                h = _hash_password(password)
                self._db.update_user(u.id, hashed_password=h, reset_token=None)
            except NoResultFound:
                raise ValueError
