from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class CreateNewForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    name = StringField("Name")
    city = StringField("City")
# Todo, Validate age to always be a number
    age = StringField("Age")

    class Meta:
        csrf = False