#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime, timedelta
import inspect
import models
from models import user
from models.base_model import BaseModel
import pep8
import unittest

User = user.User
valid_test_password = 'PassWord123!'
valid_test_passwords = ['Password1!', 'PassWord123!']
invalid_test_passwords = [
    'password1!',  # Invalid (no uppercase)
    'PASSWORD1!',  # Invalid (no lowercase)
    'Pass1!',  # Invalid (length < 8)
]
valid_test_emails = [
    'murhti@gmail.com',
    'test.email+alex@leetcode.com',
    'user@domain.co',
]
invalid_test_emails = [
    'user@domain',  # Invalid
    'user@domain.c',  # Invalid
    'user@domain.c@com',  # Invalid
]


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(user.__doc__, None, "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1, "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None, "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1, "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))
        self.assertTrue(hasattr(user, "username"))
        self.assertTrue(hasattr(user, "email"))
        self.assertTrue(hasattr(user, "password"))

    def test_id_attr(self):
        """Test User has attr id, and it's an empty string"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertTrue(hasattr(user, "id"))
        self.assertNotEqual(user.id, None)
        user = User(id='ssv4<F3>42rf3eqfv',
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertEqual(user.id, 'ssv4<F3>42rf3eqfv')
        with self.assertRaises(TypeError):
            user = User(id=1234)

    def test_created_at_attr(self):
        """Test User has attr created_at, and it's a datetime"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertTrue(hasattr(user, "created_at"))
        self.assertEqual(type(user.created_at), datetime)
        self.assertEqual(user.created_at, user.updated_at)
        user = User(email='murithimichael@gmail.com',
                    password=valid_test_password,
                    created_at=datetime.utcnow() + timedelta(days=5))
        self.assertEqual(type(user.created_at), datetime)
        self.assertRaises(TypeError,
                          User,
                          created_at=1234,
                          email='murhti@gmail.com',
                          password=valid_test_password)

    def test_updated_at_attr(self):
        """Test User has attr created_at, and it's a datetime"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertTrue(hasattr(user, "updated_at"))
        self.assertEqual(type(user.updated_at), datetime)
        user = User(username='michael',
                    updated_at=datetime.now() + timedelta(days=5),
                    password=valid_test_password)
        self.assertNotEqual(user.updated_at, user.created_at)
        with self.assertRaises(TypeError):
            user = User(updated_at=1234)

    def test_email_attr(self):
        """Test User has attr email, and it's an empty string"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertTrue(hasattr(user, "email"))
        self.assertNotEqual(user.email, None)
        self.assertEqual(user.email, 'murhti@gmail.com')
        user = User(username='michael', password=valid_test_password)
        self.assertTrue(hasattr(user, "email"))
        self.assertIs(user.email, None)
        self.assertRaises(TypeError,
                          User,
                          email=1244,
                          password=valid_test_password)
        self.assertRaises(TypeError, User, password=valid_test_password)
        for email in invalid_test_emails:
            self.assertRaises(ValueError,
                              User,
                              email=email,
                              password=valid_test_password)
        for email in valid_test_emails:
            user = User(ValueError,
                        User,
                        email=email,
                        password=valid_test_password)

    def test_large_values_attr(self):
        """test User creation with overbound length values does not happen"""
        with self.assertRaises(ValueError):
            user = User(username='x' * 130,
                        email='murhti@gmail.com',
                        password=valid_test_password)
            user = User(username='michael',
                        email='m' * 130 + '@.com',
                        password=valid_test_password)
            user = User(username='michael',
                        email='murhti@gmail.com',
                        password='UUuu!@m1w2' * 15)

    def test_username_attr(self):
        """Test User has attr username, and it's an empty string"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        self.assertTrue(hasattr(user, "username"))
        self.assertEqual(user.username, None)
        user = User(username='michael',
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertNotEqual(user.username, None)
        self.assertEqual(user.username, 'michael')
        user = User(username=1234,
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertIs(type(user.username), int)
        user = User(username=1234, password=valid_test_password)
        user = User(username='',
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertEqual(user.username, '')

    def test_password_attr(self):
        """Test User has attr password, and it's a float == 0.0"""
        user = User(username='michael',
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, valid_test_password)
        self.assertIs(type(user.password), str)
        for password in valid_test_passwords:
            user = User(username='michael',
                        email='murhti@gmail.com',
                        password=password)
        invalid_test_passwords = [
            'uuu!1x', 'UUU!1X', 'UUuu1x', 'UuU!!x', 'Uu!11'
        ]
        for invalid_test_password in invalid_test_passwords:
            self.assertRaises(ValueError,
                              User,
                              username='michael',
                              email='murhti@gmail.com',
                              password=invalid_test_password)

    def test_notifications_expenses_collections_attrs(self):
        """
        tests User has notifications, expenses and
        notifications attributes"""
        user = User(username='michael',
                    email='murhti@gmail.com',
                    password=valid_test_password)
        self.assertTrue(hasattr(user, "notifications"))
        self.assertTrue(hasattr(user, "expenses"))
        self.assertTrue(hasattr(user, "collections"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = User(email='murhti@gmail.com', password=valid_test_password)
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = User(email='murhti@gmail.com', password=valid_test_password)
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))
        for attr in ['collections', 'expenses', 'notifications']:
            self.assertEqual(type(new_d[attr]), list)
        for attr in ['id', 'created_at', 'updated_at']:
            self.assertEqual(type(new_d[attr]), str)

    def test_str(self):
        """test that the str method has the correct output"""
        user = User(email='murhti@gmail.com', password=valid_test_password)
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))
