#!/usr/bin/python3
import pytest
from models.user import User
from datetime import datetime, timedelta
from api.v1.app import app
from models import storage
import os

@pytest.fixture(scope='module')
def test_client():
    """ setup for running tests """
    app.testing = True

    # Establish an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    yield app.test_client()  # this is where the testing happens!

    # Teardown: Close the session and drop all tables
    storage.close()
    ctx.pop()

def test_post_user(test_client):
    """ Test POST /users api """
    json = {
            "email": "user@example.com",
            "password": "strongpassword",
            "username": "newuser"
            }

    #test user with correct parameters get created
    response = test_client.post('api/v1/users', json=json)
    assert response.status_code == 201
    data = response.get_json()
    first_user_email = data.get('email')
    assert data.get('email') == "user@example.com"
    assert data.get('id', None) is not None
    assert data.get('updated_at', None) is not None
    #assert data was saved
    assert storage.get(User, data['id']) is not None
    #assert creation with incorrect parameters does not happen
    inv_email_response = test_client.post('api/v1/users', json={'email': 'invalid', 'password': 'strongpass'})
    assert inv_email_response.status_code == 400
    missing_email_response = test_client.post('api/v1/users', json={'password': 'strongpass'})
    assert missing_email_response.status_code == 400
    #test creating duplicate user
    sec_user_response = test_client.post('/api/v1/users', json=json)
    assert sec_user_response.status_code == 409
