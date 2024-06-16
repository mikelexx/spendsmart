#!/usr/bin/python3
"""
entry point to the web app, it registers all blueprints
"""
from flask import Flask, Blueprint, render_template
from .auth import auth
from .main import main
from models import storage
from models.user import User
from flask_login import LoginManager
import uuid

app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(main)
app.secret_key = 'my_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """
    A user loader tells Flask-Login how to find a specific user from the ID that is stored in their session cookie.
    """
    user = storage.get(User, user_id)
    print(type(user))
    return user

@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, debug=True)
   
