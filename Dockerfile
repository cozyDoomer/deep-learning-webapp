FROM pytorch/pytorch

#add user webapp
RUN useradd -ms /bin/bash webapp

WORKDIR /home

#secret key gen
RUN mkdir -p instance
RUN head -c 24 /dev/urandom > instance/secret_key

#pip libraries
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

#copy files and change execution permission of entrypoint
COPY webapp webapp
COPY boot.sh ./
RUN chmod +x boot.sh

#move the weights to pytorch directory
RUN mkdir -p home/webapp/.torch 
COPY webapp/static/models/pnasnet5large-bf079911.pth webapp/.torch/models/pnasnet5large-bf079911.pth 
run rm -rf home/webapp/static/models

ENV FLASK_APP webapp/main.py

#recursive chown on file system
RUN chown -R webapp:webapp ./
USER webapp

#expose :5000 port
EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
