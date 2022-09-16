#!/usr/bin/python3
"""Create a route"""

from flask import Flask
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def index():
    """ returns a JSON: "status": "OK" """
    return {"status": "OK"}
