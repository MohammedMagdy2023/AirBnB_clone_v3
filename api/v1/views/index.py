#!/usr/bin/python3
"""index.py to connect to API"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def api_status():
    """Tests the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def api_stats():
    """Retrieves the stats of the API"""
    results = {}
    for key, value in classes.items():
        results[key] = storage.count(value)
    return jsonify(results)
