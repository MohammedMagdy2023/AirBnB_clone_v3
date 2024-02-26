#!/usr/bin/python3
"""API endpoints for managing places."""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve information for all places in a specified city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve information for a specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place based on its ID."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    body = request.get_json()
    if "user_id" not in body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, body["user_id"])
    if user is None:
        abort(404)
    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_place = Place(city_id=city_id, **body)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    """Update a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ["id", "user_id", "city_id", "created_at",
                             "updated_at"]:
            setattr(place, attribute, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_places():
    """Search for places."""
    if request.get_json() is not None:
        body = request.get_json()
        states = body.get("states", [])
        cities = body.get("cities", [])
        amenities = body.get("amenities", [])
        amenity_objects = [storage.get("Amenity", amenity_id)
                           for amenity_id in amenities]

        if states == cities == []:
            places = storage.all(Place).values()
        else:
            places = []
            for state_id in states:
                state = storage.get("State", state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get(City, city_id)
                for place in city.places:
                    places.append(place)

        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
