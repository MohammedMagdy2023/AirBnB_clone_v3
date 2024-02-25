#!/usr/bin/python3
"""
Define an api route for stats to get, post and delete stats from the database
"""

from flask import request, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/states/', methods=['GET', 'POST', 'DELETE'])
def states():
    """
    Return a list of all stats in the database
    """
    if request.method == 'GET':
        dict = storage.all('State')
        return jsonify([obj.to_dict() for obj in dict.values()])
    elif request.method == 'POST':
        return jsonify({'message': 'POST /stats'})
    elif request.method == 'DELETE':
        return jsonify({'message': 'DELETE /stats'})
    else:
        return jsonify({'message': 'Not F** found'}), 404
