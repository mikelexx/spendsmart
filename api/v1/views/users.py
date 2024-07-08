#!/usr/bin/python3
""" routes that handle all default 
RestFul API actions for notifications """
from models import storage
from werkzeug.security import generate_password_hash
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage
from flask import jsonify


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ returns user having the given id"""
    users = storage.all(User)
    users_dict = []
    for user in users.values():
        users_dict.append(user.to_dict(hide_password=True))
    return jsonify(users_dict), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """posts a user to the database """
    data = request.get_json()
    password = data.get("password")
    email = data.get("email")
    username = data.get("username")
    if not email:
        abort(400, description="Email must be provided!")
    elif '@' not in email:
        abort(400, description='Invalid email')
    if not password:
        abort(400, description="Password must be provided!")
    if len(password) < 5:
        abort(400, description="Weak password, provide a stronger password")

    existing_users = storage.all(User)
    if existing_users:
        for user in existing_users.values():
            if user.email == email:
                abort(409, description="User with that email already exists!")
    new_user = User(email=email,
                    password=generate_password_hash(password,
                                                    method='pbkdf2:sha256'))
    if username:
        setattr(new_user, 'username', username)
    new_user.save()
    storage.reload()
    return jsonify(storage.get(User, new_user.id).to_dict(hide_password=True)), 201


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes user with given id from the database """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return '', 204
