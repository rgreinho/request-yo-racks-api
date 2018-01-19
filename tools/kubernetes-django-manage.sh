#!/bin/bash
set -euo pipefail

API_POD=$(kubectl get pod -l app=api -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it ${API_POD} -- python manage.py $@
