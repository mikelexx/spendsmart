#!/usr/bin/python3
""" routes that handle all default RestFul API actions for expenses """
from models.expense import Expense
from models import storage
from models.user import User
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
    if collection_id is None:
        abort(400, description="Missing collection_id")
    if price is None:
        abort(400, description="Missing price")
    if user_id is None:
        abort(400, description="Missing user_id")

    if purchase_date:
        try:
            datetime.strptime(purchase_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            abort(400, description="invalid date format")
    if type(price) not in [int, float]:
        abort(400, description="invalid currency input")
    if type(user_id) not in [str]:
        abort(400, description="invalid user id input")
    if type(collection_id) not in [str]:
        abort(400, description="invalid collection id input")

    user=  storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exists")
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d %H:%M:%S")
    data = request.get_json()
    instance = Expense(**data)
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/<user_id>/expenses', methods=['GET'], strict_slashes=False)
def get_user_expenses(user_id):
    """ returns collections beloging to particular user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    expenses = storage.user_all(user_id, Expense)
    expenses_dict = []
    for expense in expenses:
        expenses_dict.append(expense.to_dict())
    return expenses_dict
