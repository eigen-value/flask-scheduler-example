from itsdangerous import URLSafeTimedSerializer
from flask import url_for, render_template
from app import app
from .emails import send_email

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_confirm_token(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('login.confirm', token=token, _external=True)
    html = render_template('login/activate.html', confirm_url=confirm_url)
    send_email(email, "Confirm your email", html)