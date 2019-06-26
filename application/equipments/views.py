from application import app, db, login_required
from application.equipments.models import Equipment
from application.equipments.forms import addEquipmentForm, listEquipmentForm
from flask_login import current_user
from flask import render_template, request, redirect, url_for, flash
from application.equipments.forms import equipmentSelectForm


@app.route("/equipments/menu", methods=["GET"])
@login_required(role="ADMIN")
def equipment_menu():
    return render_template("equipments/menu.html")


@app.route("/equipments/add", methods=["GET", "POST"])
@login_required(role="ADMIN")
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
            flash("Varuste on jo järjestelmässä!", "error")
            return render_template("equipments/addequipment.html", form=addEquipmentForm())
        flash('Varuste lisätty onnistuneesti!', "info")
        return redirect(url_for("equipment_add"))
    return render_template("equipments/addequipment.html", form=form)


@app.route("/equipments/listandremove", methods=["GET", "POST"])
@login_required(role="ADMIN")
def equipment_listandremove():
    form = listEquipmentForm()
    for equipment in Equipment.query.order_by(Equipment.name.asc()).all():
        equipmentform = equipmentSelectForm()
        equipmentform.equip = equipment.name
        equipmentform.equipment_id = equipment.equipment_id
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
        flash("Ei poistettavaksi valittuja välineitä!", "warning")
        return render_template("equipments/list.html", form=form)

    try:
        db.session().query(Equipment).filter(Equipment.name.in_(
        selected)).delete(synchronize_session='fetch')
        db.session().commit()
    except:
        db.session().rollback()
        flash("Poistettaessa tapahtui virhe! Välineitä ei poistettu!", "error")
        return redirect(url_for('equipment_listandremove'))

    flash("Valitut välineet poistettu onnistuneesti!", "info")
    return redirect(url_for("equipment_listandremove"))
