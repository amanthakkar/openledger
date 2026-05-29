# Schema Plan

Canonical first-wave entities for migrations:

- `users`
- `plaid_items`
- `accounts`
- `transactions`
- `net_worth_snapshots`
- `splitwise_balances`
- `holdings`

Key constraints:

- All provider-linked records are user-scoped through `user_id`.
- `transactions.plaid_transaction_id` is unique for idempotent sync.
- `accounts.plaid_account_id` is unique for external account identity.
- `net_worth_snapshots` enforces unique `(user_id, date)` for one daily snapshot.
