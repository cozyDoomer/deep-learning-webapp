#!/bin/bash

source venv/bin/activate
cd webapp
exec gunicorn -c static/conf/gunicorn_config.py --access-logfile - --error-logfile - main:app