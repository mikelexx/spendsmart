#!/usr/bin/python3
""" Starts a Flash Web Application """

from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models.collection import Collection
from models import storage
import uuid
from datetime import datetime
main = Blueprint('main', __name__)

@main.route('/', strict_slashes=False)
def home():
    """ HBNB is alive! """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html',
                           cache_id=uuid.uuid4())
@main.route('/log_expense_page', strict_slashes=False)
@login_required
def log_expense_page():
    api_url = "http://127.0.0.1:5001/api/v1/{}/collections/".format(current_user.id)
    response = requests.get(api_url)
    collections = response.json()
    return render_template('log_expense.html', collections=collections, cache_id=uuid.uuid4())
@main.route('/log_expense', methods=['POST'], strict_slashes=False)
@login_required
def log_expense():
    """ adds an item to the list of items bought for a certain 
    tracked collection 
    """
    name = request.form.get("name")
    collection_id = request.form.get("collection_id")
    price = request.form.get("price")
    purchase_date_str = request.form.get("purchase_date")
    purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d %H:%M:%S")
    expense_data = {
        "name": name,
        "collection_id": collection_id,
        "price": float(price),
        "purchase_date": purchase_date.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": current_user.id
    }

    api_url = "http://127.0.0.1:5001/api/v1/expenses"
    response = requests.post(api_url, json=expense_data)

    if response.status_code == 201:
        flash("Expense added successfully!", "success")
        return redirect(url_for('main.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")
        return redirect(url_for('main.log_expense_page'))

@main.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    """ shows the analytics for tracked collections """
    expenses_api_url = "http://127.0.0.1:5001/api/v1/{}/expenses".format(current_user.id)
    collections_api_url = "http://127.0.0.1:5001/api/v1/{}/collections".format(current_user.id)
    params = {'count': 5}
    expenses = requests.get(expenses_api_url, params=params).json()
    collections = requests.get(collections_api_url).json()
    for expense in expenses:
        for col in collections:
            if expense["collection_id"] == col["id"]:
                print(col["name"])
    return render_template('dashboard.html', 
            expenses=expenses,
            collections=collections,
            cache_id=uuid.uuid4())


@main.route('/track_collection_page', strict_slashes=False)
@login_required
def track_collection_page():
    return render_template('track_collection.html', cache_id=uuid.uuid4())

@main.route('/track_collection', methods=['POST'], strict_slashes=False)
@login_required
def track_collection():
    """ tracks a collection """
    name = request.form.get("name")
    description = request.form.get("description")
    limit = request.form.get("limit")
    raw_start_date = request.form.get("start_date")
    raw_end_date = request.form.get("end_date")
    start_date = datetime.strptime(raw_start_date, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(raw_end_date, "%Y-%m-%d %H:%M:%S")
    collection_data = {
        "name": name,
        "description": description,
        "limit": float(limit),
        "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S"),
        "end_date": end_date.strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": str(current_user.id) 
    }

    # Make the API call to the collections endpoint
    api_url = "http://127.0.0.1:5001/api/v1/collections"
    response = requests.post(api_url, json=collection_data)

    if response.status_code == 201:
        flash("Collection tracked successfully!", "success")
        return redirect(url_for('main.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")

        return redirect(url_for('main.track_collection_page'))
if __name__ == "__main__":
    """ Main Function """
    main.run(host='0.0.0.0', port=5000)
