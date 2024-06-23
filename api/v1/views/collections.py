#!/usr/bin/python3
""" routes that handle all default RestFul API actions for collections """
from models.collection import Collection
from models import storage
from models.user import User
from models.expense import Expense
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models.notification import Notification
import requests
from datetime import datetime
time = "%Y-%m-%dT%H:%M:%S.%f"
@app_views.route('/<user_id>/collections/<collection_id>', methods=['DELETE'], strict_slashes=False)
def delete_collection(collection_id, user_id):
    """ deletes collection from the database and all 
    the associated expenses and alerts
    """
    api_url = "http://127.0.0.1:5001/api/v1/{}/collections/{}/expenses/".format(user_id, collection_id)
    response = requests.get(api_url)
    if response.status_code == 200:
        expenses = response.json()
        for expense in expenses:
            expense_id = expense.get('id');
            delete_expense_url = "http://127.0.0.1:5001/api/v1/{}/expenses/{}".format(user_id, expense_id)
            response = requests.delete(delete_expense_url)
            if response.status_code != 201:
                abort(500)
        collection_obj = storage.get(Collection, collection_id)
        notifications = storage.all(Notification)
        if notifications:
            print("==================start of problems ===========================")
            for notification in notifications.values():
                print(notification.to_dict())
                if notification.collection_id == collection_obj.id:
                    notification.delete()
                    storage.save()
        collection_obj.delete()
        storage.save()
        return jsonify({"success": True}), 204
    else:
        abort(response.status_code);

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
                datetime.strptime(date_str, time)
            except ValueError:
                abort(400, description="invalid date format")
    if type(limit) not in [int, float]:
        abort(400, description="invalid currency input")
    if type(user_id) not in [str]:
        abort(400, description="invalid user id input")

    user=  storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exists")
    start_date = datetime.strptime(start_date, time)
    end_date = datetime.strptime(end_date, time)
    time_delta = end_date - start_date
    if time_delta.total_seconds() <= 0:
        abort(400, description="tracking duration end date must be after start date")
    api_url = "http://127.0.0.1:5001/api/v1/{}/collections".format(user_id)
    response = requests.get(api_url)
    if response.status_code == 200:
        existing_collections = response.json()
        for col in existing_collections:
            if col["name"] == name:
                abort(400, description="already monitoring {}".format(name))

    data = request.get_json()
    instance = Collection(**data)
    instance.save()
    instance.check_notifications()
    return jsonify(instance.to_dict()), 201

@app_views.route('/<user_id>/collections/<collection_id>/expenses/', methods=['GET'], strict_slashes=False)
def get_user_collection_expenses(user_id, collection_id):
    """ returns user expenses associated with a specific collection id
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    api_url = "http://127.0.0.1:5001/api/v1/{}/expenses/".format(user_id)
    response = requests.get(api_url)
    if response.status_code == 200:
        collection_expenses = []
        amount_spent = 0.00
        expenses = response.json()
        if len(expenses) > 0:
            for expense in expenses:
                if expense["collection_id"] == collection_id:
                    collection_expenses.append(expense)
        return jsonify(collection_expenses), 200
    else:
        abort(500)
@app_views.route('/<user_id>/collections', methods=['GET'], strict_slashes=False)
def get_user_collections(user_id):
    """ returns collections beloging to particular user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    count = request.args.get('count', type=int)
    collections = storage.user_all(user_id, Collection)
    if count and isinstance(count, int):
        collections = collections[:count]
    colls = []
    for collection in collections:
        api_url = "http://127.0.0.1:5001/api/v1/{}/collections/{}/expenses/".format(user_id, collection.id)
        response = requests.get(api_url)
        if response.status_code  != 200:
            abort(500)
        collection = collection.to_dict()
        expenses = response.json()
        total_spent = 0.0
        for expense in expenses:
            total_spent += expense["price"]

        collection["expenses"] = expenses
        collection["total_spent"] = total_spent
        collection["remaining_amount"] = collection["limit"] - collection["total_spent"]
        collection["percentage_spent"] = int((collection["total_spent"] / collection["limit"]) * 100)
        colls.append(collection)
    return colls
