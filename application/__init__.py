from flask import Flask, render_template, flash
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
# Tietokanta eri herokussa ja paikallisella laitteella

import os

# observations.db niminen tietokanta.
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///observations.db"
    # Tulosta kaikki SQL-kyselyt
    app.config["SQLALCHEMY_ECHO"] = True

# db-olio.
db = SQLAlchemy(app)

# kirjautuminen
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi tätä toiminnallisuutta."

# Palautettava kun auterisointi epäonnistuu
@login_manager.unauthorized_handler
def unauth_handler():
    flash('Pääkäyttäjän toiminnallisuus!')
    return render_template("index.html")

# autorisoini

from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if (role != "ANY") and (current_user.get_urole() != role):
                unauthorized = True

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

from application import views

from application.observations import models
from application.observations import views

from application.animals import models
from application.animals import views

from application.equipments import models
from application.equipments import views

from application.auth import models
from application.auth import views


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
# Luo taulut
try :
    db.create_all()
except:
    pass