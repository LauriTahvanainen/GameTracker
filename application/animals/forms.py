from flask_wtf import FlaskForm
from wtforms import StringField, validators

class addNewAnimalForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!')])
    lat_name = StringField("Latinankielinen nimi")
    info = StringField("Tietoja", [validators.url(message='Tiedon on oltava url-osoite')])

    class Meta:
        csrf = False