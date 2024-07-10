#!/usr/bin/python3
"""
contains tests for Expense resource api
"""
from models.expense import Expense
from models import storage
from datetime import datetime

def test_post_expense(test_client):
    """ tests POST /expenses api """
    #send create with no json
    #send with missing required values
    #send with incorrect field data types
    #send long purchase date
    #send with non existing user id and or collection id
    #send with purchase range not in tracking duration range
    #try saving when expiry date is due
