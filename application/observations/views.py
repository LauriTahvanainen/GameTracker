from application import app, db
from application.observations.models import Observation
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
    if request.method == "GET":
        return render_template("observations/addobservation.html", form=addNewObservationForm())

    form = addNewObservationForm(request.form)

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
