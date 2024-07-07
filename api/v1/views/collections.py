#!/usr/bin/python3
""" routes that handle all default RestFul API actions for collections """
from models.collection import Collection
from models import storage
from os import getenv
from models.user import User
from models.expense import Expense
from datetime import datetime
from api.v1.views import app_views
from sqlalchemy.exc import SQLAlchemyError
from flask import abort, jsonify, request, current_app as app
from flasgger.utils import swag_from
from models.notification import Notification
import requests
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"

api_port = getenv("SPENDSMART_API_PORT")
api_host = getenv("SPENDSMART_API_HOST")

@app_views.route('/collections/<collection_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_collection(collection_id):
    """ deletes collection from the database and all 
    the associated expenses and and read notifications
    """
    try:
        collection_obj = storage.get(Collection, collection_id)
        if not collection_obj:
            app.logger.info('collection with id {} not found', collection_id)
            return jsonify({"success": False}), 404
        expenses = [exp for exp in storage.user_all(collection_obj.user_id, Expense) if exp.collection_id == collection_id]
        for expense in expenses:
            expense.delete()
        notifications = storage.all(Notification)
        for notification in notifications.values():
            if notification.collection_id == collection_obj.id:
                notification.delete()
        collection_obj.delete()
        storage.save()
    except SQLAlchemyError as e:
        app.logger.error('SQLAlchemyError: {}'.format(e))
        return jsonify({'success': False, 'error': 'Internal Error'}), 500
    except Exception as e:
        app.logger.error('Error: {}'.format(e))
        return jsonify({'success': False, 'error': 'Internal Error'}), 500
    return '', 204

@app_views.route('/collections', methods=['POST'], strict_slashes=False)
def post_collection():
    """
    Creates a Collection
    """
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    required_fields = ["name", "start_date", "end_date", "limit", "user_id"]
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing {field}")

    name = data.get("name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    limit = data.get("limit")
    user_id = data.get("user_id")

    for date_str in [start_date, end_date]:
        if date_str:
            try:
                datetime.strptime(date_str, time)
            except ValueError:
                abort(400, description="invalid date format")

    if not isinstance(limit, (int, float)):
        abort(400, description="invalid currency input")
    if not isinstance(user_id, str):
        abort(400, description="invalid user id input")

    user = storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exist")

    start_date = datetime.strptime(start_date, time)
    end_date = datetime.strptime(end_date, time)
    time_delta = end_date - start_date
    if time_delta.total_seconds() <= 0:
        abort(
            400,
            description="tracking duration end date must be after start date")

    existing_collections = storage.user_all(user_id, Collection)
    for col in existing_collections:
        if col.name == name:
            abort(400, description=f"already monitoring {name}")

    instance = Collection(**data, amount_spent=0.00)
    instance.save()
    instance.check_notifications()
    return jsonify(instance.to_dict()), 201


@app_views.route('/<user_id>/collections/<collection_id>/expenses/',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_collection_expenses(user_id, collection_id):
    """ returns user expenses associated with a specific collection id
    """
    #    storage.reload()
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    collection_expenses = [exp.to_dict() for exp in storage.user_all(user_id, Expense) if exp.collection_id == collection_id]
    return jsonify(collection_expenses), 200


@app_views.route('/<user_id>/collections',
                 methods=['GET'],
                 strict_slashes=False)
def get_user_collections(user_id):
    """Return collections belonging to a particular user."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    count = request.args.get('count', type=int)
    collections = storage.user_all(user_id, Collection)
    if count and isinstance(count, int):
        collections = collections[:count]

    colls = []
    coll_ids = []
    for collection in collections:
        expenses = [exp.to_dict() for exp in storage.user_all(user_id, Expense) if exp.collection_id == collection.id] 
        coll_ids.append(collection.id)
        collection_dict = collection.to_dict()
        collection.check_notifications()
        collection_dict["expenses"] = expenses
        collection_dict["total_spent"] = collection_dict["amount_spent"]
        collection_dict["remaining_amount"] = float(
            collection_dict["limit"] - collection_dict["amount_spent"])
        collection_dict["percentage_spent"] = min(int(
            (collection_dict["amount_spent"] / collection_dict["limit"]) * 100), 100)

        colls.append(collection_dict)
    for notif in storage.user_all(user_id, Notification):
        if notif.collection_id in coll_ids and notif.is_read:
            notif.delete()
    storage.save()
    return jsonify(colls), 200

