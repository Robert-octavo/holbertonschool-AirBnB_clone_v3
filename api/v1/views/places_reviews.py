#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API"""

from os import stat
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_reviews(place_id):
    """ All cities by state objects """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def review_by_id(review_id):
    """ List a review by id """
    review = storage.get('Review', review_id)
    return jsonify(review.to_dict()) if review else abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review_by_id(review_id):
    """ Delete a review by id """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def review_post_by_id(place_id):
    """Create a new review """

    review = request.get_json()
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if not review:
        return jsonify('Not a JSON'), 400

    if "user_id" not in review:
        return jsonify('Missing user_id'), 400

    user = review['user_id']
    if storage.get('User', user) is None:
        abort(404)

    if "text" not in review:
        return jsonify('Missing text'), 400

    new_city = Review(**review)
    setattr(new_city, 'place_id', place_id)
    storage.new(new_city)
    storage.save()
    return new_city.to_dict(), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review_by_id(review_id):
    """Update a review"""

    update = request.get_json()
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    if not update:
        return jsonify('Not a JSON'), 400

    for k, v in update.items():
        if k not in ["id", "user_id", "place_id", "updated_at", "created_at"]:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
