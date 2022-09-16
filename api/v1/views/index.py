#!/usr/bin/python3
"""Create a route"""

from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def index():
    """ returns a JSON: "status": "OK" """
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type"""
    new_dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return new_dict
