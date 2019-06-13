from flask_wtf import FlaskForm
from wtforms import StringField, validators

class addNewAnimalForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!')], render_kw={"placeholder": "Susi"})
    lat_name = StringField("Latinankielinen nimi", render_kw={"placeholder": "Canis lupus"})
    info = StringField("Tietoja", [validators.url(message='Tiedon on oltava url-osoite')], render_kw={"placeholder": "URL-osoite. Esim. Wikipedia"})

    class Meta:
        csrf = False