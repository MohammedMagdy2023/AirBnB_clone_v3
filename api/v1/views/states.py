#!/usr/bin/python3
"""
Define an api route for stats to get, post and delete stats from the database
"""

from flask import request


@app_views.route("/stats")
def stats():
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    new_dict = {}
    for key, value in classes.items():
        new_dict[value] = storage.count(key)
    return jsonify(new_dict, 200)
