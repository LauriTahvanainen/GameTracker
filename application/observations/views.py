from application import app, db, login_required
from application.observations.models import Observation
from application.animals.models import Animal
from application.equipments.models import Equipment
from application.auth.models import User
from application.observations.forms import AddNewObservationForm, ListFiltersForm
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash
from datetime import date, time, datetime
from flask import jsonify
import traceback


@app.route("/observations/menu", methods=["GET"])
@login_required()
def observation_menu():
    return render_template("observations/menu.html")

# TODO certain types of equipment should not be possible to select to an observation with a specific type.
# TODO Check if animal is a suggestion.
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
        date_observed = form.date_observed.data
        time_observed = time(form.hour.data, form.minute.data)
        datetime_observed = datetime.combine(date_observed, time_observed)
        equipment = Equipment.query.get(form.equipment.data)
        if not equipment.get_allowed_value_by_index(form.observ_type.data):
            flash("Tapahtui virhe, valittua välinettä ei voi valita valitun havaintotyypin kanssa!", "error")
            return render_template("observations/addobservation.html", form=form)
        new_obs = Observation(current_user.account_id,
                             date_observed, time_observed,
                             datetime_observed,
                             form.city.data, form.latitude.data,
                             form.longitude.data, form.animal.data,
                             form.weight.data, form.sex.data,
                             form.observ_type.data,
                             form.equipment.data,
                             form.info.data)
        try:
            db.session().add(new_obs)
            db.session().commit()
        except Exception:
            db.session().rollback()
            form = AddNewObservationForm()
            form = fill_choices(form)
            flash("Tapahtui virhe, havaintoa ei lisätty!", "error")
            return render_template("observations/addobservation.html", form=form)
        flash('Havainto lisätty onnistuneesti!', "info")
        return redirect(url_for('observation_add'))
    return render_template("observations/addobservation.html", form=form)

#TODO Fetch all observation information for the table and the map with one request to the database.
@app.route("/observations/list/user", methods=["GET", "POST"])
@login_required()
def observation_listuser():
    # The ajax request that fills the map on a page with observations also uses this function.
    # The same function is used bećause the data in the filter form is necessary, and because the function can be tailored for the ajax request
    # with a simple parameter. The page parameter is used as the parameter. The function knows that the request is an ajax request, when the parameter page is 0.
    # The observations fetched in case of the ajax request are fetched by exactly the same function, that the normal request use: "Observation.list_filtered(form, page, user_id)"
    # In case of the ajax request, the fetched observations are jsonified and returned.

    # The changing of pages with filters is now done with a post request. 
    # A pagenumber button sends a new post request to the server with the current filter form.
    page = request.args.get('page', 1, type=int)

    if request.method == "GET":
        form = ListFiltersForm()
        form = fill_choices_with_cities(form, current_user.account_id)
        if page == 0:
            form = ListFiltersForm(request.form)
            form = fill_choices_with_cities(form, current_user.account_id)
            observations = Observation.list_filtered(
                form, 0, current_user.account_id)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        else:
            pagination = Observation.list_filtered(
                form, page, current_user.account_id)
        return render_template("observations/listuser.html", form=form, pagination=pagination)

    # filtering
    form = ListFiltersForm(request.form)
    form = fill_choices_with_cities(form, current_user.account_id)
    if form.validate():
        if page == 0:
            observations = Observation.list_filtered(
                form, 0, current_user.account_id)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        pagination = Observation.list_filtered(
            form, page, current_user.account_id)
        return render_template("observations/listuser.html", form=form, pagination=pagination)
    flash("Virhe rajaussyötteissä! Näytetään kaikki käyttäjän havainnot!", "warning")
    return render_template("observations/listuser.html", form=form, pagination=pagination)


@app.route("/observations/list/<user_id>", methods=["GET", "POST"])
@login_required()
def observation_list_by_id(user_id):
    # The ajax request that fills the map on a page with observations also uses this function.
    # The same function is used bećause the data in the filter form is necessary, and because the function can be tailored for the ajax request
    # with a simple parameter. The page parameter is used as the parameter. The function knows that the request is an ajax request, when the parameter page is 0.
    # The observations fetched in case of the ajax request are fetched by exactly the same function, that the normal request use: "Observation.list_filtered(form, page, user_id)"
    # In case of the ajax request, the fetched observations are jsonified and returned.

    # The changing of pages with filters is now done with a post request. 
    # A pagenumber button sends a new post request to the server with the current filter form.
    page = request.args.get('page', 1, type=int)
    account = User.query.get(user_id)
    if account is None:
        flash("Virheellinen osoite!", "error")
        return redirect(url_for("index"))
    obs_count = Observation.count_observations_on_user(user_id)
    if request.method == "GET":
        form = ListFiltersForm()
        form = fill_choices_with_cities(form, user_id)
        if page == 0:
            observations = Observation.list_filtered(form, 0, user_id)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        else:
            pagination = Observation.list_filtered(form, page, user_id)
        return render_template("observations/listobsbyid.html", form=form, pagination=pagination, account=account, obs_count=obs_count)

    form = ListFiltersForm(request.form)
    form = fill_choices_with_cities(form, user_id)
    if form.validate():
        if page == 0:
            observations = Observation.list_filtered(
                form, 0, user_id)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        pagination = Observation.list_filtered(form, page, user_id)
        return render_template("observations/listobsbyid.html", form=form, pagination=pagination, account=account, obs_count=obs_count)
    flash("Virhe rajaussyötteissä! Näytetään kaikki käyttäjän havainnot!", "warning")
    return render_template("observations/listobsbyid.html", form=form, pagination=pagination, account=account, obs_count=obs_count)


@app.route("/observations/list/all", methods=["GET", "POST"])
@login_required()
def observation_list_all():
    # The ajax request that fills the map on a page with observations also uses this function.
    # The same function is used bećause the data in the filter form is necessary, and because the function can be tailored for the ajax request
    # with a simple parameter. The page parameter is used as the parameter. The function knows that the request is an ajax request, when the parameter page is 0.
    # The observations fetched in case of the ajax request are fetched by exactly the same function, that the normal request use: "Observation.list_filtered(form, page, user_id)"
    # In case of the ajax request, the fetched observations are jsonified and returned.

    # The changing of pages with filters is now done with a post request. 
    # A pagenumber button sends a new post request to the server with the current filter form.
    page = request.args.get('page', 1, type=int)

    if request.method == "GET":
        form = ListFiltersForm()
        form = fill_choices_with_cities(form)
        if page == 0:
            observations = Observation.list_filtered(form, 0)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        else:
            pagination = Observation.list_filtered(form, page)
        return render_template("observations/listall.html", form=form, pagination=pagination)

    form = ListFiltersForm(request.form)
    form = fill_choices_with_cities(form)
    if form.validate():
        if page == 0:
            observations = Observation.list_filtered(form, 0)
            marker_data = jsonify(serialize(observations.all()))
            return marker_data
        pagination = Observation.list_filtered(form, page)
        return render_template("observations/listall.html", form=form, pagination=pagination)
    flash("Virhe rajaussyötteissä! Näytetään kaikki havainnot!", "warning")
    return render_template("observations/listall.html", form=form, pagination=pagination)


@app.route("/observations/delete/<obs_id>", methods=["POST", "GET"])
@login_required()
def observation_delete(obs_id):
    obs = Observation.query.get(obs_id)
    if obs is None:
        flash("Virheellinen osoite!", "error")
        return redirect(url_for('index'))
    last_path = request.args.get('last_path', None)
    if obs.account_id == current_user.account_id or current_user.urole == "ADMIN":
        try:
            db.session().delete(obs)
            db.session().commit()
        except:
            db.session().rollback()
            flash("Poistettaessa tapahtui virhe! Havaintoa ei poistettu", "error")
            return redirect(last_path)
        flash("Havainto poistettu onnistuneesti!", "info")
        return redirect(last_path)
    flash("Sinulla ei ole oikeuksia poistaa kyseistä havaintoa!", "error")
    if (last_path is None):
        return redirect(url_for('index'))
    return redirect(last_path)

# TODO Check if the observation has not changed, so that the database will not be under too much stress
# TODO Datetime observed can not be edited to be too much further in time.
@app.route("/observations/edit/<obs_id>", methods=["POST", "GET"])
@login_required()
def observation_edit(obs_id):
    obs = Observation.query.get(obs_id)
    obs_username = User.query.get(obs.account_id).username
    if obs is None:
        flash("Virheellinen osoite!", "error")
        return redirect(url_for('index'))
    last_path = request.args.get('last_path', None)
    if obs.account_id == current_user.account_id or current_user.urole == "ADMIN":
        if request.method == "GET":
            form = AddNewObservationForm()
            form = fill_choices(form)
            form.animal.data = obs.animal_id
            form.date_observed.data = obs.date_observed
            form.hour.data = obs.time_observed.hour
            form.minute.data = obs.time_observed.minute
            form.city.data = obs.city
            form.latitude.data = obs.latitude
            form.longitude.data = obs.longitude
            form.weight.data = obs.weight
            form.sex.data = obs.sex
            form.observ_type.data = obs.observ_type
            form.equipment.data = obs.equipment_id
            form.info.data = obs.info
            return render_template("observations/editobservation.html", form=form, observation=obs, last_path=last_path, obs_username=obs_username)

        form = AddNewObservationForm(request.form)
        form = fill_choices(form)
        if form.validate():
            date_observed = form.date_observed.data
            time_observed = time(form.hour.data, form.minute.data)
            datetime_observed = datetime.combine(date_observed, time_observed)
            try:
                obs.animal_id = form.animal.data
                obs.date_observed = date_observed
                obs.time_observed = time_observed
                obs.date_observed = datetime_observed
                obs.city = form.city.data
                obs.latitude = form.latitude.data
                obs.longitude = form.longitude.data
                obs.weight = form.weight.data
                obs.sex = form.sex.data
                obs.observ_type = form.observ_type.data
                obs.equipment_id = form.equipment.data
                obs.info = form.info.data
                db.session().commit()
            except Exception:
                flash("Muokatessa tapahtui virhe! Havaintoa ei muokattu", "error")
                return redirect(last_path)
            flash("Havaintoa muokattu onnistuneesti!", "info")
            return redirect(last_path)
        return render_template("observations/editobservation.html", form=form, observation=obs, last_path=last_path,  obs_username=obs_username)
    if (last_path is None):
        return redirect(url_for('index'))
    flash("Sinulla ei ole oikeuksia muokata kyseistä havaintoa!", "error")
    return redirect(last_path)


@app.route("/observations/stats", methods=["GET"])
@login_required()
def observation_stats():
    return render_template("observations/statistics.html",
                           top_users=Observation.list_top_users(),
                           users_no_obs=Observation.list_users_without_observations(),
                           top_animals=Observation.list_top_animals(),
                           bottom_animals=Observation.list_bottom_animals(),
                           top_equipments=Observation.list_top_equipment(),
                           bottom_equipments=Observation.list_bottom_equipment(),
                           most_hunted=Observation.list_most_hunted_animals())


def fill_choices(form, acc_id=-1):
    if acc_id == -1:
        form.equipment.choices = [(equipment.equipment_id, equipment.name)
                                  for equipment in Equipment.query.order_by(Equipment.name.asc()).all()]
        form.animal.choices = [(animal.animal_id, animal.name)
                               for animal in Animal.query.filter(Animal.suggestion_flag == False).order_by(Animal.name.asc()).all()]
    else:
        form.equipment.choices = [(equipment.equipment_id, equipment.name) for equipment in Equipment.query.outerjoin(
            Observation).filter(Observation.account_id == acc_id).order_by(Equipment.name.asc()).distinct()]
        form.animal.choices = [(animal.animal_id, animal.name) for animal in Animal.query.outerjoin(
            Observation).filter(Observation.account_id == acc_id).order_by(Animal.name.asc()).distinct()]
    return form


def fill_choices_with_cities(form, acc_id=-1):
    if acc_id == -1:
        form.city.choices = [(city[0], city[0]) for city in db.session.query(
            Observation.city).order_by(Observation.city.asc()).distinct()]
    else:
        form.city.choices = [(city[0], city[0]) for city in db.session.query(Observation.city).filter(
            Observation.account_id == acc_id).order_by(Observation.city.asc()).distinct()]
    return fill_choices(form, acc_id)


def serialize(observations):
    # (<Observation 93>, <Animal 3>, 'test', <User 1>)
    array = []
    for observation in observations:
        array.append({
            'observation': {
                'observation_id': observation[0].observation_id,
                'date_observed': observation[0].date_observed.strftime("%d-%m-%Y"),
                'time_observed': observation[0].time_observed.strftime("%M:%S"),
                'city': observation[0].city,
                'latitude': str(observation[0].latitude),
                'longitude': str(observation[0].longitude),
                'weight': parseWeight(observation[0].weight),
                "sex": parseSex(observation[0].sex),
                'observ_type': parseObsType(observation[0].observ_type),
                'info': parseInfo(observation[0].info)
            },
            'animal': {
                'animal_id': observation[1].animal_id,
                'name': observation[1].name,
                'lat_name': observation[1].lat_name,
                'info': parseAnimalInfo(observation[1].info, observation[1].animal_id)
            },
            'equipment': observation[2],
            'observer': observation[3].username,
            'observer_id': observation[3].account_id
        })
    return array


def parseObsType(value):
    if value == 0:
        return "Saalis"
    elif value == "1":
        return "Näköhavainto"
    elif value == "2":
        return "Kiinniotto"
    return "Onnettomuus"


def parseWeight(value):
    if not value:
        return "Ei annettu!"
    else:
        return "{0:.3f}".format(value) + " Kg"


def parseInfo(value):
    if not value:
        return "Ei annettu!"
    else:
        return value


def parseSex(value):
    if value == 1:
        return "Uros"
    elif value == 2:
        return "Naaras"
    elif value == 3:
        return "Muu"
    return "Ei tiedossa!"


def parseAnimalInfo(value, id):
    if value == None or value == "":
        return "/animals/edit_or_delete/" + str(id)
    return value


# For filling the filter form with values given by the url. Was used with pagination but now page switch with filters is handled by post requests.
# def fill_filter_data(form, args):
#     form.username.data = args.get('username', type=str)
#     # datetimes are not passed in the right format as a parameter,
#     # so they have to be formatted first
#     if 'dateObservedLow' in args.keys():
#         date_observed_low = args['dateObservedLow']
#         date_observed_low = datetime.strptime(
#             date_observed_low, '%Y-%m-%d').date()
#         form.date_observed_low.data = date_observed_low

#     if 'dateObservedHigh' in args.keys():
#         date_observed_high = args['dateObservedHigh']
#         date_observed_high = datetime.strptime(
#             date_observed_high, '%Y-%m-%d').date()
#         form.date_observed_high.data = date_observed_high
#     form.hour_high1.data = args.get('hour_high1')
#     form.hour_high2.data = args.get('hour_high2')
#     form.hour_low1.data = args.get('hour_low1')
#     form.hour_low2.data = args.get('hour_low2')
#     form.minute_low1.data = args.get('minute_low1')
#     form.minute_low2.data = args.get('minute_low2')
#     form.minute_high1.data = args.get('minute_high1')
#     form.minute_high2.data = args.get('minute_high2')
#     form.city.data = args.getlist('city')
#     form.latitude_low.data = args.get('latitude_low', type=float)
#     form.latitude_high.data = args.get('latitude_high', type=float)
#     form.longitude_low.data = args.get('longitude_low', type=float)
#     form.longitude_high.data = args.get('longitude_high', type=float)
#     form.animal.data = args.getlist('animal')
#     form.weight_low.data = args.get('weight_low', type=float)
#     form.weight_high.data = args.get('weight_high', type=float)
#     form.sex.data = args.getlist('sex')
#     form.observ_type.data = args.getlist('observ_type')
#     form.equipment.data = args.getlist('equipment')
#     form.info.data = args.get('info', type=str)
#     return form
