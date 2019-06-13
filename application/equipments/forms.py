from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, FormField, FieldList
from wtforms.form import BaseForm, Form
from application.equipments.models import Equipment


class addEquipmentForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(
        message='Nimi ei voi olla tyhjä!')])

    class Meta:
        csrf = False

def form_for_select(fields):
    def create_form(prefix='', **kwargs):
        form = BaseForm(fields, prefix='')
        form.process(**kwargs)
        return form
    return create_form

# list and remove view
class equipmentSelectForm(FlaskForm):
    equip = StringField("equip", render_kw={'readonly': True})
    selected = BooleanField("selected")

class listEquipmentForm(FlaskForm):
    select = FieldList(FormField(equipmentSelectForm))

    class Meta:
        csrf = False