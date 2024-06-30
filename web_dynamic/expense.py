from flask import Flask, flash, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required
import requests
from models import storage

expense = Blueprint('expense', __name__)


@expense.route('/update_expenses', methods=['POST'], strict_slashes=False)
def update_expenses():
    expense_ids = request.form.getlist("expense_ids")
    return expense_ids


@expense.route('/delete_expenses', methods=['POST'], strict_slashes=False)
@login_required
def delete_expenses():
    """Deletes a list of expenses from the database using their IDs."""
    expense_ids = request.form.getlist("expense_ids")
    base_url = "http://127.0.0.1:5001/api/v1/{}/expenses".format(
        current_user.id)

    for expense_id in expense_ids:
        expense_url = "{}/{}".format(base_url, expense_id)
        response = requests.delete(expense_url)

        if response.status_code != 204:
            flash('Deletion failed. Please try again.')
            return redirect(url_for('collection.dashboard'))

    flash('Successfully deleted.')
    return redirect(url_for('collection.dashboard'))


@expense.route('/move_expenses', methods=['POST'], strict_slashes=False)
def move_expenses():
    """Moves a list of expenses to a different collection."""
    expense_ids = request.form.getlist("expense_ids")
    destination_collection_id = request.form.get("destination_id")

    for expense_id in expense_ids:
        update_expense_url = "http://127.0.0.1:5001/api/v1/{}/expenses/{}".format(
            current_user.id, expense_id)
        json_data = {"collection_id": destination_collection_id}
        response = requests.put(update_expense_url, json=json_data)
        if response.status_code != 200:
            flash('Move failed. Please try again.')
            return redirect(url_for('collection.dashboard'))

    return redirect(url_for('collection.dashboard'))


if __name__ == "__main__":
    """Main Function"""
    expense.run(host='0.0.0.0', port=5000)
