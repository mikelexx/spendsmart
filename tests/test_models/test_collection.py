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
        self.assertEqual(collection.user_id, None)
        collection = Collection(user_id='ssv4<F3>42rf3eqfv')
        self.assertEqual(collection.user_id, 'ssv4<F3>42rf3eqfv')
        with self.assertRaises(TypeError):
            collection = Collection(user_id=1234)

    def test_end_date_attr(self):
        """Test Collection has attr end_date, and it's a datetime"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "end_date"))
        self.assertEqual(collection.end_date, None)
        collection = Collection(end_date=datetime.utcnow())
        self.assertEqual(type(collection.end_date), datetime)
        with self.assertRaises(TypeError):
            collection = Collection(end_date=1234)

    def test_start_date_attr(self):
        """Test Collection has attr end_date, and it's a datetime"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "start_date"))
        self.assertEqual(collection.start_date, None)
        with self.assertRaises(TypeError):
            collection = Collection(start_date=1234)

    def test_description_attr(self):
        """Test Collection has attr description, and it's an empty string"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "description"))
        self.assertEqual(collection.description, None)
        collection = Collection(description='money is spent on entertainment')
        self.assertEqual(collection.description,
                         'money is spent on entertainment')
        with self.assertRaises(TypeError):
            collection = Collection(description=13244)

    def test_name_attr(self):
        """Test Collection has attr name, and it's an empty string"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "name"))
        self.assertEqual(collection.name, None)
        collection = Collection(name='food')
        self.assertEqual(collection.name, 'food')
        with self.assertRaises(TypeError):
            collection = Collection(name=13244)

    def test_limit_attr(self):
        """Test Collection has attr limit, and it's a float == 0.0"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "limit"))
        self.assertEqual(collection.limit, None)
        collection = Collection(limit=100)
        self.assertEqual(type(collection.limit), float)
        self.assertEqual(collection.limit, 100.0)
        with self.assertRaises(TypeError):
            collection = Collection(limit='13244')

    def test_amount_spent_attr(self):
        """Test Collection has attr amount_spent, and it's a float == 0.0"""
        collection = Collection()
        self.assertTrue(hasattr(collection, "amount_spent"))
        if models.storage == 'db':
            self.assertEqual(collection.amount_spent, None)
        else:
            self.assertEqual(type(collection.amount_spent), float)
            self.assertEqual(collection.amount_spent, 0.00)
        with self.assertRaises(TypeError):
            collection = Collection(amount_spent='invld')

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Collection()
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
