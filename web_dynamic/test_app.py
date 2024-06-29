import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, current_app
import web_dynamic
import .
from models.user import User
from flask_login import LoginManager, UserMixin
from .app import app, load_user, get_notifications, inject_notifications, close_db
from models.notification import Notification
class TestFlaskApp(unittest.TestCase):
    
    def setUp(self):
        """ Set up the Flask app for testing """
        self.app = app.test_client()
        self.app.testing = True
    
    def tearDown(self):
        """ Clean up after each test """
        pass
    
    def test_blueprint_registration(self):
        """ Test blueprint blueprints are registered """
        self.assertIn('auth', app.blueprints)
        self.assertIn('main', app.blueprints)
        self.assertIn('collection', app.blueprints)
        self.assertIn('expense', app.blueprints)
    
    def test_login_manager_configuration(self):
        """ Test login manager configuration """
        self.assertIsInstance(app.login_manager, LoginManager)
        self.assertEqual(app.login_manager.login_view, 'auth.login')
    
    def test_load_user(self):
        """ Test user loader function """
        with patch('models.storage.get') as mock_get:
            # simulate storage.get(User, 'user_id')
            mock_user = MagicMock(spec=UserMixin)
            mock_get.return_value = mock_user
            
            # Call the user loader function
            user = load_user('user_id')
            
            # Assert that the correct user was loaded
            self.assertEqual(user, mock_user)
            mock_get.assert_called_once_with(User, 'user_id')
    
    @patch('app.requests.get')
    def test_get_notifications(self, mock_get):
        """ Test notification retrieval function """
        # Mock response for successful notifications retrieval
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'message': 'Test notification'}]
        mock_get.return_value = mock_response
        
        notifications = get_notifications('user_id', params={'read': False})
        
        # Assert that notifications were retrieved correctly
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['message'], 'Test notification')
        
        # Test error handling for requests exception
        mock_get.side_effect = requests.exceptions.RequestException('Mock error')
        notifications = get_notifications('user_id', params={'read': False})
        self.assertEqual(notifications, [])
    
    @patch('app.current_user')
    def test_inject_notifications_authenticated(self, mock_current_user):
        """ Test context processor for authenticated user """
        # Mock authenticated user
        mock_current_user.is_authenticated = True
        mock_current_user.id = 'user_id'
        
        # Mock get_notifications function
        with patch('app.get_notifications') as mock_get_notifications:
            mock_get_notifications.return_value = [{'message': 'Test notification'}]
            
            # Call the context processor function
            with app.app_context():
                notifications = inject_notifications()
            
            # Assert that notifications were injected
            self.assertEqual(len(notifications['notifications']), 1)
            self.assertEqual(notifications['notifications'][0]['message'], 'Test notification')
    
    @patch('app.storage.close')
    def test_teardown_appcontext(self, mock_close_db):
        """ Test teardown app context """
        # Call the teardown function directly
        close_db(None)
        
        # Assert that the close method was called
        mock_close_db.assert_called_once()

if __name__ == '__main__':
    unittest.main()
