# OpenLedger

OpenLedger is a privacy-first, self-hosted personal finance dashboard.

## Architecture

- Frontend: Next.js 14 application that renders dashboard UX.
- Backend: FastAPI service for auth, integrations, sync, and analytics.
- Data: PostgreSQL for durable records and Redis for cache/job state.

## Quick Start

1. Copy environment template: `cp .env.example .env`
2. Start services: `docker compose up -d`
3. Open frontend: [http://localhost:3000](http://localhost:3000)

## Repository Layout

- `backend/` - FastAPI app and migrations.
- `frontend/` - Next.js app.
- `docs/` - setup, security, plugin, and contribution guides.

## Contracts

- Service boundary and request/data flow details: `docs/ARCHITECTURE.md`
