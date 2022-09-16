#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from os import stat
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ All cities by state objects """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_by_id(city_id):
    """ List a city by id """
    city = storage.get('City', city_id)
    return jsonify(city.to_dict()) if city else abort(404)


@app_views.route('/states/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_city_by_id(city_id):
    """ Delete an city by id """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def city_post_by_id(state_id):
    """Create a new city"""

    city = request.get_json()
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not city:
        return jsonify('Not a JSON'), 400

    if "name" not in city:
        return jsonify('Missing name'), 400

    new_city = City(**city)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city_by_id(city_id):
    """Update a City"""

    update = request.get_json()
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if not update:
        return jsonify('Not a JSON'), 400

    for k, v in update.items():
        if k not in ["id", "state_id", "updated_at", "created_at"]:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
