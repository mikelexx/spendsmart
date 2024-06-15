#!/usr/bin/python3
""" Starts a Flash Web Application """

from flask import Flask, render_template, Blueprint
from flask_login import login_required, current_user
import uuid
main = Blueprint('main', __name__)

@main.route('/', strict_slashes=False)
def home():
    """ HBNB is alive! """
    return render_template('home.html',
                           cache_id=uuid.uuid4())

@main.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    print(current_user)
    return render_template('dashboard.html', 
            cache_id=uuid.uuid4())

if __name__ == "__main__":
    """ Main Function """
    main.run(host='0.0.0.0', port=5000)
