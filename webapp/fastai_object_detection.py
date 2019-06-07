#!/venv/bin python

import os
import sys
from flask import Flask, Blueprint, current_app, render_template
import numpy as np

from fastai.vision import *
from object_detection_utils.RetinaNetFocalLoss import RetinaNetFocalLoss
from object_detection_utils.object_detection_helper import process_output, create_anchors, nms, rescale_boxes, draw_bbox_on_orig, filter_predictions

object_detection = Blueprint('object_detection', __name__)

app = Flask(__name__)

model_links = {
    'resnet34': 'https://arxiv.org/pdf/1512.03385.pdf',
}


def init_learner(model_name):
    learn = load_learner(path='static/weights/',
                         file='retinanet_resnet34.pkl', device='cpu')
    learn.model = learn.model.eval()
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
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    print(f'model name: {model_name}')

    if not os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        print('error, filename not found in static/uploads/<filename>')
        return render_template("object-detection.html", filename=filename, name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])

    anchors = create_anchors(sizes=[(16, 16), (8, 8), (4, 4)], ratios=[
                             0.5, 1, 2], scales=[0.5, 0.6, 1, 1.25, ])
    tfm_image = open_image(image_path).resize(256)
    learn = init_learner(model_name)
    classes = [i for i in learn.data.train_ds.y.classes[1:]]
    print('init model successfully')

    pred = learn.model(tfm_image.data.unsqueeze(0).cpu())
    class_output, bbox_output = pred[:2]
    bbox_preds, preds, scores = filter_predictions(
        tfm_image, class_output[0], bbox_output[0], anchors, thresh=0.15)
    print('prediction done')

    # change from center to top left
    bbox_preds[:, :2] = bbox_preds[:, :2] - bbox_preds[:, 2:] / 2
    print(f'bbox on 256 size: {bbox_preds}')

    class_names = [learn.data.train_ds.classes[1:][pred.item()]
                   for pred in preds]
    print(f'predicted classes: {class_names}')

    img = draw_bbox_on_orig(image_path, tfm_image, [
                            score.item() for score in scores], bbox_preds, class_names)
    print(f'bbox on 256 size: {bbox_preds}')

    ext = filename.rfind('.')
    fname_bbox = f'{filename[:ext]}_bbox{filename[ext:]}'
    img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fname_bbox))
    print(f'saved original image with bbox')

    return render_template("object-detection.html",  prediction=True, filename=fname_bbox, name=model_name,
                           link=model_link, mail=current_app.config['MAIL_USERNAME'])
