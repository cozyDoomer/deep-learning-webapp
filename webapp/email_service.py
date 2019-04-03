#!/venv/bin python

import os
from flask import Flask, Blueprint, current_app
from flask_mail import Mail, Message

email = Blueprint('email', __name__)

app = Flask(__name__)

mail = Mail(app)

@app.route("/email")
def send_email(message, sender):
    msg = Message(message, sender=sender, recipients=current_app.config['EMAIL'])
    return '0'