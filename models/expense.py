#!/usr/bin/python
""" holds class Expense"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship


class Expense(BaseModel, Base):
    """Representation of an expense """
    if models.storage_type == "db":
        __tablename__ = 'expenses'
        name = Column(String(128), nullable=False)
        price = Column(DECIMAL(precision=10, scale=2), nullable=False)
        category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        name = ""
        price = 0.00
        category_id = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes expense"""
        super().__init__(*args, **kwargs)

