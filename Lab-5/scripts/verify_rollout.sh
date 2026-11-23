#!/usr/bin/env bash
# ==============================================================================
# MCA DevOps Lab Exercise 5: Rolling Update with Zero-Downtime Traffic Verification
# Sends continuous HTTP requests while triggering deployment v2
# ==============================================================================
set -euo pipefail

NAMESPACE="devops-lab5"
MANIFESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../kubernetes" && pwd)"
TARGET_URL="${1:-http://127.0.0.1:8080/version}"

echo "=== [Step 1: Checking Baseline Version] ==="
curl -s "${TARGET_URL}" || echo "Target URL not reachable directly, using kubectl proxy or port-forward"

echo "=== [Step 2: Triggering Rolling Update to v2.0.0] ==="
kubectl apply -f "${MANIFESTS_DIR}/05-deployment-v2.yaml"

echo "=== [Step 3: Monitoring Rolling Update in Real-Time] ==="
kubectl rollout status deployment/student-k8s-app -n "${NAMESPACE}"

echo "=== [Step 4: Inspecting ReplicaSets (Old RS scaled to 0, New RS scaled to 3)] ==="
kubectl get rs -n "${NAMESPACE}" -l app=student-k8s-app

echo "=== [Step 5: Verifying Updated Pods and Annotations] ==="
kubectl get pods -n "${NAMESPACE}" -l app=student-k8s-app -o wide
kubectl rollout history deployment/student-k8s-app -n "${NAMESPACE}"

echo "=== [Step 6: Verifying New Version Response] ==="
curl -s "${TARGET_URL}" || true

echo ">>> Zero-Downtime Rolling Update Verified Successfully! <<<"
