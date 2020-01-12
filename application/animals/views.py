from application import app, db, login_required
from application.animals.models import Animal
from application.animals.models import Animal
from application.votes.models import Vote
from application.observations.models import Observation
from application.auth.models import User
from application.animals.forms import addNewAnimalForm
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user


@app.route("/animals/menu", methods=["GET"])
@login_required()
def animal_menu():
    return render_template("animals/menu.html")


@app.route("/animals/add", methods=["GET", "POST"])
@login_required(role="ADMIN")
def animal_add():
    if request.method == "GET":
        return render_template("animals/addanimal.html", form=addNewAnimalForm())

    form = addNewAnimalForm(request.form)

    if form.validate():
        if form.lat_name.data == "":
            lat_name = None
        else:
            lat_name = form.lat_name.data
        newAnimal = Animal(form.name.data, lat_name, form.info.data, False, False, current_user.account_id)
        try:
            db.session().add(newAnimal)
            db.session().commit()
        except Exception:
            db.session().rollback()
            flash("Eläimen nimi tai latinankielinen nimi on jo järjestelmässä!", "error")
            return render_template("animals/addanimal.html", form=addNewAnimalForm())
        flash('Eläin lisätty onnistuneesti!', "info")
        return redirect(url_for("animal_add"))
    return render_template("animals/addanimal.html", form=form)


@app.route("/animals/list", methods=["GET"])
@login_required()
def animal_list_all():
    page = request.args.get('page', 1, type=int)
    return render_template("animals/listanimals.html", animals=Animal.query.filter(Animal.suggestion_flag == False).order_by(Animal.name.asc()).paginate(page, 10, False))


@app.route("/animals/edit_or_delete/<animal_id>", methods=["GET", "POST"])
@login_required(role="ADMIN")
def animal_edit_or_delete(animal_id):
    animal = Animal.query.get(animal_id)
    if animal is None:
        flash("Virheellinen osoite!", "error")
        return redirect(url_for("index"))
    if request.method == "GET":
        form = addNewAnimalForm()
        form.name.data = animal.name
        form.lat_name.data = animal.lat_name
        form.info.data = animal.info
        return render_template("animals/editordelete.html", animal=animal, form=form)

    form = addNewAnimalForm(request.form)
    if form.validate():
        try:
            animal = Animal.query.get(animal_id)
            animal.name = form.name.data
            animal.lat_name = form.lat_name.data
            animal.info = form.info.data
            db.session().commit()
        except:
            db.session().rollback()
            flash(
                "Eläimen nimi tai latinankielinen nimi on jo järjestelmässä! Eläintä ei muokattu!", "error")
            return render_template("animals/editordelete.html", animal=animal, form=form)
        flash("Eläintä muokattu onnistuneesti!", "info")
        return redirect(url_for("animal_list_all"))
    return render_template("animals/editordelete.html", animal=animal, form=form)


@app.route("/animals/delete/<animal_id>", methods=["POST"])
@login_required(role="ADMIN")
def animal_delete(animal_id):
    try:
        # Could not get cascade working so deleting observations separately
        Observation.query.filter_by(animal_id=animal_id).delete()
        Animal.query.filter_by(animal_id=animal_id).delete()
        db.session().commit()
    except:
        flash("Poistettaessa tapahtui virhe! Eläintä ei poistettu!", "error")
        return render_template("animals/listanimals.html", animals=Animal.query.order_by(Animal.name.asc()).all())
    flash("Eläin poistettu onnistuneesti", "info")
    return redirect(url_for("animal_list_all"))


@app.route("/animals/suggest", methods=["GET", "POST"])
@login_required()
def animal_suggest():
    if request.method == "GET":
        return render_template("animals/suggestanimal.html", form=addNewAnimalForm())

    form = addNewAnimalForm(request.form)

    if form.validate():
        if (db.session().query(Animal.animal_id).filter(Animal.suggestion_flag == True).count() < 500):
            if form.lat_name.data == "":
                lat_name = None
            else:
                lat_name = form.lat_name.data
            newAnimalSuggestion = Animal(
                form.name.data, lat_name, form.info.data, True, True, current_user.account_id)
            try:
                db.session().add(newAnimalSuggestion)
                db.session().commit()
            except Exception:
                db.session().rollback()
                flash(
                    "Eläimen nimi tai latinankielinen nimi on jo järjestelmässä!", "error")
                return render_template("animals/suggestanimal.html", form=addNewAnimalForm())
            flash('Eläimen lisäämistä ehdotettu onnistuneesti!', "info")
            return redirect(url_for("animal_suggest"))
        flash("Ehdotusten määrän raja (500) on täyttynyt. Ehdotusta ei lisätty! Yritä myöhemmin!")
        return redirect(url_for("animal_suggest"))
    return render_template("animals/suggestanimal.html", form=form)


@app.route("/animals/list_suggested", methods=["GET"])
@login_required()
def animal_list_suggested():
    page = request.args.get('page', 1, type=int)
    return render_template("animals/listsuggestedanimals.html", animals=Animal.query.filter(Animal.suggestion_flag == True).paginate(page, 10, False))


@app.route("/animals/delete_suggestion/<suggestion_id>", methods=["GET","POST"])
@login_required()
def animal_delete_suggestion(suggestion_id):
    try:
        suggestedAnimal = Animal.query.get(suggestion_id)
        if suggestedAnimal.account_id != current_user.account_id and current_user.get_urole() != "ADMIN":
            flash("Sinulla ei ole käyttöoikeuksia kyseiseen toimintoon!", "error")
            return redirect(url_for("index"))
        suggestion_owner = User.query.get(suggestedAnimal.account_id)
        if suggestion_owner is not None:
            suggestion_owner.suggestions_deleted = suggestion_owner.suggestions_deleted + 1
        Vote.query.filter(Vote.animal_id == suggestedAnimal.animal_id).delete()
        db.session.delete(suggestedAnimal)
        db.session.commit()
    except:
        db.session.rollback()
        flash("Poistettaessa tapahtui virhe! Ehdotettua eläintä ei poistettu!", "error")
        return render_template("animals/listsuggestedanimals.html", animals=Animal.query.filter(Animal.suggestion_flag == True).paginate(1, 10, False))
    flash("Ehdotus poistettu onnistuneesti", "info")
    return redirect(url_for("animal_list_suggested"))


@app.route("/animals/edit_suggestion/<suggestion_id>", methods=["GET", "POST"])
@login_required()
def animal_edit_suggestion(suggestion_id):
    suggestedAnimal = Animal.query.get(suggestion_id)
    if suggestedAnimal is None:
        flash("Virheellinen osoite!", "error")
        return redirect(url_for("index"))
    if suggestedAnimal.account_id != current_user.account_id and current_user.get_urole() != "ADMIN":
        flash("Sinulla ei ole käyttöoikeuksia kyseiseen toimintoon!", "error")
        return redirect(url_for("index"))
    if request.method == "GET":
        form = addNewAnimalForm()
        form.name.data = suggestedAnimal.name
        form.lat_name.data = suggestedAnimal.lat_name
        form.info.data = suggestedAnimal.info
        return render_template("animals/editsuggestion.html", animal=suggestedAnimal, form=form)

    form = addNewAnimalForm(request.form)
    if form.validate():
        try:
            # suggestedAnimal = Animal.query.get(suggestion_id)
            suggestedAnimal.name = form.name.data
            suggestedAnimal.lat_name = form.lat_name.data
            suggestedAnimal.info = form.info.data
            db.session().commit()
        except:
            db.session().rollback()
            flash("Eläimen nimi tai latinankielinen nimi on jo järjestelmässä! Eläintä ei muokattu!", "error")
            return render_template("animals/editsuggestion.html", animal=suggestedAnimal, form=form)
        flash("Eläintä muokattu onnistuneesti!", "info")
        return redirect(url_for("animal_list_suggested"))
    return render_template("animals/editsuggestion.html", animal=suggestedAnimal, form=form)

@app.route("/animals/accept_suggestion/<suggestion_id>", methods=["GET","POST"])
@login_required(role="ADMIN")
def animal_accept_suggestion(suggestion_id):
    try:
        suggestedAnimal = Animal.query.get(suggestion_id)
        suggestedAnimal.suggestion_flag = 0
        suggestion_owner = User.query.get(suggestedAnimal.account_id)
        if suggestion_owner is not None:
            suggestion_owner.suggestions_accepted = suggestion_owner.suggestions_accepted + 1
        Vote.query.filter(Vote.animal_id == suggestedAnimal.animal_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        flash("Virheellinen osoite!", "error")
        return(redirect(url_for("index")))
    flash("Ehdotus hyväksytty onnistuneesti!", "info")
    return redirect(url_for("animal_list_suggested"))
