#!/venv/bin python

import os, sys
from flask import Flask, Blueprint, current_app, render_template
import numpy as np

from fastai.vision import *
import pretrainedmodels

image_classifier = Blueprint('image_classifier', __name__)

app = Flask(__name__)

model_links = {
  'inceptionresnetv2':  'https://arxiv.org/pdf/1712.00559.pdf'
}

def top_5_accuracy(input, targs, k=5):
  return top_k_accuracy(input, targs, k)

def init_learner(model_name):
  thismodule = sys.modules['__main__']
  setattr(thismodule, 'top_5_accuracy', top_5_accuracy)
  learn = load_learner(path='static/weights/', file='inceptionresnetv2.pkl')
  return learn

def get_name():
    return os.getenv('NNET', 'inceptionresnetv2') # resnet50 default

def get_link(model_name):
    return model_links[model_name]

@image_classifier.route("/image-classifier")

def show():
    model_name = get_name()
    model_link = get_link(model_name)
    return render_template("image-classifier.html", mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_link)


@image_classifier.route("/image-classifier/<filename>")

def analyze(filename):
    model_name = get_name()
    model_link = get_link(model_name)
    
    if not os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        print('error, filename not found in static/uploads/<filename>')
        return render_template("image-classifier.html", filename=filename, name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])

    print(model_name) 
    print(model_link)

    learn = init_learner(model_name)

    print('init model successfully')

    _, _, preds = learn.predict(open_image(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)))

    print('prediction done')

    # Load Imagenet Synsets
    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_synsets.txt'), 'r') as f:
        synsets = f.readlines()

    # create index: class dictionary
    synsets = [x.strip() for x in synsets]
    synsets = [line.split(' ') for line in synsets]
    key_to_classname = {spl[0]:' '.join(spl[1:]) for spl in synsets}

    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_classes.txt'), 'r') as f:
        class_id_to_key = f.readlines()

    class_id_to_key = [x.strip() for x in class_id_to_key]

    # get highest confidence index and value 
    preds_sorted, idxs = preds.sort(descending=True)

    # extract classname from index
    idxs = idxs.numpy()[:3]

    class_keys = [class_id_to_key[i] for i in idxs] 
    
    class_names = [', '.join([str(y) for y in key_to_classname[x].split(",", 2)[:2]]) for x in class_keys]

    percent = (preds_sorted[:3].numpy() * 100).round(decimals=2)
    
    print(f'predicted classes: {class_names}') 
    print(f'confidence: {percent}')
    
    return render_template("image-classifier.html", filename=filename, prediction=class_names, confidence=percent, 
                                                    name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])