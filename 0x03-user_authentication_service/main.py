#!/usr/bin/env python3
"""
Task 20. End-to-end integration test.
"""


import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    register_user(email: str, password: str) -> None
    """
    url = "{}/users".format("http://localhost:5000")
    in_ = {"email": email, "password": password}
    resp = requests.post(url, data=in_)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    log_in_wrong_password(email: str, password: str) -> None
    """
    url = "{}/sessions".format("http://localhost:5000")
    in_ = {"email": email, "password": password}
    resp = requests.post(url, data=in_)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    log_in(email: str, password: str) -> str
    """
    url = "{}/sessions".format("http://localhost:5000")
    in_ = {"email": email, "password": password}
    resp = requests.post(url, data=in_)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    session_id = resp.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """
    profile_unlogged() -> None
    """
    url = "{}/profile".format("http://localhost:5000")
    cookies = {"session_id": ""}
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    profile_logged(session_id: str) -> None
    """
    url = "{}/profile".format("http://localhost:5000")
    cookies = {"session_id": session_id}
    resp = requests.get(url, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """
    log_out(session_id: str) -> None
    """
    url = "{}/sessions".format("http://localhost:5000")
    cookies = {"session_id": session_id}
    resp = requests.delete(url, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    reset_password_token(email: str) -> str
    """
    url = "{}/reset_password".format("http://localhost:5000")
    resp = requests.post(url, data={"email": email})
    assert resp.status_code == 200
    tkn = resp.json().get("reset_token")
    assert resp.json() == {"email": email, "reset_token": tkn}
    return tkn


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    update_password(email: str, reset_token: str, new_password: str) -> None
    """
    url = "{}/reset_password".format("http://localhost:5000")
    in_ = {"email": email, "reset_token": reset_token,
           "new_password": new_password}
    resp = requests.put(url, data=in_)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
