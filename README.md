# personal image-classifier webapp

## Getting Started

It would be a good idea to fork the repository because there is a lot of personal information on the website 

things that would need to be changed for your own website: 

- change personal information in home.html and cv.html 

- include Photos for the frontend 

- add email configuration under webapp/static/conf/email_conf.py

    - format: see email_conf_example.py, MAIL_SERVER and MAIL_PORT need to be changed depending on your provider

    - if you get an google api error take a look at this [answer](https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail)

- include your own cv named cv.pdf in ./webapp/documents

# Installing

## Clone Repo or fork
```
git clone https://github.com/DollofCuty/deep-learning-webapp.git
```

# How to run

## With docker-compose

## This includes nginx and letsencrypt setup so you have to do the following steps:

- change environment parameters on gunicorn docker in docker-compose.yml:
    - LETSENCRYPT_EMAIL=[your-email]
    - LETSENCRYPT_HOST=[your-domain-name]
    - VIRTUAL_HOST=[your-domain-name]
    - The domain has to be valid and connected with the [instance you are running docker-compose on](https://cloud.google.com/dns/docs/quickstart)
    - then for namecheap.com I had to choose custom dns and enter the ns-cloud nameservers (this should be possible for all domain registrars)

- set up a google cloud instance with [container-optimized-os](https://cloud.google.com/community/tutorials/docker-compose-on-container-optimized-os)
    - also follow the section 'Making an alias to Docker Compose' to shorten the commands for the future

```
docker network create webproxy
```
```
docker-compose up
```

The first time you run this will take some time because it has to build all the containers (web, nginx-web, nginx-gen, nginx-letsencrypt)
and then nginx-letsencrypt will request a certificate

If all went well the webservice should use nginx and the letsencrypt certificate to run on https, with reverse proxy and serving static files

### updating the docker-compose setup (when you change the Dockerfile for example)

```
docker-compose build
```

### freeing disk space if you have dangling/unnecassary images (this removes all unused images!)

for reference look at the [docker docs](https://docs.docker.com/engine/reference/commandline/system_prune/)

```
docker system prune -a
```


## With docker (Linux, Mac, Windows)

## This does not include nginx and https connection!

```
docker build -t webapp:latest .
```
```
docker run -p 8080:8080 webapp
```

## Flask/gunicorn wrapper only

(useful for testing)

prerequisites:

- Python3
- Pip

```
python -m venv virtual_env
```

```
virtual_env/bin/pip install -r requirements.txt
```

### linux/mac

```
source virtual_env/env/activate
```

### windows 

```
./virtual_env/env/activate
```

and then finally

```
python main.py
```

# Details

## personal website I use including a pytorch image-classifier

## Frontend

Simple html/css template with minimal javascript 
    
- Thinking about using a bootstrap theme and rebuild the frontend

## Backend

Flask: micro webframework for Python based on Werkzeug, Jinja 2

## Gunicorn

Python WSGI HTTP Server for UNIX

acts as webserver accepting requests from Flask

## Docker 

The Dockerfile builds some layers on top of the pytorch-cpu docker from [Deepo](https://github.com/ufoym/deepo) 

The specific docker is: ufoym/deepo:pytorch-py36-cpu
