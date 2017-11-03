# app/home/views.py
"""
Views for homepage
"""
### Libraries
# Third party libraries
from flask_login import login_required
from flask_login import current_user
from flask import render_template

# Local imports
from . import home
from .. import admin

@home.route('/')
def home():
    """
    Render the homepage template on the / route
    """
    return render_template('home.html', title="Home")

