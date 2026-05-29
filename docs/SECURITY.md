# Security

## Secrets

- Commit `.env.example` only. Never commit `.env`.
- Generate `JWT_SECRET` and `ENCRYPTION_KEY` with strong randomness.

## Token Handling

- User passwords must be bcrypt hashed.
- Provider access tokens must be encrypted at rest (Fernet).
- Session cookies should be `httpOnly`, `secure`, and `SameSite=Lax` (or stricter).

## Network Controls

- Bind all exposed ports to `127.0.0.1` by default.
- Restrict backend CORS to frontend localhost origin.
- Add auth endpoint rate limiting target of 5 attempts/minute per IP.

## Session Lifetime Baseline

- Access token TTL: 24 hours.
- Refresh token TTL: 7 days.
