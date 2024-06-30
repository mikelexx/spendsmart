#!/usr/bin/python3
""" Starts a Flash Web Application """

from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models.collection import Collection
from .collection import collection
from models import storage
import uuid
from datetime import datetime

main = Blueprint('main', __name__)


@main.route('/landing', strict_slashes=False)
def landing_page():
    """landing page for website """
    return render_template('landing.html', cache_id=uuid.uuid4())


@main.route('/home', strict_slashes=False)
@main.route('/', strict_slashes=False)
def home():
    """ Spendsmart is alive! """
    if current_user.is_authenticated:
        return redirect(url_for('collection.dashboard'))
    return render_template('landing.html', cache_id=uuid.uuid4())


@main.route('/log_expense_page', strict_slashes=False)
@login_required
def log_expense_page():
    api_url = "http://127.0.0.1:5001/api/v1/{}/collections/".format(
        current_user.id)
    response = requests.get(api_url)
    collections = response.json()
    disable = False
    if not collections:
        disable = True
    return render_template('log_expense.html',
                           disable=disable,
                           collections=collections,
                           cache_id=uuid.uuid4())


@main.route('/notifications', methods=['GET'], strict_slashes=False)
@login_required
def notifications():
    params = {'read': False}
    notification_api_url = "http://127.0.0.1:5001/api/v1/{}/notifications".format(
        current_user.id)
    notification_response = requests.get(notification_api_url, params=params)
    notifications = []
    if notification_response.status_code == 200:
        notifications = notification_response.json()
    return render_template('notifications.html',
                           notifications=notifications,
                           cache_id=uuid.uuid4())


@main.route('/mark_notification_as_read',
            methods=['POST'],
            strict_slashes=False)
@login_required
def mark_notification_as_read():
    notification_id = request.form.get('notification_id')
    data = {"is_read": True}
    notification_api_url = "http://127.0.0.1:5001/api/v1/{}/notifications/{}".format(
        current_user.id, notification_id)
    notification_response = requests.put(notification_api_url, json=data)
    return notifications()


@main.route('/log_expense', methods=['POST'], strict_slashes=False)
@login_required
def log_expense():
    """ adds an item to the list of items bought for a certain 
    tracked collection 
    """
    name = request.form.get("name")
    collection_id = request.form.get("collection_id")
    price = request.form.get("price")
    purchase_date = request.form.get("purchase_date")[:-1] + '001'
    print(purchase_date)
    expense_data = {
        "name": name,
        "collection_id": collection_id,
        "price": float(price),
        "purchase_date": purchase_date,
        "user_id": current_user.id
    }

    api_url = "http://127.0.0.1:5001/api/v1/expenses"
    response = requests.post(api_url, json=expense_data)

    if response.status_code == 201:
        flash("Expense added successfully!", "success")
        return redirect(url_for('collection.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")
        return redirect(url_for('main.log_expense_page'))


if __name__ == "__main__":
    """ Main Function """
    main.run(host='0.0.0.0', port=5000)
