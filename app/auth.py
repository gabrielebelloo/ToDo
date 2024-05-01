from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db

auth = Blueprint("auth", __name__)


# Login route - deals with logging user
@auth.route("/login", methods=["POST", "GET"])
def login():
  if request.method == "POST":
    username = request.form.get("username").lower()
    password = request.form.get("password")

    user_found = User.query.filter_by(username=username).first()
    if user_found:
      if check_password_hash(user_found.password, password):
        flash("Logged in!", category="success")
        login_user(user_found, remember=True)
        return redirect(url_for("views.dashboard"))
      else:
        flash("Incorrect password.", category="error")
    else:
      flash("Username does not exist.", category="error")
    
    return render_template("login.html", user=current_user)

  elif request.method == "GET":
    return render_template("login.html", user=current_user)


# Sign Up route - Deals with registering the user
@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username").lower()
    password = request.form.get("password")
    passwordConfirm = request.form.get("passwordConfirm")

    user_email = User.query.filter_by(email=email).first()
    user_username = User.query.filter_by(username=username).first()

    if user_email:
      flash("Email already exists.", category="error")
    elif user_username:
      flash("Username already exists.", category="error")
    elif len(email) < 4:
      flash("Insert valid email.", category="error")
    elif len(username) < 2:
      flash("Insert a valid username.", category="error")
    elif len(password) < 8:
      flash("Password must be at least 8 characters long.", category="error")
    elif password != passwordConfirm:
      flash("Passwords do not match.", category="error")
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password, method="pbkdf2:sha256"))
      db.session.add(new_user)
      db.session.commit()
      flash("Account created!", category="success")
      return redirect(url_for("auth.login"))

    return render_template("sign_up.html", user=current_user)

  elif request.method == "GET":
    return render_template("sign_up.html", user=current_user)


# Logout route - Deals with logging out the user
@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.login"))