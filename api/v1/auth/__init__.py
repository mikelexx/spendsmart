#!/usr/bin/python3
""" importing auth blueprint """
from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/api/v1')
from api.v1.auth.auth import *
