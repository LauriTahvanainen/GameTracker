from application import app, db, login_required
from application.animals.models import Animal
from application.animals.forms import addNewAnimalForm
from flask import render_template, request, redirect, url_for, flash

@app.route("/animals/menu", methods=["GET"])
@login_required()
def animal_menu():
    return render_template("animals/menu.html")

@app.route("/animals/add", methods=["GET", "POST"])
@login_required()
def animal_add():
    if request.method == "GET":
        return render_template("animals/addanimal.html", form=addNewAnimalForm())

    form = addNewAnimalForm(request.form)

    if form.validate():
        newAnimal = Animal(form.name.data, form.lat_name.data, form.info.data)
        try:
            db.session().add(newAnimal)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("animals/addanimal.html", form=addNewAnimalForm(), error = "Eläin on jo järjestelmässä!")
        flash('Eläin lisätty onnistuneesti!')
        return redirect(url_for("animal_add"))
    return render_template("animals/addanimal.html", form=form)

@app.route("/animals/list", methods=["GET"])
@login_required()
def animal_list_all():
    return render_template("animals/listanimals.html", animals=Animal.query.order_by(Animal.name.asc()).all())

@app.route("/animals/edit_or_delete/<animal_id>", methods=["GET", "POST"])
@login_required(role="ADMIN")
def animal_edit_or_delete(animal_id):
    animal = Animal.query.get(animal_id)
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
            return render_template("animals/listanimals.html", animals=Animal.query.order_by(Animal.name.asc()).all(), error="Muokatessa tapahtui virhe! Eläintä ei muokattu!")
        flash("Eläintä muokattu onnistuneesti!")
        return redirect(url_for("animal_list_all"))
    return render_template("animals/editordelete.html", animal=animal, form=form)
    
@app.route("/animals/delete/<animal_id>", methods=["POST"])
@login_required(role="ADMIN")
def animal_delete(animal_id):
    try:
        Animal.query.filter_by(animal_id=animal_id).delete()
        db.session().commit()
    except:
        return render_template("animals/listanimals.html", animals=Animal.query.order_by(Animal.name.asc()).all(), error="Poistettaessa tapahtui virhe! Eläintä ei poistettu!")
    flash("Eläin poistettu onnistuneesti")
    return redirect(url_for("animal_list_all"))


    