"""Auth blueprint — login, signup, logout."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.models import db, User
from auth.forms import LoginForm, SignupForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Welcome back ✨", "success")
            next_url = request.args.get("next") or url_for("main.dashboard")
            return redirect(next_url)
        flash("Invalid username or password", "error")
    return render_template("login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data.strip()).first():
            flash("Username already taken", "error")
        elif User.query.filter_by(email=form.email.data.strip()).first():
            flash("Email already registered", "error")
        else:
            user = User(
                username=form.username.data.strip(),
                email=form.email.data.strip(),
                password=generate_password_hash(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Account created — welcome!", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("signup.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("main.index"))
