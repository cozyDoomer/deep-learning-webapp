#!/venv/bin python

import os
from flask import Flask, Blueprint, render_template, send_file, current_app

cv = Blueprint('cv', __name__)

app = Flask(__name__)


@cv.route("/cv")
def show():
    return render_template("cv.html", mail=current_app.config['MAIL_USERNAME'])


@cv.route("/cv/download/")
def download():
    return send_file('static/documents/cv.pdf', as_attachment=True)
