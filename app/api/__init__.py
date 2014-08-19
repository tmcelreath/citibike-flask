""" API application blueprint defining routes and error pages """
from flask import Blueprint

api = Blueprint('api', __name__)

from . import routes, errors