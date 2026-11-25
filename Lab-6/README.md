# MCA DevOps Lab Exercise 6 — Kubernetes Jobs, CronJobs, ConfigMaps, Secrets & Helm

**Course:** 2026-5 MCA B-DevOps  
**Faculty:** Cynthia T Computer Science  
**Assignment:** Lab Exercise - 6 (100 Points)  
**Git Branch:** `feature/devops-lab-6-jobs-cronjobs-helm`  
**Cluster Verified On:** Killercoda Kubernetes (`v1.37.1`, 2 nodes: `controlplane`, `node01`), Helm `v4.3.0`, Docker `29.1.3`

---

## 1. Aim
Implement and verify finite Kubernetes batch execution (`Job`), scheduled automation (`CronJob`), non-sensitive and sensitive runtime configuration (`ConfigMap` and `Secret`), and packaged release management (`Helm`) on an active Kubernetes cluster.

---

## 2. Project Directory Structure

```text
Lab-6/
├── app/
│   ├── src/
│   │   ├── public/style.css
│   │   └── server.js                    # Express server (/healthz, /ready, /config, /secret-status)
│   ├── Dockerfile                       # Multi-stage Node.js 20 Alpine non-root build
│   ├── .dockerignore
│   └── package.json
├── jobs/
│   ├── job.yaml                         # student-batch-report-job (500-record Node.js batch summary)
│   ├── job-retry-test.yaml              # retry-demo-job (temporary failing Job for backoffLimit test)
│   └── cronjob.yaml                     # periodic-audit-cronjob (scheduled audit, concurrencyPolicy: Forbid)
├── kubernetes/
│   ├── namespace.yaml                   # devops-lab6 namespace
│   ├── configmap.yaml                   # Non-sensitive configuration (student-app-config)
│   ├── secret-example.yaml              # Dummy sample template (no real credentials)
│   └── deployment-standalone.yaml       # Standalone Deployment + NodePort :30085 for ConfigMap/Secret tests
├── helm/
│   └── student-app/                     # Custom Helm chart
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── .helmignore
│       ├── README.md
│       └── templates/
│           ├── _helpers.tpl
│           ├── configmap.yaml
│           ├── deployment.yaml
│           ├── service.yaml             # NodePort :30086
│           └── NOTES.txt
├── scripts/
│   ├── deploy_jobs_and_config.sh
│   ├── helm_lifecycle.sh
│   └── build_lab6_pdf.py
├── evidence/                            # Original Chrome/Killercoda screenshots
├── COMMAND_REFERENCE.md
├── Lab6_DevOps_Kubernetes_Report.pdf
├── .gitignore
└── README.md
```

---

## 3. Environment Requirements
- Kubernetes cluster (`v1.37.1` verified on Killercoda `controlplane` + `node01`)
- `kubectl` CLI
- `helm` (`v4.3.0` verified)
- Docker Engine (`29.1.3` verified) & `ctr` (`containerd://2.2.1`)

---

## 4. Build and Load Container Image

```bash
cd Lab-6
docker build -t student-app:1.0.0 ./app
docker images student-app

# Import built image into Kubernetes containerd runtime on both cluster nodes
docker save student-app:1.0.0 | ctr -n k8s.io images import -
docker save student-app:1.0.0 | ssh node01 ctr -n k8s.io images import -

# Verify container endpoint directly
docker run -d --rm -p 18080:8080 --name test-app student-app:1.0.0
curl -s http://127.0.0.1:18080/healthz
docker stop test-app
```

---

## 5. Step-by-Step Execution Commands

### A. Namespace Setup
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl get ns devops-lab6
```

### B. Kubernetes Job (`student-batch-report-job`)
```bash
kubectl apply -f jobs/job.yaml
kubectl get jobs -n devops-lab6
kubectl get pods -n devops-lab6
kubectl describe job student-batch-report-job -n devops-lab6
JOB_POD=$(kubectl get pods -n devops-lab6 -l job=student-batch-report-job -o jsonpath='{.items[0].metadata.name}')
kubectl logs "$JOB_POD" -n devops-lab6
```

**Self-Learning Enhancement A — Controlled Retry Test (`backoffLimit: 2`):**
```bash
kubectl apply -f jobs/job-retry-test.yaml
kubectl wait --for=condition=failed job/retry-demo-job -n devops-lab6 --timeout=90s
kubectl get pods -n devops-lab6 -l job=retry-demo-job
kubectl describe job retry-demo-job -n devops-lab6
kubectl delete -f jobs/job-retry-test.yaml
```

### C. Kubernetes CronJob (`periodic-audit-cronjob`)
```bash
kubectl apply -f jobs/cronjob.yaml
kubectl get cronjobs -n devops-lab6
kubectl describe cronjob periodic-audit-cronjob -n devops-lab6
kubectl get jobs -n devops-lab6
# Retrieve logs from completed scheduled Pod:
POD=$(kubectl get pods -n devops-lab6 -l cronjob=periodic-audit-cronjob --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
kubectl logs "$POD" -n devops-lab6
```

**Self-Learning Enhancement B — Suspension & Resumption:**
```bash
kubectl patch cronjob periodic-audit-cronjob -n devops-lab6 -p '{"spec":{"suspend":true}}'
# Confirmed 0 new Jobs created over a 65s wait window
kubectl patch cronjob periodic-audit-cronjob -n devops-lab6 -p '{"spec":{"suspend":false}}'
# Re-suspend after verification so rapid test jobs do not accumulate:
kubectl patch cronjob periodic-audit-cronjob -n devops-lab6 -p '{"spec":{"suspend":true}}'
```

### D. ConfigMap & Secret Setup (Dummy Credentials Only)
> **Security Note:** Kubernetes Secrets encode values in base64, which is **encoding, not encryption**. Never store real passwords or tokens in Git or expose Secret values in logs/screenshots.

```bash
kubectl apply -f kubernetes/configmap.yaml
kubectl describe configmap student-app-config -n devops-lab6

# Create dummy credentials via a temporary env-file removed immediately afterward
printf 'APP_USERNAME=demo-user\nAPP_PASSWORD=demo-password\n' > /tmp/.demo-creds.env
kubectl create secret generic app-credentials --from-env-file=/tmp/.demo-creds.env -n devops-lab6
rm -f /tmp/.demo-creds.env
kubectl describe secret app-credentials -n devops-lab6

# Standalone verification + ConfigMap update & rollout restart check
kubectl apply -f kubernetes/deployment-standalone.yaml
kubectl rollout status deployment/student-config-demo -n devops-lab6
curl -s http://127.0.0.1:30085/config
curl -s http://127.0.0.1:30085/secret-status

kubectl patch configmap student-app-config -n devops-lab6 --type merge \
  -p '{"data":{"LOG_LEVEL":"debug","PUBLIC_MESSAGE":"Updated ConfigMap applied after Pod restart"}}'
# Running Pod keeps initial env until restarted:
kubectl rollout restart deployment/student-config-demo -n devops-lab6
kubectl rollout status deployment/student-config-demo -n devops-lab6
curl -s http://127.0.0.1:30085/config

# Clean up standalone demo resources before Helm takes ownership of student-app-config
kubectl delete -f kubernetes/deployment-standalone.yaml
kubectl delete -f kubernetes/configmap.yaml
```

### E. Helm Chart Validation, Installation, Upgrade & Rollback
```bash
helm lint ./helm/student-app
helm template student-app ./helm/student-app

helm install student-app ./helm/student-app -n devops-lab6 --create-namespace
helm list -n devops-lab6
helm status student-app -n devops-lab6
kubectl get all -n devops-lab6 -l app.kubernetes.io/instance=student-app

# Upgrade using values-dev.yaml (Self-Learning Enhancement C)
helm upgrade student-app ./helm/student-app -n devops-lab6 -f ./helm/student-app/values-dev.yaml
kubectl rollout status deployment/student-app -n devops-lab6
helm history student-app -n devops-lab6

# Roll back Helm release to Revision 1
helm rollback student-app 1 -n devops-lab6
kubectl rollout status deployment/student-app -n devops-lab6
helm history student-app -n devops-lab6
```

---

## 6. Verification Test Matrix

| # | Requirement | Command / Verification | Observed Result | Status |
|---|---|---|---|---|
| 1 | Docker build & runtime | `docker build -t student-app:1.0.0 ./app`, `curl /healthz` | 138MB non-root image built; `/healthz` returned HTTP 200 JSON | **PASS** |
| 2 | Job creation & completion | `kubectl apply -f jobs/job.yaml`, `kubectl get jobs` | `student-batch-report-job` reached `Complete (1/1)` in `7s` | **PASS** |
| 3 | Job logs | `kubectl logs student-batch-report-job-wlnfl -n devops-lab6` | Processed 500 records, 444 passed, avg 76.94, checksum `18e4cc52de0e` | **PASS** |
| 4 | Job retry (`backoffLimit`) | `kubectl apply -f jobs/job-retry-test.yaml` | Created 3 failing Pods under `backoffLimit: 2`, recorded `BackoffLimitExceeded`, cleaned up | **PASS** |
| 5 | CronJob execution | `kubectl apply -f jobs/cronjob.yaml`, `kubectl get jobs,logs` | Triggered `periodic-audit-cronjob-29927292` (`Complete 1/1`), logged `auditStatus: OK` | **PASS** |
| 6 | CronJob suspend / resume | `kubectl patch cronjob ... suspend:true/false` | 0 new Jobs created over 65s suspension; triggered `29927293` on resume; re-suspended | **PASS** |
| 7 | ConfigMap update behavior | `kubectl patch cm`, `curl /config`, `rollout restart` | Live Pod kept `info` until `rollout restart`, then new Pod served `debug` | **PASS** |
| 8 | Secret creation & safety | `kubectl create secret generic app-credentials --from-env-file=...` | `Opaque` Secret with 2 keys (`9` and `13` bytes); `/secret-status` reports `secretConfigured: true` (masked) | **PASS** |
| 9 | Helm lint & template | `helm lint ./helm/student-app`, `helm template` | `1 chart(s) linted, 0 chart(s) failed`; valid `ConfigMap`, `Service`, `Deployment` YAML rendered | **PASS** |
| 10 | Helm install & browser UI | `helm install student-app ...`, Chrome NodePort `:30086` | Revision 1 `deployed` (2/2 Pods); Chrome rendered portal UI with baseline ConfigMap & masked Secret | **PASS** |
| 11 | Helm upgrade (`values-dev.yaml`) | `helm upgrade ... -f values-dev.yaml` | Revision 2 `deployed` (3/3 Pods, `development-override`, `debug`); Chrome UI updated | **PASS** |
| 12 | Helm history & rollback | `helm history`, `helm rollback student-app 1` | Revision 3 `Rollback to 1` restored 2/2 Pods and `production-helm` baseline config | **PASS** |

---

## 7. Cleanup

```bash
helm uninstall student-app -n devops-lab6
kubectl delete namespace devops-lab6
```
