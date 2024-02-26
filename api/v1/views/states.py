#!/usr/bin/python3
"""API endpoints for managing states."""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve information for all states."""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve information for a specific state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state based on its ID."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new state."""
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    if "name" not in request.get_json():
        return make_response(
            jsonify({"error": "Missing required attribute: name."}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"],
                 strict_slashes=False)
def update_state(state_id):
    """Update a state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ["id", "created_at", "updated_at"]:
            setattr(state, attribute, value)
    state.save()
    return jsonify(state.to_dict())
