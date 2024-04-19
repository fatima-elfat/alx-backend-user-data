#!/usr/bin/env python3
"""
Task 10. Sessions in database
"""
from models.base import Base


class UserSession(Base):
    """
     inherits from Base
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Constructor Method, User but for these 2 attributes:
        user_id: string
        session_id: string
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
