#!/venv/bin python

import os
from flask import Flask, Blueprint, current_app, render_template, send_file

cv = Blueprint('cv', __name__)

app = Flask(__name__)

@cv.route("/cv")

def show():
    return render_template("cv.html")


@cv.route("/cv/download/")

def download():
    return send_file('static/documents/cv.pdf', as_attachment=True)