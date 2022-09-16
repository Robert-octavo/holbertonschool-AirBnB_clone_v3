#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from os import stat
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """ All States objects """
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_by_id(state_id):
    """ State by id """
    state = storage.get('State', state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_by_id(state_id):
    """ Delete an State by id """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_by_id():
    """Create a new State"""
    try:
        state = request.get_json()
        if "name" not in state:
            return jsonify('Missing name'), 400

        new_state = State(**state)
        storage.new(new_state)
        storage.save()
        return new_state.to_dict(), 201
    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_by_id(state_id):
    """Update a State"""
    update = request.get_json()
    try:
        state = storage.get('State', state_id)
        if not state:
            abort(404)
        for k, v in update.items():
            setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
    except Exception:
        return jsonify('Not a JSON'), 400
