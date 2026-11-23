#!/usr/bin/env bash
# ==============================================================================
# MCA DevOps Lab Exercise 5: Deployment Rollback Verification
# Demonstrates: kubectl rollout undo back to previous stable revision
# ==============================================================================
set -euo pipefail

NAMESPACE="devops-lab5"
DEPLOYMENT="student-k8s-app"

echo "=== [Step 1: Inspect Rollout History Before Rollback] ==="
kubectl rollout history deployment/"${DEPLOYMENT}" -n "${NAMESPACE}"

echo "=== [Step 2: Executing Rollback to Revision 1 (v1.0.0)] ==="
kubectl rollout undo deployment/"${DEPLOYMENT}" -n "${NAMESPACE}" --to-revision=1

echo "=== [Step 3: Waiting for Rollback to Settle] ==="
kubectl rollout status deployment/"${DEPLOYMENT}" -n "${NAMESPACE}"

echo "=== [Step 4: Verifying Rollback Pods & Version] ==="
kubectl get pods -n "${NAMESPACE}" -l app=student-k8s-app -o wide
kubectl get rs -n "${NAMESPACE}" -l app=student-k8s-app
kubectl rollout history deployment/"${DEPLOYMENT}" -n "${NAMESPACE}"

echo ">>> Rollback Successfully Verified! <<<"
