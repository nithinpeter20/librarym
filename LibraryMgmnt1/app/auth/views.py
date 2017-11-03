#app/auth/views.py
"""
Views for authentication of users
"""
### Libraries
# Third party libraries
from flask import render_template
from flask import request
from flask import flash
from flask import abort
from flask import redirect
from flask import url_for
from flask_login import current_user
from flask_login import login_required,login_user, logout_user

# Local imports
from app import db
from . import auth
from .forms import RegistrationForm
from .forms import LoginForm
from ..models import Users

@auth.route('/register',  methods=['GET', 'POST'])
def register():
    """
    Handle requests to register route
    Add an users to database through registraton form
    """
   
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = Users(email=form.email.data,
                            username= form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Succesfully registretrd...now u can login:')
        return redirect(url_for('auth.login'))

        
    return render_template('register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function for to login user/admin
    """
    form = LoginForm()
    if form.validate_on_submit():

        # Checks any employee exist in database checks the password matches
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            
            login_user(user)

            if user.is_admin:
                
                return redirect(url_for('admin.adminpage'))
            
            else:
                
                return redirect(url_for('auth.userpage'))

        else:
            
            flash('Invalid email or password')

    return render_template('login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Function to logout user
    """
    
    logout_user()
    flash('You have  been successfully  logged out.')
    
    return redirect(url_for('auth.login'))

@auth.route('/user')
@login_required
def userpage():
    """
    Function to load userpage
    """
    
    return render_template('user.html', title='User')

