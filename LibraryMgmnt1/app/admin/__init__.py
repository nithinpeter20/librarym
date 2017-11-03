#app/admin/__init__.py
"""
Script for admin blue print
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

# Local imports
from . import views