from app.entities.models import get_groups
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms.fields import StringField, IntegerField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class UserForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    firstname = StringField(lazy_gettext('First name'), validators=[DataRequired()])
    lastname = StringField(lazy_gettext('Last name'), validators=[DataRequired()])
    age = IntegerField(lazy_gettext('Age'))
    group = QuerySelectField(lazy_gettext('Group'), query_factory=get_groups, allow_blank=False)


class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember password'))


class RegisterForm(FlaskForm):
    admin = BooleanField('Admin')
    firstname = StringField(lazy_gettext('First name'), validators=[DataRequired()])
    lastname = StringField(lazy_gettext('Last name'), validators=[DataRequired()])
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(lazy_gettext('Confirm password'), validators=[DataRequired(),
                                     EqualTo('password', message=lazy_gettext('Passwords must match'))])


class ConfirmationForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])


class EmailForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])


class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
