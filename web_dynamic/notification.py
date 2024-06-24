#!/usr/bin/python3
""" This module defines authentication API routes """
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, render_template, redirect, flash, url_for, Blueprint
from models.user import User
from models import storage
import uuid
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
notification = Blueprint('notification', __name__)

@notification.route('/mark_read', methods=['POST'], strict_slashes=False)
def mark_read():
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
