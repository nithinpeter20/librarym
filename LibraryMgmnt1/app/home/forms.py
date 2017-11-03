"""
Form for registration
"""
### Libraries
# Third party libraries
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.validators import Email
from wtforms.validators import EqualTo

# Local imports
from ..models import Users

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField(  validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')