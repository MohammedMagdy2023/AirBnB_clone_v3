#!/usr/bin/python3
"""API endpoints for managing cities."""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieve information for all cities in a specified state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieve information for a specified city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city based on its ID."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>/cities/", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new city."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    if "name" not in request.get_json():
        return make_response(
            jsonify({"error": "Missing required attribute: name."}), 400)
    city = City(state_id=state_id, **request.get_json())
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, attribute, value)
    city.save()
    return jsonify(city.to_dict())
