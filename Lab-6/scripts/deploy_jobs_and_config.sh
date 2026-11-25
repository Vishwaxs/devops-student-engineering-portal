#!/usr/bin/env bash
# Reproducible script for Lab 6: Namespace, Jobs, CronJob, ConfigMap, and Safe Secret Creation
set -euo pipefail

NAMESPACE="devops-lab6"
LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== 1. Creating Dedicated Namespace ==="
kubectl apply -f "${LAB_DIR}/kubernetes/namespace.yaml"

echo "=== 2. Executing Batch Report Job ==="
kubectl apply -f "${LAB_DIR}/jobs/job.yaml"
kubectl wait --for=condition=complete job/student-batch-report-job -n "${NAMESPACE}" --timeout=90s
kubectl get jobs,pods -n "${NAMESPACE}"
JOB_POD=$(kubectl get pods -n "${NAMESPACE}" -l job=student-batch-report-job -o jsonpath='{.items[0].metadata.name}')
kubectl logs "${JOB_POD}" -n "${NAMESPACE}"

echo "=== 3. Applying Scheduled CronJob (Suspended after verification in lab demo) ==="
kubectl apply -f "${LAB_DIR}/jobs/cronjob.yaml"
kubectl get cronjobs -n "${NAMESPACE}"

echo "=== 4. Creating ConfigMap (Non-Sensitive Runtime Config) ==="
kubectl apply -f "${LAB_DIR}/kubernetes/configmap.yaml"
kubectl describe configmap student-app-config -n "${NAMESPACE}"

echo "=== 5. Creating Dummy Demonstration Secret Safely ==="
# Do not commit real credentials. Temporary env-file avoids echoing values into shell history logs.
TMP_CREDS=$(mktemp)
printf 'APP_USERNAME=demo-user\nAPP_PASSWORD=demo-password\n' > "${TMP_CREDS}"
kubectl delete secret app-credentials -n "${NAMESPACE}" 2>/dev/null || true
kubectl create secret generic app-credentials --from-env-file="${TMP_CREDS}" -n "${NAMESPACE}"
rm -f "${TMP_CREDS}"
kubectl describe secret app-credentials -n "${NAMESPACE}"
