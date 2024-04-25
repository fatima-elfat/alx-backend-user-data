#!/usr/bin/env python3
"""
Task 6. Basic Flask app.
Task 7. Register user.
Task 11. Log in.
Task 14. Log out.
Task 15. User profile.
Task 17. Get reset password token.
Task 19. Update password end-point.
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def bienvenue() -> str:
    """
    has a single GET route ("/") and use flask.jsonify
    to return a JSON payload of the form:
        {"message": "Bienvenue"}
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    the end-point to register a user. Define a users
    function that implements the POST /users route.
    """
    try:
        email, pwd = request.form.get("email"), request.form.get("password")
    except KeyError:
        abort(400)
    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    expected to contain form data with "email" and a "password" fields.
    """
    try:
        email = request.form["email"]
        pwd = request.form["password"]
        if not AUTH.valid_login(email, pwd):
            abort(401)
        uuid_ = AUTH.create_session(email)
        r = jsonify({"email": email, "message": "logged in"})
        r.set_cookie("session_id", uuid_)
    except KeyError:
        abort(400)
    return r


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    Find the user with the requested session ID.
    If the user exists destroy the session and redirect
    the user to GET /. If the user does not exist,
    respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def user_profile() -> str:
    """
    The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist, respond
    with a 200 HTTP status and the following JSON payload:
        {"email": "<user email>"}
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> str:
    """The request is expected to contain
    form data with the "email" field.
    If the email is not registered, respond with a 403
    status code. Otherwise, generate a token and respond
    with a 200 HTTP status and the following JSON payload:
        {"email": "<user email>", "reset_token": "<reset token>"}
    """
    try:
        email = request.form["email"]
        reset_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update the password. If the token is invalid,
    catch the exception and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP code
    and the following JSON payload:
        {"email": "<user email>", "message": "Password updated"}
    """
    try:
        email = request.form["email"]
        tkn = request.form["reset_token"]
        new_pwd = request.form["new_password"]
        AUTH.update_password(tkn, new_pwd)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
