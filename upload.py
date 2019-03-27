import os
from flask import Flask, request, redirect, url_for, Blueprint, render_template
from upload import upload

from werkzeug.utils import secure_filename

image_classifier = Blueprint('image_classifier', __name__)
upload = Blueprint('upload', __name__)

UPLOAD_FOLDER = './static/uploaded'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@image_classifier.route('/upload', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('image_classifier.upload_file',
                                    filename=filename))
    return render_template("image-classifier.html")

@image_classifier.route("/image-classifier")

def show():
    return render_template("image-classifier.html")
