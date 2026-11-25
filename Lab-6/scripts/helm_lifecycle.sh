#!/usr/bin/env bash
# Reproducible script for Lab 6: Helm Chart Validation, Install, Upgrade, History, and Rollback
set -euo pipefail

NAMESPACE="devops-lab6"
LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHART_DIR="${LAB_DIR}/helm/student-app"

echo "=== 1. Linting and Rendering Helm Chart ==="
helm lint "${CHART_DIR}"
helm template student-app "${CHART_DIR}" > /dev/null
echo "Template rendering succeeded."

echo "=== 2. Installing Baseline Release (Revision 1) ==="
helm install student-app "${CHART_DIR}" -n "${NAMESPACE}" --create-namespace
kubectl rollout status deployment/student-app -n "${NAMESPACE}" --timeout=90s
helm list -n "${NAMESPACE}"

echo "=== 3. Upgrading Release with values-dev.yaml Override (Revision 2) ==="
helm upgrade student-app "${CHART_DIR}" -n "${NAMESPACE}" -f "${CHART_DIR}/values-dev.yaml"
kubectl rollout status deployment/student-app -n "${NAMESPACE}" --timeout=90s
helm history student-app -n "${NAMESPACE}"

echo "=== 4. Rolling Back Release to Revision 1 (Revision 3) ==="
helm rollback student-app 1 -n "${NAMESPACE}"
kubectl rollout status deployment/student-app -n "${NAMESPACE}" --timeout=90s
helm history student-app -n "${NAMESPACE}"
helm status student-app -n "${NAMESPACE}"
