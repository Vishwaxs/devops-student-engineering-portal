# student-app Helm Chart

Custom Helm chart built for **MCA DevOps Lab Exercise 6** to manage the Express application Deployment, ConfigMap, Service, and external Secret references.

## Parameters

| Key | Description | Default |
|---|---|---|
| `replicaCount` | Number of Pod replicas | `2` |
| `image.repository` | Container image name | `student-app` |
| `image.tag` | Image tag | `1.0.0` |
| `service.type` | Kubernetes Service type | `NodePort` |
| `service.nodePort` | Static NodePort for cluster access | `30086` |
| `config.*` | Non-sensitive ConfigMap entries | See `values.yaml` |
| `secretRef.name` | Externally created Secret providing `APP_USERNAME` and `APP_PASSWORD` | `app-credentials` |

## Commands

```bash
helm lint ./helm/student-app
helm template student-app ./helm/student-app
helm install student-app ./helm/student-app -n devops-lab6 --create-namespace
helm upgrade student-app ./helm/student-app -n devops-lab6 -f ./helm/student-app/values-dev.yaml
helm history student-app -n devops-lab6
helm rollback student-app 1 -n devops-lab6
```

