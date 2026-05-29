# Architecture

## Service Boundaries

### Frontend (Next.js 14)

- Owns route structure, dashboard UI, and authenticated user workflows.
- Calls backend REST endpoints and renders normalized view models.
- Must not persist provider credentials or access tokens in browser storage.

### Backend (FastAPI)

- Owns authentication, connector orchestration, sync scheduling, analytics, and plugin discovery.
- Exposes domain APIs consumed by frontend.
- Enforces user-level data isolation and secure secret handling.

### Data Layer

- PostgreSQL stores durable financial records and historical snapshots.
- Redis stores job/sync state and ephemeral cache values.

## Interaction Flow

1. Frontend sends authenticated API request.
2. Backend validates JWT/session and user scope.
3. Backend reads/writes PostgreSQL and optional Redis cache.
4. Backend returns transformed response for UI rendering.
