#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
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
    Task 5. Request validation!
    if auth is None, do nothing
    if request.path is not part of this list
    ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'],
    do nothing - you must use the method require_auth from the auth instance
    if auth.authorization_header returns None, raise  401 - you must use abort
    if auth.current_user returns None, raise 403 - you must use abort.
    """
    if auth:
        p = ["/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"]
        if auth.require_auth(request.path, p):
            auth_ = auth.authorization_header(request)
            if auth_ is None:
                abort(401)
            user = auth.current_user(request)
            if user is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
