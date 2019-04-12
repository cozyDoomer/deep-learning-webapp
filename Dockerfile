FROM ufoym/deepo:pytorch-py36-cpu

# add user webapp
RUN useradd -ms /bin/bash webapp

WORKDIR /home

# secret key is needed to keep the client-side sessions secure
RUN mkdir -p  webapp/instance
RUN head -c 24 /dev/urandom > webapp/instance/secret_key

# pip libraries
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

# copy files and change execution permission of entrypoint
COPY webapp webapp

WORKDIR webapp

# download the weights for pnasnet5 from github release
RUN echo 'downloading image-classifier weights'

# pnasnet5, requires quite some ram and cpu
#ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/pnasnet5.pth static/weights/pnasnet5.pth
#ENV NNET pnasnet5

# resnet152
#ADD https://download.pytorch.org/models/resnet152-b121ed2d.pth static/weights/resnet152.pth
#ENV NNET resnet152

# resnet50
ADD https://download.pytorch.org/models/resnet50-19c8e357.pth static/weights/resnet50.pth
ENV NNET resnet50

# alternatively download the weights for one model with the links above 
# store them in webapp/static/weights/<model>.pth in the local repository 
# (keep the <100MB single file limit of github in mind) and copy with this:
#COPY webapp/static/weights/<model>.pth webapp/static/weights/<model>.pth

ENV FLASK_APP main.py
ENV PYTHONUNBUFFERED TRUE

#recursive chown on file system for the webapp user
RUN chown -R webapp:webapp ./

USER webapp

# expose :5000 port is not supported by heroku!
#EXPOSE 5000

CMD gunicorn -R --bind 0.0.0.0:$PORT main:app

#ENTRYPOINT ["./boot.sh"] 