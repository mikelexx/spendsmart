""" this module is reusable across mutliple testfiles"""
#!/usr/bin/python3
import pytest
from api.v1.app import app
from models import storage
from models.user import User

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

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Ensure each test starts with a clean table 
    and deletes the data it has added on exit."""
    # Setup: clean the table
    for user in storage.all(User).values():
        storage.delete(user)
    storage.save()
    yield
    # Teardown: clean the table
    for user in storage.all(User).values():
        storage.delete(user)
    storage.save()
