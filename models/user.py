#!/usr/bin/python3
""" holds class User"""

import models
import re
from datetime import datetime
from models.collection import Collection
from models.expense import Expense
from models.notification import Notification
from models.base_model import BaseModel, Base
from flask_login import UserMixin
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5

email_pattern = re.compile(
    r'''
    ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
''', re.VERBOSE)
password_pattern = re.compile(
    r'''^(?=.*[A-Z])         # Must contain at least one uppercase letter
       (?=.*[a-z])          # Must contain at least one lowercase letter
       (?=.*[!@#$&*])       # Must contain at least one special character
       (?=.*[0-9])          # Must contain at least one digit
       .{7,}$               # Length must be at least 8 characters (7 + 1)
    ''', re.VERBOSE)


class User(UserMixin, BaseModel, Base):
    """Representation of a user """
    if models.storage_type == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        username = Column(String(128), nullable=True)
        expenses = relationship("Expense", backref="user")
        collections = relationship("Collection",
                                   backref="user",
                                   cascade='all, delete-orphan')
        notifications = relationship("Notification",
                                     backref="user",
                                     cascade='all, delete-orphan')
    else:
        email = ""
        password = ""
        username = ""

    def __init__(self, *args, **kwargs):
        """Initializes a User instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Variable length keyword arguments.

        Raises:
            TypeError: If attributes are of incorrect type.
            ValueError: If attribute values exceed allowed length.
        """
        super().__init__(*args, **kwargs)
        # must have password pattern to qualify a password
        attributes = {
            'notifications': Notification,
            'expenses': Expense,
            'collections': Collection
        }
        for attr in attributes:
            attr_values = getattr(self, attr)
            if attr_values:
                if type(attr_values) is not list:
                    raise TypeError('invalid notifications type {}'.format(
                        type(attr_values)))
                for val in attr_values:
                    if type(val) is not attributes.get(attr):
                        raise TypeError('invalid notification type: {}'.format(
                            type(val)))
        for attr in ['email', 'id', 'password']:
            if getattr(self, attr):
                if type(getattr(self, attr)) is not str:
                    raise TypeError('invalid {} type {}'.format(
                        attr, type(getattr(self, attr))))
                if len(getattr(self, attr)) > 128:
                    raise ValueError(
                        'large attrbute value for {}'.format(attr))
        for attr in ['created_at', 'updated_at']:
            if getattr(self, attr) and type(getattr(self, attr))\
              is not datetime:
                raise TypeError('invalid {} type {}'.format(
                    attr, type(getattr(self, attr))))
        if self.email and not email_pattern.match(self.email):
            raise ValueError('invalid email format {}'.format(self.email))
        if self.password and not password_pattern.match(self.password):
            raise ValueError('weak password')
        if not self.email and not self.username:
            raise TypeError('must provide either username, email or both')
        if not self.password:
            raise TypeError('must provide password')

    def to_dict(self, hide_password=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict(hide_password)
        new_dict['collections'] = [coll.to_dict() for coll in self.collections]
        new_dict['expenses'] = [exp.to_dict() for exp in self.expenses]
        new_dict['notifications'] = [
            notif.to_dict() for notif in self.notifications
        ]
        return new_dict

    # override userMixin function to add docstring for it to pass unittests

    def get_id(self):
        """Return the unique identifier for the user."""
        return super().get_id()
