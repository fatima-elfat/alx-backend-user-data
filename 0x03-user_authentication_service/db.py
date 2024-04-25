#!/usr/bin/env python3
"""
Task 1. create user.
Task 2. Find user.
Task 3. update user.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar
from user import Base, User


class DB:
    """ DB Class"""

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        save the user to the database.
        """
        user = None
        try:
            user = User(
                email=email,
                hashed_password=hashed_password
            )
            self._session.add(user)
            self._session.commit()
        except Exception:
            self._session.rollback()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        first row found in the users table as filtered by the method’s input
        arguments. No validation of input arguments required at this point.
        """
        keys = User.__table__.columns.keys()
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in keys:
                raise InvalidRequestError
        result = self._session.query(
            User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        locate the user to update, then will update the user’s
        attributes as passed in the method’s arguments then
        commit changes to the database.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in keys:
                raise ValueError
        for key, val in kwargs.items():
            setattr(user, key, val)
        self._session.commit()
