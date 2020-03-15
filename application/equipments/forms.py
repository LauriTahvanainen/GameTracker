from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, FormField, FieldList, SelectMultipleField
from wtforms.form import BaseForm, Form
from application.equipments.models import Equipment


class AddEquipmentForm(FlaskForm):
    name = StringField("Nimi", [validators.Regexp('^[a-zA-ZåöäÅÖÄ]*$', message='Välineen nimessä on vain kirjaimia!'), validators.input_required(
        message='Nimi ei voi olla tyhjä!')], render_kw={"placeholder": "Kiikarit"})
    allowed_types = SelectMultipleField("Sallitut havaintotyypit", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Liikenneonnettomuus"), (4, "Onnettomuus")], coerce=int)

    class Meta:
        csrf = False

# list and remove view
class EquipmentSelectForm(FlaskForm):
    equip = StringField("equip", render_kw={'readonly': True})
    selected = BooleanField("selected")

class ListEquipmentForm(FlaskForm):
    select = FieldList(FormField(EquipmentSelectForm))

    class Meta:
        csrf = False