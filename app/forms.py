from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
