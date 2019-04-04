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

#download the weights for pnasnet5 from google drive
RUN echo 'downloading image-classifier weights'
RUN gdown https://drive.google.com/uc?id=1sifDhGShFfsLRr38gaC4NiodzW421QTv -O webapp/static/weights/pnasnet5large.pth

# alternatively one can download the weights with the link above and put them 
# to webapp/static/weights/pnasnet5large.pth in the repository and copy with this:
#COPY webapp/static/weights/pnasnet5large.pth webapp/static/weights/pnasnet5large.pth

ENV FLASK_APP webapp/main.py

#recursive chown on file system
RUN chown -R webapp:webapp ./
USER webapp

#expose :5000 port
EXPOSE 5000

RUN cd webapp

ENTRYPOINT ["./boot.sh"] 