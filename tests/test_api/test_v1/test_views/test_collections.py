#!/usr/bin/python3
"""
this module contains tests for Collection resource
api 
"""
import pytest
from models.collection import Collection
from models.expense import Expense
from models import storage

def test_post_collection(test_client):
    """ tests the Post api for /collection """
    api_url = 'api/v1/collections'
    user = {
            'email': 'test_user@gmail.com',
            'password': 'vdgwegsevfs3',
            "id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
            }
    #register user to db for collections to be associated with user
    post_user_response = test_client.post('api/v1/users', json=user)
    if post_user_response.status_code == 201:
        #test with correct data
        collection = {
                "name": "Entertainment",
                "start_date": "2024-07-01T00:00:00.000000",
                "end_date": "2024-07-31T23:59:59.000000",
                "limit": 1000.00,
                "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
                }
        post_collection_response = test_client.post(api_url, json=collection)
        print(collection)
        posted_data = post_collection_response.get_json()
        print(posted_data)
        assert post_collection_response.status_code == 201
        saved_obj = storage.get(Collection, posted_data.get('id'))
        assert saved_obj is not None
        #check incorrect formats and missing fields in api payload
        required_fields = ["name", "start_date", "end_date", "limit", "user_id"]
        for val in required_fields:
            new_collection = collection
            new_collection[val] = None
            post_collection_response = test_client.post(api_url, json=new_collection)
            assert post_collection_response.status_code == 400
            if 'date' in val:
                new_collection[val] = '213:23'
                post_collection_response = test_client.post(api_url, json=new_collection)
                assert post_collection_response.status_code == 400
            if val == 'limit':
                new_collection[val] = 'notfloat'
                post_collection_response = test_client.post(api_url, json=new_collection)
                assert post_collection_response.status_code == 400
        #check for valid tracking duration

        reversed_dates_collection = {
                "name": "Entertainment",
                "start_date": "2024-07-31T23:59:59.000000",
                "end_date": "2024-07-01T00:00:00.000000",
                "limit": 1000.00,
                "user_id": "ee95989a-20a1-41d9-bb18-131c649b91cc"
                }
        post_collection_response = test_client.post(api_url, json=reversed_dates_collection)
        assert post_collection_response.status_code == 400
        #check duplicate names avoidance for collections
        post_collection_response = test_client.post(api_url, json=collection)
        assert post_collection_response.status_code == 400
