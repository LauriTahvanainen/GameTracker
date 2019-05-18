from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
# observations.db niminen tietokanta.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///observations.db"
# Tulosta kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True

# db-olio.
db = SQLAlchemy(app)

from application import views

from application.observations import models

from application.animals import models

from application.equipments import models

from application.auth import models

# Luo taulut
db.create_all()
