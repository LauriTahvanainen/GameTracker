from flask_wtf import FlaskForm
from wtforms import StringField, validators

class addEquipmentForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!')])

    class Meta:
        csrf = False