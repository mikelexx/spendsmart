#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import models
from models.base_model import BaseModel

from models.user import User
from models.expense import Expense
from models.collection import Collection
from models.notification import Notification
from datetime import datetime
classes = {
    "User": User,
    "Expense": Expense,
    "Collection": Collection,
    "Notification": Notification
}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
            """returns the dictionary __objects"""
            self.reload()
            if cls is not None:
                new_dict = {}
                for key, value in self.__objects.items():
                    if cls == value.__class__ or cls == value.__class__.__name__:
                        new_dict[key] = value
                return new_dict
            print(f"storage.all({cls}) returned {self.__objects}")
            return self.__objects


    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(save_fs=1)
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f, default=str
                      )  # Use default=str to handle datetime serialization

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                # Adjusting to handle datetime with microseconds
                if 'created_at' in jo[key]:
                    jo[key]['created_at'] = datetime.strptime(jo[key]['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                if 'updated_at' in jo[key]:
                    jo[key]['updated_at'] = datetime.strptime(jo[key]['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception as e:
            print(f"Error storage.reload(): {e}")  # Debugging line

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID, or None if not found"""
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        if all_cls:
            for value in all_cls.values():
                print(value.id)
                if value.id == id:
                    return value

        print(f"storage.get({cls},{id}) returned None")  # debuggin line 
        return None

    def user_all(self, user_id, cls=None):
        """
        get objects belonging to particular user and class
        or all objects belonging to particular user if class 
        is not specified>
        Args:
            user_id: user_id for which objects to be retrieved belongs to.
            cls: type of objects to retrieve.
        Return: objects of type `cls`
        """

        user = self.get(User, user_id)
        if not user:
            return None
        if cls is not None and cls not in classes.values():
            return None
        else:
            all_cls_objs = self.all(cls)
            user_cls_objs = []
            for obj in all_cls_objs.values():
                if getattr(obj, 'user_id', None) == user_id and isinstance(obj, cls): 
                    user_cls_objs.append(obj)
        return user_cls_objs

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
