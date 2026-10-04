from dotenv import load_dotenv
import os
from flask import Flask, url_for
from .auth import bp
from flask_login import LoginManager, login_required, current_user
from .db import SessionLocal
from .models import User


load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
  app.register_blueprint(bp)

  login_manager = LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = "auth.login"

  @login_manager.user_loader
  def load_user(user_id):
    with SessionLocal() as db:
      return db.get(User, (int(user_id)))

  @app.route("/")
  @login_required
  def index():
      return f'Hello, {current_user.username}!"  <a href={url_for("auth.logout")}>Log out</a> ' 

  return app