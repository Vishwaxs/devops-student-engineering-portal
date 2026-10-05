# Lab 4: Multi-Container Application with Docker Compose

## Objective
Develop and deploy a multi-container application using Docker Compose and validate networking and storage.

## Architecture

```
┌─────────────────────────────────────────────────┐
│           student-portal-network (bridge)        │
│                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ frontend │    │   api    │    │  redis   │   │
│  │ (nginx)  │───▶│ (node)  │───▶│ (redis)  │   │
│  │ :80      │    │ :3000   │    │ :6379    │   │
│  └──────────┘    └──────────┘    └──────────┘   │
│       │                               │          │
│   port 8080                    redis-data vol    │
│   (host)                       (persistence)     │
└─────────────────────────────────────────────────┘
```

## Services
1. **frontend** (nginx:1.27-alpine) — Serves static files + reverse proxies `/api/` to backend
2. **api** (Node.js 20) — REST API with Redis-backed student data
3. **redis** (redis:7-alpine) — Persistent data store with AOF enabled

## Key Features
- Custom bridge network: `student-portal-network`
- Named volume: `student-portal-redis-data`
- Healthcheck-based dependency ordering
- Restart policies: `unless-stopped`
- Environment variable management via `.env.example`

## Self-Learning Additions
1. **Healthcheck-based Dependencies** — Services start in order using `condition: service_healthy`
2. **Environment Variable Management** — `.env.example` for configurable port and Redis URL

## Commands
```bash
# Start all services
docker compose up -d --build

# Check status
docker compose ps

# View logs
docker compose logs

# Network inspection
docker network inspect student-portal-network

# Volume inspection
docker volume inspect student-portal-redis-data

# Test API via frontend proxy
curl http://localhost:8080/api/health
curl http://localhost:8080/api/student
curl http://localhost:8080/api/visits

# Stop all services
docker compose down
```

## Branch
- `feature/lab-4-compose`
