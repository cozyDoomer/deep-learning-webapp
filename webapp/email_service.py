#!/venv/bin python

import os
from flask import Flask, Blueprint, render_template, flash, request
from flask_mail import Mail, Message

from forms import EmailForm

email = Blueprint('email', __name__)

app = Flask(__name__)

@email.route('/', methods=['POST'])

def send():
    form = EmailForm(request.form)
    if form.validate():
        app.config.from_object('email_conf.Config')
        mail = Mail(app)
        msg = Message(sender = app.config['MAIL_USERNAME'], recipients = [app.config['MAIL_USERNAME']], subject= f'message from {form.name.data} through website')
        mail.body = form.message.data
        msg.html = f'{form.email_field.data}<br>{mail.body}'
        mail.send(msg)
        flash('Message sent', 'success')
        return render_template("home.html", form=form, mail=app.config['MAIL_USERNAME'])
    
    flash('There was an error sending the message', 'error')
    return render_template("home.html", form=form, mail=app.config['MAIL_USERNAME'])