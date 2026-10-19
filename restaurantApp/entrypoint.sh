#!/bin/sh

set -e

flask db upgrade

exec gunicorn --config gunicorn.conf.py wsgi:app