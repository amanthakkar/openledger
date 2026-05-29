# Setup

## Prerequisites

- Docker and Docker Compose
- Plaid and Splitwise API credentials

## Local Startup

1. Copy `.env.example` to `.env`.
2. Fill required secrets in `.env`.
3. Run `docker compose up -d --build`.
4. Open [http://localhost:3000](http://localhost:3000).

## First-Run Notes

- Backend and frontend bind to localhost by default.
- Use seeded/demo data only for non-production testing.
