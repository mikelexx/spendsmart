#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey

class Collection(BaseModel, Base):
    """Representation of a category """
    if models.storage_type == "db":
        __tablename__ = 'categories'
        name = Column(String(128), nullable=False)
        limit = Column(DECIMAL(precision=10, scale=2), nullable=False)
        tracking_start_date = Column(DaTetime, nullable=False) 
        tracking_end_date = Column(DateTime, nullable=False) 
        description = Column(String(1024), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        name = ""
        limit = 0.00
        tracking_start_date = ""
        tracking_end_date = ""
        description = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes category"""
        super().__init__(*args, **kwargs)

