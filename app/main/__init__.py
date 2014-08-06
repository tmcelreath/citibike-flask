""" Main application blueprint defining routes and error pages """
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes, errors