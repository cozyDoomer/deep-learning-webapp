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

# download the weights for pnasnet5 from github release
RUN echo 'downloading image-classifier weights'
ADD https://gitreleases.dev/gh/DollofCuty/deep-learning-webapp/latest/pnasnet5large.pth webapp/static/weights/pnasnet5large.pth

# for resnet50/resnet152
#ADD https://download.pytorch.org/models/resnet152.pth webapp/static/weights/resnet152.pth

# alternatively one can download the weights with the link above and put them 
# to webapp/static/weights/resnet152.pth in the repository and copy with this:
#COPY webapp/static/weights/resnet152.pth webapp/static/weights/resnet152.pth

ENV FLASK_APP webapp/main.py

#recursive chown on file system
RUN chown -R webapp:webapp ./
USER webapp

#expose :5000 port
EXPOSE 5000

RUN cd webapp

ENTRYPOINT ["./boot.sh"] 