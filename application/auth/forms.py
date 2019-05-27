from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, IntegerField

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

    class Meta:
        csrf = False

class CreateUserForm(FlaskForm):
    username = StringField("Käyttäjänimi", [
        validators.Length(min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!'),
        validators.input_required(message='Käyttäjänimi ei voi olla tyhjä!')
    ])
    password = PasswordField("Salasana", [
        validators.Length(min=8, max=30, message='Salasanan on oltava pituudeltaan 8-30 merkkiä!'),
        validators.equal_to('confirmPwd', message='Salasanojen on oltava samat!')
    ])
    confirmPwd = PasswordField("Vahvista salasana")
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!')])
    city = StringField("Kaupunki")
# Todo, Validate age to always be a number
    age = IntegerField("Syntymävuosi", [validators.number_range(min=1888, max=2012)])

    class Meta:
        csrf = False