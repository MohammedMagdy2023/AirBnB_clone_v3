#!/usr/bin/python3
"""
The API routes for the RESTFUL API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def api():
    return jsonify({"status": "OK"}, 200)

@app_views.route("/stats")
def stats():
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    new_dict = {}
    for key, value in classes.items():
        new_dict[value] = storage.count(key)
    return jsonify(new_dict, 200)
