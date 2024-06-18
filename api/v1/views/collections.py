#!/usr/bin/python3
""" routes that handle all default RestFul API actions for collections """
from models.collection import Collection
from models import storage
from models.user import User
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from

@app_views.route('/collections', methods=['POST'], strict_slashes=False)
def post_collection():
    """
    Creates a State
    """
    data = request.get_json()

    if not request.get_json():
        abort(400, description="Not a JSON")
    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    limit = data.get("limit")
    user_id = data.get("user_id")

    if name is None:
        abort(400, description="Missing name")
    if start_date is None:
        abort(400, description="Missing start_date")
    if end_date is None:
        abort(400, description="Missing end_date")
    if limit is None:
        abort(400, description="Missing limit")
    if user_id is None:
        abort(400, description="Missing user_id")

    for date_str in [start_date, end_date]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                abort(400, description="invalid date format")
    if type(limit) not in [int, float]:
        print(type(limit), limit)
        abort(400, description="invalid currency input")
    if type(user_id) not in [str]:
        abort(400, description="invalid user id input")

    user=  storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exists")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    time_delta = end_date - start_date
    if time_delta.total_seconds() <= 0:
        abort(400, description="tracking duration end date must be after start date")
    data = request.get_json()
    instance = Collection(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/<user_id>/collections', methods=['GET'], strict_slashes=False)
def get_user_collections(user_id):
    """ returns collections beloging to particular user"""
    collections = storage.user_all(user_id, Collection)
    coll_dict = []
    for collection in collections:
        coll_dict.append(collection.to_dict())
    return coll_dict

