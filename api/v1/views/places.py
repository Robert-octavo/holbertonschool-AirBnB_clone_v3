#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from os import stat
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """ All places by city objects """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    places = []
    for city in city.places:
        places.append(city.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def place_by_id(place_id):
    """ List places by id """
    place = storage.get('Place', place_id)
    return jsonify(place.to_dict()) if place else abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_place_by_id(place_id):
    """ Delete an city by id """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def place_post_by_id(city_id):
    """Create a new place"""

    place = request.get_json()
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if not place:
        return jsonify('Not a JSON'), 400
    
    if "user_id" not in place:
        return jsonify('Missing user_id'), 400

    user = place['user_id']
    if storage.get('User', user) is None:
        abort(404)

    if "name" not in place:
        return jsonify('Missing name'), 400

    new_place = Place(**place)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place_by_id(place_id):
    """Update a Place"""

    update = request.get_json()
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if not update:
        return jsonify('Not a JSON'), 400

    for k, v in update.items():
        if k not in ["id", "user_id", "city_at", "updated_at", "created_at"]:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
