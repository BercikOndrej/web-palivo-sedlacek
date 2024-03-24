#!/bin/sh

set -e

# Collect static files to one place
python manage.py collectstatic --noinput

# Command to start our app on port 8000 
# --master runs app as master thread (in background) and not in the foreground
# --enable-threads enable multi-threading in our uwsgi server
uwsgi --socket :8000 --workers 4 --master --enable-threads --module web.wsgi