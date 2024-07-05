#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from models.expense import Expense
from models.notification import Notification
from os import getenv
import requests
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

time = '%Y-%m-%dT%H:%M:%S.%f'


class Collection(BaseModel, Base):
    """Representation of a collection"""
    if models.storage_type == "db":
        __tablename__ = 'collections'
        name = Column(String(128), nullable=False)
        limit = Column(DECIMAL(precision=10, scale=2), nullable=False)
        amount_spent = Column(DECIMAL(precision=10, scale=2), nullable=False)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)
        description = Column(String(1024), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        expenses = relationship("Expense",
                                backref="collection",
                                cascade='all, delete-orphan')
    else:
        name = ""
        limit = 0.00
        amount_spent = 0.00
        start_date = ""
        end_date = ""
        description = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """Initializes collection"""
        super().__init__(*args, **kwargs)
        if kwargs:
            self._parse_dates(kwargs)
        if 'amount_spent' not in kwargs:
            self.amount_spent = 0.00

    def _parse_dates(self, kwargs):
        """Parse date strings into datetime objects"""
        if kwargs.get("start_date", None) and type(self.start_date) is str:
            self.start_date = datetime.strptime(kwargs["start_date"], time)
        if kwargs.get("end_date", None) and type(self.end_date) is str:
            self.end_date = datetime.strptime(kwargs["end_date"], time)

    def to_dict(self):
        """Returns a dictionary representation of the collection"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'limit': self.limit,
            'start_date': self.start_date.strftime(time),
            'end_date': self.end_date.strftime(time),
            'user_id': self.user_id,
            'amount_spent': self.amount_spent,
            'created_at': self.created_at.strftime(time),
            'updated_at': self.updated_at.strftime(time),
            'expenses': [expense.to_dict() for expense in self.expenses],
            '__class__': self.__class__.__name__
        }

    def create_notification(self, message, notification_type):
        """Create and save a new notification"""
        notification = Notification(
            message=message,
            notification_type=notification_type,
            user_id=self.user_id,
            collection_id=self.id,
            is_read=False
        )
        notification.save()

    def check_notifications(self, expenses_ids=None):
        """Check and handle notifications for the collection"""
        from models import storage
        limit_exceed_message = f"you have exceeded the set limit of {self.name}"
        percentage = int((self.amount_spent / self.limit) * 100)
        old_notifications = storage.user_all(self.user_id, Notification)

        self._check_limit_exceeded(old_notifications, limit_exceed_message)
        self._check_limit_reached(old_notifications)
        self._check_end_date_exceeded(old_notifications, percentage)
        self._check_remaining_amount(old_notifications, percentage)

    def _check_limit_exceeded(self, old_notifications, limit_exceed_message):
        """Check if the collection has exceeded its limit"""
        if self.amount_spent > self.limit:
            self._handle_notification(old_notifications, limit_exceed_message, 'alert')

    def _check_limit_reached(self, old_notifications):
        """Check if the collection has reached its limit"""
        if self.amount_spent == self.limit:
            message = f"you have spent all the money you had allocated on {self.name}"
            self._handle_notification(old_notifications, message, 'alert')

    def _check_end_date_exceeded(self, old_notifications, percentage):
        """Check if the collection's end date is overdue"""
        from models import storage
        if datetime.utcnow() > self.end_date:
            if self.amount_spent <= self.limit:
                self._handle_achievement(old_notifications, percentage)
            else:
                self._handle_over_limit(old_notifications)
            self._delete_collection_related_data()
            storage.save()

    def _handle_achievement(self, old_notifications, percentage):
        """Handle achievement notification"""
        if self.amount_spent <= self.limit / 2:
            message = (f"Congratulations! {self.name} Tracking period just ended! "
                       f"You have successfully managed to spend only {self.amount_spent} "
                       f"out of your {self.limit} budget for {self.name}, achieving an impressive "
                       f"{100 - percentage}% savings. You've earned the 'Savvy Saver' achievement!")
        else:
            message = (f"Well done! {self.name} Tracking period just ended! "
                       f"You have spent {self.amount_spent} out of your {self.limit} budget for {self.name}, "
                       f"saving {100 - percentage}%. You've earned the 'Smart Spender' achievement!")
        self._handle_notification(old_notifications, message, 'achievement')

    def _handle_over_limit(self, old_notifications):
        """Handle over limit notification"""
        message = (f"{self.name} Tracking period just ended! But.. You have exceeded your "
                   f"{self.limit} budget for {self.name} by {self.amount_spent - self.limit}. "
                   f"Consider adjusting your spending habits to meet your budget goals next time.")
        self._handle_notification(old_notifications, message, 'alert')

    def _delete_collection_related_data(self):
        """Delete collection and related data"""
        from models import storage
        for exp in storage.user_all(self.user_id, Expense):
            if exp.collection_id == self.id:
                exp.delete()
        for notif in storage.user_all(self.user_id, Notification):
            if notif.collection_id == self.id:
                notif.delete()
        self.delete()

    def _check_remaining_amount(self, old_notifications, percentage):
        """Check if the remaining amount is less than half or quarter"""
        remaining_amount = self.limit - self.amount_spent
        if datetime.utcnow() < self.end_date:
            if (self.limit / 4) <= remaining_amount < self.limit / 2:
                message = (f"you have spent more than half of set limit on {self.name}. "
                           f"Monitor your spending closely to stay within your limit.")
                self._handle_notification(old_notifications, message, 'warning')
            elif 0 < remaining_amount < self.limit / 4:
                message = (f"You've spent {percentage}% out of your {self.limit} {self.name} budget. "
                           f"You are close to reaching your budget limit. Consider reviewing your upcoming expenses.")
                self._handle_notification(old_notifications, message, 'warning')

    def _handle_notification(self, old_notifications, message, new_notification_type):
        """Handle creating notifications"""
        if any(notification.message == message for notification in old_notifications):
            return
        self.create_notification(message=message, notification_type=new_notification_type)

