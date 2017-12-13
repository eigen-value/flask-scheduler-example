from flask_mail import Message
from app import mail, app
from app.decorators import async


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
