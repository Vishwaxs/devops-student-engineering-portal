import express from 'express';
import os from 'os';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8080;
const APP_VERSION = process.env.APP_VERSION || 'v1.0.0';
const ENVIRONMENT = process.env.ENVIRONMENT || 'Production';
const POD_NAME = process.env.HOSTNAME || os.hostname();
const POD_NAMESPACE = process.env.POD_NAMESPACE || 'devops-lab5';
const POD_IP = process.env.POD_IP || '10.244.0.1';

let requestCount = 0;
const startTime = Date.now();

// Serve static assets
app.use(express.static(join(__dirname, 'public')));
app.use(express.json());

// API: Version Check (for rolling update validation)
app.get('/version', (req, res) => {
  requestCount++;
  res.json({
    version: APP_VERSION,
    pod: POD_NAME,
    namespace: POD_NAMESPACE,
    environment: ENVIRONMENT,
    requestsServed: requestCount,
    status: 'ACTIVE'
  });
});

// API: Detailed Health & Cluster Metadata
app.get('/api/info', (req, res) => {
  requestCount++;
  res.json({
    app: 'DevOps MCA Lab 5 - Kubernetes Portal',
    version: APP_VERSION,
    podName: POD_NAME,
    podIp: POD_IP,
    namespace: POD_NAMESPACE,
    environment: ENVIRONMENT,
    uptimeSeconds: Math.floor((Date.now() - startTime) / 1000),
    requestsServed: requestCount,
    nodeArchitecture: process.arch,
    memoryUsageMB: Math.round(process.memoryUsage().rss / 1024 / 1024)
  });
});

// Self-Learning Probe: Liveness Probe
app.get('/healthz', (req, res) => {
  res.status(200).json({
    status: 'UP',
    check: 'liveness',
    pod: POD_NAME,
    timestamp: new Date().toISOString()
  });
});

// Self-Learning Probe: Readiness Probe
app.get('/ready', (req, res) => {
  res.status(200).json({
    status: 'READY',
    check: 'readiness',
    pod: POD_NAME,
    trafficEligible: true
  });
});

// Root: Dynamic HTML Visual Dashboard
app.get('/', (req, res) => {
  requestCount++;
  const uptime = Math.floor((Date.now() - startTime) / 1000);
  const isV2 = APP_VERSION.includes('2');
  const themeColor = isV2 ? '#059669' : '#2563eb';
  const badgeColor = isV2 ? '#10b981' : '#3b82f6';
  const accentGlow = isV2 ? 'rgba(16, 185, 129, 0.2)' : 'rgba(59, 130, 246, 0.2)';

  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevOps Lab 5 - Kubernetes Portal</title>
  <link rel="stylesheet" href="/style.css">
  <style>
    :root {
      --primary: ${themeColor};
      --badge: ${badgeColor};
      --glow: ${accentGlow};
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="logo-badge">☸️ K8s</div>
      <div class="title-group">
        <h1>MCA DevOps Lab Exercise 5</h1>
        <p class="subtitle">Kubernetes Deployment, Services, Scaling & Rolling Updates</p>
      </div>
      <div class="version-tag">${APP_VERSION}</div>
    </header>

    <main class="grid">
      <div class="card pod-card">
        <h3>📦 Serving Pod Replica</h3>
        <div class="pod-id">${POD_NAME}</div>
        <div class="meta-row"><span>Pod IP:</span> <strong>${POD_IP}</strong></div>
        <div class="meta-row"><span>Namespace:</span> <strong>${POD_NAMESPACE}</strong></div>
        <div class="meta-row"><span>Environment:</span> <strong>${ENVIRONMENT}</strong></div>
      </div>

      <div class="card metrics-card">
        <h3>📊 Real-Time Metrics</h3>
        <div class="meta-row"><span>Requests Handled by this Pod:</span> <strong>${requestCount}</strong></div>
        <div class="meta-row"><span>Pod Uptime:</span> <strong>${uptime}s</strong></div>
        <div class="meta-row"><span>Liveness Probe:</span> <span class="badge healthy">/healthz (200 OK)</span></div>
        <div class="meta-row"><span>Readiness Probe:</span> <span class="badge healthy">/ready (Ready)</span></div>
      </div>

      <div class="card architecture-card">
        <h3>🏛️ Kubernetes Architecture Flow</h3>
        <div class="arch-flow">
          <div class="arch-step">Browser / Client</div>
          <div class="arch-arrow">➔</div>
          <div class="arch-step">Service (ClusterIP / NodePort :80)</div>
          <div class="arch-arrow">➔</div>
          <div class="arch-step active">Target Pod :8080</div>
        </div>
        <p class="arch-note">When scaled, the Service evenly round-robins traffic across all healthy replica Pods matching selector <code>app: student-k8s-app</code>.</p>
      </div>

      <div class="card actions-card">
        <h3>🧪 Quick Verification Endpoints</h3>
        <div class="button-group">
          <a href="/version" class="btn" target="_blank">View /version (JSON)</a>
          <a href="/api/info" class="btn" target="_blank">View /api/info (Full Meta)</a>
          <a href="/healthz" class="btn" target="_blank">Liveness Probe (/healthz)</a>
        </div>
      </div>
    </main>

    <footer class="footer">
      <p>Course: 2026-5 MCA B-DevOps · Lab 5 · Automated Zero-Downtime Rolling Update Demonstration</p>
    </footer>
  </div>
</body>
</html>`);
});

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`[Kubernetes Portal] Server running on http://0.0.0.0:${PORT}`);
  console.log(`[Metadata] Version: ${APP_VERSION} | Pod: ${POD_NAME} | Namespace: ${POD_NAMESPACE}`);
});

// Self-Learning Concept: Graceful Zero-Downtime Termination (SIGTERM / SIGINT)
const gracefulShutdown = (signal) => {
  console.log(`\n[${signal}] Initiating graceful shutdown for Pod: ${POD_NAME}...`);
  server.close(() => {
    console.log('[K8s] Closed active HTTP listeners. Pod exiting cleanly with 0 downtime.');
    process.exit(0);
  });
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
