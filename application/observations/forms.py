from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, FloatField, SelectField, TextAreaField, SelectMultipleField, ValidationError
from wtforms.validators import StopValidation
# Compares the value in the given field to the validating field and raises an validationError if the given fields value is bigger than this fields value


def StopEmpty(form, field):
    if not field.data:
        field.errors[:] = []
        raise StopValidation()

class BiggerThan(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext(
                "Invalid field name '%s'.") % self.fieldname)
        if other.data is None:
            return
        if field.data > other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext(
                    'Alarajan on oltava pienempi kuin ylärajan')

            raise ValidationError(message % d)

class AddNewObservationForm(FlaskForm):
    date_observed = DateTimeField("Havainnon päivämäärä ja aika",  format='%d-%m-%Y %H:%M', validators=[
                                  validators.input_required(message="Päivämäärä ei voi olla tyhjä!")], render_kw={"placeholder": "Muodossa 14-12-2019 22:45"})
    city = StringField("Kaupunki")
    latitude = FloatField("Leveysaste", [StopEmpty, validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")], render_kw={"placeholder": "Esimerkiksi 25.439399"})
    longitude = FloatField("Pituusaste", [StopEmpty, validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")], render_kw={"placeholder": "Esimerkiksi 121.203030"})

    animal = SelectField("Eläin", validators=[validators.input_required(
        message="Eläin pitää valita!")], coerce=int)

    weight = FloatField("Paino", [StopEmpty, validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!")], render_kw={"placeholder": "Kilogrammoina"})
    sex = SelectField("Sukupuoli", choices=[(0, "Uros"), (1, "Naaras"), (2, "Muu"), (3, "Ei tiedossa")], validators=[
                      validators.input_required(message="Sukupuoli pitää valita!")], coerce=int)
    observ_type = SelectField("Havaintotapa", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Onnettomuus")], validators=[
                              validators.input_required(message="Havaintotapa pitää valita!")], coerce=int)

    equipment = SelectField("Väline",  validators=[validators.input_required(
        message="Väline pitää valita!")], coerce=int)
    info = TextAreaField("Muita tietoja", [validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")], render_kw={"placeholder": "Maksimissaan 500 merkkiä!"})

    class Meta:
        csrf = False


class ListFiltersForm(FlaskForm):
    date_observedLow = DateTimeField("Havainnon päivämäärän ja ajan ala- ja yläraja",
                                     format='%d-%m-%Y %H:%M', validators=[StopEmpty, BiggerThan('date_observedHigh')])
    date_observedHigh = DateTimeField(
        "Havainnon päivämäärän ja ajan ala- ja yläraja",  format='%d-%m-%Y %H:%M', validators=[StopEmpty])
    city = SelectMultipleField("Kaupunki")
    latitudeLow = FloatField("Leveysasteen ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!"), BiggerThan('latitudeHigh')])
    latitudeHigh = FloatField("Leveysasteen ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")])

    longitudeLow = FloatField("Pituusasteen ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!"), BiggerThan('longitudeHigh')])
    longitudeHigh = FloatField("Pituusasteen ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")])

    animal = SelectMultipleField("Eläin", coerce=int)

    weightLow = FloatField("Painon ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(min=0, message="Paino ei voi olla negatiivinen!"), BiggerThan('weightHigh')])
    weightHigh = FloatField("Painon ajan ala- ja yläraja", validators=[StopEmpty, validators.number_range(min=0, message="Paino ei voi olla negatiivinen!")])
    sex = SelectMultipleField("Sukupuoli", choices=[(0, "Uros"), (1, "Naaras"), (2, "Muu"), (3, "Ei tiedossa")], coerce=int)
    observ_type = SelectMultipleField("Havaintotapa", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto")], coerce=int)

    equipment = SelectMultipleField("Väline", coerce=int)
    info = TextAreaField("Muita tietoja", validators=[validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")])
