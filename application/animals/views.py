from application import app, db
from application.animals.models import Animal
from application.animals.forms import addNewAnimalForm
from flask_login import login_required
from flask import render_template, request, redirect, url_for, flash

@app.route("/animals/menu", methods=["GET"])
@login_required
def animal_menu():
    return render_template("animals/menu.html")

@app.route("/animals/add", methods=["GET", "POST"])
@login_required
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