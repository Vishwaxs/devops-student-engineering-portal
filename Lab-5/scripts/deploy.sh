#!/usr/bin/env bash
# ==============================================================================
# MCA DevOps Lab Exercise 5: Kubernetes Deployment Script
# Deploys: Namespace, ConfigMap, Deployment v1, Service
# ==============================================================================
set -euo pipefail

NAMESPACE="devops-lab5"
MANIFESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../kubernetes" && pwd)"

echo "=== [Step 1] Applying Kubernetes Namespace ==="
kubectl apply -f "${MANIFESTS_DIR}/01-namespace.yaml"

echo "=== [Step 2] Applying ConfigMap ==="
kubectl apply -f "${MANIFESTS_DIR}/02-configmap.yaml"

echo "=== [Step 3] Applying Deployment v1.0.0 (2 Replicas) ==="
kubectl apply -f "${MANIFESTS_DIR}/03-deployment-v1.yaml"

echo "=== [Step 4] Applying Service (NodePort :30080 & ClusterIP :80) ==="
kubectl apply -f "${MANIFESTS_DIR}/04-service.yaml"

echo "=== [Step 5] Waiting for Deployment Rollout to Complete ==="
kubectl rollout status deployment/student-k8s-app -n "${NAMESPACE}" --timeout=120s

echo "=== [Step 6] Verification of Cluster Resources ==="
echo "--- Deployments ---"
kubectl get deployments -n "${NAMESPACE}" -o wide
echo "--- ReplicaSets ---"
kubectl get rs -n "${NAMESPACE}"
echo "--- Pods ---"
kubectl get pods -n "${NAMESPACE}" -o wide --show-labels
echo "--- Services & Endpoints ---"
kubectl get svc,endpoints -n "${NAMESPACE}"

echo ">>> Deployment v1 Successfully Active and Serving Traffic! <<<"
