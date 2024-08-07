#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
import uuid

time = '%Y-%m-%dT%H:%M:%S.%f'
if models.storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        default_date = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if hasattr(self, key):
                        setattr(self, key, value)
            try:
                created_at = kwargs.get('created_at')
                updated_at = kwargs.get('updated_at')
                if updated_at:
                    if type(updated_at) is str:
                        self.updated_at = datetime\
                         .strptime(kwargs["created_at"], time)
                    elif type(updated_at) is datetime:
                        # check if it conforms to our format
                        updated_at.strftime(time)
                    else:
                        raise TypeError(
                            'invalid date type: {}'.format(updated_at))
                else:
                    self.updated_at = default_date
                if created_at:
                    if type(created_at) is str:
                        self.created_at = datetime\
                         .strptime(kwargs["created_at"], time)
                    elif type(created_at) is datetime:
                        # check if it conforms to our format
                        created_at.strftime(time)
                    else:
                        raise TypeError(
                            'invalid date type: {}'.format(created_at))
                else:
                    self.created_at = default_date
            except Exception as e:
                raise e
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, hide_password=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(
                '%Y-%m-%dT%H:%M:%S.%f')
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(
                '%Y-%m-%dT%H:%M:%S.%f')
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if hide_password:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        # models.storage.expunge(self)
        models.storage.delete(self)
