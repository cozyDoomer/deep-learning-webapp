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

#move the weights to pytorch directory
RUN mkdir -p home/webapp/.torch 
COPY webapp/static/weights/pnasnet5large.pth webapp/.torch/models/pnasnet5large-bf079911.pth 

ENV FLASK_APP webapp/main.py

#recursive chown on file system
RUN chown -R webapp:webapp ./
USER webapp

#expose :5000 port
EXPOSE 5000

RUN cd webapp

ENTRYPOINT ["./boot.sh"] 