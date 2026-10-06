# ATL accounts Workers (MVP Phase 0/1 scaffold, NOT deployed)

Code-only scaffold for the ATL MVP spec (`docs/mvp/ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md`, §6, §7, §9, §14). Tracking issue: #60.

**Status: blocked on the owner steps in spec §13.** Nothing here is deployed. No DNS records, no Cloudflare resources and no secrets have been created. Every ID in the `wrangler.toml` files is a placeholder (`REPLACE_WITH_...`).

| Worker | Host (planned) | Phase | What is here |
|---|---|---|---|
| `atl-id` | `id.arctictradelanes.com` | 1 | `POST /auth/email` (magic link), `GET /auth/email/verify`, `POST /auth/logout`, `POST /account/consents`, `GET /c/:token` (double opt-in), `GET/POST /u/:token` (RFC 8058 one-click unsubscribe), `GET /healthz`, Queue consumer (outbox → R2), reconciler cron |
| `atl-api` | `api.arctictradelanes.com` | 3 | `GET /healthz` and `GET /v1/objects/:id` stub only (agent registry and x402 v2 come later) |
| `atl-mcp` | `mcp.arctictradelanes.com` | 3 | `GET /healthz` stub only (OAuthProvider + McpAgent come later) |

Bindings (spec §14 Phase 0): `DB` (D1 `atl-accounts`), `EVENTS` (Queue producer `atl-events`), `EVENTS_R2` (R2 `atl-events`, EU, bucket lock 400 days), `BACKUPS_R2` (R2 `atl-backups`, EU, bucket lock 35 days), `OAUTH_KV`, `EMAIL` (Email Service send binding), `TURNSTILE_SECRET` (secret), `RATE_LIMITER` (Rate Limiting binding).

Secrets (set later with `wrangler secret put`, never committed): `TURNSTILE_SECRET`, `KEK_B64` (wraps per-subject data keys, §7.4), `EMAIL_PEPPER` (HMAC pepper for `email_hmac`), `SESSION_SECRET`.

## Durable write path (spec §7.1)
1. Validate (Turnstile for humans).
2. One atomic `DB.batch()` writes the domain rows **and** an `outbox` row (`payload_enc` = AES-GCM under the subject key).
3. After commit, `EVENTS.send(envelope)`; on failure the outbox row stays un-enqueued.
4. The Queue consumer writes `events/YYYY/MM/DD/HH/{event_id}.json` to `EVENTS_R2` (idempotent key) and sets `outbox.archived_at`.
5. If D1 is down: send to the Queue **and** `PUT inbox/{event_id}.json` to R2, then return **202**.
6. Cron reconciler re-enqueues outbox rows not enqueued after 5 minutes.

## Local checks only
```
cd workers/atl-id && npx wrangler types && npx wrangler dev --local   # needs the owner's resources for anything beyond local mode
npx wrangler d1 migrations apply atl-accounts --local                  # from workers/atl-id (migrations_dir = ../migrations)
```
Do **not** run `wrangler deploy`, `wrangler d1 create` or `wrangler r2 bucket create` from this branch until the owner finishes spec §13.
