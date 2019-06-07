#!/venv/bin python

import os
from flask import Flask, Blueprint, current_app, render_template

from torch.nn.functional import softmax

from pnasnet import pnasnet5
from resnet import resnet50, resnet152

import utils

image_classifier = Blueprint('image_classifier', __name__)

app = Flask(__name__)

model_links = {
    'pnasnet5': 'https://arxiv.org/pdf/1712.00559.pdf',
    'resnet152': 'https://arxiv.org/pdf/1512.03385.pdf',
    'resnet50': 'https://arxiv.org/pdf/1512.03385.pdf',
    'inceptionresnetv2': 'https://arxiv.org/pdf/1602.07261.pdf'
}


def init_model(model_name):
    # initialize model depending on env. variable set in dockerfile
    if model_name == 'pnasnet5':
        model = pnasnet5(pretrained=True)
    elif model_name == 'resnet152':
        model = resnet152(pretrained=True)
    elif model_name == 'resnet50':
        model = resnet50(pretrained=True)
    return model


def get_name():
    return os.getenv('NNET', 'resnet50')  # resnet50 default


@image_classifier.route("/image-classifier")
def show():
    model_name = get_name()
    model_link = model_links[model_name]

    return render_template("image-classifier.html", mail=current_app.config['MAIL_USERNAME'], name=model_name, link=model_link)


@image_classifier.route("/image-classifier/<filename>")
def analyze(filename):
    model_name = get_name()
    model_link = model_links[model_name]
    print(f'model name: {model_name}')

    if not os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        print('error, filename not found in static/uploads/<filename>')
        return render_template("image-classifier.html", filename=filename, name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])

    model = init_model(model_name)
    print('init model successfully')

    model.eval()
    # loading image uploaded to the server
    load_img = utils.LoadImage()
    # rescale, center crop, normalize, and others (ex: ToBGR, ToRange255)
    tf_img = utils.TransformImage(model)
    print('rescale, center crop, normalize done')

    # 3x600x500 -> 3x299x299 size may differ
    tensor = tf_img(load_img(os.path.join(
        current_app.config['UPLOAD_FOLDER'], filename)))
    tensor = tensor.unsqueeze(0)  # 3x299x299 -> 1x3x299x299

    # Load Imagenet Synsets
    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_synsets.txt'), 'r') as f:
        synsets = f.readlines()

    # create index: class dictionary
    synsets = [x.strip() for x in synsets]
    synsets = [line.split(' ') for line in synsets]
    key_to_classname = {spl[0]: ' '.join(spl[1:]) for spl in synsets}

    with open(os.path.join(current_app.config['IMAGENET_FOLDER'], 'imagenet_classes.txt'), 'r') as f:
        class_id_to_key = f.readlines()

    class_id_to_key = [x.strip() for x in class_id_to_key]

    # Make predictions
    output = model(tensor)  # size(1, 1000)
    print('prediction done')

    # Softmax to get confidence summing up to 1
    output = softmax(output.data.squeeze(), dim=0)

    # sort by highest confidence index and value
    preds_sorted, idxs = output.sort(descending=True)

    # extract classname from index
    idxs = idxs.numpy()[:3]

    class_keys = [class_id_to_key[i] for i in idxs]
    class_names = [', '.join(
        [str(y) for y in key_to_classname[x].split(",", 2)[:2]]) for x in class_keys]
    percent = (preds_sorted[:3].numpy() * 100).round(decimals=2)

    print(f'predicted classes: {class_names}')
    print(f'confidence: {percent}')

    return render_template("image-classifier.html", filename=filename, prediction=class_names, confidence=percent,
                           name=model_name, link=model_link, mail=current_app.config['MAIL_USERNAME'])
