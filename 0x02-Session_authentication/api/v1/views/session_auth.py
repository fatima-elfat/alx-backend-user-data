#!/usr/bin/env python3
"""
Task 7. New view for Session Authentication.
Task 8. Logout.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Task 7. New view for Session Authentication.
    POST /auth_session/login
    """
    email = request.form.get("email")
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if users is None or not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
    # You must use from api.v1.app import auth - WARNING: please import
    # it only where you need it - not on top of the file
    # (can generate circular import - and break first tasks of this project)
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    session_name = getenv("SESSION_NAME")
    res = jsonify(users[0].to_json())
    res.set_cookie(session_name, session_id)
    return res


@app_views.route(
    "/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Task 8. Logout.
    DELETE /auth_session/logout
    """
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)
    return jsonify({}), 200
