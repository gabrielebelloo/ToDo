from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, ToDo, db
from werkzeug.security import generate_password_hash, check_password_hash
import json


views = Blueprint("views", __name__, template_folder='templates', static_folder='static')


@views.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
  if request.method == "POST":
    todo = request.form.get("todo")

    if len(todo) < 1:
      flash("Insert text.", category="error")
    else:
      new_todo = ToDo(text=todo, user_id=current_user.id, status=False)
      db.session.add(new_todo)
      db.session.commit()
      flash("ToDo created!", category="success")
  
    return render_template("dashboard.html", user=current_user)
    
  elif request.method == "GET": 
    return render_template("dashboard.html", user=current_user)
  

@views.route("/my-account", methods=["GET", "POST"])
@login_required
def my_account():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username").lower()
    full_name = request.form.get("fullName")
    password = request.form.get("password")
    passwordConfirm = request.form.get("passwordConfirm")

    user_email = User.query.filter_by(email=email).first()
    user_username = User.query.filter_by(username=username).first()
    current = User.query.filter_by(id=current_user.id).first()


    if email != current.email:
      if user_email and not user_email.email == current.email:
        flash("Email already exists.", category="error")
        return render_template("my_account.html", user=current_user)
      elif len(email) < 4:
        flash("Insert valid email.", category="error")
        return render_template("my_account.html", user=current_user)
      else:
        current.email = email
        db.session.commit()
        


    if username != current.username:
      if user_username and not user_username.username == current.email:
        flash("Username already exists.", category="error")
        return redirect(url_for(views.my_account))
      elif len(username) < 2:
        flash("Insert a valid username.", category="error")
        return render_template("my_account.html", user=current_user)
      else:
        current.username = username
        db.session.commit()


    if full_name != current.full_name:
      if len(full_name) < 3:
        flash("Insert a valid full name.", category="error")
        return render_template("my_account.html", user=current_user)
      else:
        current.full_name = full_name
        db.session.commit()


    if not password:
      pass
    else:
      if check_password_hash(current.password, password):
        flash("Password is the same.", category="error")
        return render_template("my_account.html", user=current_user)
      else:
        if len(password) < 8:
          flash("Password must be at least 8 characters long.", category="error")
          return render_template("my_account.html", user=current_user)
        elif password != passwordConfirm:
          flash("Passwords do not match.", category="error")
          return render_template("my_account.html", user=current_user)
        else:
          current.password = generate_password_hash(password, method="pbkdf2:sha256")
          db.session.commit()

    flash("Account data saved!", category="success")
    return render_template("my_account.html", user=current_user)
  elif request.method == "GET":
    
    return render_template("my_account.html", user=current_user)
  

@views.route("/delete-todo", methods=['POST'])
@login_required
def delete_todo():
  data = json.loads(request.data)
  todo_id = data['toDoId']
  todo_found = ToDo.query.get(todo_id)
  if todo_found:
    if todo_found.user_id == current_user.id:
      db.session.delete(todo_found)
      db.session.commit()
      flash("Note deleted successfully!", category="success")

  return jsonify({})


@views.route("/edit-todo", methods=['POST'])
@login_required
def edit_todo():
  edited_todo = request.form.get('edited_todo')
  edited_todo_id = request.form.get('button')
  
  todo_found = ToDo.query.get(edited_todo_id)

  if todo_found:
    if todo_found.user_id == current_user.id:
      if edited_todo == "":
        db.session.delete(todo_found)
        db.session.commit()
        flash("Note deleted successfully!", category="success")
      else:
        todo_found.text = edited_todo
        db.session.commit()
        flash("Note edited successfully!", category="success")

  return redirect(url_for('views.dashboard'))


@views.route("/checkbox", methods=['POST'])
@login_required
def checkbox():
  data = json.loads(request.data)
  todo_id = data['toDoId']
  todo_found = ToDo.query.get(todo_id)

  if todo_found:
    if todo_found.user_id == current_user.id:
      if todo_found.status == True:
        todo_found.status = False
        flash('ToDo unchecked.', category='success')
      else:
        todo_found.status = True
        flash('ToDo checked!', category='success')        
      db.session.commit()

  return jsonify({})