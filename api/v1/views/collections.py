#!/usr/bin/python3
""" routes that handle all default RestFul API actions for collections """
from models.collection import Collection
from models import storage
from os import getenv
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
    print("delete collection  API called")
    collection_obj = storage.get(Collection, collection_id)
    if not collection_obj:
        return jsonify({"success": True}), 204
    if getenv("SPENDSMART_TYPE_STORAGE") == 'db':
        collection_obj.delete()
        storage.save()
        return jsonify({"success": True}), 204

    api_url = "http://127.0.0.1:5001/api/v1/{}/collections/{}/expenses/".format(user_id, collection_id)
    response = requests.get(api_url)
    if response.status_code == 200:
        expenses = response.json()
        for expense in expenses:
            expense_id = expense.get('id');
            delete_expense_url = "http://127.0.0.1:5001/api/v1/{}/expenses/{}".format(self.user_id, expense_id)
            response = requests.delete(delete_expense_url)
            if response.status_code != 201:
                abort(500)
    notifications =  storage.all(Notification)
    for notification in notifications.values():
        if notification.collection_id == collection_obj.id:
            notification.delete()
            notification.save()
    collection_obj.delete()
    storage.save()
    return jsonify({"success": True}), 204
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
        abort(400, description="tracking duration end date must be after start date")

    api_url = f"http://127.0.0.1:5001/api/v1/{user_id}/collections"
    response = requests.get(api_url)
    if response.status_code == 200:
        existing_collections = response.json()
        for col in existing_collections:
            if col["name"] == name:
                abort(400, description=f"already monitoring {name}")

    instance = Collection(**data, amount_spent=0.00)
    instance.save()
    instance.check_notifications()
    return jsonify(instance.to_dict()), 201

@app_views.route('/<user_id>/collections/<collection_id>/expenses/', methods=['GET'], strict_slashes=False)
def get_user_collection_expenses(user_id, collection_id):
    """ returns user expenses associated with a specific collection id
    """
#    storage.reload()
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
        coll_ids.append(collection.id)
        api_url = "http://127.0.0.1:5001/api/v1/{}/collections/{}/expenses/".format(user_id, collection.id)
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  
            expenses = response.json()
            print("expenses=", expenses)
        except requests.exceptions.RequestException as e:
            print("exception was", e)
            abort(500)
        
        collection_dict = collection.to_dict()
        collection.check_notifications()
        collection_dict["expenses"] = expenses
        collection_dict["total_spent"] = collection_dict["amount_spent"]  
        collection_dict["remaining_amount"] = float(collection_dict["limit"] - collection_dict["amount_spent"])
        collection_dict["percentage_spent"] = int((collection_dict["amount_spent"] / collection_dict["limit"]) * 100)
        
        colls.append(collection_dict)
    for notif in storage.user_all(user_id, Notification):
        if notif.collection_id in coll_ids and notif.is_read:
            notif.delete()
    storage.save()
    return jsonify(colls), 200

