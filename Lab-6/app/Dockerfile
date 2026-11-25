# Multi-Stage Dockerfile for MCA DevOps Lab 6
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

FROM node:20-alpine AS runner
WORKDIR /app

LABEL org.opencontainers.image.title="MCA DevOps Lab 6 Student App" \
      org.opencontainers.image.description="Express app configured via Kubernetes ConfigMaps, Secrets, and Helm" \
      org.opencontainers.image.version="1.0.0"

ENV NODE_ENV=production \
    PORT=8080

COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
COPY --chown=node:node src/ ./src/
RUN chmod -R a+rX /app/src

# Non-root user execution for container security
USER node
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8080/healthz || exit 1

CMD ["node", "src/server.js"]

