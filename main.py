from flask import Flask
from app.views import views
from app.auth import auth
from os import path
from app.models import db, DB_NAME, User
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "qwertyuiop"

app.register_blueprint(views)
app.register_blueprint(auth)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

if __name__ == "__main__":
  with app.app_context():
    if not path.exists(f"instance/{DB_NAME}"):
      print("Database created")
      db.create_all()
  app.run(debug=True)