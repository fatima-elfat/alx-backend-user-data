#!/usr/bin/env python3
"""
Task 10. Sessions in database.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    inherits from SessionExpAuth.
    """

    def create_session(self, user_id=None):
        """
        creates and stores new instance of UserSession
        and returns the Session ID.
        """
        session_id = super().create_session(user_id)
        if session_id is None or not isinstance(session_id, str):
            return None
        kwargs = {
            "user_id": user_id,
            "session_id": session_id
        }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the User ID by requesting UserSession in
        the database based on session_id.
        """
        if session_id is None:
            return None
        try:
            session = UserSession.search({
                "session_id": session_id
                })
        except Exception:
            return None
        if not session:
            return False
        session = session[0]
        created_at = session.created_at
        expired_time = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()
        if expired_time < current_time:
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on
        the Session ID from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            session = UserSession.search({
                "session_id": session_id
                })
        except Exception:
            return None
        if not session:
            return False
        session = session[0]
        try:
            session.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
