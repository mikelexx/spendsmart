#!/usr/bin/python3
"""
contains tests for Notification resource api
"""
from models.notification import Notification
from models.user import User
from models.collection import Collection
from models import storage
from datetime import datetime, timedelta
import pytest

def check_invalid_notification_values(notif_api_url, method, test_client, notification_data, post_user_response, post_collection_response):
    """send notification dictionary to api 
    with invalid values for Notification fields 
    """
    iterable = notification_data.copy().items()

    assert getattr(test_client, method)(notif_api_url, json={key: 123 if key == 'message' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(notif_api_url, json={key: '' if key == 'message' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(notif_api_url, json={key: 'fakeuserid' if key == 'user_id' else val for key, val in iterable}).status_code == 400
    assert getattr(test_client, method)(notif_api_url, json={key: 'fakecollectionid' if key == 'collection_id' else val for key, val in iterable}).status_code == 400

    if method == 'post':
        for key, val in iterable:
            #test with one field being none at a time
            json = {new_key: None if new_key == key else val for new_key, val in  iterable}
            assert test_client.post(notif_api_url, json=json).status_code == 400

def test_post_notification(test_client, user_data, post_user_response, post_collection_response, notification_data):
    """ tests POST /users/<user_id>/notifications api """
    notif_api_url = 'api/v1/notifications'
    iterable = notification_data.copy().items()

    # test api with notification data
    assert len(storage.all(Notification).values()) == 0
    assert len(storage.all(User)) == 1
    assert test_client.post(notif_api_url, json=notification_data).status_code == 201
    assert len(storage.all(Notification).values()) == 1
    #  test api with invalid field data 
    check_invalid_notification_values(notif_api_url, 'post', test_client, notification_data, post_user_response, post_collection_response)

#    dup_notification = notification_data.copy()
 #   dup_notification['id'] = 'testduplicateid123'
  #  assert test_client.post(notif_api_url, json=dup_notification).status_code == 201
   # assert test_client.post(notif_api_url, json=dup_notification).status_code == 201

def test_update_notification(test_client, user_data, post_user_response, post_collection_response,  notification_data):
    """ tests PUT /users/<user_id>/notifications/<notification_id> api """
    notif_api_url = 'api/v1/users/{}/notifications/{}'
    notification_data = notification_data.copy()
    notification_data['id'] = 'notificationid1243'
    #test invalid routes
    assert test_client.put(notif_api_url.format('fakeuserid', notification_data.get('id')), json=notification_data).status_code == 404
    assert test_client.put(notif_api_url.format(user_data.get('id'), 'fakenotificationid3'), json=notification_data).status_code == 404
    #test updating nonexisting notification
    assert test_client.put(notif_api_url.format(user_data.get('id'), notification_data.get('id')), json=notification_data).status_code == 404

    post_notif_response = test_client.post('api/v1/notifications', json=notification_data)
    assert post_notif_response.status_code == 201
    #  test api with invalid field data 
    notif_api_url = notif_api_url.format(user_data.get('id'), notification_data.get('id'))
    check_invalid_notification_values(notif_api_url, 'put', test_client, notification_data, post_user_response, post_collection_response)

def test_get_user_notifications(test_client, user_data, post_user_response, post_collection_response, post_notification_response,  notification_data):
    """
    tests /users/<user_id>/notifications API
    """
    assert test_client.get('api/v1/users/fakeuserid/notifications').status_code == 404
    api_url = 'api/v1/users/{}/notifications'.format(user_data.get('id'))
    assert test_client.get(api_url).status_code == 200
    notif_response = test_client.get(api_url)
    notif_response_data = notif_response.get_json()
    assert isinstance(notif_response_data, list)
    for notif in notif_response_data:
        assert isinstance(notif, dict)
        for field in ['message', 'user_id', 'collection_id', 'notification_type', 'is_read']:
            assert field in notif 
            if field != 'is_read':
                assert type(notif.get(field)) is str
            assert type(notif.get('is_read')) is bool
def test_get_notification(test_client, user_data, notification_data, post_user_response, post_collection_response, post_notification_response):
    """
    tests getting a notification via /users/<user_id>/notifications/<notification_id> api
    """
    notification_data['id'] = post_notification_response.get_json().get('id')
    assert test_client.get('api/v1/users/fakeuser13/notifications/{}'.format(notification_data['id'])).status_code == 400
    assert test_client.get('api/v1/users/{}/notifications/{}'.format(user_data.get('id'), 'rondomfakeid12344')).status_code == 404
    notif_res = test_client.get('api/v1/users/{}/notifications/{}'.format(user_data.get('id'), notification_data['id']))
    assert notif_res.status_code == 200
    notif = notif_res.get_json()
    assert isinstance(notif, dict)
    for field in ['is_read', 'message', 'user_id', 'collection_id', 'notification_type']:
        assert field in notif 
        if field != 'is_read':
            assert type(notif.get(field)) is str
        assert type(notif.get('is_read')) is bool

def test_delete_notification(test_client, user_data, post_user_response, post_collection_response, notification_data):
    """
    tests deleting a notification via /users/<user_id>/notifications/<notification_id> api
    """
    notification_data['id'] = 'newnotificationid1233'
    assert test_client.post('api/v1/notifications', json=notification_data).status_code == 201
    notif_url = 'api/v1/users/{}/notifications/{}'.format(user_data.get('id'), notification_data['id'])
    assert test_client.get(notif_url).status_code == 200
    assert test_client.delete(notif_url).status_code == 204
    assert test_client.get(notif_url).status_code == 404
