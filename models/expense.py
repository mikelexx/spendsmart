import models
from datetime import datetime
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship

time = '%Y-%m-%dT%H:%M:%S.%f'


class Expense(BaseModel, Base):
    """Representation of an expense"""

    # Define table name if using database storage
    if models.storage_type == "db":
        __tablename__ = 'expenses'

        # Define columns for database storage
        name = Column(String(128), nullable=False)
        price = Column(DECIMAL(precision=10, scale=2), nullable=False)
        collection_id = Column(String(60),
                               ForeignKey('collections.id'),
                               nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        purchase_date = Column(DateTime, nullable=False)

    else:
        # Default values if not using database storage
        name = ""
        price = 0.00
        collection_id = ""
        purchase_date = datetime.strptime(datetime.utcnow(),
                                          time)  # Default to current UTC time
        user_id = ""

    def __init__(self, *args, **kwargs):
        """Initialize expense object"""
        super().__init__(*args, **kwargs)
        if kwargs and kwargs.get("purchase_date", None) and type(
                self.purchase_date) is str:
            self.purchase_date = datetime.strptime(kwargs["purchase_date"],
                                                   time)

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = super().to_dict()
        if "purchase_date" in new_dict:
            new_dict["purchase_date"] = new_dict["purchase_date"].strftime(
                time)

        # Remove or convert non-serializable attributes
        if "colllection" in new_dict:
            # del new_dict["collection"] Remove the entire collection object
            del new_dict["colllection"]
        if "collection" in new_dict:
            del new_dict["collection"]
        if "user" in new_dict:
            del new_dict["user"]
        return new_dict
