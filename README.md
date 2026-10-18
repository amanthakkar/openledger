# OpenLedger

**Privacy-first, self-hosted personal finance dashboard.**

Your bank data shouldn't have to live on someone else's cloud to be useful. OpenLedger runs entirely on your own hardware: it syncs accounts via Plaid, stores everything in your Postgres, and renders it in a dashboard only you can reach.

## Architecture

- **Frontend** — Next.js 14: dashboard UX, authenticated workflows, normalized view models. Never persists provider tokens in browser storage.
- **Backend** — FastAPI: auth, connector orchestration, sync scheduling, analytics, and a plugin system for new data sources.
- **Data** — PostgreSQL for durable financial records + historical snapshots; Redis for job / sync state and cache.

Full detail: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · Security model: [`docs/SECURITY.md`](docs/SECURITY.md) (bcrypt passwords, Fernet-encrypted provider tokens, httpOnly secure cookies, localhost-bound by default)

## Quick start

```bash
cp .env.example .env   # fill in JWT_SECRET, ENCRYPTION_KEY, Plaid + Splitwise credentials
docker compose up -d --build
# → http://localhost:3000
```

Prerequisites and full walkthrough: [`docs/SETUP.md`](docs/SETUP.md)

## Repository layout

- `backend/` — FastAPI app, migrations, plugin contract (`backend/app/plugins/`)
- `frontend/` — Next.js app
- `docs/` — architecture, setup, security, plugins, contributing

## Plugins

New importers/connectors ship as plugins without touching core: identity + connect validation + account/transaction sync + balance fetch. See [`docs/PLUGINS.md`](docs/PLUGINS.md).

## Contributing

Scoped branches, tests with behavior changes, short test plan in the PR — [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
