from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, CreateUserForm
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    #Validate

    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form = form, error = "Annettua käyttäjää ei ole olemassa, tai salasana oli väärä!")

    login_user(user)
    flash('Kirjautuminen onnistui!')
    return redirect(url_for("index"))

@app.route("/auth/logout")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/create", methods = ["GET", "POST"])
def auth_create():
    if request.method == "GET":
        return render_template("auth/createuserform.html", form = CreateUserForm())
    
    form = CreateUserForm(request.form)
    # Create the new user from the form
    if form.validate():
        newUser = User(form.username.data, form.name.data, form.password.data, form.city.data, int(form.age.data))
        try:
            db.session().add(newUser)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("auth/createuserform.html", form = CreateUserForm(), error = "Käyttäjänimi on jo käytössä!")
        flash('Rekisteröityminen onnistui!')
        return redirect(url_for("index"))
    return render_template("auth/createuserform.html", form=form)
