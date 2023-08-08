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
CORS(app, resources={r"/api/v1/*": {"origins": "*"}},)
auth = None

if os.getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif os.getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif os.getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif os.getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
elif os.getenv('AUTH_TYPE') == 'session_cookie_auth':
    from api.v1.auth.session_cookie_auth import SessionCookieAuth
    auth = SessionCookieAuth()
elif os.getenv('AUTH_TYPE') == 'session_cookie_db_auth':
    from api.v1.auth.session_cookie_db_auth import SessionCookieDBAuth
    auth = SessionCookieDBAuth()
else:
    pass

@app.before_request
def before_request_func() -> str:
    """ Before request handler
    """
    if auth is None:
        return None
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return None
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)
    request.current_user = auth.current_user(request)
    return None


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
