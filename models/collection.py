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
        amount_spent = Column(DECIMAL(precision=10, scale=2), nullable=False)
        start_date = Column(DaTetime, nullable=False) 
        end_date = Column(DateTime, nullable=False) 
        description = Column(String(1024), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        name = ""
        limit = 0.00
        amount_spent = 0.00
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
    def update_notification(self, **kwargs):
        """ update notification state for this collection """
        for key, val in kwargs.items():
            setattr(old_notification, key, val)

    def check_notifications(self):
        from models import storage
        # Check if the collection has exceeded its limit
        if self.amount_spent > self.limit:
            message=f"The collection '{self.name}' has exceeded its limit.",
            notification_type='alert'
            old_notification = storage.get(Notification, self.id)
            if old_notification:
                self.update_notification(message=message, notification_type=notification_type)
            else:
                self.create_notification(
                    message=message,
                    notification_type=notification_type
                )
        # Check if the collection's end date is overdue
        if datetime.utcnow() > self.end_date:
            message=f"The collection '{self.name}' is overdue.",
            notification_type='alert'
            old_notification = storage.get(Notification, self.id)
            if old_notification:
                self.update_notification(message=message, notification_type=notification_type)
            else:
                self.create_notification(
                        message=message,
                        notification_type=notification_type
                )
        # Check if the remaining amount is less than half or quarter
        remaining_amount = self.limit - self.amount_spent
        if remaining_amount < self.limit / 2:
            message=f"The collection '{self.name}' has less than half its limit remaining.",
            notification_type='reminder'
            old_notification = storage.get(Notification, self.id)
            if old_notification:
                self.update_notification(message=message, notification_type=notification_type)
            else:
                self.create_notification(
                    message=message,
                    notification_type=notification_type
                )
        if remaining_amount < self.limit / 4:
            message=f"The collection '{self.name}' has less than a quarter of its limit remaining.",
            notification_type='reminder'
            old_notification = storage.get(Notification, self.id)
            if old_notification:
                self.update_notification(message=message, notification_type=notification_type)
            else:
                self.create_notification(
                        message=message,
                        notification_type=notification_type
                )
        # Check if the tracking duration is over and the limit has not been exceeded
        if datetime.utcnow() > self.end_date and self.amount_spent <= self.limit:
            message=f"Congratulations! The collection '{self.name}' has successfully completed without exceeding its limit.",
            notification_type='achievement'
            old_notification = storage.get(Notification, self.id)
            if old_notification:
                self.update_notification(message=message, notification_type=notification_type)
            else:
                self.create_notification(
                        message=message,
                        notification_type=notification_type
                )

    def create_notification(self, message, notification_type):
        notification = Notification(
            message=message,
            notification_type=notification_type,
            user_id=self.user_id,
            collection_id = self.id,
            is_read=False
        )
        notification.save()
