# personal image-classifier webapp

## Getting Started

It would be a good idea to fork the repository because there is a lot of personal information on the website 

things that would need to be changed for your own website: 

- change personal information in home.html and cv.html 

- include Photos for the frontend 

- include your own cv named cv.pdf in ./webapp/documents

Everything is under MIT license so feel free to change and tear apart everything, I'd be happy about a shoutout.

## personal website I use including a pytorch image-classifier

## Frontend

Simple html/css template not a lot of javascript 
    
- Thinking about using a bootstrap theme and rebuild the frontend

## Backend

Flask: micro webframework for Python based on Werkzeug, Jinja 2

## Gunicorn

Python WSGI HTTP Server for UNIX

acts as webserver accepting requests from Flask

- TODO: add Nginx as reverse Proxy and load balancer (probably not needed for my own site but can't hurt)

## Docker 

The dockerfile builds some layers on top of the pytorch-cpu docker from [Deepo](https://github.com/ufoym/deepo) 

The specific docker is: ufoym/deepo:pytorch-py36-cpu

# Installing

## Clone Repo or fork
```
git clone https://github.com/DollofCuty/deep-learning-webapp.git
```

# How to run

## With Docker (Linux, Mac, Windows)

```
docker build -t webapp:latest .
```
```
docker run -p 5000:5000 webapp
```

## Flask only

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