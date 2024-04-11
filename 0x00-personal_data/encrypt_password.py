#!/usr/bin/env python3
"""
Task 5 and 6.
Passwords managment.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    expects one string argument name password
    and returns a salted, hashed password, which is a byte string.
    Use the bcrypt package to perform the hashing (with hashpw).

    Args:
        password (str): the password.

    Returns:
        bytes: salted, hashed password.
    """
    encode = password.encode('utf-8')
    return bcrypt.hashpw(encode, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password.
    Args:
        hashed_password (bytes): the hashed password.
        password (str): the password to validate

    Returns:
        bool: is it valid.
    """
    encode = password.encode('utf-8')
    return bcrypt.checkpw(encode, hashed_password)
