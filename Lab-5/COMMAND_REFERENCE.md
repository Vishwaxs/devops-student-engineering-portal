# MCA DevOps Lab Exercise 5: Complete Kubernetes Command Reference

**Course:** 2026-5 MCA B-DevOps  
**Lab Assignment:** Lab Exercise - 5 (Kubernetes Deployment, Services, Scaling, Rolling Updates)  
**Student:** Vishwaxs (2447262)  
**Faculty:** Dr. Cynthia T, Department of Computer Science, Christ University  

---

## 1. Classification Overview

To support structured academic learning, every command in this laboratory is classified into:
- `[PREVIOUSLY PRACTISED]`: Concepts covered during earlier labs (Docker, Compose, Killercoda debugging).
- `[NEW IN LAB 5]`: Advanced orchestration, declarative operations, scaling, rolling updates, and rollbacks.

---

## 2. Docker & Containerization Commands

### 1. `docker build -t <tag> -f <Dockerfile> <context>`
- **Category:** `[PREVIOUSLY PRACTISED]`
- **Purpose:** Compiles the multi-stage Docker image using `node:20-alpine`, isolating build tools in the builder stage and packaging only runtime artifacts with an unprivileged non-root user.
- **Expected Output:**
  ```text
  => [internal] load build definition from Dockerfile
  => => transferring dockerfile: 1.2kB
  => [stage-1 1/4] FROM docker.io/library/node:20-alpine
  => [stage-1 4/4] COPY --from=builder /usr/src/app .
  => exporting to image
  => => naming to docker.io/vishwaxs/student-k8s-app:v1.0.0
  ```
- **Troubleshooting:**
  - `failed to connect to docker API`: Docker daemon is stopped. Start Docker Desktop service.
  - `COPY failed: file not found`: Check the context path passed at the end of the command.

### 2. `docker images`
- **Category:** `[PREVIOUSLY PRACTISED]`
- **Purpose:** Verifies that the built image exists in the local image cache and inspects its virtual size.
- **Expected Output:**
  ```text
  REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
  vishwaxs/student-k8s-app   v1.0.0    a1b2c3d4e5f6   2 minutes ago   148MB
  ```

---

## 3. Kubernetes Declarative Operations & Namespace

### 3. `kubectl apply -f <manifest.yaml>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Declares the desired state of a resource in the Kubernetes apiserver. If the resource does not exist, it is created. If it already exists, Kubernetes computes a 3-way strategic merge patch between the live state, the previous configuration, and the new manifest.
- **Why we need it:** Declarative management is the industry standard for GitOps, version-controlled infrastructure, and reproducible deployments.
- **Expected Output:**
  ```text
  namespace/devops-lab5 created
  configmap/k8s-portal-config created
  deployment.apps/student-k8s-app created
  service/student-k8s-service created
  ```
- **Troubleshooting:**
  - `error validating data: ValidationError`: YAML syntax error or invalid Kubernetes schema field.

### 4. `kubectl get ns` & `kubectl get cm -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Lists active namespaces and ConfigMaps.
- **Why we need it:** Verifies environmental multi-tenancy and decoupled runtime configurations.
- **Expected Output:**
  ```text
  NAME              STATUS   AGE
  default           Active   10d
  devops-lab5       Active   1m
  ```

---

## 4. Deployments, ReplicaSets & Pods

### 5. `kubectl get deploy -n <namespace>`
- **Category:** `[PREVIOUSLY PRACTISED]`
- **What it does:** Displays the high-level status of the Deployment controller.
- **Output Columns Explained:**
  - `READY`: Number of replicas passing readiness probes / Total desired replicas (e.g., `2/2`).
  - `UP-TO-DATE`: Replicas matching the current deployment template.
  - `AVAILABLE`: Pods available to serve end-user traffic.
- **Expected Output:**
  ```text
  NAME              READY   UP-TO-DATE   AVAILABLE   AGE
  student-k8s-app   2/2     2            2           45s
  ```

### 6. `kubectl get rs -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Lists ReplicaSets managed by Deployments.
- **Why we need it:** In Kubernetes, a Deployment does not manage Pods directly; it manages ReplicaSets, which in turn create and destroy Pods. Observing ReplicaSets is essential to verify rolling updates.
- **Expected Output:**
  ```text
  NAME                         DESIRED   CURRENT   READY   AGE
  student-k8s-app-7d9b4f6c8a   2         2         2       50s
  ```

### 7. `kubectl get pods -n <namespace> -o wide`
- **Category:** `[PREVIOUSLY PRACTISED]`
- **What it does:** Lists all active Pods with assigned cluster IP addresses and node scheduling information.
- **Expected Output:**
  ```text
  NAME                               READY   STATUS    RESTARTS   AGE   IP           NODE
  student-k8s-app-7d9b4f6c8a-x9j2k   1/1     Running   0          55s   10.244.1.4   node-1
  student-k8s-app-7d9b4f6c8a-m3q7p   1/1     Running   0          55s   10.244.1.5   node-1
  ```
- **Troubleshooting:**
  - `Pending`: Insufficient CPU/memory resources, or no nodes match scheduling requirements.
  - `CrashLoopBackOff`: Application crashed on startup. Check `kubectl logs <pod> --previous`.

---

## 5. Services & Endpoint Discovery

### 8. `kubectl get svc -n <namespace>`
- **Category:** `[PREVIOUSLY PRACTISED]`
- **What it does:** Displays active Services, cluster IPs, external access ports, and NodePorts.
- **Expected Output:**
  ```text
  NAME                  TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
  student-k8s-service   NodePort   10.96.142.88    <none>        80:30080/TCP   1m
  ```

### 9. `kubectl get endpoints <service-name> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Displays the live list of healthy Pod IP:Port targets receiving traffic from the Service selector.
- **Why we need it:** Demonstrates service discovery. When Pods scale up or down, this list updates dynamically within milliseconds.
- **Expected Output:**
  ```text
  NAME                  ENDPOINTS                           AGE
  student-k8s-service   10.244.1.4:8080,10.244.1.5:8080    1m
  ```
- **Troubleshooting:**
  - `<none>`: The Service selector does not match any Pod labels, or matching Pods failed readiness probes.

---

## 6. Scaling & Rolling Updates

### 10. `kubectl scale deployment/<name> --replicas=<N> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Imperatively updates the `spec.replicas` field of the Deployment.
- **Why we need it:** Allows manual horizontal scaling to absorb sudden traffic surges or reduce resource costs.
- **Expected Output:**
  ```text
  deployment.apps/student-k8s-app scaled
  ```

### 11. `kubectl rollout status deployment/<name> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Blocks the terminal and outputs real-time progress as Pods transition across ReplicaSets.
- **Why we need it:** Ensures that deployment pipelines wait until the rollout finishes successfully before declaring success.
- **Expected Output:**
  ```text
  Waiting for deployment "student-k8s-app" rollout to finish: 1 out of 3 new replicas have been updated...
  Waiting for deployment "student-k8s-app" rollout to finish: 2 out of 3 new replicas have been updated...
  deployment "student-k8s-app" successfully rolled out
  ```

### 12. `kubectl rollout history deployment/<name> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Displays the revision history of the Deployment, recorded via `--record` or annotations.
- **Expected Output:**
  ```text
  REVISION  CHANGE-CAUSE
  1         kubectl apply -f 03-deployment-v1.yaml
  2         kubectl apply -f 05-deployment-v2.yaml
  ```

### 13. `kubectl rollout undo deployment/<name> --to-revision=<N> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Rolls back the Deployment to a previous stable revision by reinstating that revision's ReplicaSet.
- **Why we need it:** Critical production safety mechanism when a new version introduces critical defects.
- **Expected Output:**
  ```text
  deployment.apps/student-k8s-app rolled back
  ```

---

## 7. Self-Healing & Pod Termination

### 14. `kubectl delete pod <pod-name> -n <namespace>`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Terminates an individual Pod instance.
- **Why we need it:** Demonstrates Kubernetes self-healing. The ReplicaSet controller continuously reconciles desired state vs actual state; the moment a Pod enters `Terminating`, a replacement Pod is scheduled immediately.
- **Expected Output:**
  ```text
  pod "student-k8s-app-7d9b4f6c8a-x9j2k" deleted
  ```

---

## 8. Horizontal Pod Autoscaler (HPA) Prerequisites

### 15. `kubectl get apiservice v1beta1.metrics.k8s.io`
- **Category:** `[NEW IN LAB 5]`
- **What it does:** Checks whether the Kubernetes Metrics Server API is registered and healthy.
- **Why we need it:** HPA requires real-time CPU/memory metrics from `metrics-server` to compute scaling calculations:
  $$\text{Target Replicas} = \left\lceil \text{Current Replicas} \times \frac{\text{Current Metric Value}}{\text{Target Metric Value}} \right\rceil$$
- **Expected Output (if available):**
  ```text
  NAME                     SERVICE                      AVAILABLE   AGE
  v1beta1.metrics.k8s.io   kube-system/metrics-server   True        5d
  ```
- **Fallback (if unavailable):** If the status is not `True`, HPA cannot function and will display `<unknown>/70%`. In that case, HPA must be documented as an optional manifest that could not be verified in the local environment.
