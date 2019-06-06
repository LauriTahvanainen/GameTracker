from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, FloatField, SelectField, TextAreaField

class addNewObservationForm(FlaskForm):
    date_observed = DateTimeField("Havainnon päivämäärä ja aika",  format='%d-%m-%Y %H:%M', validators=[validators.input_required(message="Päivämäärä ei voi olla tyhjä!")])
    city = StringField("Kaupunki")
    latitude = FloatField("Leveysaste", [validators.number_range(min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")])
    longitude = FloatField("Pituusaste", [validators.number_range(min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")])

    # animalChoices = [(animal.animal_id, animal.name) for animal in Animal.query.all()]
    animal = SelectField("Eläin", validators = [validators.input_required(message="Eläin pitää valita!")], coerce=int)

    weight = FloatField("Paino", [validators.number_range(min=0, message="Paino ei voi olla negatiivinen!")])
    sex = SelectField("Sukupuoli", choices=[(0, "Uros"), (1, "Naaras"), (2 ,"Muu"), (3, "Ei tiedossa")], validators=[validators.input_required(message="Sukupuoli pitää valita!")], coerce=int)
    observ_type = SelectField("Havaintotapa", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto")], validators=[validators.input_required(message="Havaintotapa pitää valita!")], coerce=int)

    # equipChoices = [(equipment.equipment_id, equipment.name) for equipment in Equipment.query.all()]
    equipment = SelectField("Väline",  validators = [validators.input_required(message="Väline pitää valita!")], coerce=int)
    info = TextAreaField("Muita tietoja", [validators.length(max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")])

    class Meta:
        csrf = False