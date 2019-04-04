#!/venv/bin python

import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, current_app, render_template, send_from_directory

from werkzeug.utils import secure_filename

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['POST', 'GET'])

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return render_template("image-classifier.html", filename=filename, mail=current_app.config['MAIL_USERNAME']) 
    return render_template("image-classifier.html", error='error', mail=current_app.config['MAIL_USERNAME']) 

@upload.route('/upload/<filename>', methods=['GET'])

def send_file(filename):
    if request.method=='GET':
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    return render_template("image-classifier.html", error='error', mail=current_app.config['MAIL_USERNAME']) 