from flask import Blueprint, flash, request, redirect, render_template, g
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import UserForm, LoginForm, RegisterForm, ConfirmationForm
from app.decorators import only_for_admin
from app.util.security import send_confirm_token, confirm_token


mod = Blueprint('login', __name__)


@mod.route('/register', methods=['GET', "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username has already taken', 'warning')
            return render_template('login/register.html', form=form)
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email has already taken', 'warning')
            return render_template('login/register.html', form=form)

        new_user = User(form.username.data, form.password.data, form.email.data,
                        form.firstname.data, form.lastname.data, form.admin.data)
        new_user.add()

        send_confirm_token(new_user.email)
        return redirect('/unconfirmed')

    return render_template('login/register.html', form=form)


@mod.route('/confirm/<token>')
def confirm(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    found_user = User.query.filter_by(email=email).first_or_404()
    if found_user.email_confirmed:
        flash('Account already confirmed. Please login.', 'warning')
    else:
        found_user.confirm_email()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect('/login')


@mod.route('/unconfirmed')
def unconfirmed():
    return render_template('login/unconfirmed.html')


@mod.route('/resend', methods=['GET', 'POST'])
def resend_confirmation():
    form = ConfirmationForm(request.form)
    if form.validate_on_submit():
        send_confirm_token(form.email.data)
        flash('A new confirmation email has been sent.', 'success')
        return redirect('/')
    return render_template('login/resend.html', form=form)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        registered_user = User.query.filter_by(username=form.username.data,
                                               password=form.password.data).first()
        if registered_user is None:
            flash('Username or Password is invalid', 'warning')
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
            flash('Username has already taken', 'warning')
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
                               title='Update user %s' % curr_user,
                               text_button="Update",
                               form=form)
