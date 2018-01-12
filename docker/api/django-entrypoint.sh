#!/bin/bash
set -eo pipefail

# Define variables.
: ${RYR_API_API_PORT:=8000}

# Debug.
echo "PWD is ${PWD}"
ls -lh

# Migrate db, so we have the latest db schema.
python manage.py migrate

# Start development server on public ip interface, on port 8000.
exec gunicorn ${RYR_API_API_OPTS} -b 0.0.0.0:${RYR_API_API_PORT} api.wsgi
