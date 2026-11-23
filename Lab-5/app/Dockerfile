# Multi-Stage Dockerfile for DevOps MCA Lab 5: Kubernetes Containerized App
# Stage 1: Build & Dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

# Stage 2: Minimal Production Runtime
FROM node:20-alpine AS runner
WORKDIR /app

# Best Practice: OCI Image Metadata
LABEL org.opencontainers.image.title="DevOps MCA Lab 5 Portal" \
      org.opencontainers.image.description="Kubernetes Deployment, Services, Scaling and Rolling Updates" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Vishwas Vashishtha <vishwas.vashishtha@mca.christuniversity.in>"

ENV NODE_ENV=production \
    PORT=8080 \
    APP_VERSION=v1.0.0

# Copy installed dependencies and application source
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
COPY src/ ./src/

# Best Practice: Non-root user execution for container security
USER node

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8080/healthz || exit 1

CMD ["node", "src/server.js"]
