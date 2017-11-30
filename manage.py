#!/usr/bin/env python
from flask_script import Manager
from app import create_app
from app.database import db
from flask_login import LoginManager, current_user
from app.login.models import User
from flask import g

app = create_app()
app.config.from_object("config.DevelopmentConfig")
manager = Manager(app)

db.init_app(app)
with app.test_request_context():
    db.create_all()

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login.login'


@app.before_request
def before_request():
    g.user = current_user


@lm.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))


if __name__ == '__main__':
    manager.run()  