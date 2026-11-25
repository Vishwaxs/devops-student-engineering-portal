# Lab Exercise 6 — Command Reference & Viva Guide

**Course:** 2026-5 MCA B-DevOps | **Branch:** `feature/devops-lab-6-jobs-cronjobs-helm`  
**Verified Cluster Environment (Killercoda):** Kubernetes `v1.37.1`, Helm `v4.3.0`, Docker `29.1.3`

---

## 1. Command Distinction: Previously Practised vs. New in Lab 6

### Previously Practised (Labs 2–5)
- `kubectl get`, `kubectl describe`, `kubectl logs`, `kubectl apply`, `kubectl delete`, `kubectl port-forward`, `kubectl rollout status`, `kubectl rollout restart`
- Core workloads: Namespaces, Deployments, ReplicaSets, Pods, ClusterIP/NodePort Services

### New Commands Introduced in Lab 6

| Command | Purpose | Practical Lab 6 Example | Observed Expected Result |
|---|---|---|---|
| `kubectl create job` | Imperatively starts a one-time Job (helpful for ad-hoc or CronJob triggers). | `kubectl create job manual-audit --from=cronjob/periodic-audit-cronjob -n devops-lab6` | `job.batch/manual-audit created` |
| `kubectl get jobs` | Lists Jobs with completion ratios, durations, and statuses. | `kubectl get jobs -n devops-lab6` | `student-batch-report-job Complete 1/1 7s` |
| `kubectl describe job` | Displays Pod template, completions, `backoffLimit`, and Job controller events. | `kubectl describe job retry-demo-job -n devops-lab6` | Shows `SuccessfulCreate` retries and `BackoffLimitExceeded` on failure |
| `kubectl get cronjobs` | Lists CronJob schedules, suspend flag, active jobs, and last schedule time. | `kubectl get cronjobs -n devops-lab6` | `periodic-audit-cronjob * * * * * False 0 5s` |
| `kubectl describe cronjob` | Shows concurrency policy, deadline seconds, history limits, and active/completed Jobs. | `kubectl describe cronjob periodic-audit-cronjob -n devops-lab6` | Shows `SawCompletedJob` events and schedule timestamps |
| `kubectl create configmap` | Imperatively builds a ConfigMap from literals or files (`--dry-run=client -o yaml` supported). | `kubectl create configmap app-cfg --from-literal=LOG_LEVEL=info -n devops-lab6` | `configmap/app-cfg created` |
| `kubectl create secret generic` | Creates an Opaque Secret from literals or a temporary env-file without committing plaintext YAML. | `kubectl create secret generic app-credentials --from-env-file=/tmp/.demo-creds.env -n devops-lab6` | `secret/app-credentials created` (2 keys stored) |
| `helm lint` | Validates `Chart.yaml`, templates, and values formatting against Helm schema rules. | `helm lint ./helm/student-app` | `1 chart(s) linted, 0 chart(s) failed` |
| `helm template` | Renders Helm templates locally into plain Kubernetes YAML without contacting a cluster. | `helm template student-app ./helm/student-app` | Prints rendered `ConfigMap`, `Service`, and `Deployment` manifests |
| `helm install` | Creates a tracked Helm release in the cluster namespace. | `helm install student-app ./helm/student-app -n devops-lab6 --create-namespace` | `STATUS: deployed`, `REVISION: 1` |
| `helm upgrade` | Updates an existing release using modified values or templates and increments revision. | `helm upgrade student-app ./helm/student-app -n devops-lab6 -f ./helm/student-app/values-dev.yaml` | `Upgrade complete`, `REVISION: 2`, pods rolled to 3 replicas |
| `helm list` | Lists active Helm releases with chart version, revision, and status. | `helm list -n devops-lab6` | Displays `student-app` release status (`deployed`) |
| `helm history` | Prints the revision history (`superseded`, `deployed`, rollback descriptions) of a release. | `helm history student-app -n devops-lab6` | Lists Revisions 1 (`Install`), 2 (`Upgrade`), 3 (`Rollback to 1`) |
| `helm rollback` | Restores a Helm release to an earlier revision as a new forward revision number. | `helm rollback student-app 1 -n devops-lab6` | `Rollback was a success!`, creates Revision 3 matching Revision 1 |
| `helm uninstall` | Deletes all Kubernetes resources tracked by a release and removes its release metadata. | `helm uninstall student-app -n devops-lab6` | `release "student-app" uninstalled` |

*(Note: `kubectl create job --help` and `kubectl create secret generic --help` were verified directly against `kubectl v1.37.1` / `v1.34.1`, and all Helm commands were executed on `Helm v4.3.0`.)*

---

## 2. Concise Viva Preparation Q&A

1. **Job vs CronJob:** A `Job` runs a finite task once until desired completions succeed (`student-batch-report-job`). A `CronJob` runs a `Job` repeatedly on a cron schedule (`periodic-audit-cronjob`, `* * * * *`).
2. **Job retry behaviour & `backoffLimit`:** When a Pod fails and `restartPolicy: Never`, the Job controller spawns replacement Pods using exponential backoff delays until `backoffLimit` retries are exhausted (`retry-demo-job` with `backoffLimit: 2` created 3 failed Pods and stopped with `BackoffLimitExceeded`).
3. **Cron schedule syntax:** Five space-separated fields: `minute hour day-of-month month day-of-week`. `* * * * *` runs every minute; `0 * * * *` runs once per hour.
4. **`concurrencyPolicy`:** Controls overlapping executions. `Allow` permits overlap; `Forbid` skips the new schedule if the prior Job is still running; `Replace` cancels the active Job and starts a new one.
5. **Suspension & Resumption:** Setting `spec.suspend: true` pauses new CronJob scheduling immediately (`0` new Jobs created during our 65s test window) without deleting the CronJob object; setting `false` resumes normal scheduling.
6. **ConfigMap vs Secret:** ConfigMaps hold non-sensitive settings (`APP_NAME`, `APP_ENV`, `LOG_LEVEL`); Secrets (`Opaque`) hold sensitive values (`APP_USERNAME`, `APP_PASSWORD`).
7. **Environment-variable injection & updates:** Injecting ConfigMaps via `envFrom` or `configMapKeyRef` populates container environment variables at Pod startup. Updating the ConfigMap does **not** refresh environment variables inside already-running containers—a Pod restart (`kubectl rollout restart`) or Helm `checksum/config` annotation rollout is required.
8. **Base64 encoding in Secrets:** Kubernetes Secret YAML/data fields use base64 encoding so binary or multi-character strings transmit safely in JSON/YAML. **Base64 is encoding, not encryption**—anyone with `kubectl get secret -o yaml` RBAC permission can decode it unless etcd Encryption-at-Rest and strict RBAC are enabled.
9. **Helm Chart vs Release:** A **Chart** (`./helm/student-app`) is the reusable package of templates and default values on disk. A **Release** (`student-app` in `devops-lab6`) is a live deployed instance of that chart tracked inside Kubernetes Secrets/storage.
10. **`values.yaml` vs `values-dev.yaml`:** `values.yaml` defines baseline defaults (2 replicas, `production-helm`, `info` log level). Passing `-f values-dev.yaml` overrides specific keys during install/upgrade (3 replicas, `development-override`, `debug`).
11. **Helm templates & `_helpers.tpl`:** Templates use Go templating (`{{ .Values.replicaCount }}`, `{{ include "student-app.fullname" . }}`) to generate Kubernetes manifests consistently and add a `checksum/config` annotation so ConfigMap edits trigger automatic rolling updates during `helm upgrade`.
12. **`helm install` vs `helm upgrade`:** `install` creates Revision 1 of a new release; `upgrade` computes changes from updated values/templates and creates Revision 2+ (`helm upgrade --install` handles either).
13. **`helm rollback` mechanism:** `helm rollback student-app 1` restores the full manifest bundle of Revision 1 (including ConfigMaps, Services, and Deployment replica counts) and records it cleanly as Revision 3.
14. **`kubectl rollout undo` vs `helm rollback`:** `kubectl rollout undo` only reverts a single `Deployment` Pod template (leaving separate ConfigMaps/Services unchanged and desynchronizing Helm release metadata). `helm rollback` restores the **entire release** (Deployment + ConfigMap + Service) consistently under Helm revision tracking.
15. **Verification without exposing secrets:** Instead of printing `APP_PASSWORD`, our Express `/secret-status` route checks key presence booleans only (`APP_USERNAME: true`, `APP_PASSWORD: true`), keeping values redacted in browser views, logs, and screenshots.
