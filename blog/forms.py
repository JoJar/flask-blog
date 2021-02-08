from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, InputRequired, Regexp
from blog.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField(u'First Name', validators= [DataRequired()])
    last_name = StringField(u'Last Name', validators= [DataRequired()])
    username= StringField('Username', validators= [DataRequired(), Length(min=3, max=15)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired(), Regexp('^.{6,128}$', message='You password should be at least 6 characters long and no longer than 128 characters.')])
    confirm_password = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a something else.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists. Please choose a something else.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

    def validate_username_login(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username does not exist.')
    
    def validate_email_login(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This is email does not exist.')