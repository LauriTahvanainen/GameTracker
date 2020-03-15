from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateTimeField, DecimalField, SelectField, TextAreaField, SelectMultipleField, ValidationError, BooleanField
from wtforms.validators import StopValidation
from wtforms.fields.html5 import DateField
from datetime import date
from application import city_choices

# Compares the value in the given field to the validating field and raises an validationError if the given fields value is bigger than this fields value
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

class DateBetween(object):
    def __init__(self, date_min=date.min, date_max=date.today(), message=None):
        self.date_min = date_min
        self.date_max = date_max
        if not message:
            self.message = 'Havainnon päivämäärä ei voi olla tulevaisuudessa!'
        else:
            self.message = message
    
    def __call__(self, form, field):
        date = field.data

        if date > self.date_max or date < self.date_min:
            raise ValidationError(self.message)

class AddNewObservationForm(FlaskForm):
    # date_observed = DateTimeField("Havainnon päivämäärä",  format='%d-%m-%Y', validators=[
    #                               validators.input_required(message="Päivämäärä ei voi olla tyhjä!")], render_kw={"placeholder": "Muodossa 14-12-2019"},)
    date_observed = DateField("Havainnon päivämäärä", validators=[
                                  validators.input_required(message="Päivämäärä ei voi olla tyhjä!"), DateBetween()], render_kw={'max': date.today().strftime('%Y-%m-%d'), 'class': 'datepicker'}, default=date.today())
    hour = SelectField("Tunti", choices=[(0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')],
                        validators=[validators.input_required(message="Kellonaika pitää valita!")], coerce=int)
    minute = SelectField("Minuutti", choices=[(0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59')], validators=[
        validators.input_required(message="Kellonaika pitää valita!")], coerce=int)
    city = SelectField("Kunta", choices=city_choices, validators=[
        validators.input_required(message="Kunta pitää valita!")], coerce=str)
    latitude = DecimalField("Leveysaste", validators=[validators.input_required(message="Koordinaatit eivät voi olla tyhjänä!"), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")], places=6, render_kw={"placeholder": "Esimerkiksi 25.439399"})
    longitude = DecimalField("Pituusaste", validators=[validators.input_required(message="Koordinaatit eivät voi olla tyhjänä!"), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")], places=6, render_kw={"placeholder": "Esimerkiksi 121.203030"})

    animal = SelectField("Eläin", validators=[validators.input_required(
        message="Eläin pitää valita!")], coerce=int)

    weight = DecimalField("Paino", [validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!")], places=3, render_kw={"placeholder": "Kilogrammoina"})
    sex = SelectField("Sukupuoli", choices=[(0, "Ei tiedossa"),(1, "Uros"), (2, "Naaras"), (3, "Muu")], validators=[
                      validators.input_required(message="Sukupuoli pitää valita!")], coerce=int)
    observ_type = SelectField("Havaintotapa", choices=[(0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Liikenneonnettomuus"), (4, "Onnettomuus")], validators=[
                              validators.input_required(message="Havaintotapa pitää valita!")], coerce=int)

    equipment = SelectField("Väline",  validators=[validators.input_required(
        message="Väline pitää valita!")], coerce=int)
    info = TextAreaField("Muita tietoja", validators=[validators.optional(strip_whitespace=True), validators.Regexp('^[\w.?!, ]*$', message="Vain kirjaimet, numerot, piste, huuto- ja kysymysmerkki ovat sallittuja merkkejä!"), validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")], render_kw={"placeholder": "Maksimissaan 500 merkkiä!"})

    class Meta:
        csrf = False


class ListFiltersForm(FlaskForm):
    date_observed_low = DateField("Havainnon päivämäärän ja ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), BiggerThan('date_observed_high'), DateBetween()], render_kw={'max': date.today().strftime('%Y-%m-%d'), 'class': 'datepicker'})
    hour_low1 = SelectField("Tunti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    minute_low1 = SelectField("Minuutti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    date_observed_high = DateField("Havainnon päivämäärän ja ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), DateBetween()], render_kw={'max': date.today().strftime('%Y-%m-%d'), 'class': 'datepicker'})
    hour_high1 = SelectField("Tunti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    minute_high1 = SelectField("Minuutti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    hour_low2 = SelectField("Tunti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    minute_low2 = SelectField("Minuutti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    hour_high2 = SelectField("Tunti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    minute_high2 = SelectField("Minuutti", choices=[(-1, ''), (0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59')],
                        validators=[validators.optional(strip_whitespace=True)], coerce=int)
    city = SelectMultipleField("Kunta")
    latitude_low = DecimalField("Leveysasteen ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!"), BiggerThan('latitude_high')], render_kw={"placeholder": "3.554446"})
    latitude_high = DecimalField("Leveysasteen ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-90, max=90, message="Leveysasteen on oltava välillä -90.000000 ja 90.000000!")], render_kw={"placeholder": "83.456722"})

    longitude_low = DecimalField("Pituusasteen ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!"), BiggerThan('longitude_high')], render_kw={"placeholder": "-104.234224"})
    longitude_high = DecimalField("Pituusasteen ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=-180, max=180, message="Pituusasteen on oltava välillä -180.000000 ja 180.000000!")], render_kw={"placeholder": "80.224422"})

    animal = SelectMultipleField("Eläin", coerce=int)

    weight_low = DecimalField("Painon ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!"), BiggerThan('weight_high')], render_kw={"placeholder": "3"})
    weight_high = DecimalField("Painon ajan ala- ja yläraja", validators=[validators.optional(strip_whitespace=True), validators.number_range(
        min=0, message="Paino ei voi olla negatiivinen!")], render_kw={"placeholder": "50"})
    sex = SelectMultipleField("Sukupuoli", choices=[(
        0, "Uros"), (1, "Naaras"), (2, "Muu"), (3, "Ei tiedossa")], coerce=int)
    observ_type = SelectMultipleField("Havaintotapa", choices=[(
        0, "Saalis"), (1, "Näköhavainto"), (2, "Kiinniotto"), (3, "Liikenneonnettomuus"), (4, "Onnettomuus")], coerce=int)

    equipment = SelectMultipleField("Väline", coerce=int)
    info = TextAreaField("Muita tietoja", validators=[validators.optional(), validators.Regexp('^[\w.?!, ]*$', message="Vain kirjaimet, numerot ja '. ? ! , ' ovat sallittuja merkkejä!"), validators.length(
        max=500, message="Teksti on liian pitkä. Maksimissaan 500 merkkiä!")])
    username = StringField("Käyttäjänimi", [validators.optional(strip_whitespace=True),
                                            validators.Regexp(
                                                '^[a-zA-Z0-9_]*$', message='Käyttäjänimessä saa olla vain latinalaisia kirjaimia, numeroita tai alaviivoja!'),
                                            validators.Length(
                                                min=4, max=16, message='Käyttäjänimen on oltava pituudeltaan 4-16 merkkiä!')
                                            ], render_kw={"placeholder": "Min. 4, maks. 16 merkkiä"})
