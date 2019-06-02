#!/venv/bin python

import os, sys
from flask import Flask, Blueprint, current_app, render_template
import numpy as np

from fastai.vision import *
from object_detection_utils.RetinaNetFocalLoss import RetinaNetFocalLoss
from object_detection_utils.object_detection_helper import process_output, create_anchors, nms, rescale_boxes

object_detection = Blueprint('object_detection', __name__)

app = Flask(__name__)

model_links = {
  'resnet34': 'https://arxiv.org/pdf/1512.03385.pdf',
}

def init_learner(model_name):
    learn = load_learner(path='static/weights/', file='resnet34_bbox.pkl', device='cpu')
    return learn

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
    classes = [i for i in learn.data.train_ds.y.classes[1:]]
    thresh = 0.30
    nms_thresh = 0.1
    anchors = create_anchors(sizes=[(16,16),(8,8),(4,4)], ratios=[0.5, 1, 2], scales=[0.5, 0.6, 1, 1.25,])
    
    tfm_image = open_image(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)).apply_tfms(get_transforms()[0]).resize(256)
    pred = learn.model(tfm_image.data.unsqueeze(0).cpu())
    class_output, bbox_output = pred[:2]
    print('prediction done')
    bbox_pred, scores, preds = process_output(class_output[0], bbox_output[0], anchors, detect_thresh=thresh)

    while bbox_pred is None:
        print(f'lowering threshold to: {thresh}')
        thresh -= 0.05
        bbox_pred, scores, preds = process_output(class_output[0], bbox_output[0], anchors, detect_thresh=thresh)
    
    if bbox_pred is not None:
        to_keep = nms(bbox_pred, scores, nms_thresh)
        bbox_pred, preds, scores = bbox_pred[to_keep].cpu(), preds[to_keep].cpu(), scores[to_keep].cpu()
        t_sz = torch.Tensor([*tfm_image.size])[None].cpu()
        bbox_pred = to_np(rescale_boxes(bbox_pred, t_sz))
        # change from center to top left
        bbox_pred[:, :2] = bbox_pred[:, :2] - bbox_pred[:, 2:] / 2
        class_names = learn.data.train_ds.classes[1:][preds.item()] 
        print('extracted bounding box, classes and confidence')
        return render_template("object-detection.html",  prediction=True, filename=filename, name=model_name, 
                               link=model_link, mail=current_app.config['MAIL_USERNAME'])

    error = 'no suitable prediction found'
    print(error)
    return render_template("object-detection.html", error=error, prediction=True, filename=filename, 
                           name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])