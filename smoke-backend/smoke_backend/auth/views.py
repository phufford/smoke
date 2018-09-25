# -*- coding: utf-8 -*-
"""Creates view for user login authentication.

Attributes:
    blueprint (Flask Blueprint): The blueprint scheme for smoke. [#f1]_ [#f2]_

.. [#f1] https://flask-restful.readthedocs.io/en/latest/
.. [#f2] http://flask.pocoo.org/docs/1.0/blueprints/#blueprints
.. [#f3] http://flask.pocoo.org/docs/1.0/api/#flask.json.jsonify
.. [#f4] https://flask-jwt-extended.readthedocs.io/en/latest/token_freshness.html
"""

from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)

from smoke_backend.models import User
from smoke_backend.extensions import pwd_context, jwt


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token.

    Uses flask's jsonify [#f3]_ function to convert requests to valid JSON objects.

    Return:
        flask.Response: If valid request & credentials, returns the valid access tokens for the backend.

            If the user password or username is missing or invalid then method returns a JSON message noting how the
            method failed.

    .. _Flask Local Proxy Request through werkzeug local:
        http://werkzeug.pocoo.org/docs/0.14/wrappers/
    """
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    ret = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return jsonify(ret), 200


@blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Receives access token and refreshes the page.

    Requires a valid jwt token [#f4]_ for access to method.

    Returns:
        Flask Response: A JSONified object containing the updated contents of the login page.
    """
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    """Returns user information

    Parameters:
        identity: The unique identifier for the user

    Returns:

    """
    return User.query.get(identity)
