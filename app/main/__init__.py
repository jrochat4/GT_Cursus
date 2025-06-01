# app/main/__init__.py
from flask import Blueprint

bp = Blueprint('main', __name__)

from . import routes # Import routes to ensure they are registered with the blueprint
