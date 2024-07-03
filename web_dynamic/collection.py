from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from os import getenv
from models.collection import Collection
from models import storage
import uuid
from datetime import datetime

collection = Blueprint('collection', __name__)
time = "%Y-%m-%dT%H:%M:%S.%f"

api_port = getenv("SPENDSMART_API_PORT")
api_host = getenv("SPENDSMART_API_HOST")

def format_timedelta(end_date):
    timedelta = end_date - datetime.utcnow()
    seconds = timedelta.total_seconds()
    if seconds < 0:
        return "tracking duration expired"
    intervals = (('year', 3600 * 24 * 7 * 4 * 12),
                 ('month', 3600 * 24 * 7 * 4), ('week', 3600 * 24 * 7),
                 ('day', 3600 * 24), ('hour', 3600), ('minute', 60))
    for name, seconds_per_unit in intervals:
        count = seconds / seconds_per_unit
        if count >= 2:
            return "{} {}s".format(int(count), name)
        elif count >= 1:
            return "{} {}".format(int(count), name)
        seconds %= seconds_per_unit
    return "Less than a minute"


def get_notifications(user_id, params=None):
    notification_api_url = "http://{}:{}/api/v1/{}/notifications".format(api_host, api_port,
        user_id)
    params = params
    try:
        notification_response = requests.get(notification_api_url,
                                             params=params)
        notifications = notification_response.json(
        ) if notification_response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching notifications: {e}")
        notifications = []
    return notifications


@collection.route('/dashboard', strict_slashes=False)
@login_required
def dashboard(purchases_list_conf=None):
    """ shows the analytics for tracked collections """
    expenses_api_url = "http://{}:{}/api/v1/{}/expenses".format(api_host, api_port,
        current_user.id)
    collections_api_url = "http://{}:{}/api/v1/{}/collections".format(api_host, api_port,
        current_user.id)
    count = {'count': 5}
    if purchases_list_conf == 'all':
        count = None
    expenses_response = requests.get(expenses_api_url, params=count)
    collections_response = requests.get(collections_api_url)
    expenses = expenses_response.json()
    collections = collections_response.json()

    # Logging responses
    #    print(f"Expenses API Response: {expenses_response.status_code} - {expenses}")
    #    print(f"Collections API Response: {collections_response.status_code} - {collections}")

    if expenses_response.status_code != 200 or collections_response.status_code != 200:
        return "Error fetching data", 500
    detailed_collections = []
    month_names = [
        "jan", "feb", "match", "april", "may", "jun", "july", "aug", "sep",
        "oct", "nov", "dec"
    ]
    for collection in collections:
        for expense in collection["expenses"]:
            purchase_date = datetime.strptime(expense["purchase_date"], time)
            purchase_date = "{} {:d}, {:d}".format(
                month_names[purchase_date.month - 1], purchase_date.day,
                purchase_date.year)
            expense["purchase_date"] = purchase_date
        collection['amount_spent'] = collection["total_spent"]
        remaining_amount = collection['remaining_amount']
        if remaining_amount > 0:
            collection['amount_remaining'] = remaining_amount
        else:
            # here also fire an alert
            collection['exceeded_amount'] = 0 - remaining_amount
        print(collection["end_date"])
        end_date = datetime.strptime(collection["end_date"], time)
        collection["remaining_duration"] = format_timedelta(end_date)
        end_date = "{} {:d}, {:d}".format(month_names[end_date.month - 1],
                                          end_date.day, end_date.year)
        collection["end_date"] = end_date
        detailed_collections.append(collection)
        params = {'read': False}
        notifications = get_notifications(current_user.id, params=params)
    return render_template('dashboard.html',
                           expenses=expenses,
                           collections=detailed_collections,
                           float=float,
                           cache_id=uuid.uuid4())


@collection.route('/show_all_purchases', strict_slashes=False)
@login_required
def show_all_purchases():
    return dashboard(purchases_list_conf='all')


@collection.route('/track_collection_page', strict_slashes=False)
@login_required
def track_collection_page():
    return render_template('track_collection.html', cache_id=uuid.uuid4())


@collection.route('/untrack_collection',
                  methods=['POST'],
                  strict_slashes=False)
@login_required
def untrack_collection():
    """ deletes the selected category and all its associated objects """
    print("BUTTON rleads to untrack_collection: Success")
    collection_id = request.form.get("collection_id")
    collection_name = request.form.get("collection_name")
    api_url = "http://{}:{}/api/v1/{}/collections/{}".format(api_host, api_port,
        current_user.id, collection_id)
    response = requests.delete(api_url)
    if response.status_code == 204:
        flash("""Successfully untracked {},
        purchases of this kind category will no longer be monitored""".format(
            collection_name))
        return redirect(url_for('collection.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")
        return redirect(url_for('collection.dashboard'))


@collection.route('/track_collection', methods=['POST'], strict_slashes=False)
@login_required
def track_collection():
    """ tracks a collection """
    name = request.form.get("name")
    description = request.form.get("description")
    limit = request.form.get("limit")
    start_date = request.form.get("start_date")[:-1] + '001'
    end_date = request.form.get("end_date")[:-1] + '001'
    collection_data = {
        "name": name,
        "description": description,
        "limit": float(limit),
        "start_date": start_date,
        "end_date": end_date,
        "user_id": str(current_user.id)
    }

    # Make the API call to the collections endpoint
    api_url = "http://{}:{}/api/v1/collections".format(api_host, api_port)
    response = requests.post(api_url, json=collection_data)

    if response.status_code == 201:
        flash("Collection tracked successfully!", "success")
        return redirect(url_for('collection.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")

        return redirect(url_for('collection.track_collection_page'))


if __name__ == "__collection__":
    """ Main Function """
    collection.run(host=api_port, port=api_host)
