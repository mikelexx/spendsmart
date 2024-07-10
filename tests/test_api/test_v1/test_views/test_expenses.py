#!/usr/bin/python3
"""
contains tests for Expense resource api
"""
from models.expense import Expense
from models import storage
from datetime import datetime, timedelta

date_format = '%Y-%m-%dT%H:%M:%S.%f'
def test_post_expense(test_client, user_data, collection_data, expense_data):
    """ tests POST /expenses api """
    #setup
    exp_api_url = 'api/v1/expenses'
    post_user_response = test_client.post('api/v1/users', json=user_data)
    post_collection_response = test_client.post('api/v1/collections', json=collection_data)

    start_date = datetime.strptime(post_collection_response.get_json().get('start_date'), date_format)
    end_date = datetime.strptime(post_collection_response.get_json().get('end_date'), date_format)

    before_start_date = (start_date - timedelta(days=1)).strftime(date_format)
    after_end_date = (end_date + timedelta(days=1)).strftime(date_format)

    iterable = expense_data.copy().items()
    assert post_user_response.status_code == 201
    assert post_collection_response.status_code == 201

    # test api with collect data
    assert len(storage.all(Expense).values()) == 0
    assert test_client.post(exp_api_url, json=expense_data).status_code == 201
    assert test_client.post(exp_api_url, json={key: 234.03 if key == 'price' else val for key, val in iterable}).status_code == 201
    assert len(storage.all(Expense).values()) == 2
    #  test api with missing required values
    for key, val in iterable:
        #  test api with missing required values
        assert test_client.post(exp_api_url, json={new_key: None if new_key == key else val for new_key, val in  iterable}).status_code == 400
        #  test api with invalid field data 
        assert test_client.post(exp_api_url, json={key: '2020-4-23' if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: before_start_date if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: after_end_date if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: '234' if key == 'price' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: 9999999999999 if key == 'price' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: 'fakeuserid' if key == 'user_id' else val for key, val in iterable}).status_code == 400
        assert test_client.post(exp_api_url, json={key: 'fakecollectionid' if key == 'collection_id' else val for key, val in iterable}).status_code == 400
