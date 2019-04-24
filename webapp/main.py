#!/venv/bin python

import os, sys, logging
from flask import Flask, render_template, current_app, request, flash
from flask_mail import Mail, Message
from forms import EmailForm

#from pytorch_classifier import image_classifier
from fastai_classifier import image_classifier

#from werkzeug.contrib.profiler import ProfilerMiddleware

from upload import upload
from cv import cv

app = Flask(__name__)

app.register_blueprint(image_classifier)
app.register_blueprint(upload)
app.register_blueprint(cv)

model_links = {
  'pnasnet5': 'https://arxiv.org/pdf/1712.00559.pdf',
  'resnet152': 'https://arxiv.org/pdf/1512.03385.pdf',
  'resnet50': 'https://arxiv.org/pdf/1512.03385.pdf',
  'inceptionresnetv2': 'https://arxiv.org/pdf/1602.07261.pdf'
}


with app.app_context():
    #initialize email configuration
    app.config.from_object('email_conf.Config')

    UPLOAD_FOLDER = './static/uploaded'
    IMAGENET_FOLDER = './static/imagenet'

    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    current_app.config['IMAGENET_FOLDER'] = IMAGENET_FOLDER
    current_app.config['MAIL_USERNAME'] = app.config['MAIL_USERNAME']

    # initialize model depending on env. variable set in dockerfile
    model_name = os.getenv('NNET', 'resnet50')

def install_secret_key(app, filename='secret_key'):
    '''Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    '''
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


@app.route('/')

def home():
    form = EmailForm(request.form)
    return render_template('home.html', form=form, mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_links[model_name])

@app.route('/message', methods=['POST'])

def send_message():
    form = EmailForm(request.form)
    if form.validate():
        app.config.from_object('email_conf.Config')
        mail = Mail(app)
        msg = Message(sender = current_app.config['MAIL_USERNAME'], recipients = [current_app.config['MAIL_USERNAME']], 
                      subject= f'message from {form.name.data} through website')
        mail.body = form.message.data
        msg.html = f'{form.email_field.data}<br>{mail.body}'
        mail.send(msg)
        flash('Message sent', 'success')
        return render_template('home.html', form=form, mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_links[model_name])
    
    flash('There was an error sending the message', 'error')
    return render_template('home.html', form=form, mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_links[model_name])


install_secret_key(app)

if __name__ == '__main__':
    # heroku loggin:
    #stream_handler = logging.StreamHandler()
    #stream_handler.setLevel(logging.INFO)
    #app.logger.addHandler(stream_handler)

    # for profiling:
    #app.config['PROFILE'] = True
    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

    app.run(debug=False, host='0.0.0.0', port=8080)
