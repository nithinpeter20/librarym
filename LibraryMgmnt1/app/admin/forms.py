# Forms for admin blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextField, DateField, FloatField, IntegerField,  ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class CreateBookForm(FlaskForm):
	"""
	Form for creating book
	"""

	name = StringField('Book Name', validators=[DataRequired()])	
	author = TextField("Author", validators=[DataRequired()])
	publication_date = DateField('Publication_date', format='%m/%d/%Y')
	rating = FloatField("Rating", validators=[DataRequired()])
	review = StringField('Review', validators=[DataRequired()])
	book_count = IntegerField('Count', validators= [DataRequired()])
	image = FileField('image', validators=[FileRequired()])
	submit = SubmitField('Create Book')


class AddAuthorForm(FlaskForm):
	"""
	Form for adding author
	"""

	author_name = StringField('Author Name', validators=[DataRequired()])
	place = StringField('Place', validators=[DataRequired()])
	age = IntegerField('Age', validators= [DataRequired()])
	image = FileField('image', validators=[FileRequired()])
	submit = SubmitField('Add Author')



class LendRequestForm(FlaskForm):
	"""
	Form for lending request
	"""

	user_id = IntegerField('User id', validators=[DataRequired()])
	book_id =IntegerField('Book id', validators=[DataRequired()])
	date = DateField('Date',  format='%m/%d/%Y')
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Lend Book')



class ReturnRequestForm(FlaskForm):
	"""
	Form for return request
	"""

	user_id = IntegerField('User id', validators=[DataRequired()])
	book_id =IntegerField('Boook id', validators=[DataRequired()])
	date = DateField('Date', validators= [DataRequired()])
	status = StringField('status', validators=[DataRequired()])
	submit = SubmitField('Return Book')
	