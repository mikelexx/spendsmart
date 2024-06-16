#!/usr/bin/python3
""" Starts a Flash Web Application """

from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
import uuid
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
    return 'tracked'
if __name__ == "__main__":
    """ Main Function """
    main.run(host='0.0.0.0', port=5000)
