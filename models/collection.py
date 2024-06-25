#!/usr/bin/python3
""" holds class Category"""
import models
from models.base_model import BaseModel, Base
from models.expense import Expense
from models.notification import Notification
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

        if 'amount_spent' not in kwargs:
            self.amount_spent = 0.00


    def to_dict(self, save_fs=None):
            """returns a dictionary containing all keys/values of the instance"""
            new_dict = super().to_dict()
            for name in ["start_date", "end_date"]:
                if name in new_dict:
                    new_dict[name] = new_dict[name].strftime(time)
            return new_dict
    def update_notification(self, old_notification,  **kwargs):
        """ update notification state for this collection """
        for key, val in kwargs.items():
            setattr(old_notification, key, val)

        old_notification.save()

    def create_notification(self, message, notification_type):
        notification = Notification(
            message=message,
            notification_type=notification_type,
            user_id=self.user_id,
            collection_id = self.id,
            is_read=False
        )
        notification.save()
    def check_notifications(self, expenses_ids=None):
        from models import storage
        from datetime import datetime

        percentage = int((self.amount_spent / self.limit) * 100)
        all_notifications = storage.user_all(self.user_id, Notification)
        old_notifications = [notif for notif in all_notifications if notif.collection_id == self.id]
        # delete orphan notifications that were notifyig of object deletion but have now been read;
        for notif in old_notifications:
            if notif.is_read and storage.get(Notification, notif.collection_id) == '':
                notif.delete()
                storage.save()
          # Check if the collection has exceeded its limit
        if self.amount_spent > self.limit:
            new_notification_type = 'alert'
            message = f"you have exceeded the set limit of {self.name}"
            self._handle_notification(old_notifications, message, new_notification_type)

        # Check if the collection's end date is overdue
        if datetime.utcnow() > self.end_date:
            # Only show achievement if not exceeded
            if self.amount_spent <= self.limit:
                new_notification_type = 'achievement'
                if self.amount_spent <= self.limit / 2:
                    message = f"Congratulations! {self.name} Tracking period just ended! You have successfully managed to spend only {self.amount_spent} out of your {self.limit} budget for {self.name}, achieving an impressive {100 - percentage}% savings. You've earned the 'Savvy Saver' achievement!"
                else:
                    message = f"Well done! {self.name} Tracking period just ended! You have spent {self.amount_spent} out of your {self.limit} budget for {self.name}, saving {100 - percentage}%. You've earned the 'Smart Spender' achievement!"
                self._handle_notification(old_notifications, message, new_notification_type)
            else:
                new_notification_type = 'alert'
                message = f"{self.name} Tracking period just ended! But.. You have exceeded your {self.limit} budget for {self.name} by {self.amount_spent - self.limit}. Consider adjusting your spending habits to meet your budget goals next time."
                
                self._handle_notification(old_notifications, message, new_notification_type)
            self._handle_notification(old_notifications, f'Deleted {self.name} as its monitoring period is over', 'alert')
            # delete collection object if its the end date has passed
            for notif in old_notifications:
                notif.delete()
                storage.save()
            #make sure expenses related to collection are deleted if its due its over
            if expenses_ids:
                for expense_id in expenses_ids:
                    storage.get(Expense, expense_id).delete()
                    storage.save()
            self.delete()
            storage.save()

        # Check if the remaining amount is less than half or quarter
        remaining_amount = self.limit - self.amount_spent
        if datetime.utcnow() < self.end_date:  # Ensure we are within the tracking period
            if remaining_amount < self.limit / 2 and remaining_amount > self.limit / 4:
                new_notification_type = 'warning'
                message = f"you have spent more than half of set limit on {self.name}. Monitor your spending closely to stay within your limit."
                self._handle_notification(old_notifications, message, new_notification_type)
            elif 0 < remaining_amount < self.limit / 4:
                new_notification_type = 'warning'
                message = f"You've spent {percentage}% out of your {self.limit} {self.name} budget. You are close to reaching your budget limit. Consider reviewing your upcoming expenses."
                self._handle_notification(old_notifications, message, new_notification_type)

    def _handle_notification(self, old_notifications, message, new_notification_type):
        found_old_notifications = False
        for notification in old_notifications:
            if notification.message == message:
                self.update_notification(notification, message=message, notification_type=new_notification_type)
                return
        self.create_notification(message=message, notification_type=new_notification_type)
