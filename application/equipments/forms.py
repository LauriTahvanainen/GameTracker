from flask_wtf import FlaskForm
from wtforms import StringField, validators, BooleanField, FormField
from wtforms.form import BaseForm, Form
from application.equipments.models import Equipment

class addEquipmentForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!')])

    class Meta:
        csrf = False

def form_for_select(fields):
    def create_form(prefix='', **kwargs):
        form = BaseForm(fields, prefix='')
        form.process(**kwargs)
        return form
    return create_form

class listEquipmentForm(FlaskForm):
    results = Equipment.query.all()
       
    list_equipment = FormField(
        form_for_select(
            [(equipment.name, BooleanField(equipment.name)) for equipment in results]
        )
    )

    class Meta:
        csrf = False