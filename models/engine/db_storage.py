#!/usr/bin/python3
from sqlalchemy.orm import scoped_session, sessionmaker, object_session
from sqlalchemy.orm import mapper
from sqlalchemy import exc as sa_exc
from sqlalchemy import orm
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.expense import Expense
from models.collection import Collection
from models.notification import Notification
from os import getenv

classes = {
    "User": User,
    "Expense": Expense,
    "Collection": Collection,
    "Notification": Notification
}


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session_factory = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        SPENDSMART_MYSQL_USER = getenv('SPENDSMART_MYSQL_USER')
        SPENDSMART_MYSQL_PWD = getenv('SPENDSMART_MYSQL_PWD')
        SPENDSMART_MYSQL_HOST = getenv('SPENDSMART_MYSQL_HOST')
        SPENDSMART_MYSQL_DB = getenv('SPENDSMART_MYSQL_DB')
        SPENDSMART_ENV = getenv('SPENDSMART_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            SPENDSMART_MYSQL_USER, SPENDSMART_MYSQL_PWD, SPENDSMART_MYSQL_HOST,
            SPENDSMART_MYSQL_DB))

        self.__session_factory = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = self.__session_factory()

    def all(self, cls=None):
        """Query on the current database session with eager loading for relationships"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).options(
                    orm.joinedload('*')).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        try:
            self.__session.commit()
        except Exception as e:
            # self.__session.rollback()
            print("error in saving==>", e)

    def delete(self, obj=None, confirm_deleted_rows=False):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            try:
                existing_obj = self.__session.query(obj.__class__).get(obj.id)
                if existing_obj:
                    # print("Found existing object instance {}".format(existing_obj))
                    '''
                    for expense in existing_obj.expenses:
                        expense.delete()
                        '''
                    #self.__session.expunge(existing_obj)
                    self.__session.delete(existing_obj)
                else:
                    self.__session.delete(obj)
                    if not confirm_deleted_rows:
                        mapper(obj.__class__).confirm_deleted_rows = False
                    self.save()
            except Exception as e:
                print("error occured in storage.delete() ===>", e)

    def reload(self):
        """Reload data from the database"""
        #  Base.metadata.create_all(self.__engine)
        # self.__session = self.__session_factory()
        try:
            # Create all tables if they do not exist
            Base.metadata.create_all(self.__engine)
        except sa_exc.OperationalError as e:
            print(f"OperationalError: {e}")
        self.__session = self.__session_factory()

    def close(self):
        """Close the current session"""
        self.__session_factory.remove()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID, or None if not found"""
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def user_all(self, user_id, cls=None):
        """
        Get objects belonging to a particular user and class,
        or all objects belonging to a particular user if class 
        is not specified.
        """
        user = self.get(User, user_id)
        if not user:
            return None

        if cls is not None and cls not in classes.values():
            return None

        user_cls_objs = self.__session.query(cls).filter_by(
            user_id=user_id).all()
        return user_cls_objs

    def count(self, cls=None):
        """Count the number of objects in storage"""
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count

