#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """ All Amenities objects """
    all = []
    for amenity in storage.all('Amenity').values():
        all.append(amenity.to_dict())
    return jsonify(all)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def amenity_by_id(amenity_id):
    """ Amenity by id """
    amenity = storage.get('Amenity', amenity_id)
    return jsonify(amenity.to_dict()) if amenity else abort(404)


@app_views.route('amenities/<amenity_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """ Delete an State by id """
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def amenity_post_by_id():
    """Create a new Amenity"""
    try:
        amenity = request.get_json()
        if "name" not in amenity:
            return jsonify('Missing name'), 400

        new_amenity = Amenity(**amenity)
        storage.new(new_amenity)
        storage.save()
        return new_amenity.to_dict(), 201
    except Exception:
        return jsonify('Not a JSON'), 400


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity_by_id(amenity_id):
    """Update an Amenity"""

    update = request.get_json()
    anmenity = storage.get('Amenity', amenity_id)
    if not anmenity:
        abort(404)
    if not update:
        return jsonify('Not a JSON'), 400

    for k, v in update.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(anmenity, k, v)
    storage.save()
    return jsonify(anmenity.to_dict()), 200
