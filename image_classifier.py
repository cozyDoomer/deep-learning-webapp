import os
from flask import Flask, Blueprint, render_template
from upload import upload

from werkzeug.utils import secure_filename

image_classifier = Blueprint('image_classifier', __name__)

app = Flask(__name__)

@image_classifier.route("/image-classifier")

def show():
    return render_template("image-classifier.html")