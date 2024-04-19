#!/usr/bin/env python3
"""
Task 9. Expiration?
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    inherits from SessionAuth.
    """

    def __init__(self):
        """
        Constructor Method, Assign an instance attribute session_duration.
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overload def create_session(self, user_id=None).
        """
        session_id = super().create_session(user_id)
        if session_id is None or not isinstance(session_id, str):
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overload def user_id_for_session_id(self, session_id=None).
        """
        if session_id is None or\
                session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if "created_at" not in session_dict:
            return None
        created_at = session_dict.get("created_at")
        expired = created_at + timedelta(seconds=self.session_duration)
        now = datetime.now()
        if expired < now:
            return None
        return session_dict.get("user_id")
