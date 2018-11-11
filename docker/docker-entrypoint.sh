#!/bin/bash
set -eo pipefail

# Define global variables.
: ${RYR_LOG_LEVEL:=info}

# Define API variables.
: ${RYR_API_API_PORT:=8000}

# Define Celery variables.
: ${RYR_API_CELERY_APP:=api.celery.worker}

# Compute variables.
DATE=$(date -u +%Y%m%dT%H%M%S%Z)

# Run the API.
if [ "$1" == "api" ]; then
  # Start WSGI server.
  exec gunicorn ${RYR_API_API_OPTS} --log-level ${RYR_LOG_LEVEL} -b 0.0.0.0:${RYR_API_API_PORT} api.wsgi
fi

# Run a Celery command.
if [ "$1" == "celery" ]; then
  # Start Celery command.
  exec $@ \
    -A ${RYR_API_CELERY_APP} \
    -l ${RYR_LOG_LEVEL} \
    --pidfile=celery_${CELERY_COMMAND}-${DATE}.pid
fi
