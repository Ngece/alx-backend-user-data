#!/usr/bin/env python3
"""Route module for the API"""

from flask import Flask, jsonify, request, abort, Response
from flask import Flask, redirect, url_for, session
from auth import Auth
from flask.helpers import make_response
from typing import List, Dict
from os import getenv 

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> Response:
    """Welcome message for the API"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Response:
    """Register a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    

"""main"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")