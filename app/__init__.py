from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

# Babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    print("getting locale")
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


# login & security
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login.login'
mail = Mail(app)
bcrypt = Bcrypt(app)

# blueprints:
import app.entities.controllers as entities
import app.login.controllers as login
app.register_blueprint(entities.mod)
app.register_blueprint(login.mod)

from app import views

if not app.config['DEBUG']:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/schedule.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('schedule startup')
