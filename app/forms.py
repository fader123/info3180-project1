from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, InputRequired

    
class MyForm(FlaskForm):
    lastname = StringField('Last Name',validators=[InputRequired()])
    firstname = StringField('First Name',validators=[InputRequired()])
    email = StringField('Email',validators=[InputRequired()])
    location = StringField('Location',validators=[InputRequired()])
    biography = TextAreaField('Biography',validators=[InputRequired()])
    gender = SelectField('Gender',choices=[('','Select Gender'),('Male','Male'),('Female','Female')] ,validators=[validators.Required("Please select a gender")])
    photo= FileField('Profile Picture',validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only')])