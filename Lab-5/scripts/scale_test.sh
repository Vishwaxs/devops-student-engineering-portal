#!/usr/bin/env bash
# ==============================================================================
# MCA DevOps Lab Exercise 5: Horizontal Application Scaling
# Demonstrates: Scale Up (2 -> 4 Replicas) & Scale Down (4 -> 3 Replicas)
# ==============================================================================
set -euo pipefail

NAMESPACE="devops-lab5"
DEPLOYMENT="student-k8s-app"

echo "=== [Phase 1: Current Replica State] ==="
kubectl get deployment "${DEPLOYMENT}" -n "${NAMESPACE}"
kubectl get pods -n "${NAMESPACE}" -l app=student-k8s-app

echo "=== [Phase 2: Scaling Up to 4 Replicas] ==="
kubectl scale deployment/"${DEPLOYMENT}" --replicas=4 -n "${NAMESPACE}"
kubectl rollout status deployment/"${DEPLOYMENT}" -n "${NAMESPACE}"

echo "--- Verifying 4 Pods Running ---"
kubectl get pods -n "${NAMESPACE}" -l app=student-k8s-app -o wide

echo "--- Verifying Service Endpoints (should show 4 target IPs) ---"
kubectl get endpoints student-k8s-service -n "${NAMESPACE}"

echo "=== [Phase 3: Scaling Down to 3 Replicas] ==="
kubectl scale deployment/"${DEPLOYMENT}" --replicas=3 -n "${NAMESPACE}"
kubectl rollout status deployment/"${DEPLOYMENT}" -n "${NAMESPACE}"

echo "--- Final 3 Replicas Verification ---"
kubectl get deployment "${DEPLOYMENT}" -n "${NAMESPACE}"
kubectl get pods -n "${NAMESPACE}" -l app=student-k8s-app

echo ">>> Scaling Verification Successfully Completed! <<<"
