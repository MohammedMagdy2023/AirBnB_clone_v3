#!/usr/bin/python3
"""API endpoints for managing reviews."""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve reviews for a specified place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve information for a specified review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review based on its ID."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new review."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    body = request.get_json()
    if "user_id" not in body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get("User", body["user_id"])
    if user is None:
        abort(404)
    if "text" not in body:
        return make_response(jsonify({"error": "Missing text"}), 400)
    review = Review(place_id=place_id, **body)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Update a review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Request body must be JSON."}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ["id", "user_id", "place_id",
                             "created_at", "updated_at"]:
            setattr(review, attribute, value)
    review.save()
    return jsonify(review.to_dict())
