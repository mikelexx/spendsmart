#!/usr/bin/python3
"""
contains tests for Expense resource api
"""
from models.expense import Expense
from decimal import Decimal
from models.collection import Collection
from models.user import User
from models import storage
from datetime import datetime, timedelta
date_format = '%Y-%m-%dT%H:%M:%S.%f'
import pytest

def check_invalid_values(exp_api_url, method, test_client, expense_data, post_user_response, post_collection_response):  
    """send expense dictionary to api 
    with invalid values for Expense fields 
    """
    iterable = expense_data.copy().items()
    post_collection_response_json = post_collection_response.get_json()

    start_date = datetime.strptime(post_collection_response_json.get('start_date'), date_format)
    end_date = datetime.strptime(post_collection_response_json.get('end_date'), date_format)


    before_start_date = (start_date - timedelta(days=1)).strftime(date_format)
    after_end_date = (end_date + timedelta(days=1)).strftime(date_format)
    assert getattr(test_client, method)(exp_api_url, json={key: '2020-4-23' if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(exp_api_url, json={key: before_start_date if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(exp_api_url, json={key: after_end_date if key == 'purchase_date' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(exp_api_url, json={key: '234' if key == 'price' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(exp_api_url, json={key: 9999999999999 if key == 'price' else val for key, val in iterable}).status_code == 400
    json={key: 'fakeuserid' if key == 'user_id' else val for key, val in iterable}
    user_response = getattr(test_client, method)(exp_api_url, json=json)
    collection_response = getattr(test_client, method)(exp_api_url, json={key: 'fakecollecitionid' if key == 'collection_id' else val for key, val in iterable})
    assert user_response.status_code == 400
    if method == 'post':
        assert collection_response.status_code == 400
        for key, val in iterable:
            #test with one field being none at a time
            json = {new_key: None if new_key == key else val for new_key, val in  iterable}
            assert test_client.post(exp_api_url, json=json).status_code == 400
    else:
        print(collection_response.get_json())
        assert collection_response.status_code == 404

def test_post_expense(test_client, user_data,post_user_response, post_collection_response,  collection_data, expense_data):
    """ tests POST /expenses api """
    """
    mentioning a function fixture in params automatically calls it,
    so user and collections were arleady created before code below
    """
    exp_api_url = 'api/v1/expenses'
    iterable = expense_data.copy().items()

    # test api with collect data
    assert len(storage.all(Expense).values()) == 0
    assert test_client.post(exp_api_url, json=expense_data).status_code == 201
    assert test_client.post(exp_api_url, json={key: 234.03 if key == 'price' else val for key, val in iterable}).status_code == 201
    assert len(storage.all(Expense).values()) == 2
    #  test api with invalid field data 
    check_invalid_values(exp_api_url, 'post', test_client, expense_data, post_user_response, post_collection_response)
    dup_expense = expense_data.copy()
    dup_expense['id'] = 'testduplicateid123'
    assert test_client.post(exp_api_url, json=dup_expense).status_code == 201
    assert test_client.post(exp_api_url, json=dup_expense).status_code == 409

def test_update_expense(test_client, user_data, collection_data, expense_data, post_user_response, post_collection_response):
    """ tests PUT /users/<user_id>/expenses/<expense_id> api """
    exp_api_url = 'api/v1/users/{}/expenses/{}'
    expense_data = expense_data.copy()
    expense_data['id'] = 'expenseid1243'
    #test invalid routes
    assert test_client.put(exp_api_url.format('fakeuserid', expense_data.get('id')), json=expense_data).status_code == 400
    assert test_client.put(exp_api_url.format(user_data.get('id'), 'fakeexpenseid3'), json=expense_data).status_code == 404
    #test updating nonexisting expense
    assert test_client.put(exp_api_url.format(user_data.get('id'), expense_data.get('id')), json=expense_data).status_code == 404

    post_exp_response = test_client.post('api/v1/expenses', json=expense_data)
    assert post_exp_response.status_code == 201
    #  test api with invalid field data 
    exp_api_url = exp_api_url.format(user_data.get('id'), expense_data.get('id'))
    check_invalid_values(exp_api_url, 'put', test_client, expense_data, post_user_response, post_collection_response)
def test_post_update_expense(test_client, user_data, collection_data, expense_data, post_user_response, post_collection_response):
    '''
    tests that amount spent for collection is correctly modified when 
    an expense is posted via /expenses or modified 
    vi /users/<user_id>/expenses/<expense_id> api
    '''
    exp_api_url = 'api/v1/users/{}/expenses/{}'
    coll2 = collection_data.copy()
    coll2['name'] = 'coll2name'
    coll2['id'] = 'coll212344'
    new_expense = expense_data.copy()
    new_expense['id'] = 'newexpenseid2134324252'

    coll2_res = test_client.post('api/v1/collections', json=coll2)
    assert coll2_res.status_code == 201
    
    new_expense_res = test_client.post('api/v1/expenses', json=new_expense)
    assert new_expense_res.status_code == 201
    updated_coll1 = storage.get(Collection, collection_data.get('id'))
    assert updated_coll1.amount_spent == new_expense_res.get_json().get('price')

    updated_exp_data = new_expense
    updated_exp_data['collection_id'] = coll2['id']
    updated_new_exp_res = test_client.put(exp_api_url.format(user_data.get('id'), updated_exp_data['id']), json=updated_exp_data)
    assert updated_new_exp_res.status_code == 200
    updated_coll1 = storage.get(Collection, collection_data.get('id'))
    updated_coll2 = storage.get(Collection, coll2.get('id'))
    assert updated_coll1.amount_spent == Decimal(0.0)
    assert updated_coll2.amount_spent == updated_new_exp_res.get_json().get('price')

    updated_exp_data['price'] = 400.0
    updated_new_exp_res = test_client.put(exp_api_url.format(user_data.get('id'), updated_exp_data['id']), json=updated_exp_data)
    assert updated_new_exp_res.status_code == 200
    updated_coll1 = storage.get(Collection, collection_data.get('id'))
    latest_updated_coll2 = storage.get(Collection, coll2.get('id'))
    assert updated_coll1.amount_spent == Decimal(0.0)
    assert latest_updated_coll2.amount_spent == Decimal(updated_exp_data['price'])
