#!/venv/bin python

import os, gc
from flask import Flask, Blueprint, current_app, render_template

import torch
import numpy as np

from fastai.vision import *

import utils

image_classifier = Blueprint('image_classifier', __name__)

app = Flask(__name__)

model_links = {
  'fastai-resnet50':  'https://arxiv.org/pdf/1712.00559.pdf'
}

def init_learner(model_name):
    # initialize model depending on env. variable set in dockerfile

    if model_name == 'fastai-resnet50':
        learn = cnn_learner(data, models.resnet50, pretrained=True)

    return learn

def get_name():
    return os.getenv('NNET', 'fastai-resnet50') # resnet50 default

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

    learn = init_learner(model_name)

    output = learn.predict(open_image(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)))

    # Softmax to get confidence summing up to 1
    output = torch.nn.functional.softmax(output.data.squeeze(), dim=0)

    # get highest confidence index and value 
    preds_sorted, idxs = output.sort(descending=True)
    #max, argmax = output.max(0)

    # extract classname from index
    idxs = idxs.numpy()[:3]

    class_keys = class_id_to_key[idxs]
    
    class_names = [', '.join([str(x) for x in key_to_classname[x].split(",", 2)[:2]]) for x in class_keys]

    percent = (preds_sorted[:3].numpy() * 100).round(decimals=2)


    del model, load_img, tf_img, img, tensor, input, synsets, splits, class_id_to_key, output, preds_sorted, idxs, class_keys
    gc.collect()
    
    return render_template("image-classifier.html", filename=filename, prediction=class_names, confidence=percent, 
                                                    name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])