#!/venv/bin python

import os, sys
from flask import Flask, Blueprint, current_app, render_template
import numpy as np

from fastai.vision import *
from object_detection_utils.object_detection_helper import *
from object_detection_utils.RetinaNetFocalLoss import RetinaNetFocalLoss
from object_detection_utils.RetinaNet import RetinaNet
from object_detection_utils.callbacks import BBLossMetrics, BBMetrics, PascalVOCMetric

object_detection = Blueprint('object_detection', __name__)

app = Flask(__name__)

model_links = {
  'resnet34': 'https://arxiv.org/pdf/1512.03385.pdf',
}

def init_learner(model_name):
    learn = load_learner(path='static/weights/', file='resnet34_bbox.pkl')
    return learn

def get_name():
    # only resnet34 so far for fastai object detection
    return 'resnet34'

def get_link(model_name):
    return model_links[model_name]

@object_detection.route("/object-detection")

def show():
    model_name = 'resnet34'
    model_link = get_link(model_name)
    return render_template("object-detection.html", mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_link)


@object_detection.route("/object-detection/<filename>")

def analyze(filename):
    model_name = 'resnet34'
    model_link = get_link(model_name)
    print(f'model name: {model_name}') 
    
    if not os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        print('error, filename not found in static/uploads/<filename>')
        return render_template("object-detection.html", filename=filename, name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])

    learn = init_learner(model_name)
    print('init model successfully')
    print(learn)
    # TODO: predict with retinanet
    print('prediction done')

    # TODO: extract bbox and class from prediction
    print(f'predicted classes: {class_names}') 
    print(f'predict bounding box: {bbox}') 
    print(f'confidence: {percent}')
    
    return render_template("object-detection.html", filename=filename, prediction=class_names, confidence=percent, 
                                                    name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])