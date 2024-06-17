#!/usr/bin/python3
""" Starts a Flash Web Application """

from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models.collection import Collection
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

@main.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    return render_template('dashboard.html', 
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
