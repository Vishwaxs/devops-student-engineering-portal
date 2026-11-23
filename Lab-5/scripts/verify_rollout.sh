#!/usr/bin/env bash
# ==============================================================================
# MCA DevOps Lab Exercise 5: Rolling Update with Continuous HTTP Traffic Audit
# Sends continuous requests while deployment v2 rolls out to verify zero-downtime
# ==============================================================================
set -euo pipefail

NAMESPACE="devops-lab5"
MANIFESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../kubernetes" && pwd)"
TARGET_URL="${1:-http://127.0.0.1:8080/version}"
LOG_FILE="/tmp/rollout_traffic.log"
rm -f "${LOG_FILE}"

echo "======================================================================"
echo " Starting Continuous Traffic Audit for Zero-Downtime Rolling Update"
echo " Target Endpoint : ${TARGET_URL}"
echo " Namespace       : ${NAMESPACE}"
echo "======================================================================"

# Step 1: Pre-flight check
echo -n "[Check] Verifying target endpoint availability... "
HTTP_CHECK=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "${TARGET_URL}" || echo "000")
if [ "${HTTP_CHECK}" != "200" ]; then
  echo "FAILED (HTTP ${HTTP_CHECK})"
  echo "ERROR: Target endpoint is not reachable at ${TARGET_URL}."
  echo "Start port-forward or NodePort service before executing traffic test:"
  echo "  kubectl port-forward -n ${NAMESPACE} svc/student-k8s-service 8080:80"
  exit 1
fi
echo "OK (HTTP 200)"

# Step 2: Launch background traffic generator
echo "[Traffic] Starting background continuous request worker..."
STOP_FLAG="/tmp/stop_rollout_worker"
rm -f "${STOP_FLAG}"

(
  REQ_ID=0
  while [ ! -f "${STOP_FLAG}" ]; do
    REQ_ID=$((REQ_ID + 1))
    TIMESTAMP=$(date +"%T")
    # Capture HTTP code and JSON body
    RESP=$(curl -s -w "\n%{http_code}" --connect-timeout 1 "${TARGET_URL}" 2>/dev/null || echo -e "\n000")
    BODY=$(echo "${RESP}" | head -n -1)
    CODE=$(echo "${RESP}" | tail -n 1)
    
    # Extract version if present
    VERSION=$(echo "${BODY}" | grep -o '"version":"[^"]*"' | cut -d':' -f2 | tr -d '"' || echo "unknown")
    echo "${REQ_ID}|${TIMESTAMP}|${CODE}|${VERSION}" >> "${LOG_FILE}"
    sleep 0.1
  done
) &
WORKER_PID=$!

echo "[Traffic] Worker active (PID: ${WORKER_PID}). Capturing baseline traffic..."
sleep 2

# Step 3: Trigger Rolling Update
echo "[Rollout] Applying updated deployment manifest (05-deployment-v2.yaml)..."
kubectl apply -f "${MANIFESTS_DIR}/05-deployment-v2.yaml"

echo "[Rollout] Monitoring rollout status in real-time..."
kubectl rollout status deployment/student-k8s-app -n "${NAMESPACE}"

# Step 4: Allow brief post-rollout stabilization
sleep 2

# Step 5: Stop worker and signal shutdown
touch "${STOP_FLAG}"
wait "${WORKER_PID}" 2>/dev/null || true
rm -f "${STOP_FLAG}"

# Step 6: Detailed Analysis of Traffic Results
echo ""
echo "======================================================================"
echo "                  TRAFFIC AUDIT SUMMARY RESULTS                       "
echo "======================================================================"

if [ ! -f "${LOG_FILE}" ] || [ ! -s "${LOG_FILE}" ]; then
  echo "STATUS: UNVERIFIED (No traffic logs were recorded)"
  exit 1
fi

TOTAL_REQUESTS=$(wc -l < "${LOG_FILE}")
SUCCESS_200=$(grep -c "|200|" "${LOG_FILE}" || true)
NON_200=$((TOTAL_REQUESTS - SUCCESS_200))
V1_COUNT=$(grep -c "|v1.0.0" "${LOG_FILE}" || true)
V2_COUNT=$(grep -c "|v2.0.0" "${LOG_FILE}" || true)

echo "Total HTTP Requests Sent : ${TOTAL_REQUESTS}"
echo "Successful (HTTP 200 OK)  : ${SUCCESS_200}"
echo "Failed / Dropped Requests : ${NON_200}"
echo "Requests served by v1.0.0: ${V1_COUNT}"
echo "Requests served by v2.0.0: ${V2_COUNT}"

echo ""
echo "HTTP Status Code Breakdown:"
awk -F'|' '{print $3}' "${LOG_FILE}" | sort | uniq -c | while read -r COUNT STATUS; do
  echo "  HTTP ${STATUS}: ${COUNT} requests"
done

echo "======================================================================"
if [ "${TOTAL_REQUESTS}" -gt 10 ] && [ "${NON_200}" -eq 0 ]; then
  echo "VERIFICATION RESULT: PASS"
  echo "Zero downtime achieved. 100% of requests returned HTTP 200 during transition."
elif [ "${NON_200}" -gt 0 ]; then
  echo "VERIFICATION RESULT: FAIL"
  echo "Downtime detected! ${NON_200} requests failed during the rolling update."
  exit 1
else
  echo "VERIFICATION RESULT: INCONCLUSIVE (Insufficient sample size: ${TOTAL_REQUESTS} requests)"
  exit 1
fi
