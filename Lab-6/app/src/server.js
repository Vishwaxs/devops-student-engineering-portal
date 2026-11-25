import express from 'express';
import os from 'os';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = Number(process.env.PORT || 8080);

// ConfigMap values (non-sensitive configuration)
const APP_NAME = process.env.APP_NAME || 'MCA DevOps Student Portal';
const APP_ENV = process.env.APP_ENV || 'local-dev';
const LOG_LEVEL = process.env.LOG_LEVEL || 'info';
const APP_MODE = process.env.APP_MODE || 'standard';
const PUBLIC_MESSAGE = process.env.PUBLIC_MESSAGE || 'Default local configuration active';

// Pod metadata (Downward API / OS fallback)
const POD_NAME = process.env.POD_NAME || process.env.HOSTNAME || os.hostname();
const POD_NAMESPACE = process.env.POD_NAMESPACE || 'devops-lab6';
const POD_IP = process.env.POD_IP || '127.0.0.1';

// Secret verification helper: checks presence only without exposing values
function getSecretStatus() {
  const hasUser = Boolean(process.env.APP_USERNAME && process.env.APP_USERNAME.length > 0);
  const hasPass = Boolean(process.env.APP_PASSWORD && process.env.APP_PASSWORD.length > 0);
  return {
    secretConfigured: hasUser && hasPass,
    keysPresent: {
      APP_USERNAME: hasUser,
      APP_PASSWORD: hasPass
    },
    note: 'Secret values are intentionally masked and never returned in responses or logs.'
  };
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

app.use(express.static(join(__dirname, 'public')));

app.get('/healthz', (req, res) => {
  res.status(200).json({ status: 'UP', check: 'liveness', pod: POD_NAME });
});

app.get('/ready', (req, res) => {
  res.status(200).json({ status: 'READY', check: 'readiness', pod: POD_NAME });
});

app.get('/config', (req, res) => {
  res.status(200).json({
    appName: APP_NAME,
    environment: APP_ENV,
    logLevel: LOG_LEVEL,
    mode: APP_MODE,
    publicMessage: PUBLIC_MESSAGE,
    pod: POD_NAME,
    namespace: POD_NAMESPACE
  });
});

app.get('/secret-status', (req, res) => {
  res.status(200).json(getSecretStatus());
});

app.get('/', (req, res) => {
  const secretStatus = getSecretStatus();
  const isDevOverride = APP_ENV.toLowerCase().includes('dev');
  const accentColor = isDevOverride ? '#10b981' : '#3b82f6';

  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(APP_NAME)} — Lab 6</title>
  <link rel="stylesheet" href="/style.css">
  <style>:root { --accent: ${accentColor}; }</style>
</head>
<body>
  <div class="container">
    <header class="header">
      <div>
        <h1>${escapeHtml(APP_NAME)}</h1>
        <p class="subtitle">MCA DevOps Lab 6 — ConfigMaps, Secrets &amp; Helm</p>
      </div>
      <span class="badge">ENV: ${escapeHtml(APP_ENV)}</span>
    </header>

    <div class="banner">
      <strong>Public ConfigMap Message:</strong> ${escapeHtml(PUBLIC_MESSAGE)}
    </div>

    <div class="grid">
      <section class="card">
        <h2>ConfigMap Injection</h2>
        <div class="row"><span class="label">APP_NAME</span><span class="val">${escapeHtml(APP_NAME)}</span></div>
        <div class="row"><span class="label">APP_ENV</span><span class="val">${escapeHtml(APP_ENV)}</span></div>
        <div class="row"><span class="label">LOG_LEVEL</span><span class="val">${escapeHtml(LOG_LEVEL)}</span></div>
        <div class="row"><span class="label">APP_MODE</span><span class="val">${escapeHtml(APP_MODE)}</span></div>
      </section>

      <section class="card">
        <h2>Secret Reference Check</h2>
        <div class="row"><span class="label">Credentials Injected</span><span class="val ${secretStatus.secretConfigured ? 'ok' : 'warn'}">${secretStatus.secretConfigured ? 'PRESENT' : 'NOT SET'}</span></div>
        <div class="row"><span class="label">APP_USERNAME</span><span class="val">${secretStatus.keysPresent.APP_USERNAME ? 'Injected (Masked)' : 'Missing'}</span></div>
        <div class="row"><span class="label">APP_PASSWORD</span><span class="val">${secretStatus.keysPresent.APP_PASSWORD ? 'Injected (Masked)' : 'Missing'}</span></div>
        <div class="row"><span class="label">Exposure Policy</span><span class="val ok">Values Redacted</span></div>
      </section>

      <section class="card">
        <h2>Kubernetes Pod Info</h2>
        <div class="row"><span class="label">Pod Name</span><span class="val">${escapeHtml(POD_NAME)}</span></div>
        <div class="row"><span class="label">Namespace</span><span class="val">${escapeHtml(POD_NAMESPACE)}</span></div>
        <div class="row"><span class="label">Pod IP</span><span class="val">${escapeHtml(POD_IP)}</span></div>
        <div class="row"><span class="label">Health Probe</span><span class="val ok">HTTP 200 (/healthz)</span></div>
      </section>
    </div>

    <div class="card endpoints">
      Endpoints: <code>/healthz</code> &middot; <code>/ready</code> &middot; <code>/config</code> &middot; <code>/secret-status</code>
    </div>
  </div>
</body>
</html>`);
});

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`[Lab6 App] Listening on port ${PORT} (env=${APP_ENV}, logLevel=${LOG_LEVEL}, secretInjected=${getSecretStatus().secretConfigured})`);
});

process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});

