from flask import Blueprint, flash, request, redirect, render_template, g
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import gettext
from .models import User
from .forms import UserForm, LoginForm, RegisterForm, ConfirmationForm, EmailForm, PasswordForm
from app.decorators import only_for_admin
from app.util.security import confirm_token
from app.util.emails import send_confirm_token, send_reset_token


mod = Blueprint('login', __name__)


@mod.route('/register', methods=['GET', "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash(gettext('Username was already taken'), 'warning')
            return render_template('login/register.html', form=form)

        elif User.query.filter_by(email=form.email.data).first():
            flash(gettext('Email was already taken'), 'warning')
            return render_template('login/register.html', form=form)

        new_user = User(form.username.data, form.password.data, form.email.data,
                        form.firstname.data, form.lastname.data, form.admin.data)
        new_user.add()

        send_confirm_token(new_user.email)
        flash(gettext('A confirmation link has been sent to your email address'), 'success')
        return redirect('/unconfirmed')

    return render_template('login/register.html', form=form)


@mod.route('/confirm/<token>')
def confirm(token):
    email = confirm_token(token)
    if not email:
        flash(gettext('The confirmation link is invalid or has expired.'), 'danger')
        return redirect('/login')

    found_user = User.query.filter_by(email=email).first_or_404()
    if found_user.email_confirmed:
        flash(gettext('Account already confirmed. Please login.'), 'warning')
    else:
        found_user.confirm_email()
        flash(gettext('You have confirmed your account. Thanks!'), 'success')
    return redirect('/login')


@mod.route('/unconfirmed')
def unconfirmed():
    return render_template('login/unconfirmed.html')


@mod.route('/resend', methods=['GET', 'POST'])
def resend_confirmation():
    form = ConfirmationForm(request.form)
    if form.validate_on_submit():
        send_confirm_token(form.email.data)
        flash(gettext('A new confirmation email has been sent.'), 'success')
        return redirect('/')
    return render_template('login/resend.html', form=form)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        registered_user = User.query.filter_by(username=form.username.data).first()
        if registered_user is None:
            flash(gettext('Username is invalid'), 'warning')
            return render_template('login/login.html', title='Sing in', form=form)

        if not registered_user.is_correct_password(form.password.data):
            flash(gettext('Password is invalid'), 'warning')
            return render_template('login/login.html', title='Sing in', form=form)

        if not registered_user.email_confirmed:
            return redirect('/unconfirmed')

        login_user(registered_user, remember=form.remember_me.data)
        next = request.args.get('next')
        return redirect(next or '/')
    return render_template('login/login.html', title='Sing in', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@mod.route('/reset', methods=['GET', "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(email=form.email.data).first_or_404()
        send_reset_token(found_user.email)
        flash(gettext('A link to reset your password has been sent to the email address'), 'success')
        return redirect('/')
    return render_template('login/reset.html', form=form)


@mod.route('/reset/<token>', methods=['GET', "POST"])
def reset_with_token(token):
    email = confirm_token(token)
    if not email:
        flash(gettext('The reset link is invalid or has expired.'), 'danger')
        return redirect('/login')

    form = PasswordForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(email=email).first_or_404()
        found_user.set_password(form.password.data)
        flash(gettext('Your Password has been changed successfully!'), 'success')
        return redirect('/login')
    return render_template('login/reset_with_token.html',
                           form=form, token=token)


@mod.route('/users', methods=['GET'])
@only_for_admin
def user():
    form = UserForm(request.form)
    users = User.query.filter_by().all()
    return render_template('entities/entity.html', name='user', title='Users',
                           form=form, entities=users)


@mod.route('/update', methods=['GET', "POST"])
@login_required
def user_update():
    curr_user = g.user
    form = UserForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if current_user.username != form.username.data \
                and User.query.filter_by(username=form.username.data).first():
            flash(gettext('Username was already taken'), 'warning')
            return redirect('/update')
        curr_user.edit(username=form.username.data,
                       lastname=form.lastname.data,
                       firstname=form.firstname.data,
                       age=form.age.data,
                       group=form.group.data)
        return redirect('/')
    else:
        form.username.data = curr_user.username
        form.lastname.data = curr_user.lastname
        form.firstname.data = curr_user.firstname
        form.age.data = curr_user.age
        form.group.data = curr_user.group
        return render_template('entities/entity_update.html',
                               title=gettext('Update user %s') % curr_user,
                               text_button=gettext("Update"),
                               form=form)
