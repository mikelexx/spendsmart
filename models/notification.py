#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey

class Notification(BaseModel, Base):
    """Representation of a category """
    if models.storage_type == "db":
        __tablename__ = 'categories'
        message = Column(String(1024), nullable=True)
        notification_type = Column(String(1024), nullable=True)
        marked_as_read = Column(Boolean, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        message = ""
        notification_type = ""
        marked_as_read = False
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes category"""
        super().__init__(*args, **kwargs)

