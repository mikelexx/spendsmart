""" this module is reusable across mutliple testfiles"""
#!/usr/bin/python3
import pytest
from api.v1.app import app
from models import storage
from models.user import User
from models.expense import Expense
from models.notification import Notification
from models.collection import Collection

"""
fixtures functions will automatically
be called by pytest whenever they are used after
passing them as arguments
"""
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure each test starts with a clean table 
    and deletes the data it has added on exit."""
    # Setup: clean the table
    for expense in storage.all(Expense).values():
        storage.delete(expense)
    for notif in storage.all(Notification).values():
        storage.delete(notif)
    for col in storage.all(Collection).values():
        storage.delete(col)
    for user in storage.all(User).values():
        storage.delete(user)
    storage.save()
    yield
    # Teardown: clean the table
    for expense in storage.all(Expense).values():
        storage.delete(expense)
    for notif in storage.all(Notification).values():
        storage.delete(notif)
    for col in storage.all(Collection).values():
        storage.delete(col)
    for user in storage.all(User).values():
        storage.delete(user)
    storage.save()

@pytest.fixture(scope='module')
def user_data():
    """ returns a sample user data """
    data= {
            'email': 'user1@gmail.com',
            'password': 'strongpassword',
            'id': "ee95989a-20a1-41d9-bb18-131c649b91cc",
            }
    return data

@pytest.fixture(scope='module')
def collection_data():
    """returns  a sample collection data
    """
    data = {
            "name": "Entertainment",
            "start_date": "2024-07-01T00:00:00.000000",
            "end_date": "2024-07-31T23:59:59.000000",
            'id': 'defaultcollectionid234',
            "limit": 1000.00,
            'user_id': "ee95989a-20a1-41d9-bb18-131c649b91cc"
            }
    return data

@pytest.fixture(scope='module')
def expense_data():
    """ returns a sample expense data """
    data = { 
            "name": "Movie Night",
            "purchase_date": "2024-07-02T10:00:00.000000",
            "price": 100.00,
            'user_id': "ee95989a-20a1-41d9-bb18-131c649b91cc",
            'collection_id': 'defaultcollectionid234'
            }
    return data
@pytest.fixture(scope='module')
def notification_data():
    """returns a sample notification data """
    data = {
            'message': 'you have spent more than half of set limit',
            'notification_type': 'alert',
            'user_id': "ee95989a-20a1-41d9-bb18-131c649b91cc",
            'collection_id': 'defaultcollectionid234',
            }
    return data

@pytest.fixture
def post_user_response(test_client, user_data):
    """posts an user to database via users api"""
    return test_client.post('api/v1/users', json=user_data)

@pytest.fixture
def post_collection_response(test_client, collection_data):
    """posts a collection to database via /collections api"""
    return test_client.post('api/v1/collections', json=collection_data)

@pytest.fixture
def post_expense_response(test_client, expense_data):
    """posts an expense to database via /expenses api"""
    return test_client.post('api/v1/expenses', json=expense_data)

@pytest.fixture
def post_notification_response(test_client, notification_data):
    """ posta a notificaiont to database via /notifications api"""
    return test_client.post('api/v1/notifications', json=notification_data)

@pytest.fixture(scope='module')
def test_client():
    """ Setup for running tests and database cleanup """
    app.testing = True

    # Establish an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    yield app.test_client()  # this is where the testing happens!

    # Teardown: Close the session and drop all tables
    storage.close()
    ctx.pop()
