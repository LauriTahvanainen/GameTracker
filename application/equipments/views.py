from application import app, db
from application.equipments.models import Equipment
from application.equipments.forms import addEquipmentForm, listEquipmentForm
from flask_login import login_required, current_user, login_user
from flask import render_template, request, redirect, url_for, flash
from application.equipments.forms import equipment_selectForm


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
            return render_template("equipments/addequipment.html", form=addEquipmentForm(), error="Varuste on jo järjestelmässä!")
        flash('Varuste lisätty onnistuneesti!')
        return redirect(url_for("equipment_add"))
    return render_template("equipments/addequipment.html", form=form)


@app.route("/equipments/listandremove", methods=["GET", "POST"])
@login_required
def equipment_listandremove():
    form = listEquipmentForm()
    for equipment in Equipment.query.all():
        equipmentform = equipment_selectForm()
        equipmentform.equip = equipment.name
        equipmentform.selected = False
        form.select.append_entry(equipmentform)

    if request.method == "GET":
        return render_template("equipments/list.html", form=form)

    form = listEquipmentForm(request.form)
    selected = []
    for entry in form.select.entries:
        if entry.data['selected'] == True:
            selected.append(entry.data['equip'])
    if len(selected) == 0:
        flash("Ei poistettavaksi valittuja välineitä!")
        return render_template("equipments/list.html", form=form)

    db.session().query(Equipment).filter(Equipment.name.in_(
        selected)).delete(synchronize_session='fetch')
    db.session().commit()

    flash("Valitut välineet poistettu onnistuneesti!")
    return redirect(url_for("equipment_listandremove"))
