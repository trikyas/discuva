from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
    first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
    last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    email = StringField('email', validators=[DataRequired("Please enter your email address."), Email("Please enter your correct email address.")])
    password = PasswordField('password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
    submit = SubmitField('Sign up')