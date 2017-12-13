from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    firstname = db.Column(db.String(10), nullable=False)
    lastname = db.Column(db.String(10), nullable=False)
    id_group = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Group', backref=db.backref('users', lazy='dynamic'))
    age = db.Column(db.Integer)
    admin = db.Column(db.Boolean)
    registered_on = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    email_confirmed = db.Column(db.Boolean, default=False)
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, username, password, email, firstname, lastname, admin):
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.admin = admin
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return self.username

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, username, firstname, lastname, age, group):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.group = group
        db.session.commit()

    def get_id(self):
        return unicode(self.id)

    def get_list(self):
        result = [('id', self.id),
                  ('firstname', self.firstname),
                  ('lastname', self.lastname),
                  ('group', self.group),
                  ('age', self.age),
                  ('email', self.email),
                  ('last seen', self.last_seen),
                  ('email confirmed', self.email_confirmed)]
        return result

    def confirm_email(self):
        self.email_confirmed = True
        db.session.commit()
