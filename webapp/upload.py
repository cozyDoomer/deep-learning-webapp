#!/venv/bin python

import os
from flask import Flask, flash, request, redirect, url_for, Blueprint, current_app, render_template, send_from_directory

from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
import piexif

upload = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(filepath, min_size=299):
    img = Image.open(filepath)

    # rotate if exif encoded
    exif_bytes = None
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            exif_bytes = piexif.dump(exif_dict)

            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90,
                                 expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(
                    Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)

    # resize image to min_size (keep aspect ratio)
    ratio = max(min_size/img.width, min_size/img.height)
    img.thumbnail((img.width * ratio, img.height * ratio), Image.ANTIALIAS)

    print(f'resized image: {img.size}')
    if exif_bytes:
        img.save(filepath, exif=exif_bytes)
    img.save(filepath)


@upload.route('/upload/<reason>', methods=['POST', 'GET'])
def upload_file(reason):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)

        # check if file extension is in ALLOWED_EXTENSIONS
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            size = 299
            if reason == 'object-detection':
                size = 500
            preprocess_image(filepath, min_size=size)
            return render_template(f'{reason}.html', filename=filename, mail=current_app.config['MAIL_USERNAME'])

    return render_template(f'{reason}.html', error='error', mail=current_app.config['MAIL_USERNAME'])


@upload.route('/upload/<reason>/<filename>', methods=['GET'])
def send_file(reason, filename):
    if request.method == 'GET':
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    return render_template(f'{reason}.html', error='error', mail=current_app.config['MAIL_USERNAME'])
