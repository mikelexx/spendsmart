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
        """
        TODO
        figure the relationships between use and expenses ...
        """
        expenses = relationship("Expense", backref="user")
    else:
        email = ""
        password = ""
        username = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
