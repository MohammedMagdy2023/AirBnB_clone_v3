#!/usr/bin/python3
"""
The API routes for the RESTFUL API
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/status", strict_slashes=False)
def api():
    """
    test the api status 
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    function to return the count of all class objects
    """
    if request.method == 'GET':
        response = {}
        classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in classes.items():
            response[value] = storage.count(key)
        return jsonify(response)
