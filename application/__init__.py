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
from application.auth import views

# kirjautuminen
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toiminnallisuutta."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
# Luo taulut
db.create_all()
