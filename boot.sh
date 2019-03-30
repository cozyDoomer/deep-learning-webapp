#!/bin/bash

source venv/bin/activate
cd webapp
exec gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - main:app
#exec python main.py 