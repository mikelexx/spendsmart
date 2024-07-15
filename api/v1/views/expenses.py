#!/usr/bin/python3
""" routes that handle all default RestFul API actions for expenses """
from models.expense import Expense
from decimal import Decimal
from models import storage
from models.user import User
from models.collection import Collection
from datetime import datetime
from api.v1.views import app_views
from flask import abort, jsonify, request, current_app as app
from flasgger.utils import swag_from
from models import storage
from flask import jsonify
from os import getenv
time =  '%Y-%m-%dT%H:%M:%S.%f'
def validate_fields(purchase_date=None, name=None, price=None, user_id=None, collection_id=None, id=None):
    """checks for logic and format validity of the fields for creating an Expense """
    if purchase_date:
        try:
            datetime.strptime(purchase_date, time)
        except ValueError:
            abort(400, description="invalid date format")
    if price and type(price) not in [int, float]:
        abort(400, description="invalid currency input")
    elif price:
        try:
            price = Decimal(price)
            if price > Decimal('99999999.99'):
                abort(400, description='Price is too large')
            if price <= 0:
                abort(400, description='Price is too loo')
        except Exception as e:
            abort(400, description='invalid price')
    if user_id and type(user_id) not in [str]:
        abort(400, description="invalid user id input")
    if collection_id:
        if type(collection_id) not in [str]:
            abort(400, description="invalid collection id input")
    
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
    collection  = storage.get(Collection, collection_id)
    if not collection:
        abort(400, description='no collection exists for that collection id')
    validate_fields(**data)


    user = storage.get(User, user_id)
    if not user:
        abort(400, description="user with that id does not exists")
    collection = storage.get(Collection, data["collection_id"])
    if not collection:
        abort(400, description="create a budget first")
    formatted_purchase_date = datetime.strptime(purchase_date, time)
    if not collection.start_date <= formatted_purchase_date <= collection.end_date:
        abort(400, description='purchase date not in tracking time range for {}'.format(collection.name))

    existing_expense = storage.get(Expense, data.get('id'))
    if existing_expense:
        abort(409, description='same expense entry already exists')
    instance = Expense(**data)
    try:
        collection.amount_spent += Decimal(instance.price)
        collection.check_notifications()
    except Exception as e:
        print(e)
        abort(500, description=e)
    data = request.get_json()
    #expired collection may have been deleted at time of saving
    try:
        collection.save()
    except Exception as e:
        abort(400, description="{} no longer exists".format(collection.name))
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/users/<user_id>/expenses', methods=['GET'], strict_slashes=False)
def get_user_expenses(user_id):
    """ returns collections beloging to particular user"""
    storage.reload()
    user = storage.get(User, user_id)
    if user is None:
        abort(400)
    count = request.args.get('count', type=int)

    expenses = storage.user_all(user_id, Expense)
    if count and isinstance(count, int):
        expenses = expenses[:count]

    expenses_dict = [expense.to_dict() for expense in expenses]
    return jsonify(expenses_dict), 200


@app_views.route('/expenses/<expense_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_expense(expense_id):
    """ deletes an expense of given id from storage """
    try:
        expense = storage.get(Expense, expense_id)
        if not expense:
            app.logger.info('Expense with Id {} was not found'.format(expense_id))
            return jsonify({'success': False, 'error': 'Expense not found'}), 404
        if getenv("SPENDSMART_TYPE_STORAGE") == 'db':
            if expense.collection:
                expense.collection.amount_spent -= expense.price
        else:
            collection = storage.get(Collection, expense.collection_id)
            if collection:
                collection.amount_spent -= expense.price
                collection.save()
                collection.check_notifications()
        expense.delete()
        storage.save()
    except  Exception as e:
        app.logger.error('Error: {}'.format(e))
        return jsonify({'success': False, 'error': 'Server Error'}), 500
    return '', 204

@app_views.route('/users/<user_id>/expenses/<expense_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_expense(user_id, expense_id):
    """ updates the details of an expense """
    user = storage.get(User, user_id)
    move = request.args.get('move', type=bool) or False
    if not user:
        abort(400)
    expense = storage.get(Expense, expense_id)
    if not expense:
        abort(404)
    initial_price = expense.price
    old_collection = storage.get(Collection, expense.collection_id)
    data = request.get_json()
    data["id"] = expense_id
    if data.get('user_id') and data.get('user_id') != user_id:
        abort(400, 'updating user_id not allowed')
    data['user_id'] = user_id
    validate_fields(**data)
    new_collection = storage.get(Collection, data.get('collection_id'))
    #check if new_coll exists to avoid database integrity error
    if not new_collection:
        abort(404, description="destination collection not found")
    for key, val in data.items():
        if hasattr(expense, key):
            if key =='purchase_date' and type(key) is str:
                val = datetime.strptime(val, time)
            setattr(expense, key, val)
    expense.save()

    if not new_collection.start_date <= expense.purchase_date <= new_collection.end_date:
        abort(400, description='purchase date not in tracking time range for {}'.format(new_collection.name))
    if new_collection:
        if new_collection.id != old_collection.id:
            new_collection.amount_spent = new_collection.amount_spent + Decimal(
                expense.price)
            if move:
                old_collection.amount_spent = old_collection.amount_spent - Decimal(
                    initial_price)
        else:
            old_collection.amount_spent = (old_collection.amount_spent -
                                           Decimal(initial_price)) + Decimal(
                                               expense.price)
        old_collection.save()
        new_collection.save()
        new_collection.check_notifications()
        old_collection.check_notifications()

    return jsonify(expense.to_dict()), 200
