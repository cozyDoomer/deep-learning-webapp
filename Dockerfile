FROM ufoym/deepo:pytorch-py36-cpu

#add user webapp
RUN useradd -ms /bin/bash webapp

WORKDIR /home

#secret key is needed to keep the client-side sessions secure
RUN mkdir -p instance
RUN head -c 24 /dev/urandom > instance/secret_key

#pip libraries
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

#copy files and change execution permission of entrypoint
COPY webapp webapp
COPY boot.sh ./
RUN chmod +x boot.sh

RUN dir
WORKDIR webapp
RUN dir

# download the weights for pnasnet5 from github release
RUN echo 'downloading image-classifier weights'
ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/pnasnet5large.pth static/weights/pnasnet5large.pth

# for resnet50/resnet152
#ADD https://download.pytorch.org/models/resnet152.pth webapp/static/weights/resnet152.pth

# alternatively one can download the weights with the links above and put them 
# to webapp/static/weights/resnet152.pth in the repository and copy with this:
#COPY webapp/static/weights/resnet152.pth webapp/static/weights/resnet152.pth

ENV FLASK_APP main.py

#recursive chown on file system
RUN chown -R webapp:webapp ./

USER webapp

#expose :5000 port is not supported by heroku!
#EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:$PORT main:app

#CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - --error-logfile - main:app

#CMD gunicorn -c webapp/static/conf/gunicorn_config.py --access-logfile - --error-logfile - main:app

#ENTRYPOINT ["./boot.sh"] 