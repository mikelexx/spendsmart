#!/usr/bin/python3
""" routes that handle all default RestFul API actions for expenses """
from models.expense import Expense
from models import storage
from models.user import User
from models.collection import Collection
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger.utils import swag_from
from models import storage
from flask import jsonify


@app_views.route('/expenses', methods=['POST'], strict_slashes=False)
def post_expense():
    """ posts an expense to the database """
    data = request.get_json()
    if not request.get_json():
        abort(400, description="Not a JSON")
    name = data.get("name")
    purchase_date = data.get("purchase_date")
    price = data.get("price")
    user_id = data.get("user_id")
    collection_id = data.get("collection_id")

    if name is None:
        abort(400, description="Missing name")
    if purchase_date is None:
        abort(400, description="Missing purchase_date")
    if price is None:
        abort(400, description="Missing price")
    if user_id is None:
        abort(400, description="Missing user_id")
    if collection_id is None:
        abort(400, description="Missing collection_id")

    if purchase_date:
        try:
            datetime.strptime(purchase_date, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            abort(400, description="invalid date format")
    if type(price) not in [int, float]:
        abort(400, description="invalid currency input")
    if type(user_id) not in [str]:
        abort(400, description="invalid user id input")
    if collection_id and type(collection_id) not in [str]:
        abort(400, description="invalid collection id input")

    user=  storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exists")

    data = request.get_json()
    instance = Expense(**data)
    instance.save()
    collection = storage.get(Collection, instance.collection_id)
    if collection:
        collection.amount_spent += instance.price
        collection.save()
        collection.check_notifications()
    return jsonify(instance.to_dict()), 201

@app_views.route('/<user_id>/expenses', methods=['GET'], strict_slashes=False)
def get_user_expenses(user_id):
    """ returns collections beloging to particular user"""
    storage.reload()
    user = storage.get(User, user_id)
    if user is None:
        print("no user found")
        abort(404)
    count = request.args.get('count', type=int)
    
    expenses = storage.user_all(user_id, Expense)
    if count and isinstance(count, int):
        expenses = expenses[:count]

    expenses_dict = []
    for expense in expenses:
        expenses_dict.append(expense.to_dict())
    return jsonify(expenses_dict), 200
@app_views.route('/<user_id>/expenses/<expense_id>', methods=['DELETE'], strict_slashes=False)
def delete_expense(user_id, expense_id):
    """ deletes an expense belonging to particular user id given from storage """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    expense = storage.get(Expense, expense_id)
    if not expense:
        abort(404);
    collection = storage.get(Collection, expense.collection_id)
    if collection:
        collection.amount_spent -= expense.price
        collection.save()
        collection.check_notifications()
    expense.delete()
    storage.save()
    return jsonify({"success": True}), 201
@app_views.route('/<user_id>/expenses/<expense_id>', methods=['PUT'], strict_slashes=False)
def update_expense(user_id, expense_id):
    """ updates the details of an expense """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    expense = storage.get(Expense, expense_id)
    initial_price = expense.price
    old_collection = storage.get(Collection, expense.collection_id)
    if not expense:
        abort(404)
    data = request.get_json()
    data["id"] = expense_id
    data["user_id"] = user_id
    for key, val in data.items():
        if hasattr(expense, key):
            setattr(expense, key, val)
    expense.save()
    new_collection = storage.get(Collection, expense.collection_id)
    if new_collection:
        if new_collection.id != old_collection.id:
            new_collection.amount_spent = new_collection.amount_spent + expense.price
            old_collection.amount_spent = old_collection.amount_spent - initial_price
        else:
            old_collection.amount_spent = (old_collection.amount_spent - initial_price) + expense.price
        old_collection.save()
        new_collection.save()
        new_collection.check_notifications()
        old_collection.check_notifications()

    return jsonify(expense.to_dict()), 200
