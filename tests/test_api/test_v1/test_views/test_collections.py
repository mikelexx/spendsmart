#!/usr/bin/python3
"""
this module is for testing Collection resource API
"""
import pytest
from models.collection import Collection
from models.expense import Expense
from models import storage

coll_data_types =  {
            "__class__": str,
            "amount_spent": float,
            "created_at": str,
            "description": str,
            "end_date": str,
            "expenses": list,
            "id": str,
            "limit": float,
            "name": str,
            "percentage_spent": int,
            "remaining_amount": float,
            "start_date": str,
            "total_spent": float,
            "updated_at": str,
            "user_id": str
            }

default_user_json = {
        'email': 'user1@gmail.com',
        'password': 'strongpassword',
        'id': "ee95989a-20a1-41d9-bb18-131c649b91cc",
        }
default_collection_json = {
                "name": "Entertainment",
                "start_date": "2024-07-01T00:00:00.000000",
                "end_date": "2024-07-31T23:59:59.000000",
                "limit": 1000.00,
                "user_id": default_user_json.get('id')
                }
default_expense_json = { 
        "name": "Movie Night",
        "purchase_date": "2024-07-02T10:00:00.000000",
        "price": 100.00,
        "user_id": default_user_json.get('id'),
        "collection_id": default_collection_json.get('id')
        }
def post_user(test_client, user_json=default_user_json):
    """ adds the user to database """
    return test_client.post('api/v1/users', json=user_json)

def post_collection(test_client, collection_json=default_collection_json):
    """ adds collection to the database """
    return test_client.post('api/v1/collections', json=collection_json)
def post_expense(test_client, expense_json=default_expense_json):
    """ adds an expense to database """
    return test_client.post('api/v1/expenses', json=expense_json)

def test_post_collection(test_client):
    """ tests the Post api for /collection """
    api_url = 'api/v1/collections'
    user = {
            'email': 'test_user@gmail.com',
            'password': 'vdgwegsevfs3',
            "id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
            }
    #register user to db for collections to be associated with user
    post_user_response = post_user(test_client, user_json=user) 

    if post_user_response.status_code == 201:
        #test with correct data
        collection = {
                "name": "Entertainment",
                "start_date": "2024-07-01T00:00:00.000000",
                "end_date": "2024-07-31T23:59:59.000000",
                "limit": 1000.00,
                "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
                }
        post_collection_response = post_collection(test_client, collection_json=collection) 
        posted_data = post_collection_response.get_json()
        assert post_collection_response.status_code == 201
        saved_obj = storage.get(Collection, posted_data.get('id'))
        assert saved_obj is not None
        #check incorrect formats and missing fields in api payload
        required_fields = ["name", "start_date", "end_date", "limit", "user_id"]
        for val in required_fields:
            new_collection = collection
            new_collection[val] = None
            post_collection_response = post_collection(test_client, collection_json=new_collection) 
            assert post_collection_response.status_code == 400
            if 'date' in val:
                new_collection[val] = '213:23'
                post_collection_response = post_collection(test_client, collection_json=new_collection) 
                assert post_collection_response.status_code == 400
            if val == 'limit':
                new_collection[val] = 'notfloat'
                post_collection_response = post_collection(test_client, collection_json=new_collection) 
                assert post_collection_response.status_code == 400
                assert post_collection_response.status_code == 400
        #check for valid tracking duration

        reversed_dates_collection = {
                "name": "Entertainment",
                "start_date": "2024-07-31T23:59:59.000000",
                "end_date": "2024-07-01T00:00:00.000000",
                "limit": 1000.00,
                "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
                }
        post_collection_response = post_collection(test_client, collection_json=reversed_dates_collection) 
        assert post_collection_response.status_code == 400
        #check duplicate names avoidance for collections
        post_collection_response = post_collection(test_client, collection_json=collection) 
        assert post_collection_response.status_code == 400
def test_get_user_collections(test_client):
    """Tests the GET /user_id/collections API"""
    assert test_client.get('api/v1/fakeid123/collections').status_code == 404
    user2 = {
            'email': 'user1@gmail.com',
            'password': 'strongpassword',
            'id': "user2id",
            }

    user1_res = post_user(test_client) 
    user2_res = post_user(test_client, user_json=user2) 

    if user1_res.status_code == 201 and user2_res.status_code == 201:
        user1_res_data = user1_res.get_json()
        assert test_client.get('api/v1/{}/collections'.format(user1_res_data.get('id'))).status_code == 200

        collection2 = {
                "name": "Entertainment",
                "start_date": "2024-07-01T00:00:00.000000",
                "end_date": "2024-07-31T23:59:59.000000",
                "limit": 1000.00,
                "user_id": user2.get('id')
                }
        collection1_res = post_collection(test_client) 
        collection2_res = post_collection(test_client, collection2) 
        if collection1_res.status_code == 201 and \
                collection2_res.status_code == 201 \
                and exp1_res.status_code == 201:
            user1_coll_res = test_client.get('api/v1/{}/collections'.format(user1_res_data.get('id')))
            assert user1_coll_res.status_code == 200
            user1_coll_res_data = user1_coll_res.get_json()
            assert type(user1_coll_res_data) is list

            for collection in user1_coll_res_data:
                assert collection.get('id') != collection2.get('id')
                assert collection.get('user_id') != user2.get('id')
                for key, val in collection.items():
                    assert key in coll_data_types and type(val) is coll_data_types[key]
                    if key == 'expenses':
                        assert len(collection[key]) == 1
                        for item in collection[key]:
                            assert type(item) is dict

def test_get_user_collection_expenses(test_client):
    """ Tests  
    Get /<user_id>/collections/<collection_id>/expenses/ Api endpoint 
    """
    assert test_client.get('api/v1/users/fakeuserid/collections/fakecollectionid/expenses/')\
    .status_code == 404
    collection_res = post_collection(test_client)
    collection_id = collection_res.get_json().get('id')
    user_id = collection_res.get_json().get('user_id')
    exp_res = post_expense(test_client)
    coll_expenses_res = test_client.get('api/v1/users/{}/collections/{}/expenses'.format(user_id, collection_id))
    assert coll_expenses_res.status_code == 200
    coll_expenses_data =  coll_expenses_res.get_json()
    assert type(coll_expenses_data) is list
    assert type(coll_expenses_data[0]) is dict

