#!/venv/bin python

import os
from flask import Flask, Blueprint, current_app, render_template

import torch
import numpy as np

from pnasnet import pnasnet5large

import utils

image_classifier = Blueprint('image_classifier', __name__)

app = Flask(__name__)


@image_classifier.route("/image-classifier")

def show():
    return render_template("image-classifier.html", mail=current_app.config['MAIL_USERNAME'])


@image_classifier.route("/image-classifier/<filename>")

def analyze(filename):
    model = pnasnet5large(num_classes=1000, pretrained='imagenet')
    model.eval()
    # loading image uploaded to the server
    load_img = utils.LoadImage()
    # rescale, center crop, normalize, and others (ex: ToBGR, ToRange255)
    tf_img = utils.TransformImage(model) 

    img = load_img(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    tensor = tf_img(img)         # 3x600x500 -> 3x299x299 size may differ
    tensor = tensor.unsqueeze(0) # 3x299x299 -> 1x3x299x299

    input = torch.autograd.Variable(tensor, requires_grad=False)

    # Load Imagenet Synsets
    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_synsets.txt'), 'r') as f:
        synsets = f.readlines()

    # len(synsets)==1001
    # sysnets[0] == background
    synsets = [x.strip() for x in synsets]
    splits = [line.split(' ') for line in synsets]
    key_to_classname = {spl[0]:' '.join(spl[1:]) for spl in splits}

    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_classes.txt'), 'r') as f:
        class_id_to_key = f.readlines()

    class_id_to_key = np.array([x.strip() for x in class_id_to_key])

    # Make predictions
    output = model(input) # size(1, 1000)

    # Softmax to get confidence summing up to 1
    output = torch.nn.functional.softmax(output.data.squeeze(), dim=0)

    # get highest confidence index and value 
    preds_sorted, idxs = output.sort(descending=True)
    #max, argmax = output.max(0)

    # extract classname from index
    idxs = idxs.numpy()[:3]

    class_keys = class_id_to_key[idxs]
    
    class_names = [key_to_classname[x] for x in class_keys]

    percent = (preds_sorted[:3].numpy() * 100).round(decimals=2)

    return render_template("image-classifier.html", filename=filename, prediction=class_names, confidence=percent, mail=current_app.config['MAIL_USERNAME'])