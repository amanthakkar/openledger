# Plugins

OpenLedger supports community data-source plugins under backend plugin contracts.

## Goals

- Add importers/connectors without touching core modules.
- Keep all plugin sync behavior user-scoped and auditable.

## Required Contract

- Plugin identity (`name`, `description`)
- Connect validation
- Account sync
- Transaction sync
- Balance fetch

## Code Locations

- Interface: `backend/app/plugins/base.py`
- Registration: `backend/app/plugins/registry.py`
- Authoring guide: `backend/app/plugins/README.md`
