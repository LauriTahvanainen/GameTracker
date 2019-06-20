from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, DecimalField, SelectField, TextAreaField, SelectMultipleField, ValidationError
from wtforms.validators import StopValidation
# Compares the value in the given field to the validating field and raises an validationError if the given fields value is bigger than this fields value


def stopEmpty(form, field):
    if not field.data or field.data == '':
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
    city = StringField("Kaupunki", validators=[validators.Regexp('^[a-zA-ZåöäÅÖÄ]*$', message='Kaupungin nimessä on vain kirjaimia!'),
                                               validators.input_required(message="Kaupunki ei voi olla tyhjä")])
    latitude = DecimalField("Leveysaste", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")], places=6, render_kw={"placeholder": "Esimerkiksi 25.439399"})
    longitude = DecimalField("Pituusaste", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")], places=6, render_kw={"placeholder": "Esimerkiksi 121.203030"})

    animal = SelectField("Eläin", validators=[validators.input_required(
        message="Eläin pitää valita!")], coerce=int)

    weight = DecimalField("Paino", [validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!")], places=3, render_kw={"placeholder": "Kilogrammoina"})
    sex = SelectField("Sukupuoli", choices=[(0, "Uros"), (1, "Naaras"), (2, "Muu"), (3, "Ei tiedossa")], validators=[
                      validators.input_required(message="Sukupuoli pitää valita!")], coerce=int)
    observ_type = SelectField("Havaintotapa", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Onnettomuus")], validators=[
                              validators.input_required(message="Havaintotapa pitää valita!")], coerce=int)

    equipment = SelectField("Väline",  validators=[validators.input_required(
        message="Väline pitää valita!")], coerce=int)
    info = TextAreaField("Muita tietoja", validators=[validators.optional(), validators.Regexp('[\w.?!]+', message="Vain kirjaimet, numerot ja piste ovat sallittuja merkkejä!"), validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")], render_kw={"placeholder": "Maksimissaan 500 merkkiä!"})

    class Meta:
        csrf = False


class ListFiltersForm(FlaskForm):
    date_observedLow = DateTimeField("Havainnon päivämäärän ja ajan ala- ja yläraja",
                                     format='%d-%m-%Y %H:%M', validators=[stopEmpty, BiggerThan('date_observedHigh')], render_kw={"placeholder": "12-03-2005 12:00"})
    date_observedHigh = DateTimeField(
        "Havainnon päivämäärän ja ajan ala- ja yläraja",  format='%d-%m-%Y %H:%M', validators=[stopEmpty], render_kw={"placeholder": "01-01-2010 12:00"})
    city = SelectMultipleField("Kaupunki")
    latitudeLow = DecimalField("Leveysasteen ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!"), BiggerThan('latitudeHigh')], render_kw={"placeholder": "3.554446"})
    latitudeHigh = DecimalField("Leveysasteen ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")], render_kw={"placeholder": "83.456722"})

    longitudeLow = DecimalField("Pituusasteen ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!"), BiggerThan('longitudeHigh')], render_kw={"placeholder": "-104.234224"})
    longitudeHigh = DecimalField("Pituusasteen ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")], render_kw={"placeholder": "80.224422"})

    animal = SelectMultipleField("Eläin", coerce=int)

    weightLow = DecimalField("Painon ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!"), BiggerThan('weightHigh')], render_kw={"placeholder": "3"})
    weightHigh = DecimalField("Painon ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!")], render_kw={"placeholder": "50"})
    sex = SelectMultipleField("Sukupuoli", choices=[(
        0, "Uros"), (1, "Naaras"), (2, "Muu"), (3, "Ei tiedossa")], coerce=int)
    observ_type = SelectMultipleField("Havaintotapa", choices=[(
        0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Onnettomuus")], coerce=int)

    equipment = SelectMultipleField("Väline", coerce=int)
    info = TextAreaField("Muita tietoja", validators=[validators.optional(), validators.Regexp('[\w.?!]+', message="Vain kirjaimet, numerot ja '. ? ! , ' ovat sallittuja merkkejä!"), validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")])
    username = StringField("Käyttäjänimi", [stopEmpty,
                                            validators.Regexp(
                                                '^[a-zA-Z0-9_]*$', message='Käyttäjänimessä saa olla vain aakkosia, numeroita tai alaviivoja!'),
                                            validators.Length(
                                                min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!')
                                            ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})
