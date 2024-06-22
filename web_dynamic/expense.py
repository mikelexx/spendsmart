
from flask import Flask, flash, request, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import requests
from models import storage
import uuid
from datetime import datetime
expense = Blueprint('expense', __name__)

@expense.route('/update_expenses', methods=['POST'], strict_slashes=False)
def update_expenses():
    expense_ids = request.form.getlist("expense_ids")
    return expense_ids
@expense.route('/delete_expenses', methods=['POST'], strict_slashes=False)
def delete_expenses():
    expense_ids = request.form.getlist("expense_ids")
    return expense_ids

@expense.route('/move_expenses', methods=['POST'], strict_slashes=False)
def move_expenses():
    expense_ids = request.form.getlist("expense_ids")
    return expense_ids

#    return redirect(url_for('collection.dashboard'))
if __name__ == "__collection__":
    """ Main Function """
    collection.run(host='0.0.0.0', port=5000)

