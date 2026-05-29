# OpenLedger Plugin Guide

Plugins extend OpenLedger with additional financial data sources.

## Required Interface

Each plugin must implement `DataSourcePlugin` from `base.py` with:

- `name`
- `description`
- `connect(credentials)`
- `sync_accounts(user_id)`
- `sync_transactions(user_id, since)`
- `get_balances(user_id)`

## Registration

Register plugin instances in `registry.py` during backend startup or module init.

## Suggested Plugin Layout

```text
plugins/
  your_plugin/
    __init__.py
    plugin.py
    models.py
    router.py
    README.md
```

## Safety Requirements

- All plugin operations must be scoped to a specific `user_id`.
- Secrets passed to plugins must never be logged in plaintext.
