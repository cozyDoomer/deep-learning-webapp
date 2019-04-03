#!/venv/bin python

import os, sys
from flask import Flask, render_template, current_app

from image_classifier import image_classifier
from upload import upload
from cv import cv
from email_service import email

app = Flask(__name__)

with app.app_context():
    UPLOAD_FOLDER = './static/uploaded'
    IMAGENET_FOLDER = './static/imagenet'
    EMAIL = 'chr.unterrainer@gmail.com'
                
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    current_app.config['IMAGENET_FOLDER'] = IMAGENET_FOLDER
    current_app.config['EMAIL'] = EMAIL 

app.register_blueprint(image_classifier)
app.register_blueprint(upload)
app.register_blueprint(cv)
app.register_blueprint(email)

def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)
    try:
        app.secret_key = open(filename, 'rb').read()
        app.config['SESSION_TYPE'] = 'filesystem'
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

if __name__ == "__main__":
    install_secret_key(app)
<<<<<<< HEAD
    app.run(debug=True, host='0.0.0.0')
    
=======
    app.run(host='0.0.0.0',port=5000)
>>>>>>> 8b6150b
