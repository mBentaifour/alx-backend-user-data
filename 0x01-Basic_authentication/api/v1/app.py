#!/usr/bin/env python3
"""API entry point."""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from api.v1.auth.auth import Auth
import os

app = Flask(__name__)
app.register_blueprint(app_views)
auth = None


auth_type = os.environ.get('AUTH_TYPE')
if auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

@app.before_request
def before_request():
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if request.path in excluded_paths:
        return
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error):
    """Handler for 401 errors"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    """
    Handler for 403
    """
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == "__main__":
    import os
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
