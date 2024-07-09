#!/usr/bin/python3
""" contains tests for all api endpoints for User resource """
import pytest
from models.user import User
from models import storage

def test_post_user(test_client):
    """ Test POST /users api """
    json = {
        "email": "user@example.com",
        "password": "strongpassword",
        "username": "newuser",
        "id": "wewfsav2344"
    }

    # Test user with correct parameters get created
    response = test_client.post('api/v1/users', json=json)
    assert response.status_code == 201
    data = response.get_json()
    assert data.get('email') == "user@example.com"
    assert data.get('id', None) is not None
    assert data.get('updated_at', None) is not None
    # Assert data was saved
    assert storage.get(User, data['id']).id == json.get('id')
    assert len(storage.all(User)) == 1
    # Assert creation with incorrect parameters does not happen
    inv_email_response = test_client.post('api/v1/users', json={'email': 'invalid', 'password': 'strongpass'})
    assert inv_email_response.status_code == 400
    missing_email_response = test_client.post('api/v1/users', json={'password': 'strongpass'})
    assert missing_email_response.status_code == 400
    # Test creating duplicate user
    sec_user_response = test_client.post('/api/v1/users', json=json)
    assert sec_user_response.status_code == 409

def test_get_users(test_client):
    """ Tests GET /users api """
    api_url = 'api/v1/users'
    json = {
            "email": "user2@example.com",
            "password": "strongpassword",
            "username": "user1"
            }
    
    users_response = test_client.get(api_url)
    users_data = users_response.get_json()
    assert users_response.status_code == 200
    assert len(users_data) == 0

    test_client.post(api_url, json=json)
    users_response = test_client.get(api_url)
    users_data = users_response.get_json()
    assert len(users_data) == len(storage.all(User))
    
def test_delete_user(test_client):
    """ asserts successful deletion of user resource 
    from delete /user/user_id api
    """
    json = {
            "email": "user2@example.com",
            "password": "strongpassword",
            "username": "user1"
            }
    #test deleting non existing user
    delete_response = test_client.delete('api/v1/users/111')
    assert delete_response.status_code == 404
    #delete existing user resource

    new_user_res = test_client.post('api/v1/users', json=json)
    new_user_data = new_user_res.get_json()
    delete_response = test_client.delete('api/v1/users/{}'.format(new_user_data.get('id')))
    assert delete_response.status_code == 204
    data = delete_response.get_json()
    assert len(test_client.get('api/v1/users').get_json()) == 0
