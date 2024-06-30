#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv

storage_type = getenv("SPENDSMART_TYPE_STORAGE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    print("from file")
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
