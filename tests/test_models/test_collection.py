#!/usr/bin/python3
"""
Contains the TestCollectionDocs classes
"""

from datetime import datetime
import inspect
import models
from models import collection
from models.base_model import BaseModel
import pep8
import unittest

Collection = collection.Collection


class TestCollectionDocs(unittest.TestCase):
    """Tests to check the documentation and style of Collection class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.collection_f = inspect.getmembers(Collection, inspect.isfunction)

    def test_pep8_conformance_collection(self):
        """Test that models/collection.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/collection.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_collection(self):
        """Test that tests/test_models/test_collection.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_collection.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_collection_module_docstring(self):
        """Test for the collection.py module docstring"""
        self.assertIsNot(collection.__doc__, None,
                         "collection.py needs a docstring")
        self.assertTrue(
            len(collection.__doc__) >= 1, "collection.py needs a docstring")

    def test_collection_class_docstring(self):
        """Test for the Collection class docstring"""
        self.assertIsNot(Collection.__doc__, None,
                         "Collection class needs a docstring")
        self.assertTrue(
            len(Collection.__doc__) >= 1, "Collection class needs a docstring")

    def test_collection_func_docstrings(self):
        """Test for the presence of docstrings in Collection methods"""
        for func in self.collection_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]))


class TestCollection(unittest.TestCase):
    """Test the Collection class"""

    def test_is_subclass(self):
        """Test that Collection is a subclass of BaseModel"""
        collection = Collection()
        self.assertIsInstance(collection, BaseModel)
        self.assertTrue(hasattr(collection, "id"))
        self.assertTrue(hasattr(collection, "user_id"))
        self.assertTrue(hasattr(collection, "created_at"))
        self.assertTrue(hasattr(collection, "updated_at"))
        self.assertTrue(hasattr(collection, "limit"))
        self.assertTrue(hasattr(collection, "amount_spent"))
        self.assertTrue(hasattr(collection, "start_date"))
        self.assertTrue(hasattr(collection, "end_date"))

    def test_user_id_attr(self):
        """Test Collection has attr user_id, and it's an empty string"""

    def test_user_id_attr(self):
        """Test Collection has attr user_id, and it's an empty string"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "user_id"))
        if models.storage == 'db':
            self.assertEqual(collection.user_id, None)
        else:
            self.assertEqual(collection.user_id, "")

    def test_end_date_attr(self):
        """Test Collection has attr end_date, and it's a datetime"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "end_date"))
        if models.storage == 'db':
            self.assertEqual(collection.end_date, None)
        else:
            self.assertEqual(type(collection.end_date), str)
            self.assertEqual(collection.end_date, '')

    def test_start_date_attr(self):
        """Test Collection has attr end_date, and it's a datetime"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "start_date"))
        if models.storage == 'db':
            self.assertEqual(collection.start_date, None)
        else:
            self.assertEqual(type(collection.start_date), str)
            self.assertEqual(collection.start_date, '')

    def test_description_attr(self):
        """Test Collection has attr description, and it's an empty string"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "description"))
        if models.storage == 'db':
            self.assertEqual(collection.description, None)
        else:
            self.assertEqual(type(collection.description), str)
            self.assertEqual(collection.description, "")

    def test_name_attr(self):
        """Test Collection has attr name, and it's an empty string"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "name"))
        if models.storage == 'db':
            self.assertEqual(collection.name, None)
        else:
            self.assertEqual(type(collection.name), str)
            self.assertEqual(collection.name, "")

    def test_limit_attr(self):
        """Test Collection has attr limit, and it's a float == 0.0"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "limit"))
        if models.storage == 'db':
            self.assertEqual(collection.limit, None)
        else:
            self.assertEqual(type(collection.limit), float)
            self.assertEqual(collection.limit, 0.00)

    def test_amount_spent_attr(self):
        """Test Collection has attr amount_spent, and it's a float == 0.0"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "amount_spent"))
        if models.storage == 'db':
            self.assertEqual(collection.amount_spent, None)
        else:
            self.assertEqual(type(collection.amount_spent), float)
            self.assertEqual(collection.amount_spent, 0.00)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Collection()
        new_d = p.to_dict()
        print(p.start_date)
        print(p.description)
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Collection()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Collection")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        collection = Collection()
        string = "[Collection] ({}) {}".format(collection.id,
                                               collection.__dict__)
        self.assertEqual(string, str(collection))
