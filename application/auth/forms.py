from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, IntegerField
from datetime import date


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False


class CreateUserForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.Regexp('^[a-zA-Z0-9_]*$', message='Käyttäjänimessä saa olla vain aakkosia, numeroita tai alaviivoja!'),
                                            validators.Length(
                                                min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!'),
                                            validators.input_required(
                                                message='Käyttäjänimi ei voi olla tyhjä!')
                                            ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})
    password = PasswordField("Salasana", [
        validators.Length(
            min=8, max=30, message='Salasanan on oltava pituudeltaan 8-30 merkkiä!'),
        validators.equal_to(
            'confirmPwd', message='Salasanojen on oltava samat!')
    ], render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})
    confirmPwd = PasswordField("Vahvista salasana")
    name = StringField("Nimi", validators=[validators.Regexp('^[a-zA-Z]*$', message='Nimessä on vain kirjaimia!'), validators.input_required(
        message='Nimi ei voi olla tyhjä!')], render_kw={"placeholder": "Matti Meikäläinen"})
    city = StringField("Kaupunki", validators=[validators.Regexp('^[a-zA-ZåöäÅÖÄ]*$', message='Kaupungin nimessä on vain kirjaimia!')], render_kw={"placeholder": "Nurmes"})
    age = IntegerField("Syntymävuosi", [validators.number_range(min=int(date.today().year) - 125, max=int(date.today().year), message=(
        "Syntymävuoden on oltava välillä " + str((int(date.today().year) - 125)) + " ja " + str(int(date.today().year))) + "!")], render_kw={"placeholder": "1982"})

    class Meta:
        csrf = False


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField("Nykyinen salasana")
    password = PasswordField("Uusi salasana", [
        validators.Length(
            min=8, max=30, message='Salasanan on oltava pituudeltaan 8-30 merkkiä!'),
        validators.equal_to('confirmPassword',
                            message='Salasanojen on oltava samat!')
    ], render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})
    confirmPassword = PasswordField("Vahvista uusi salasana")

    class Meta:
        csrf = False


class ChangeUsernameForm(FlaskForm):
    username = StringField("Uusi käyttäjänimi", [
        validators.Length(
            min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!'),
        validators.input_required(message='Käyttäjänimi ei voi olla tyhjä!')
    ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})

    class Meta:
        csrf = False
