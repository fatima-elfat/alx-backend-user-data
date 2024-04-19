#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv("AUTH_TYPE", "auth")
if auth_type == "auth":
    auth = Auth()
elif auth_type == "basic_auth":
    auth = BasicAuth()
if auth_type == "session_auth":
    auth = SessionAuth()
if auth_type == "session_exp_auth":
    auth = SessionExpAuth()
if auth_type == "session_db_auth":
    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Task 1. Error handler: Unauthorized.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Task 2. Error handler: Forbidden.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def authorization():
    """
    Task 0. Et moi et moi et moi!
    Task 5. Before request.
    Update @app.before_request in api/v1/app.py:
        Assign the result of auth.current_user(request)
        to request.current_user
    """
    if auth:
        p = ["/api/v1/status/", "/api/v1/unauthorized/",
             "/api/v1/forbidden/", "/api/v1/auth_session/login/"]
        if auth.require_auth(request.path, p):
            auth_ = auth.authorization_header(request)
            if auth_ is None:
                abort(401)
            user = auth.current_user(request)
            if user is None:
                abort(403)
            request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
