# Lab 3: Container Image Build, Optimization, and Vulnerability Scanning

## Objective
Build, optimize, tag and push OCI-compliant container images using Docker and scan images for vulnerabilities.

## Implementation

### Dockerfile
- **Multi-stage build**: Stage 1 (node:20-alpine) validates files, Stage 2 (nginx:1.27-alpine) serves the application
- **Non-root user**: Application runs as `appuser` instead of root
- **Healthcheck**: Periodic wget check ensures nginx is serving content
- **OCI Labels**: Proper metadata labels following OCI Image Spec
- **Pinned versions**: Base images use specific version tags

### .dockerignore
Excludes unnecessary files (docs, reports, evidence, scripts) from the build context to minimize image size.

### Key Commands
```bash
# Build the image
docker build -t student-portal:v1.0 .

# Run the container
docker run -d --name student-portal -p 8080:8080 student-portal:v1.0

# Verify the application
curl http://localhost:8080

# Inspect image metadata (OCI compliance)
docker inspect student-portal:v1.0

# Vulnerability scan
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image student-portal:v1.0
```

### Self-Learning Additions
1. **Multi-stage Docker Build** — Reduces final image size by separating validation from production
2. **Non-root Container User** — Follows security best practice of least privilege

## Branch
- `feature/lab-3-container-security`
