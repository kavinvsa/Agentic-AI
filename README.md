# Production-Ready LangGraph Agentic Application

This workspace contains an end-to-end agentic stack that covers:

- LangGraph orchestration
- MCP server integration
- FastAPI API layer
- Tool calling and fallback strategy
- PostgreSQL persistence + Redis runtime dependency
- React frontend
- Docker Compose local deployment
- Kubernetes manifests for production style deployment
- CI pipeline for backend + frontend

## Problem Statement Covered

Scenario: **E-commerce Incident Commander**

A business needs an AI agent to process incident reports (payments failing, latency spikes, timeout errors), classify severity and route, then provide concise action guidance for on-call teams. The system must be deployable and production-shaped, with API, DB, UI, tools, MCP boundary, and CI/CD workflow.

## Architecture

- `frontend/` React + Vite UI for incident input and agent output
- `backend/` FastAPI + LangGraph agent runtime
- `mcp-server/` MCP tool server exposing tool endpoints
- `db` PostgreSQL in Docker Compose
- `redis` Redis in Docker Compose
- `k8s/` deployment/service manifests
- `.github/workflows/ci.yml` CI checks

## API Contracts

### Health

`GET /api/v1/health`

Response:

```json
{"status":"ok"}
```

### Run Agent

`POST /api/v1/agent/run`

Request:

```json
{
  "session_id": "session-123",
  "prompt": "Checkout payments fail in EU after deployment"
}
```

Response:

```json
{
  "triage": "payment-critical",
  "timestamp": "2026-05-23T12:00:00.000000Z",
  "response": "...actionable incident guidance..."
}
```

## MCP Integration

Backend calls MCP server endpoints:

- `POST /tools/incident_classifier`
- `POST /tools/current_time`

If MCP is unavailable, backend falls back to local tools to keep response path alive.

## Local Run (Docker Compose)

1. Copy environment file:

```bash
cp .env.example .env
```

1. Set `OPENAI_API_KEY` in `.env`.

1. Start full stack:

```bash
docker compose up --build
```

1. Open apps:

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/api/v1/health`
- MCP health: `http://localhost:9000/health`

## Backend Run (without Docker)

```bash
cd backend
pip install -e .[test]
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests:
```bash
pytest
```

## Frontend Run (without Docker)

```bash
cd frontend
npm install
npm run dev
```

## Production Deployment Notes

- Build API image from `backend/Dockerfile`
- Build web image from `frontend/Dockerfile`
- Build MCP image from `mcp-server/Dockerfile`
- Push to image registry and replace image names in `k8s/*.yaml`
- Store secrets (`OPENAI_API_KEY`, DB URLs) in Kubernetes Secret `langgraph-secrets`

## Security and Ops Checklist

- Replace default DB credentials
- Use managed PostgreSQL/Redis in production
- Enable ingress TLS termination
- Add API auth (JWT/OIDC gateway)
- Add distributed tracing and SIEM sink
- Define SLO alerts for error rate and latency

## Next Improvements

- Add streaming token responses via server-sent events
- Add user auth and tenant isolation
- Add async worker queue for long-running tool jobs
- Add vector memory store for historical retrieval
