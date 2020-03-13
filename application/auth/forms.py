from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, IntegerField, SelectField
from datetime import date
from application import city_choices


class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.Regexp('^[a-zA-Z0-9_]*$', message='Käyttäjänimessä on vain latinalaisia kirjaimia, numeroita tai alaviivoja!'),
                                            validators.Length(
                                                min=4, max=16, message='Käyttäjänimi on pituudeltaan 4-16 merkkiä!')
                                            ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})
    password = PasswordField("Salasana", [
        validators.Length(min=8, max=30, message='Salasanan on pituudeltaan 8-30 merkkiä!')],
        render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})

    class Meta:
        csrf = False


class CreateUserForm(FlaskForm):
    username = StringField("Käyttäjänimi", [validators.Regexp('^[a-zA-Z0-9_]*$', message='Käyttäjänimessä saa olla vain latinalaisia kirjaimia, numeroita tai alaviivoja!'),
                                            validators.Length(
                                                min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!'),
                                            validators.input_required(
                                                message='Käyttäjänimi ei voi olla tyhjä!')
                                            ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})
    password = PasswordField("Salasana", [
        validators.Length(
            min=8, max=30, message='Salasanan on oltava pituudeltaan 8-30 merkkiä!'),
        validators.equal_to(
            'confirm_pwd', message='Salasanojen on oltava samat!')
    ], render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})
    confirm_pwd = PasswordField("Vahvista salasana",
        render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})
    name = StringField("Nimi", validators=[validators.Regexp('^[a-zA-Z ÅÖÄåöä]*$', message='Nimessä on vain kirjaimia!'), validators.input_required(
        message='Nimi ei voi olla tyhjä!')], render_kw={"placeholder": "Matti Meikäläinen"})
    city = SelectField("Asuinpaikka", choices=city_choices, validators=[validators.input_required()], render_kw={"placeholder": "Nurmes"})
    age = IntegerField("Syntymävuosi", [validators.number_range(min=int(date.today().year) - 125, max=int(date.today().year), message=(
        "Syntymävuoden on oltava välillä " + str((int(date.today().year) - 125)) + " ja " + str(int(date.today().year))) + "!")], render_kw={"placeholder": "1982"})

    class Meta:
        csrf = False


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField("Nykyinen salasana",
        render_kw={"placeholder": "Syötä nykyinen salasana"})
    password = PasswordField("Uusi salasana", [
        validators.Length(
            min=8, max=30, message='Salasanan on oltava pituudeltaan 8-30 merkkiä!'),
        validators.equal_to('confirmPassword',
                            message='Salasanojen on oltava samat!')
    ], render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})
    confirmPassword = PasswordField("Vahvista uusi salasana",
        render_kw={"placeholder": "Min. 8, maks. 30 merkkiä"})

    class Meta:
        csrf = False


class ChangeUsernameForm(FlaskForm):
    username = StringField("Uusi käyttäjänimi", [validators.Regexp('^[a-zA-Z0-9_]*$', message='Käyttäjänimessä saa olla vain aakkosia, numeroita tai alaviivoja!'), validators.Length(
        min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!'), validators.input_required(message='Käyttäjänimi ei voi olla tyhjä!')], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})

    class Meta:
        csrf = False


class EditUserInfoForm(FlaskForm):
    name = StringField("Nimi", validators=[validators.Regexp('^[a-zA-Z ÅÖÄåöä]*$', message='Nimessä on vain kirjaimia!'), validators.input_required(
        message='Nimi ei voi olla tyhjä!')], render_kw={"placeholder": "Matti Meikäläinen"})
    city = SelectField("Asuinpaikka", choices=city_choices, validators=[validators.input_required()], render_kw={"placeholder": "Nurmes"})
    age = IntegerField("Syntymävuosi", [validators.number_range(min=int(date.today().year) - 125, max=int(date.today().year), message=(
        "Syntymävuoden on oltava välillä " + str((int(date.today().year) - 125)) + " ja " + str(int(date.today().year))) + "!")], render_kw={"placeholder": "1982"})

    class Meta:
        csrf = False
