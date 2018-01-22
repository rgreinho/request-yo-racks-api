#!/bin/bash
set -euo pipefail

NAMESPACE=default
MINIKUBE_IP=$(minikube ip)

# PostgreSQL
PG_RELEASE=postgresql-postgresql
PG_POD_NAME=$(kubectl get pods --namespace ${NAMESPACE} -l "app=${PG_RELEASE}" -o jsonpath="{.items[0].metadata.name}")
PG_USER=$(kubectl get po ${PG_POD_NAME} -o jsonpath="{.spec.containers[*].env[?(@.name=='PGUSER')].value}")
PG_PASSWORD=$(kubectl get secret --namespace ${NAMESPACE} ${PG_RELEASE} -o jsonpath="{.data.postgres-password}" | base64 --decode; echo)
PG_HOST=${MINIKUBE_IP}
PG_PORT=$(minikube service ${PG_RELEASE} --url | awk -F/ '{print $3}' | awk -F: '{print $2}')
PG_URL="postgres://${PG_USER}:${PG_PASSWORD}@${PG_HOST}:${PG_PORT}/postgres"

# Redis
REDIS_RELEASE=redis-redis
REDIS_POD_NAME=$(kubectl get pods --namespace ${NAMESPACE} -l "app=${REDIS_RELEASE}" -o jsonpath="{.items[0].metadata.name}")
REDIS_HOST=${MINIKUBE_IP}
REDIS_PORT=$(minikube service ${REDIS_RELEASE} --url | awk -F/ '{print $3}' | awk -F: '{print $2}')
REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT}"

# Export all generated env vars.
export DATABASE_URL=${PG_URL}
export REDIS_URL=${REDIS_URL}

# Display all generated env vars.
echo "The following variables have been generated and exported:"
echo "export DATABASE_URL=${PG_URL}"
echo "export REDIS_URL=${REDIS_URL}"
