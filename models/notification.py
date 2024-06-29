#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Boolean, String, DECIMAL, DateTime, ForeignKey

class Notification(BaseModel, Base):
    """Representation of a notification """
    if models.storage_type == "db":
        __tablename__ = 'notifications'
        message = Column(String(1024), nullable=True)
        notification_type = Column(String(60), nullable=False)
        is_read = Column(Boolean, default=False, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        message = ""
        notification_type = ""
        user_id = ""
        is_read = False

    def __init__(self, *args, **kwargs):
        """initializes notification"""
        super().__init__(*args, **kwargs)
    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict()
        if "user" in new_dict:
            del new_dict["user"]
        
        return new_dict

