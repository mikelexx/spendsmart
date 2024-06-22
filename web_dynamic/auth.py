#!/usr/bin/python3
""" This module defines authentication API routes """
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, flash, url_for, Blueprint
from models.user import User
from models import storage
import uuid
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
auth = Blueprint('auth', __name__)
@auth.route('/signup')
def signup_page():
    """ Presents a signup form """
    return render_template('signup.html', cache_id=uuid.uuid4())

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
    users = storage.all(User)
    for user in users.values():
        if email_or_name == user.email or email_or_name == user.username:
            if check_password_hash(user.password, password):
                login_user(user, remember=remember)
                return redirect(url_for('collection.dashboard'))
            else:
                flash('Invalid password')
                return redirect(url_for('auth.login_page'))
    flash("User doesn't exist!")
    return redirect(url_for('auth.login_page'))

@auth.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ Creates a new account using email and password """
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    remember = True if request.form.get('remember') else False
    if not email:
        flash("Email required")
        return redirect(url_for('auth.signup_page'))
    if not password:
        flash("Password required")
        return redirect(url_for('auth.signup_page'))
    users = storage.all(User)
    if users:
        for user in users:
            if user.email == email:
                flash("User with that email already exists!")
                return redirect(url_for('auth.signup_page'))
    new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
    if username:
        new_user.username = username
    new_user.save()
    login_user(new_user, remember=remember)
    print(current_user)
    print("authenticated?", current_user.is_authenticated)
    return redirect(url_for('collection.dashboard'))

@auth.route('/logout')
def logout():
    """ Logs out a user """
    logout_user()
    return redirect(url_for('main.home'))

if __name__ == "__collection__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)

