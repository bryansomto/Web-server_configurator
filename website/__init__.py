""" Application initializer."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
basedir = path.abspath(path.dirname(__file__))
DB_NAME = "database.db"


def create_app():
  """ App creation and initialization function."""
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'jhgjetdjq wjgkfc'
  app.config['SQLALCHEMY_DATABASE_URI'] = \
      'sqlite:///' + path.join(basedir, DB_NAME)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import Server, User

  with app.app_context():
      db.create_all()

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'  # type: ignore
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  return app
