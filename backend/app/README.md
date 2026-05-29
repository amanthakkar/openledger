# Backend Module Ownership

## Platform

- `main.py`: FastAPI app initialization and router registration.
- `config.py`: environment-backed settings.
- `database.py`: SQLAlchemy engine, session, and base metadata.

## Domain Modules

- `auth/`: local account auth and JWT lifecycle.
- `plaid/`: Plaid link/exchange/sync and financial account/transaction ingestion.
- `splitwise/`: debt and shared-expense sync.
- `crypto/`: crypto import and holdings normalization.
- `analytics/`: net-worth and spending derivations.
- `sync/`: scheduler and connection health checks.
- `plugins/`: plugin interface and runtime registration.
