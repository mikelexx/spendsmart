
from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models.collection import Collection
from models import storage
import uuid
from datetime import datetime
collection = Blueprint('collection', __name__)

@collection.route('/dashboard/', strict_slashes=False)
@login_required
def dashboard(purchases_list_conf=None):
    """ shows the analytics for tracked collections """
    expenses_api_url = "http://127.0.0.1:5001/api/v1/{}/expenses".format(current_user.id)
    collections_api_url = "http://127.0.0.1:5001/api/v1/{}/collections".format(current_user.id)
    print(current_user.id)
    count = {'count': 5}
    if purchases_list_conf == 'all':
        count=None
    expenses = requests.get(expenses_api_url, params=count).json()
    collections = requests.get(collections_api_url).json()
    detailed_collections = []
    months = ["jan", "feb", "match", "april", "may", "jun", "july", "aug", "sep", "oct", "nov", "dec"]
    for collection in collections:
        total = 0
        for expense in collection["expenses"]:
            total += expense["price"]
            purchase_date = datetime.strptime(expense["purchase_date"], "%Y-%m-%d %H:%M:%S")
            purchase_date = "{} {:d}, {:d}".format(months[purchase_date.month - 1], purchase_date.day, purchase_date.year)
            expense["purchase_date"] = purchase_date
        collection['amount_spent'] = total
        remaining_amount = collection['limit'] - total
        if remaining_amount > 0:
            collection['amount_remaining'] = remaining_amount
        else:
            # here also fire an alert
            collection['exceeded_amount'] = 0 - remaining_amount
        percentage_spent = int((total / collection["limit"]) * 100)
        collection["percentage_spent"] = percentage_spent
        end_date = datetime.strptime(collection["end_date"], "%Y-%m-%d %H:%M:%S")
        end_date = "{} {:d}, {:d}".format(months[end_date.month - 1], end_date.day, end_date.year
                )
        collection["end_date"] = end_date
        detailed_collections.append(collection)
    print(detailed_collections)
    return render_template('dashboard.html', 
            expenses=expenses,
            collections=detailed_collections,
            cache_id=uuid.uuid4())

@collection.route('/show_all_purchases', strict_slashes=False)
@login_required
def show_all_purchases():
    return dashboard(purchases_list_conf='all')

@collection.route('/track_collection_page', strict_slashes=False)
@login_required
def track_collection_page():
    return render_template('track_collection.html', cache_id=uuid.uuid4())

@collection.route('/retrack_collection_page', methods=['POST'], strict_slashes=False)
@login_required
def retrack_collection_page():
    return 'retrack successful'

@collection.route('/untrack_collection_page', methods=['POST'], strict_slashes=False)
@login_required
def untrack_collection_page():
    return 'untrack collection'

@collection.route('/track_collection', methods=['POST'], strict_slashes=False)
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
        return redirect(url_for('collection.dashboard'))
    else:
        flash(f"{response.json().get('error')}", "error")

        return redirect(url_for('collection.track_collection_page'))
if __name__ == "__collection__":
    """ Main Function """
    collection.run(host='0.0.0.0', port=5000)

