from application import app, db, login_required
from application.observations.models import Observation
from application.animals.models import Animal
from application.equipments.models import Equipment
from application.auth.models import User
from application.observations.forms import AddNewObservationForm, ListFiltersForm
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash


@app.route("/observations/menu", methods=["GET"])
@login_required()
def observation_menu():
    return render_template("observations/menu.html")


@app.route("/observations/add", methods=["GET", "POST"])
@login_required()
def observation_add():
    form = AddNewObservationForm()
    form = fill_choices(form)

    if request.method == "GET":
        return render_template("observations/addobservation.html", form=form)

    form = AddNewObservationForm(request.form)
    form = fill_choices(form)

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
            form = AddNewObservationForm()
            form = fill_choices(form)
            return render_template("observations/addobservation.html", form=form, error="Tapahtui virhe, havaintoa ei lisätty!")
        flash('Havainto lisätty onnistuneesti!')
        return redirect(url_for('observation_add'))
    return render_template("observations/addobservation.html", form=form)


@app.route("/observations/listuser", methods=["GET", "POST"])
@login_required()
def observation_listuser():
    form = ListFiltersForm()
    form = fill_choices_by_id(form, current_user.account_id)
    observations = Observation.list_users_own_observations_by_observ_date()
    if request.method == "GET":
        return render_template("observations/listuser.html", form=form, observations=observations)
    
    # filtering
    form = ListFiltersForm(request.form)
    form = fill_choices_by_id(form, current_user.account_id)
    if form.validate():
        observations = Observation.list_filtered(form, current_user.account_id)
        return render_template("observations/listuser.html", form=form, observations=observations)
    return render_template("observations/listuser.html", form=form, observations=observations, error="Virhe rajaussyötteissä! Näytetään kaikki käyttäjän havainnot!")

@app.route("/observations/list/<user_id>", methods=["GET", "POST"])
@login_required()
def observation_list_by_id(user_id):
    account = User.query.get(user_id)
    form = ListFiltersForm()
    form = fill_choices_by_id(form, user_id)
    observations = Observation.list_filtered(form, user_id)
    if request.method == "GET":
        return render_template("observations/listobsbyid.html", form=form, observations=observations, account = account)

    form = ListFiltersForm(request.form)
    form = fill_choices_by_id(form, user_id)
    if form.validate():
        observations = Observation.list_filtered(form, user_id)
        return render_template("observations/listobsbyid.html", form=form, observations=observations, account = account)
    return render_template("observations/listobsbyid.html", form=form, observations=observations, account = account, error="Virhe rajaussyötteissä! Näytetään kaikki käyttäjän havainnot!")

@app.route("/observations/list/all", methods=["GET", "POST"])
@login_required()
def observation_list_all():
    form = ListFiltersForm()
    form = fill_choices_by_id(form)
    observations = Observation.list_filtered(form)
    if request.method == "GET":
        return render_template("observations/listall.html", form=form, observations=observations)

    form = ListFiltersForm(request.form)
    form = fill_choices_by_id(form)
    if form.validate():
        observations = Observation.list_filtered(form)
        return render_template("observations/listall.html", form=form, observations=observations)
    return render_template("observations/listall.html", form=form, observations=observations, error="Virhe rajaussyötteissä! Näytetään kaikki käyttäjän havainnot!")

@app.route("/observations/delete/<obs_id>", methods=["POST", "GET"])
@login_required()
def observation_delete(obs_id):
    obs = Observation.query.get(obs_id)
    last_path = request.args.get('last_path', None)
    if obs.account_id == current_user.account_id or current_user.urole == "ADMIN":
        try:
            db.session().delete(obs)
            db.session().commit()
        except:
            db.session().rollback()
            flash("Poistettaessa tapahtui virhe! Havaintoa ei poistettu")
            return redirect(last_path)
        flash("Havainto poistettu onnistuneesti!")
        return redirect(last_path)
    flash("Sinulla ei ole oikeuksia poistaa kyseistä havaintoa!")
    return redirect(last_path)

def fill_choices_by_id(form, acc_id=-1):
    form = fill_choices(form)
    if acc_id == -1:
        form.city.choices = [(city[0], city[0]) for city in db.session.query(Observation.city).order_by(Observation.city.asc()).distinct()]
    else:
        form.city.choices = [(city[0], city[0]) for city in db.session.query(Observation.city).filter(Observation.account_id == acc_id).order_by(Observation.city.asc()).distinct()]
    return form

def fill_choices(form):
    form.animal.choices = [(animal.animal_id, animal.name) for animal in Animal.query.order_by(Animal.name.asc()).all()]
    form.equipment.choices = [(equipment.equipment_id, equipment.name) for equipment in Equipment.query.order_by(Equipment.name.asc()).all()]
    return form
