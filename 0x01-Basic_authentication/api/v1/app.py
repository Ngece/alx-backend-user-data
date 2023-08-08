#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401
    abort(403)

""" Unauthorized route"""
@app.route('/api/v1/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ abort unauthorized route
    """
    abort(401)

""" Forbidden route"""
@app.errorhandler(403)
def forbidden(error) -> str:
    """ abort Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403
    
@app.route('/api/v1/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ abort forbidden route
    """
    abort(403)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
