# =============================================================================
# Dockerfile for DevOps Student Engineering Portal
# Lab 3: Build, optimize, tag and push OCI-compliant container images
# 
# Uses multi-stage build for optimization (Self-Learning Addition #1)
# Runs as non-root user for security (Self-Learning Addition #2)
# =============================================================================

# ---------- Stage 1: Build/Validation Stage ----------
FROM node:20-alpine AS validator

WORKDIR /app

# Copy only application files needed for validation
COPY index.html style.css script.js ./

# Validate that required files exist and are non-empty
RUN test -s index.html && echo "✓ index.html valid" && \
    test -s style.css && echo "✓ style.css valid" && \
    test -s script.js && echo "✓ script.js valid"

# ---------- Stage 2: Production Stage ----------
FROM nginx:1.27-alpine

LABEL maintainer="Vishwas Vashishtha <vishwas.vashishtha@mca.christuniversity.in>"
LABEL description="DevOps Student Engineering Portal - MCA Lab 3"
LABEL org.opencontainers.image.title="student-portal"
LABEL org.opencontainers.image.description="Static student engineering portal served via nginx"
LABEL org.opencontainers.image.source="https://github.com/Vishwaxs/devops-student-engineering-portal"

# Create non-root user (Self-Learning Addition #2)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy validated application files from build stage
COPY --from=validator /app/index.html /usr/share/nginx/html/
COPY --from=validator /app/style.css /usr/share/nginx/html/
COPY --from=validator /app/script.js /usr/share/nginx/html/

# Custom nginx configuration for non-root operation
RUN echo 'server { \
    listen 8080; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ =404; \
    } \
}' > /etc/nginx/conf.d/default.conf && \
    # Adjust permissions for non-root user
    chown -R appuser:appgroup /usr/share/nginx/html && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chown -R appuser:appgroup /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown appuser:appgroup /var/run/nginx.pid

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8080

# Health check to verify nginx is serving content
HEALTHCHECK --interval=10s --timeout=3s --start-period=3s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8080/ || exit 1

# Start nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
