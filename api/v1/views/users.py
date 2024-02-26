#!/usr/bin/python3
"""API endpoints for managing users."""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieve information for all users."""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieve information for a specified user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user based on its ID."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user."""
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    if "email" not in request.get_json():
        return make_response(
            jsonify({"error": "Missing required attribute: email."}), 400)
    if "password" not in request.get_json():
        return make_response(
            jsonify({"error": "Missing required attribute: password."}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Update a user."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, attribute, value)
    user.save()
    return jsonify(user.to_dict())
