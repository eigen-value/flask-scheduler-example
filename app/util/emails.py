from flask_mail import Message
from app import mail, app
from app.decorators import async
from flask import url_for, render_template
from .security import generate_token


@async
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, subject, html_body="", text_body=""):
    msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[recipients])
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)


def send_confirm_token(email):
    token = generate_token(email)
    confirm_url = url_for('login.confirm', token=token, _external=True)
    html = render_template('email/activate.html', confirm_url=confirm_url)
    send_email(email, "Confirm your email", html)


def send_reset_token(email):
    token = generate_token(email)
    recover_url = url_for('login.reset_with_token',
                          token=token, _external=True)
    html = render_template('email/recover.html', recover_url=recover_url)
    send_email(email, "Password reset requested", html)