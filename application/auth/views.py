from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, CreateUserForm, ChangePasswordForm, ChangeUsernameForm, EditUserInfoForm
from flask_login import login_user, logout_user, current_user
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text


@app.route("/auth/menu", methods=["GET"])
@login_required()
def auth_menu():
    return render_template("auth/menu.html")


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form=LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if  not form.validate() or user is None or not check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form=form, error="Annettua käyttäjää ei ole olemassa, tai salasana oli väärä!")

    login_user(user, remember=True)
    flash('Kirjautuminen onnistui!')
    return redirect(url_for("index"))


@app.route("/auth/logout")
@login_required()
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
                       form.password.data, form.city.data, form.age.data, 'USER')
        try:
            db.session().add(newUser)
            db.session().commit()
        except Exception:
            db.session().rollback()
            return render_template("auth/createuserform.html", form=CreateUserForm(), error="Käyttäjänimi on jo käytössä!")
        flash('Rekisteröityminen onnistui!')
        return redirect(url_for("auth_login"))
    return render_template("auth/createuserform.html", form=form)


@app.route("/auth/delete", methods=["GET", "POST"])
@login_required()
def auth_delete():
    if request.method == "GET":
        return render_template("auth/deleteuserform.html")

    try:
        User.delete_account(current_user.account_id)
        logout_user()
    except:
        return render_template("auth/deleteuserform.html", error="Virhe poistettaessa käyttäjää!, käyttäjää ei poistettu!")
    flash("Käyttäjä poistettu")
    return redirect(url_for("index"))


@app.route("/auth/delete/<account_id>", methods=["GET", "POST"])
@login_required(role="ADMIN")
def auth_delete_account(account_id):
    try:
        User.delete_account(account_id)
        flash("Käyttäjä poistettu onnistuneesti!")
        return redirect(url_for("index"))
    except:
        flash("Poistaminen epäonnistui!")
        return redirect(url_for("index"))


@app.route("/auth/changepw", methods=["GET", "POST"])
@login_required()
def auth_changepw():
    if request.method == "GET":
        return render_template("auth/changepasswordform.html", form=ChangePasswordForm())

    form = ChangePasswordForm(request.form)
    if form.validate() and check_password_hash(current_user.password, form.oldPassword.data):
        stmt = text("UPDATE account SET password = :newpw WHERE account_id = :cur_id").params(
            newpw=generate_password_hash(form.password.data), cur_id=current_user.account_id)
        db.engine.execute(stmt)
        db.session().commit()
        flash('Salasana vaihdettu!')
        return render_template("auth/changepasswordform.html", form=form)
    return render_template("auth/changepasswordform.html", form=form, error="Nykyinen salasana oli väärä!")


@app.route("/auth/user_info")
@login_required()
def auth_user_info():
    return render_template("auth/userinfo.html", user_info=User.find_current_user_information(current_user.account_id))


@app.route("/auth/user_info/edit/<account_id>", methods=["GET", "POST"])
@login_required()
def auth_user_info_edit(account_id):
    if account_id != current_user.get_id():
        if current_user.urole != "ADMIN":
            flash("Sinulla ei ole käyttöoikeuksia kyseiseen toimintoon")
            return redirect(url_for("index"))
    user = User.query.get(account_id)
    form = EditUserInfoForm()

    if request.method == "GET":
        form.name.data = user.name
        form.city.data = user.city
        form.age.data = user.age
        return render_template("auth/edituserinfo.html", form=form, account_id=account_id)
    form = EditUserInfoForm(request.form)
    if form.validate():
        try:
            user.name = form.name.data
            user.city = form.city.data
            user.age = form.age.data
            db.session().commit()
        except:
            db.session().rollback()
            return render_template("auth/edituserinfo.html", form=form, error="Muokatessa tapahtui virhe! Käyttäjätietoja ei muokattu!")
        flash("Käyttäjätietoja muokattiin onnistuneesti!")
        return redirect(url_for("auth_user_info"))
    return render_template("auth/edituserinfo.html", form=form)


@app.route("/auth/list")
@login_required(role="ADMIN")
def auth_list():
    page = request.args.get('page', 1, type=int)
    return render_template("auth/list.html", users=User.query.order_by(User.account_id.asc()).paginate(page, 20, False))


@app.route("/auth/change_username", methods=["GET", "POST"])
@login_required()
def auth_change_username():
    if request.method == "GET":
        return render_template("auth/changeusername.html", form=ChangeUsernameForm())

    form = ChangeUsernameForm(request.form)
    if form.username.data == current_user.username:
        return render_template("auth/changeusername.html", form=form, error="Uusi käyttäjänimi on sama kuin nykyinen käyttäjänimi!")
    if form.validate():
        try:
            current_user.username = form.username.data
            db.session().commit()
        except:
            db.session().rollback()
            return render_template("auth/changeusername.html", form=form, error="Käyttäjänimi on varattu!")
        flash("Käyttäjänimi vaihdettu onnistuneesti")
        return render_template("auth/menu.html")
    return render_template("auth/changeusername.html", form=form)
