from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, CreateUserForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form, error="Annettua käyttäjää ei ole olemassa, tai salasana oli väärä!")

    login_user(user)
    flash('Kirjautuminen onnistui!')
    return redirect(url_for("index"))


@app.route("/auth/logout")
@login_required
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth/create", methods=["GET", "POST"])
def auth_create():
    if request.method == "GET":
        return render_template("auth/createuserform.html", form=CreateUserForm())

    form = CreateUserForm(request.form)
    # Create the new user from the form
    if form.validate():
        newUser = User(form.username.data, form.name.data,
                       form.password.data, form.city.data, form.age.data)
        try:
            db.session().add(newUser)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("auth/createuserform.html", form=CreateUserForm(), error="Käyttäjänimi on jo käytössä!")
        flash('Rekisteröityminen onnistui!')
        return redirect(url_for("index"))
    return render_template("auth/createuserform.html", form=form)


@app.route("/auth/delete", methods=["GET", "POST"])
@login_required
def auth_delete():
    if request.method == "GET":
        return render_template("auth/deleteuserform.html")

    try:
        stmt = text("DELETE FROM account WHERE account_id = :cur_id").params(
            cur_id=current_user.account_id)
        db.engine.execute(stmt)
    except:
        pass
    flash("Käyttäjä poistettu")
    return redirect(url_for("index"))

@app.route("/auth/changepw", methods=["GET", "POST"])
@login_required
def auth_changepw():
    if request.method == "GET":
        return render_template("auth/changepasswordform.html", form=ChangePasswordForm())

    form = ChangePasswordForm(request.form)
    if form.validate() and check_password_hash(current_user.password, form.oldPassword.data):
        stmt = text("UPDATE account SET password = :newpw WHERE account_id = :cur_id").params(
            newpw=generate_password_hash(form.password.data), cur_id=current_user.account_id)
        db.engine.execute(stmt)
        flash('Salasana vaihdettu!')
        return render_template("auth/changepasswordform.html", form=form)
    return render_template("auth/changepasswordform.html", form=form, error="Nykyinen salasana oli väärä!")

@app.route("/auth/user_info")
@login_required
def auth_user_info():
    return render_template("auth/userinfo.html", user_info=User.find_current_user_information(current_user.account_id))

@app.route("/auth/list")
@login_required
def auth_list():
    return render_template("auth/list.html", users = User.query.all())

