from application import app, db
from application.observations.models import Observation
from application.animals.models import Animal
from application.equipments.models import Equipment
from application.observations.forms import addNewObservationForm
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash


@app.route("/observations/menu", methods=["GET"])
@login_required
def observation_menu():
    return render_template("observations/menu.html")


@app.route("/observations/add", methods=["GET", "POST"])
@login_required
def observation_add():
    form = addNewObservationForm()
    form.animal.choices = [(animal.animal_id, animal.name) for animal in Animal.query.all()]
    form.equipment.choices = [(equipment.equipment_id, equipment.name) for equipment in Equipment.query.all()]

    if request.method == "GET":
        return render_template("observations/addobservation.html", form=form)

    form = addNewObservationForm(request.form)
    form.animal.choices = [(animal.animal_id, animal.name) for animal in Animal.query.all()]
    form.equipment.choices = [(equipment.equipment_id, equipment.name) for equipment in Equipment.query.all()]
    if form.validate():
        newObs = Observation(current_user.account_id, 
                form.date_observed.data, 
                form.city.data, form.latitude.data, 
                form.longitude.data, form.animal.data, 
                form.weight.data, form.sex.data, 
                form.observ_type.data, 
                form.equipment.data, 
                form.info.data)
        try:
            db.session().add(newObs)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("observations/addobservation.html", form=addNewObservationForm(), error = "Tapahtui virhe, havaintoa ei lisätty!")
        flash('Havainto lisätty onnistuneesti!')
        return redirect(url_for('observation_add'))
    return render_template("observations/addobservation.html", form=form)


@app.route("/observations/listuser", methods=["GET"])
@login_required
def observation_listuser():
    return render_template("observations/listuser.html", observations=Observation.list_users_own_observations_by_observ_date())