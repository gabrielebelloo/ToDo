from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy()
DB_NAME = "database.db"


class ToDo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(10000))
  status = db.Column(db.Boolean)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  username = db.Column(db.String(150), unique=True)
  full_name = db.Column(db.String(150))
  password = db.Column(db.String(150))
  todos = db.relationship("ToDo")


  