# OpenLedger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

## Status & honest limitations

- **No public demo, on purpose** — a finance dashboard's demo would need someone's real accounts. The docs above are the tour.
- **Bring your own credentials** — Plaid (and Splitwise, for the shared-expenses plugin) sync uses *your* developer keys from `.env`; nothing is shared or phoned home.
- **Thin automated tests** — `backend/tests/` is currently a stub. The system is verified by running it (it is the author's own household deployment), not by a test suite; treat it as well-documented, lightly-tested software.
- **Single-deployment design** — built for one self-hosted household instance bound to localhost by default, not a multi-tenant service.

## Contributing

Scoped branches, tests with behavior changes, short test plan in the PR — [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

## More from @amanthakkar

- **[crypto_finance](https://github.com/amanthakkar/crypto_finance)** — causal crypto indicators + a live [interactive dashboard](https://amanthakkar.github.io/crypto_finance/)
- **[cortex-showcase](https://github.com/amanthakkar/cortex-showcase)** — the homelab agent stack OpenLedger's private deployment grew alongside, as an interactive architecture tour
- **[muse-mailbox](https://github.com/amanthakkar/muse-mailbox)** — E2E-encrypted Muse↔Muse messaging via a blind relay

