FROM python:3.6.8-slim

RUN export DEBIAN_FRONTEND=noninteractive \
  && echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
  && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
  && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
  && apt-get update && apt-get install -y locales \
  && locale-gen en_US.UTF-8 \
  && rm -rf /var/lib/apt/lists/* \
  \
  && pip install https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl \
                 https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl \
                 matplotlib==3.0.3 \
  && rm -rf /root/.cache/pip

ENV LANG=en_US.UTF-8 \
  LANGUAGE=en_US:en \
  LC_ALL=en_US.UTF-8

# add user webapp
RUN useradd -ms /bin/bash webapp

WORKDIR /home

# pip libraries
COPY requirements.txt requirements.txt
#RUN pip install torch torchvision
RUN pip install -r requirements.txt --no-deps

# copy files and change execution permission of entrypoint
COPY webapp webapp
WORKDIR webapp

# secret key is needed to keep the client-side sessions secure
RUN mkdir -p  instance
RUN head -c 24 /dev/urandom > instance/secret_key

# download the weights for pnasnet5 from github release
RUN echo 'downloading image-classifier weights'

# Image Classification

# Pytorch
#ENV CLASSIFICATIONLIBRARY pytorch

# pnasnet-5, requires quite some ram and cpu
#ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/pnasnet5.pth static/weights/pnasnet5.pth
#ENV NNET pnasnet5

# Resnet-152
#ADD https://download.pytorch.org/models/resnet152-b121ed2d.pth static/weights/resnet152.pth
#ENV NNET resnet152

# Resnet-50
#ADD https://download.pytorch.org/models/resnet50-19c8e357.pth static/weights/resnet50.pth
#ENV NNET resnet50

# fastai 
ENV CLASSIFICATION-LIBRARY fastai

# Inception-Resnetv2
ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/inceptionresnetv2.pkl static/weights/inceptionresnetv2.pkl
ENV NNET inceptionresnetv2


# Object Detection
# RetinaNet with ResNet-34 backbone
ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/retinanet_resnet34.pkl static/weights/retinanet_resnet34.pkl

# alternatively download the weights for one model with the links above 
# store them in webapp/static/weights/<model>.pth in the local repository 
# (keep the <100MB single file limit of github in mind) and copy with this:
#COPY webapp/static/weights/<model>.pth webapp/static/weights/<model>.pth

ENV FLASK_APP main.py
ENV PYTHONUNBUFFERED TRUE

#recursive chown on file system for the webapp user
RUN chown -R webapp:webapp ./

USER webapp

EXPOSE 8080

CMD gunicorn -R --max-requests 20 --bind 0.0.0.0:8080 --timeout 300 main:app 

#ENTRYPOINT ["./boot.sh"] 
