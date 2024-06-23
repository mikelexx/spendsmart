
from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models.collection import Collection
from models import storage
import uuid
from datetime import datetime
collection = Blueprint('collection', __name__)
time = "%Y-%m-%dT%H:%M:%S.%f"
@collection.route('/dashboard/', strict_slashes=False)
@login_required
def dashboard(purchases_list_conf=None):
    """ shows the analytics for tracked collections """
    expenses_api_url = "http://127.0.0.1:5001/api/v1/{}/expenses".format(current_user.id)
    collections_api_url = "http://127.0.0.1:5001/api/v1/{}/collections".format(current_user.id)
    count = {'count': 5}
    if purchases_list_conf == 'all':
        count=None
    expenses_response = requests.get(expenses_api_url, params=count)
    collections_response = requests.get(collections_api_url)
    expenses = expenses_response.json()
    collections = collections_response.json()

      # Logging responses
#    print(f"Expenses API Response: {expenses_response.status_code} - {expenses}")
    # print(f"Collections API Response: {collections_response.status_code} - {collections}")

    if expenses_response.status_code != 200 or collections_response.status_code != 200:
        return "Error fetching data", 500
    detailed_collections = []
    month_names = ["jan", "feb", "match", "april", "may", "jun", "july", "aug", "sep", "oct", "nov", "dec"]
    for collection in collections:
        for expense in collection["expenses"]:
            purchase_date = datetime.strptime(expense["purchase_date"], time)
            purchase_date = "{} {:d}, {:d}".format(month_names[purchase_date.month - 1], purchase_date.day, purchase_date.year)
            expense["purchase_date"] = purchase_date
        collection['amount_spent'] = collection["total_spent"]
        remaining_amount = collection['remaining_amount']
        if remaining_amount > 0:
            collection['amount_remaining'] = remaining_amount
        else:
            # here also fire an alert
            collection['exceeded_amount'] = 0 - remaining_amount
        end_date = datetime.strptime(collection["end_date"], time)
        timedelta = end_date - datetime.now()
        years = timedelta.total_seconds() / (3600 * 24 * 7 * 4 * 12)
        months = timedelta.total_seconds() / (3600 * 24 * 7 * 4)
        weeks = timedelta.total_seconds() / (3600 * 24 * 7)
        days = timedelta.total_seconds() / (3600 * 24)
        hours = timedelta.total_seconds() / (3600)
        minutes = timedelta.total_seconds() / (60)
        if years > 2:
            collection["remaining_duration"] = "{} years".format(int(years))
        elif years > 1:
            collection["remaining_duration"] = "{} year".format(int(years))
        elif months > 2:
            collection["remaining_duration"] = "{} months".format(int(months))
        elif months > 1:
            collection["remaining_duration"] = "{} month".format(int(months))
        elif weeks > 2:
           collection["remaining_duration"]= "{} weeks".format(int(weeks))
        elif weeks > 1:
           collection["remaining_duration"]= "{} week".format(int(weeks))
        elif days > 2:
           collection["remaining_duration"]= "{} days".format(int(days))
        elif days > 1:
           collection["remaining_duration"]= "{} day".format(int(days))
        elif hours > 2:
            collection["remaining_duration"]= "{} hours".format(int(hours))
        elif hours > 1:
            collection["remaining_duration"]= "{} hour".format(int(hours))
        elif minutes > 2:
            collection["remaining_duration"]= "{} minutes".format(int(minutes))
        elif minutes > 1:
            collection["remaining_duration"]= "{} minutes".format(int(minutes))
            
        end_date = "{} {:d}, {:d}".format(month_names[end_date.month - 1], end_date.day, end_date.year
                )
        collection["end_date"] = end_date
        detailed_collections.append(collection)
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


@collection.route('/untrack_collection', methods=['POST'], strict_slashes=False)
@login_required
def untrack_collection():
    """ deletes the selected category and all its associated objects """
    collection_id = request.form.get("collection_id")
    collection_name = request.form.get("collection_name")
    api_url = "http://127.0.0.1:5001/api/v1/{}/collections/{}".format(current_user.id, collection_id)
    response = requests.delete(api_url)
    if response.status_code == 204:
        flash("""Successfully untracked {},
        purchases of this kind category will no longer be monitored""".format(collection_name))
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
    start_date = request.form.get("start_date")[:-1] +'001'
    end_date = request.form.get("end_date")[:-1]+ '001'
    collection_data = {
        "name": name,
        "description": description,
        "limit": float(limit),
        "start_date": start_date,
        "end_date": end_date,
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

