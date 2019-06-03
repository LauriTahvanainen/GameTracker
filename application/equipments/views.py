from application import app, db
from application.equipments.models import Equipment
from application.equipments.forms import addEquipmentForm
from flask_login import login_required
from flask import render_template, request, redirect, url_for, flash


@app.route("/equipments/menu", methods=["GET"])
@login_required
def equipment_menu():
    return render_template("equipments/menu.html")


@app.route("/equipments/add", methods=["GET", "POST"])
@login_required
def equipment_add():
    if request.method == "GET":
        return render_template("equipments/addequipment.html", form=addEquipmentForm())

    form = addEquipmentForm(request.form)

    if form.validate():
        newEquipment = Equipment(form.name.data)
        try:
            db.session().add(newEquipment)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("equipments/addequipment.html", form=addEquipmentForm, error="Varuste on jo järjestelmässä!")
        flash('Varuste lisätty onnistuneesti!')
        return render_template("equipments/addequipment.html", form=addEquipmentForm())
    return render_template("equipments/addequipment.html", form=form)
