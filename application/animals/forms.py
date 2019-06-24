from flask_wtf import FlaskForm
from wtforms import StringField, validators

class addNewAnimalForm(FlaskForm):
    name = StringField("Nimi", [validators.input_required(message='Nimi ei voi olla tyhjä!'), validators.Regexp('^[a-zA-ZåöäÅÖÄ]*$', message='Eläimen nimessä on vain kirjaimia!')], render_kw={"placeholder": "Susi"})
    lat_name = StringField("Latinankielinen nimi", validators=[validators.Regexp('^[a-zA-Z ]*$', message='Latinankielisessä nimessä on vain latinalaisia kirjaimia!')], render_kw={"placeholder": "Canis lupus"})
    info = StringField("Lisätietoja", [validators.optional(), validators.url(message='Tiedon on oltava url-osoite')], render_kw={"placeholder": "URL-osoite. Esim. Wikipedia"})

    class Meta:
        csrf = False