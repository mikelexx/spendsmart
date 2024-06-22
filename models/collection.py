#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey
from datetime import datetime

time = '%Y-%m-%dT%H:%M:%S.%f'
class Collection(BaseModel, Base):
    """Representation of a category """
    if models.storage_type == "db":
        __tablename__ = 'categories'
        name = Column(String(128), nullable=False)
        limit = Column(DECIMAL(precision=10, scale=2), nullable=False)
        start_date = Column(DaTetime, nullable=False) 
        end_date = Column(DateTime, nullable=False) 
        description = Column(String(1024), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        name = ""
        limit = 0.00
        start_date = ""
        end_date = ""
        description = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes category"""
        super().__init__(*args, **kwargs)
        if kwargs:
            if kwargs.get("start_date", None) and type(self.start_date) is str:
                self.start_date = datetime.strptime(kwargs["start_date"], time)
            if kwargs.get("end_date", None) and type(self.end_date) is str:
                self.end_date = datetime.strptime(kwargs["end_date"], time)


    def to_dict(self, save_fs=None):
            """returns a dictionary containing all keys/values of the instance"""
            new_dict = super().to_dict()
            for name in ["start_date", "end_date"]:
                if name in new_dict:
                    new_dict[name] = new_dict[name].strftime(time)
            return new_dict
