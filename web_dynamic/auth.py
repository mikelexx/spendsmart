#!/usr/bin/python3
""" This module defines authentication API routes """
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, flash, url_for, Blueprint
from models.user import User
from models import storage
import requests
import uuid
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
auth = Blueprint('auth', __name__)
@auth.route('/signup')
def signup_page():
    """ Presents a signup form """
    return render_template('signup.html', cache_id=uuid.uuid4())

@auth.route('/delete_account', methods=['POST'], strict_slashes=False)
def delete_account():
    """ deletes a user from storage """
    user_api_url = "http://127.0.0.1:5001/api/v1/users/{}".format(current_user.id)
    response = requests.delete(user_api_url)
    if response.status_code != 201:
        flash("Server error!, please try again")
        return redirect(url_for('auth.delete_account_page'))
    logout_user()
    return redirect(url_for('main.home'))
    

@auth.route('/account_page')
@login_required
def account_page():
    """ returns account page where user can see and update his details
    """
    user = current_user
    return render_template('account.html', user=user)
@auth.route('/login')
def login_page():
    """ Returns a login form page """
    return render_template('login.html', cache_id=uuid.uuid4())

@auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ Authenticates a user """
    email_or_name = request.form.get('email_or_name')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user_api_url = "http://127.0.0.1:5001/api/v1/users"
    response = requests.get(user_api_url)
    if response.status_code == 200:
        users = response.json()
        for user_data in users:
            user = storage.get(User, user_data["id"])
            if email_or_name == user.email or email_or_name == user.username:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember)
                    return redirect(url_for('collection.dashboard'))
                else:
                    flash('Invalid password')
                    return redirect(url_for('auth.login_page'))
    flash("User doesn't exist! Try again")
    return redirect(url_for('auth.login_page'))

@auth.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ Creates a new account using email and password """
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username') 
    remember = True if request.form.get('remember') else False
    data = {"email":email, "password": password, "username": username}
    user_api_url = "http://127.0.0.1:5001/api/v1/users"
    response = requests.post(user_api_url, json=data)

    if response.status_code in [400, 409]:
            flash("{}".format(response.json().get('error')))
            return redirect(url_for('auth.signup_page'))
    elif response.status_code != 201:
            flash("Error on our side, please try again")
            return redirect(url_for('auth.signup_page'))
    storage.reload()
    new_user = storage.get(User, response.json().get("id"))
    login_user(new_user, remember=remember)
    print("user authenticated before redirection?=", current_user.is_authenticated)
    return redirect(url_for('collection.dashboard'))

@auth.route('/logout')
def logout():
    """ Logs out a user """
    print("called logout")
    logout_user()
    print(current_user)
    print("exiting logout")
    return redirect(url_for('main.home'))

if __name__ == "__collection__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)

