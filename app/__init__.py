from flask import Flask

from config import Config

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_login import LoginManager


# Create instance of Flask Application
app = Flask(__name__)
app.config.from_object(Config)
# Create instance of SQLAlchemy with the Flask Application instance
db = SQLAlchemy(app)
# Create instance of Migrate (migration engine) and pass in the app and SQLAlchemy instance
migrate = Migrate(app, db)
# Create instance of LoginManager (handles authentication) with app instance
login = LoginManager(app)
# Login manager redirects user to proper endpoint if not logged in
login.login_view = 'login'
# Maybe they are some form of programming wizard
login.login_message = "Hey! How did you get here? We're sorry, you must be logged in to do that!"
login.login_message_category = 'danger'


from . import routes, models
