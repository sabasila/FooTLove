from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileAllowed, FileRequired

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=16)])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    birthday = DateField('Birthday', validators=[DataRequired()], format='%Y-%m-%d')
    gender = RadioField('Gender', choices=[('MA', 'Male'), ('FE', 'Female')], validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('US', 'United States'),
        ('TR', 'Turkey'),
        ('UK', 'United Kingdom'),
        ('NG', 'Nigeria'),
        ('GEO', 'Georgia'),
        ('FR', 'France')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=16)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send')

class EditItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    images = FileField()
    submit = SubmitField('Save')



