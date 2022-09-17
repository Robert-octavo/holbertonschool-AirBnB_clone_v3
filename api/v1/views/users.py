#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from os import stat
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def all_users():
    """ All User objects """
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user_by_id(user_id):
    """ User by id """
    user = storage.get('User', user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@app_views.route('/users/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_a_user_by_id(user_id):
    """ Delete a User by id """
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_post_by_id():
    """Create a new User"""
    try:
        user = request.get_json()
        if "name" not in user:
            return jsonify('Missing name'), 400
        
        if "email" not in user:
            return jsonify('Missing email'), 400
        
        if "password" not in user:
            return jsonify('Missing password'), 400

        new_user = User(**user)
        storage.new(new_user)
        storage.save()
        return new_user.to_dict(), 201
    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user_by_id(user_id):
    """Update a User"""

    update = request.get_json()
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    if not update:
        return jsonify('Not a JSON'), 400

    for k, v in update.items():
        if k not in ["id", "email", "updated_at", "created_at"]:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
