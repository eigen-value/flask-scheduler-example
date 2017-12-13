from flask import Blueprint, flash, request, redirect, render_template, \
    g, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .forms import UserForm, LoginForm, RegisterForm
from app.decorators import only_for_admin
from app.util.security import ts
from app.util.emails import send_email


mod = Blueprint('login', __name__)


@mod.route('/register', methods=['GET', "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username has already taken', 'error')
            return render_template('register.html', form=form)
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email has already taken', 'error')
            return render_template('register.html', form=form)

        new_user = User(form.username.data, form.password.data, form.email.data,
                        form.firstname.data, form.lastname.data, form.admin.data)
        new_user.add()
        flash('User successfully registered')

        # Now we'll send the email confirmation link
        token = ts.dumps(form.email.data, salt='email-confirm-key')
        confirm_url = url_for('login.confirm_email', token=token, external=True)
        subject = "Confirm your email"
        html = render_template('activate.html', confirm_url=confirm_url)
        send_email([new_user.email], subject, html)
        return redirect('/login')

    return render_template('register.html', form=form)


@mod.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    found_user = User.query.filter_by(email=email).first_or_404()
    found_user.confirm_email()

    return redirect('/login')


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        registered_user = User.query.filter_by(username=form.username.data,
                                               password=form.password.data).first()
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return render_template('login.html', title='Sing in', form=form)
        login_user(registered_user, remember=form.remember_me.data)
        next = request.args.get('next')
        return redirect(next or '/')
    return render_template('login.html', title='Sing in', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# user

@mod.route('/users', methods=['GET'])
@only_for_admin
def user():
    form = UserForm(request.form)
    users = User.query.filter_by().all()
    return render_template('entity.html', name='user', title='Users',
                           form=form, entities=users)


@mod.route('/update', methods=['GET', "POST"])
@login_required
def user_update():
    curr_user = g.user
    form = UserForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if current_user.username != form.username.data \
                and User.query.filter_by(username=form.username.data).first():
            flash('Username has already taken', 'error')
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
        return render_template('entity_update.html',
                               title='Update user %s' % curr_user,
                               text_button="Update",
                               form=form)
