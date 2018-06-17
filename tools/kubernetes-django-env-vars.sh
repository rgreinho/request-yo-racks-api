#!/bin/bash
set -euo pipefail

NAMESPACE=default
MINIKUBE_IP=$(minikube ip)

# PostgreSQL
PG_RELEASE=postgresql
PG_POD_NAME=$(kubectl get pods --namespace ${NAMESPACE} -l "app=${PG_RELEASE}" -o jsonpath="{.items[0].metadata.name}")
PG_USER=$(kubectl get po ${PG_POD_NAME} -o jsonpath="{.spec.containers[*].env[?(@.name=='PGUSER')].value}")
PG_PASSWORD=$(kubectl get secret --namespace ${NAMESPACE} ${PG_RELEASE} -o jsonpath="{.data.postgres-password}" | base64 --decode; echo)
PG_HOST=${MINIKUBE_IP}
PG_PORT=$(minikube service ${PG_RELEASE} --url | awk -F/ '{print $3}' | awk -F: '{print $2}')
PG_URL="postgres://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/postgres"

# Redis
REDIS_RELEASE=redis
REDIS_POD_NAME=$(kubectl get pods --namespace ${NAMESPACE} -l "app=${REDIS_RELEASE}" -o jsonpath="{.items[0].metadata.name}")
REDIS_HOST=${MINIKUBE_IP}
REDIS_PORT=$(minikube service ${REDIS_RELEASE}-master --url | awk -F/ '{print $3}' | awk -F: '{print $2}')
REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT}/0"

# Export all generated env vars.
export DATABASE_URL=${PG_URL}
export REDIS_URL=${REDIS_URL}

# Export Celery variables.
export CELERY_BROKER_URL=${REDIS_URL}
export CELERY_RESULT_BACKEND=${REDIS_URL}

# Display all generated env vars.
echo "export DATABASE_URL=${PG_URL}"
echo "export REDIS_URL=${REDIS_URL}"
echo "export CELERY_BROKER_URL=${REDIS_URL}"
echo "export CELERY_RESULT_BACKEND=${REDIS_URL}"
echo "# The previous variables have been generated and exported."
