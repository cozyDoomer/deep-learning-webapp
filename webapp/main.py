#!/venv/bin python

import os, sys
from flask import Flask, render_template, current_app, send_file, session
from image_classifier import image_classifier
from upload import upload

app = Flask(__name__)

with app.app_context():
    UPLOAD_FOLDER = './static/uploaded'
    IMAGENET_FOLDER = './static/imagenet'
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    current_app.config['IMAGENET_FOLDER'] = IMAGENET_FOLDER 

app.config['SESSION_TYPE'] = 'filesystem'

app.register_blueprint(image_classifier)
app.register_blueprint(upload)

def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
        print('secret key found')
    except IOError:
        print('Error: No secret key. Create it with:')
        if not os.path.isdir(os.path.dirname(filename)):
            print('mkdir -p', os.path.dirname(filename))
        print('head -c 24 /dev/urandom >', filename)
        sys.exit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cv")
def cv():
    return render_template("cv.html")

@app.route("/cv/download/")
def download_cv():
    return send_file('static/documents/cv_unterrainer.pdf', as_attachment=True)

if __name__ == "__main__":
    install_secret_key(app)
    app.run(debug=True, host='0.0.0.0')
    