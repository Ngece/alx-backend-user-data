#!/usr/bin/env python3
"""Route module for the API"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from flask.helpers import make_response
from typing import List, Dict
from os import getenv 

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message for the API"""
    return jsonify({"message": "Bienvenue"})
