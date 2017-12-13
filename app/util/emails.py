from flask_mail import Message
from app import mail, app


def send_email(recipients, subject, html_body="", text_body=""):
    msg = Message(subject, sender=app.config['ADMINS'][0],
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
