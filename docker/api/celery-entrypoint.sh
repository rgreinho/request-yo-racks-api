#!/bin/bash

# Read entrypoint parameters.
CELERY_COMMAND=${1:-worker}

# Define variables.
: ${RYR_API_CELERY_APP:=api.celery}
: ${RYR_API_CELERY_LOG_LEVEL:=info}

# Start Celery command.
DATE=$(date -u +%Y%m%dT%H%M%S%Z)
su -m celery -c "celery ${CELERY_COMMAND} \
  -A ${RYR_API_CELERY_APP} \
  -l ${RYR_API_CELERY_LOG_LEVEL} \
  --pidfile=celery_${CELERY_COMMAND}-${DATE}.pid"
