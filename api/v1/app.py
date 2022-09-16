#!/usr/bin/python3
"""Flask web application"""

from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove(self):
    """ Remove the current SQLAlchemy session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors that returns a JSON-formatted"""
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
