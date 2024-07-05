#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from flask_login import UserMixin
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


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
        """initializes user"""
        super().__init__(*args, **kwargs)

    def to_dict(self, hide_password=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict(hide_password)
        new_dict['collections'] = [coll.to_dict() for coll in self.collections]
        new_dict['expenses'] = [exp.to_dict() for exp in self.expenses]
        new_dict['notifications'] = [
            notif.to_dict() for notif in self.notifications
        ]
        return new_dict
