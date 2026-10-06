# ATL MVP build spec: business & agent registration, social login, agentic payments, SEO fact pages, Arctic brands strip, Flexport MCP

**Product:** ArcticTradeLanes.com (ATL), an Arctic GIS OSINT platform covering the NSR and the Polar Silk Road, with an EPSG:3996 polar hero map and 22 locales
**Owner:** Aleksei Dolgikh (@alexdolbun) · cto@arctictradelanes.com
**Spec date:** 2026-10-06 · **Status:** SPEC ONLY. Nothing here has been built or deployed. The live site and the existing x402 endpoints are untouched.
**Deploys:** a separate deploy bot through Zo. This document is its build brief.
**Companion files:** [`0001_init.sql`](./0001_init.sql) · [`arctic-brands.csv`](./arctic-brands.csv) · [`flexport-mcp-integration.md`](./flexport-mcp-integration.md)

---

## 0. TL;DR

| Area | Decision |
|---|---|
| Hosting | New **Cloudflare Workers** on orange-clouded subdomains: `id.` (auth/accounts), `api.` (v1 API), `mcp.` (remote MCP). The apex/`www` Zo site is untouched. Discovery files (`/.well-known/agent-card.json`, `agent.json`, `llms.txt` additions) are added by the deploy bot as **new static routes only**. |
| Primary store | **D1** `atl-accounts` (location hint `weur`). **Time Travel** PITR is always on, with 30 days of history. |
| Never lose a registration | Three independent copies: (1) D1 row plus outbox, (2) **Queue → R2 append-only JSONL** with **bucket lock**, (3) **nightly encrypted D1 export** (Workflow → R2 `atl-backups`, age/X25519 public-key encryption). A reconciler cron replays anything missing. D1 outage fallback: write directly to Queue and R2, return `202`. |
| GDPR | Consent ledger (append-only, versioned text hash), **double opt-in** for marketing, RFC 8058 one-click unsubscribe, DSAR export/delete. "Never lose" is squared with "right to erasure" by **crypto-shredding** per-subject keys. |
| Public GitHub | Only schema, migrations, daily **counts** and **SHA-256 of encrypted backup files**. **No emails, and no hashes of emails** (those are pseudonymous PII). |
| Login order | **Google** (consumers; Workspace `hd` claim gives a business domain) → **Microsoft Entra ID** (logistics enterprises on M365; tenant ID) → **LinkedIn OIDC** (B2B identity) → **email magic link** (always available) → later **Apple** (iOS consumers) and **GitHub** (agent developers). |
| Business accounts | Business-email gate (free-mail blocklist + MX check + verified email), org auto-created per verified domain, optional DNS TXT domain proof. |
| Agents | Agent registry: operator business email + domain proof (DNS TXT `_atl-agent` or `/.well-known/atl-agent.json`) + API key (hashed) or OAuth client + per-call **x402** price tiers. A2A card at `/.well-known/agent-card.json` (canonical per the A2A spec) with an `/.well-known/agent.json` alias. A remote **ATL MCP** server on Workers with OAuth (workers-oauth-provider) and `paidTool` x402. |
| Payments | **x402 v2** (Cloudflare Agents SDK, `withX402`/`paidTool`, USDC on Base, same settlement wallet) for new endpoints. **Legacy x402 v1 endpoints are untouched.** **MPP** next (cards via Stripe plus stablecoins, backward compatible with x402). **ACP** and **AP2** in Phase 6. |
| SEO | Programmatic **template** SSR/pre-render of **1,316 atlas objects × 22 locales ≈ 28,952 fact pages**, with JSON-LD (Place / Organization / Dataset / BreadcrumbList), hreflang + x-default, sharded sitemaps and map deep links. **Zero per-page AI writing.** |
| Brands strip | **50 brands** researched. **22 are ready now** (Commons logo + atlas object), 22 need a press-kit logo, 6 need an atlas object first. Label: "Arctic ecosystem: companies covered on the atlas". **Never** "partners" or "trusted by". Logos link to atlas object pages. Neutral profiles only. |
| Flexport | Bring-your-own Flexport via MCP OAuth. NSR vs Suez comparison and tracking overlays on the polar map. **Every booking needs a human confirm.** See `flexport-mcp-integration.md`. |

---

## 1. Constraints and non-goals

1. **Additive only.** Do not modify, rename or re-price: `/api/x402/fulfill`, `/api/x402/upload`, `/api/x402/schema`, `/api/x402/status`, `/api/alpha/route-optimize`, `/api/alpha/status`, `/api/vessels`, `/.well-known/x402.json`, the atlas files and the existing pages. Acceptance test: the SHA-256 of each GET response body (excluding volatile timestamp fields) is the same before and after each deploy.
2. **Don't touch the live site in this task.** This spec is committed to the repo. The deploy bot implements it later.
3. **No raw PII in any public repo.** The `International-Arctic/*` repos are public.
4. **Minimise AI tokens.** Templates, not generation. The only one-off AI-adjacent cost is translating about 120 UI labels into 21 locales, which can also be done by hand or by DeepL.
5. **Neutral-content rule (strict).** No wording, sections, badges or links about government trade restrictions or restricted-party lists, anywhere: fact pages, brand strip, JSON-LD, sitemaps, emails, docs. A build-time **banned-terms lint** enforces this (§8, neutral-content lint). *Finding:* the current `public/data/atlas.4326.geojson` holds 13 occurrences of such wording in free-text fields, and `atlas.manifest.json` holds 1 (the RU `notes` field). Fact-page templates must **not render** free-text `notes`-type fields that fail the lint. Data cleanup is a separate task for the data bot.
6. **Cloudflare routing caveat.** `/.well-known/x402.json` notes that `www` is a grey-cloud CNAME to Zo, so Worker routes do not fire there. New Workers therefore get **their own orange-clouded custom domains** (`id.`, `api.`, `mcp.`). Apex discovery files are added as static files by the Zo deploy bot.

---

## 2. Architecture

```
                        ┌──────────────────────────── Cloudflare ────────────────────────────┐
 Browser ──────────────►│ id.arctictradelanes.com  (Worker "atl-id")                          │
  (consumer/business)   │   /auth/*  OIDC (Google, Microsoft, LinkedIn, Apple, GitHub)         │
                        │   /auth/email  magic link (Email Service binding EMAIL)              │
                        │   /account/*  profile, orgs, consents, API keys, DSAR                │
                        │   Turnstile on forms · Rate Limiting binding                         │
 AI agent ─────────────►│ api.arctictradelanes.com (Worker "atl-api")                          │
  (API key / OAuth /    │   /v1/agents/*  registry   /v1/objects/*  atlas facts (free+paid)    │
   x402 v2 / MPP)       │   /v1/lanes/compare (paid, x402 v2)                                  │
                        │ mcp.arctictradelanes.com (Worker "atl-mcp")                          │
 MCP client ───────────►│   OAuthProvider(/authorize,/token,/register) → McpAgent "/mcp"       │
                        │   withX402(McpServer) + paidTool · FlexportBridge DO (MCP client)    │
                        │                                                                      │
                        │  D1 atl-accounts ◄── primary                                         │
                        │  Queue atl-events ──► consumer ──► R2 atl-events (JSONL, bucket lock)│
                        │                └─► DLQ atl-events-dlq                                │
                        │  Workflow nightly-backup ──► D1 export API ──► encrypt ──► R2 atl-backups│
                        │  Cron: reconciler (*/5), stats-to-GitHub (daily), restore drill (monthly)│
                        │  KV: OAUTH_KV (MCP OAuth), FLAGS · Durable Objects: FlexportBridge    │
                        └──────────────────────────────────────────────────────────────────────┘
 Zo site (apex/www): untouched pages + NEW static: /.well-known/agent-card.json, /.well-known/agent.json,
                     llms.txt additions, /port/* etc. fact pages (pre-rendered), sitemaps, brand strip component
```

**Libraries (suggested):** `hono` (routing), `arctic` (npm OAuth 2.0/OIDC clients for Google, Microsoft Entra ID, LinkedIn, Apple and GitHub, with PKCE), `jose` (JWT/JWKS verification), `@cloudflare/workers-oauth-provider`, `agents` (Agents SDK: `McpAgent`, `agents/x402`), `zod`, `ulid`.

**Cloudflare docs used for this spec** (searched with the Cloudflare docs MCP on 2026-10-06):

| Topic | URL |
|---|---|
| Agentic payments overview (x402 + MPP) | https://developers.cloudflare.com/agents/tools/payments/ |
| x402 on Workers / Agents SDK | https://developers.cloudflare.com/agents/tools/payments/x402/ |
| Charge for MCP tools (`withX402`, `paidTool`) | https://developers.cloudflare.com/agents/tools/payments/x402/charge-for-mcp-tools/ |
| Charge for HTTP content (x402 proxy) | https://developers.cloudflare.com/agents/tools/payments/x402/charge-for-http-content/ |
| Pay from the Agents SDK (`withX402Client`) | https://developers.cloudflare.com/agents/tools/payments/x402/pay-from-agents-sdk/ |
| MPP on Cloudflare | https://developers.cloudflare.com/agents/tools/payments/mpp/ · https://developers.cloudflare.com/agents/tools/payments/mpp/accept-payments/ |
| Monetization Gateway (x402 v2, closed beta 2026-09-30) | https://developers.cloudflare.com/monetization-gateway/x402/ · https://developers.cloudflare.com/changelog/post/2026-09-30-closed-beta/ |
| Agents SDK v0.4.0 (x402 v2 migration, MCP OAuth `callbackPath`) | https://developers.cloudflare.com/changelog/post/2026-02-09-agents-sdk-v0.4.0/ |
| MCP authorization (OAuth Provider Library, third-party IdP) | https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/ |
| Build a remote MCP server | https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/ |
| D1 Time Travel (PITR, 30 days) | https://developers.cloudflare.com/d1/reference/time-travel/ |
| D1 import/export | https://developers.cloudflare.com/d1/best-practices/import-export-data/ |
| Workflow: export D1 to R2 | https://developers.cloudflare.com/workflows/examples/backup-d1/ |
| R2 bucket locks | https://developers.cloudflare.com/r2/buckets/bucket-locks/ |
| Queues retries / DLQ (wrangler config) | https://developers.cloudflare.com/workers/wrangler/configuration/ |
| Email Service (sending from Workers) | https://developers.cloudflare.com/email-service/ · https://developers.cloudflare.com/email-service/api/send-emails/workers-api/ |
| Turnstile | https://developers.cloudflare.com/turnstile/ |
| Pay Per Crawl (do **not** enable on fact pages) | https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/ |

Key facts taken from these docs:
- The Agents SDK has first-class x402: server-side `withX402` and `paidTool` for MCP servers plus `x402-hono` middleware, and client-side `withX402Client` with optional human approval. x402 uses the `PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE` and `PAYMENT-RESPONSE` headers. The Agents SDK moved to `@x402/core` and `@x402/evm` **v2** in v0.4.0.
- MPP uses `WWW-Authenticate: Payment` and `Authorization: Payment`, supports cards via Stripe as well as stablecoins, has the intents `charge`, `session` and `subscription`, and is **backward compatible with x402**.
- D1 Time Travel is always on, can restore to any minute in the last 30 days at no extra cost, and **restores in place** (so take an export before restoring).
- A Queue consumer without a `dead_letter_queue` **discards** messages that keep failing. ATL therefore always configures a DLQ.
- Email Sending (Workers binding `send_email`) requires the **Workers Paid** plan and Cloudflare DNS.

**Observation about the current x402 implementation:** the live `/.well-known/x402.json` declares `x402Version: 1` and the custom request header `x402-payment: x402:<addr>:<amount>`. This is not the standard x402 v2 header set. Leave it as is (additive rule). New endpoints use **standard x402 v2** via the Agents SDK, and `x402.json` gets a **new sibling** file, `/.well-known/x402-v2.json`, rather than an edit.

---

## 3. Identity and login providers

### 3.1 Order and justification

| Order | Provider | Who | Why this position | Business-domain signal |
|---|---|---|---|---|
| 1 | **Google** ("Sign in with Google") | Consumers (Gmail) and Google Workspace businesses | Largest consumer IdP, one-tap, free, simple OIDC. The owner asked for it first. | `hd` claim = Workspace domain (business) when present; `@gmail.com` = consumer |
| 2 | **Microsoft Entra ID** (work and personal accounts, `common` endpoint) | Freight forwarders, carriers, ports and shipowners, who mostly run Microsoft 365 / Outlook | Most logistics enterprises are M365 tenants, and Entra gives a **tenant ID (`tid`)** that proves an organisational account | `tid` ≠ consumer tenant `9188040d-6c67-4c5b-b112-36a304b66dad` → work account; use `email` + `xms_edov` (email domain owner verified) when available |
| 3 | **LinkedIn** ("Sign In with LinkedIn using OpenID Connect") | B2B professionals, sales and BD in shipping | Strong professional identity and social proof. The owner asked for it. | Email only (`email_verified`), no company domain claim, so the business gate still applies |
| always | **Email magic link** | Everyone, and **agents' operator emails** | Works for every business email domain with no IdP dependency, and is required for "register with business email" | The mailbox is proven by the click |
| 4 (Phase 6) | **Sign in with Apple** | iOS consumers | Apple requires it only if an iOS app offers other social logins. ATL is web-first, so it is optional. Costs a $99/yr developer program. | Private-relay emails cannot be business-verified |
| 5 (Phase 6) | **GitHub** | Agent builders and OSS GIS contributors | Fits the agent registry and the OSS repo community | None; developer identity only |

Other logistics-popular options for later: **Okta / generic OIDC / SAML SSO** for enterprise customers (Arctic Command tier) through a per-org OIDC config, and **Yandex ID / VK ID** if the RU-locale audience grows (out of MVP scope).

**Recommendation on ordering versus the owner's list:** keep Google first. Put Microsoft **before** LinkedIn on the **business** sign-up tab because it gives a verifiable organisational signal (`tid`). Keep LinkedIn first on the **consumer/professional** tab. Ship both in Phase 2.

### 3.2 Redirect URIs (register exactly these)

| Provider | Production redirect URI | Staging redirect URI |
|---|---|---|
| Google | `https://id.arctictradelanes.com/auth/callback/google` | `https://id-staging.arctictradelanes.com/auth/callback/google` |
| Microsoft | `https://id.arctictradelanes.com/auth/callback/microsoft` | `https://id-staging.arctictradelanes.com/auth/callback/microsoft` |
| LinkedIn | `https://id.arctictradelanes.com/auth/callback/linkedin` | `https://id-staging.arctictradelanes.com/auth/callback/linkedin` |
| Apple | `https://id.arctictradelanes.com/auth/callback/apple` (form_post) | same pattern |
| GitHub | `https://id.arctictradelanes.com/auth/callback/github` | separate OAuth app for staging |
| Flexport (MCP client) | `https://id.arctictradelanes.com/integrations/flexport/callback` | same pattern |
| Local dev | `http://localhost:8787/auth/callback/<provider>` (Google and Microsoft allow localhost; LinkedIn needs an explicit URL entry) | |

### 3.3 Provider setup steps (Aleksei does these; the bot only needs the resulting IDs and secrets)

**Google (Google Cloud Console)**
1. https://console.cloud.google.com → create project `atl-identity`.
2. *Google Auth Platform → Branding*: app name "ArcticTradeLanes", support email `cto@arctictradelanes.com`, logo, home page `https://arctictradelanes.com`, privacy `https://arctictradelanes.com/privacy`, terms `https://arctictradelanes.com/terms`, authorised domain `arctictradelanes.com`.
3. *Audience*: External → **Publish app** (In production). Scopes are only `openid`, `email` and `profile` (non-sensitive, so no security review; brand verification takes a few days).
4. *Clients → Create client → Web application*: authorised JavaScript origin `https://id.arctictradelanes.com`, redirect URIs from §3.2.
5. Hand the bot `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` (set with `wrangler secret put`). Never paste them into GitHub.

**Microsoft Entra ID (Azure portal)**
1. https://entra.microsoft.com → *App registrations → New registration*: name "ArcticTradeLanes", supported account types **"Accounts in any organizational directory and personal Microsoft accounts"**, redirect (Web) from §3.2.
2. *Certificates & secrets*: new client secret, maximum 24 months. **Put an expiry reminder in the calendar.**
3. *API permissions*: Microsoft Graph delegated `openid`, `profile`, `email`, `offline_access`, `User.Read`. No admin consent is needed for these.
4. *Token configuration*: add optional claims `email`, `xms_edov`, `verified_primary_email`.
5. *Branding & properties*: publisher domain `arctictradelanes.com`. Then complete **Publisher verification** (needs a Microsoft AI Cloud Partner Program ID) so consent screens don't say "unverified".
6. Hand over `MS_CLIENT_ID`, `MS_CLIENT_SECRET` and `MS_TENANT=common`.

**LinkedIn (LinkedIn Developer Portal)**
1. Create a **LinkedIn Company Page** "ArcticTradeLanes" if it doesn't exist (an app must be tied to a page).
2. https://www.linkedin.com/developers/apps → *Create app* → link the page → a page admin approves **app verification**.
3. *Products*: add **"Sign In with LinkedIn using OpenID Connect"** (self-serve).
4. *Auth*: add the redirect URLs from §3.2. Scopes are `openid`, `profile` and `email`.
5. Hand over `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET`.

**Apple (Phase 6):** Apple Developer Program → Identifiers → **Services ID** (`com.arctictradelanes.web`) → enable Sign in with Apple → domains `id.arctictradelanes.com`, return URL from §3.2 → create **Key** (.p8) with Sign in with Apple → hand over Team ID, Key ID, .p8 and Services ID. Also register the sending domain in *Private Email Relay* so mail to `privaterelay.appleid.com` addresses is delivered.

**GitHub (Phase 6):** org `International-Arctic` → Settings → Developer settings → OAuth Apps → New, with callback from §3.2. Hand over the client ID and secret.

### 3.4 Login flow (all OIDC providers)

`GET /auth/start/:provider?return_to=` → generate `state`, `nonce` and a PKCE `code_verifier`, keep them for 10 minutes in a signed, encrypted `__Host-atl_oauth` cookie → redirect → `GET /auth/callback/:provider` → exchange the code → verify the `id_token` with JWKS (`jose`) → upsert `identities` → link to an existing `users` row by **verified** email only → create a `sessions` row → set `__Secure-atl_session` (HttpOnly, Secure, SameSite=Lax, Domain=`.arctictradelanes.com`, 30-day rolling) → emit `user.signed_in` / `user.registered`.

**Account linking rule:** auto-link only when the IdP says `email_verified=true` **and** the email matches an existing verified user. Otherwise ask the user to confirm through a magic link to the existing address. This prevents account takeover through an unverified IdP email.

---

## 4. Registration types

### 4.1 Consumer
Any verified email or social login. Gets the free tier (atlas, map, 10 route runs/day). Marketing consent is **unchecked by default** and triggers double opt-in.

### 4.2 Business (business email required)
1. Email must be verified (magic link or IdP `email_verified`).
2. **Business-email gate:** reject domains in a free-mail and disposable blocklist (gmail.com, googlemail.com, outlook.com, hotmail.*, live.*, yahoo.*, icloud.com, me.com, proton.me, protonmail.com, gmx.*, mail.ru, yandex.*, qq.com, 163.com, 126.com, naver.com, plus a disposable list such as `disposable-email-domains`). The domain must have **MX** records (DNS-over-HTTPS lookup to `cloudflare-dns.com`).
3. Org auto-creation: the first verified user of `example.com` creates `organizations(primary_domain='example.com')` and becomes `owner`. Later users with the same verified domain join as `member`, pending owner approval (a setting).
4. Optional **strong domain proof** for "verified business" badges and Flexport/booking features: DNS TXT `_atl-verify.example.com = "atl-domain-verification=<token>"` **or** `https://example.com/.well-known/atl-verification.txt` holding the token.
5. Fields: legal name, country (ISO2), sector (shipping, port, forwarding, energy, mining, insurer, shipbuilding, government, research, other), size band and website. **No** tax IDs in the MVP.

### 4.3 AI agent (see §5)
The agent is registered **by** a business user (operator) or through a self-serve API call that is completed by the operator's email confirmation.

---

## 5. Agent registry, discovery and protocols

### 5.1 Registration flow
```
POST https://api.arctictradelanes.com/v1/agents/register
{ "name": "ice-route-bot", "operator_email": "ops@carrier.example", "domain": "carrier.example",
  "agent_card_url": "https://carrier.example/.well-known/agent-card.json",   // optional (A2A)
  "mcp_url": "https://carrier.example/mcp",                                 // optional
  "payer_wallet": "0x…", "auth": "api_key" | "oauth_client", "tier": "x402_metered" }
→ 202 { agent_id, status:"pending_operator", verify: { dns_txt: { name:"_atl-agent.carrier.example", value:"atl-agent=<token>" },
                                                       well_known: "https://carrier.example/.well-known/atl-agent.json" } }
```
1. The operator email must pass the **business gate** (§4.2). A magic link goes to the operator, who clicks "Approve agent".
2. **Domain proof** (either one): DNS TXT `_atl-agent.<domain>` = `atl-agent=<token>`, or `https://<domain>/.well-known/atl-agent.json` = `{"atl_agent_id":"…","token":"…"}`. A verifier cron runs every 10 minutes for 72 hours, then expires the request.
3. Credentials are issued once both checks pass:
   - **API key:** `atl_live_<22 chars base62>`, shown **once**. D1 stores `sha256(key)` plus an 8-character prefix. Sent as the `x-api-key` header, matching the existing convention.
   - **OAuth client:** registered in the ATL MCP OAuth provider (workers-oauth-provider, DCR at `mcp.arctictradelanes.com/register`) and bound to the agent's operator org.
4. **Pricing tier** (per-call x402 v2, USDC on Base, payTo = the existing settlement wallet unless Aleksei sets a new one):

| Tier | Price | Limits | Notes |
|---|---|---|---|
| `free` | 0 | 60 req/h per agent, `/v1/objects/*` read only | API key needed (accountability) |
| `x402_metered` | per call (table below) | 600 req/min | No key needed for paid calls, but registered agents get receipts linked in the dashboard |
| `prepaid` | top-up credits via x402 `upto` or MPP `session` | per balance | Phase 5 |
| `enterprise` | invoice | SLA | "Arctic Command" |

| Endpoint / MCP tool (NEW) | Price |
|---|---|
| `GET /v1/objects/{id}` · `get_object` | free (cached facts) |
| `GET /v1/objects?bbox=&layer=` · `search_objects` | free up to 100 results, then $0.002/call |
| `POST /v1/lanes/compare` · `compare_lanes` (NSR vs Suez/Cape: distance, transit, ice window) | $0.05 |
| `GET /v1/exports/{layer}.geojson?crs=3996` (bulk, latest) | $1.00 |
| `route_optimize` (MCP wrapper around the **existing** `/api/alpha/route-optimize`; the existing endpoint and price are unchanged) | 5 USDC (the existing price, passed through) |

### 5.2 A2A agent card
- **Canonical path per the A2A spec:** `https://arctictradelanes.com/.well-known/agent-card.json` (A2A spec §8.2 and the IANA well-known registration, https://a2a-protocol.org/latest/specification/).
- **Alias requested by the owner:** `/.well-known/agent.json` serves the same JSON (older A2A clients look there).

```json
{
  "name": "ArcticTradeLanes Atlas Agent",
  "description": "Arctic GIS OSINT: NSR / Polar Silk Road ports, lanes, vessels, programs; NSR vs Suez lane comparison on EPSG:3996.",
  "url": "https://api.arctictradelanes.com/a2a",
  "version": "1.0.0",
  "provider": { "organization": "ArcticTradeLanes.com", "url": "https://arctictradelanes.com" },
  "documentationUrl": "https://arctictradelanes.com/llms.txt",
  "capabilities": { "streaming": false, "pushNotifications": false, "extendedAgentCard": true },
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "application/geo+json"],
  "securitySchemes": {
    "apiKey": { "apiKeySecurityScheme": { "location": "header", "name": "x-api-key" } },
    "oauth":  { "oauth2SecurityScheme": { "flows": { "authorizationCode": {
                "authorizationUrl": "https://mcp.arctictradelanes.com/authorize",
                "tokenUrl": "https://mcp.arctictradelanes.com/token", "scopes": { "atlas:read": "Read atlas", "lanes:compare": "Lane comparison" } } } } }
  },
  "skills": [
    { "id": "atlas_lookup", "name": "Atlas object lookup", "description": "Facts for ports, shipyards, programs, rail, industry, vessels", "tags": ["arctic","ports","gis"] },
    { "id": "lane_compare", "name": "NSR vs Suez lane comparison", "description": "Distance, transit days, ice window (paid, x402)", "tags": ["nsr","routing"] },
    { "id": "route_optimize", "name": "NSR route optimisation", "description": "Wraps /api/alpha/route-optimize (5 USDC via x402)", "tags": ["nsr"] }
  ],
  "extensions": [
    { "uri": "https://x402.org", "description": "x402 v2 payments, USDC on Base", "required": false },
    { "uri": "https://mpp.dev",  "description": "Machine Payments Protocol (Phase 5)", "required": false }
  ]
}
```
(Field names follow the current A2A spec's protobuf JSON style. The bot must validate against the A2A JSON schema in CI.)

### 5.3 ATL remote MCP server (`https://mcp.arctictradelanes.com/mcp`)
- `OAuthProvider({ apiRoute:"/mcp", apiHandler: AtlMCP.serve("/mcp"), defaultHandler: AtlAuthHandler, authorizeEndpoint:"/authorize", tokenEndpoint:"/token", clientRegistrationEndpoint:"/register" })`. `AtlAuthHandler` reuses `id.` sessions, which means Google, Microsoft and LinkedIn upstream (the "third-party OAuth provider" pattern in the Cloudflare docs). KV namespace `OAUTH_KV`.
- `server = withX402(new McpServer({name:"ATL",version:"1.0.0"}), { network:"base", recipient: PAY_TO, facilitator:{ url: FACILITATOR_URL } })`.
- Tools: `search_objects` (free), `get_object` (free), `list_layers` (free), `compare_lanes` (`paidTool`, $0.05), `export_layer` (`paidTool`, $1), `route_optimize` (`paidTool`, 5 USDC, calls the existing endpoint server-side), and later `flexport_*` proxies (§10). All tools carry correct MCP annotations (`readOnlyHint`, `destructiveHint`).
- **Facilitator:** the docs' examples use `https://x402.org/facilitator`. Before mainnet, confirm that facilitator supports **Base mainnet**. If not, use the Coinbase CDP facilitator (needs CDP API keys). As an alternative, apply for Cloudflare **Monetization Gateway** (closed beta) and let it settle x402 at the edge.
- Stateless MCP note: with MCP SDK ≥ 1.26, create one `McpServer` per request or session and never share a global instance (per the Cloudflare changelog).

### 5.4 llms.txt (additive)
Append a section to the existing `/llms.txt`. Do not rewrite it.
```
## Accounts & agents (new)
- Register an agent: POST https://api.arctictradelanes.com/v1/agents/register (operator business email + DNS TXT or /.well-known/atl-agent.json proof)
- A2A card: https://arctictradelanes.com/.well-known/agent-card.json (alias /.well-known/agent.json)
- MCP: https://mcp.arctictradelanes.com/mcp (OAuth 2.1; paid tools via x402 v2, USDC on Base)
- Fact pages: https://arctictradelanes.com/port/{slug}, /shipyard/{slug}, /program/{slug}, /lane/{slug}, /vessel/{slug}, … (22 languages)
- Payments: x402 v2 discovery https://arctictradelanes.com/.well-known/x402-v2.json (legacy v1: /.well-known/x402.json unchanged)
```

### 5.5 Payment protocol matrix

| Protocol | Steward | What it does | Fit for ATL | Cloudflare support | Phase | ATL implementation |
|---|---|---|---|---|---|---|
| **x402** (v1 legacy) | x402 Foundation (Coinbase + Cloudflare) | HTTP 402 stablecoin pay-per-request | **Live today** (custom `x402-payment` header) | n/a | live | **Leave untouched** |
| **x402 v2** | same | `PAYMENT-REQUIRED` / `PAYMENT-SIGNATURE` / `PAYMENT-RESPONSE`, `exact` and `upto` schemes, facilitator verify/settle | Best fit for per-call agent pricing | **Native**: Agents SDK `withX402`/`paidTool`, `x402-hono`, `withX402Client`; Monetization Gateway (beta) | 3 | New `/v1/*` and MCP paid tools |
| **MPP** (Machine Payments Protocol) | mpp.dev (IETF draft, paymentauth.org) | 402 + `WWW-Authenticate: Payment`; **cards via Stripe** + stablecoins; intents charge/session/subscription; backward compatible with x402 | Lets agents pay **by card**, and supports the $49/mo plan as `subscription` | **Native**: `mppx`, mpp-proxy template, MCP `Transport.mcpSdk()` | 5 | Accept MPP alongside x402 on the same paid routes |
| **ACP** (Agentic Commerce Protocol) | OpenAI + Stripe, Apache-2.0 (https://agentic-commerce-protocol.com/) | Merchant checkout API for agent purchases (ChatGPT Instant Checkout); ATL stays merchant of record | Selling **Arctic Intel $49/mo** and data packs inside ChatGPT | none specific (REST/MCP on Workers) | 6 | `/acp/checkout_sessions` endpoints plus product feed; needs a Stripe account and OpenAI merchant approval |
| **AP2** (Agent Payments Protocol) | Google + partners (https://ap2-protocol.org/) | Verifiable **mandates** (intent and cart) proving user authorisation; extension to A2A; has an x402 extension for crypto settlement | Enterprise agents buying ATL reports with an auditable mandate | none specific | 6 | Advertise the AP2 extension in the agent card; accept a cart mandate on `/v1/orders`, settle through x402 or MPP |
| **Pay Per Crawl** | Cloudflare | Charge crawlers per page | **Do not enable on fact pages** (SEO/AEO reach matters more) | native | — | Not used |

---

## 6. Data model (D1 SQL)

This schema is also committed as [`0001_init.sql`](./0001_init.sql). It was checked with SQLite on 2026-10-06: every table is created, the consent ledger rejects `UPDATE` and `DELETE`, and the `marketing_status` view returns the latest action. All IDs are ULIDs (TEXT), all timestamps are ISO-8601 UTC TEXT, and emails are stored lower-cased. `-- PII` marks personal data. The consent ledger stores **no raw email**, only an HMAC lookup key plus the email encrypted under the subject key, so erasure through crypto-shredding still leaves a non-personal record that consent existed.

```sql
-- ATL accounts D1 schema v0001 (spec 2026-10-06). IDs are ULIDs; timestamps are ISO-8601 UTC; emails lower-case. "-- PII" marks personal data.
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id                TEXT PRIMARY KEY,
  email             TEXT NOT NULL UNIQUE,              -- PII
  email_verified_at TEXT,
  display_name      TEXT,                              -- PII
  locale            TEXT NOT NULL DEFAULT 'en' CHECK (locale IN ('en','ru','zh','ja','ko','el','de','nl','fr','es','it','pt','tr','ar','hi','vi','id','da','fi','sv','nb','is')),
  account_type      TEXT NOT NULL DEFAULT 'consumer' CHECK (account_type IN ('consumer','business','agent_operator','admin')),
  country_iso2      TEXT,
  subject_key_id    TEXT NOT NULL,                     -- envelope key for crypto-shredding
  status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','suspended','deleted')),
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  updated_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  deleted_at        TEXT
);

CREATE TABLE identities (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider          TEXT NOT NULL CHECK (provider IN ('google','microsoft','linkedin','apple','github','email')),
  provider_subject  TEXT NOT NULL,                     -- IdP 'sub'
  email_at_idp      TEXT,                              -- PII
  email_verified    INTEGER NOT NULL DEFAULT 0,
  hd_or_tenant      TEXT,                              -- Google 'hd' / Microsoft 'tid'
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  last_login_at     TEXT,
  UNIQUE (provider, provider_subject)
);
CREATE INDEX idx_identities_user ON identities(user_id);

CREATE TABLE sessions (
  id                TEXT PRIMARY KEY,                  -- sha256 of a 256-bit random token
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  expires_at        TEXT NOT NULL,
  ip_prefix         TEXT,                              -- /24 IPv4 or /48 IPv6 only
  user_agent_hash   TEXT,
  revoked_at        TEXT
);
CREATE INDEX idx_sessions_user ON sessions(user_id);

CREATE TABLE email_tokens (
  token_hash        TEXT PRIMARY KEY,                  -- sha256(token)
  email             TEXT NOT NULL,                     -- PII
  purpose           TEXT NOT NULL CHECK (purpose IN ('login','verify','marketing_doi','agent_operator_approve','dsar')),
  ref_id            TEXT,
  expires_at        TEXT NOT NULL,
  used_at           TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE organizations (
  id                TEXT PRIMARY KEY,
  legal_name        TEXT NOT NULL,
  primary_domain    TEXT NOT NULL UNIQUE,
  country_iso2      TEXT,
  sector            TEXT CHECK (sector IN ('shipping','port','forwarding','energy','mining','insurer','shipbuilding','government','research','other')),
  size_band         TEXT,
  website           TEXT,
  verification      TEXT NOT NULL DEFAULT 'email' CHECK (verification IN ('email','dns_txt','well_known','manual')),
  verified_at       TEXT,
  created_by        TEXT REFERENCES users(id),
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE org_domains (
  org_id            TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  domain            TEXT NOT NULL UNIQUE,
  method            TEXT NOT NULL CHECK (method IN ('email','dns_txt','well_known')),
  token_hash        TEXT,
  verified_at       TEXT,
  PRIMARY KEY (org_id, domain)
);

CREATE TABLE memberships (
  org_id            TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role              TEXT NOT NULL CHECK (role IN ('owner','admin','member','billing','viewer')),
  status            TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('pending','active','removed')),
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  PRIMARY KEY (org_id, user_id)
);

-- Consent ledger (append-only; enforced by triggers)
CREATE TABLE consent_texts (
  id                TEXT PRIMARY KEY,                  -- e.g. 'marketing_email-v1-en'
  purpose           TEXT NOT NULL CHECK (purpose IN ('terms','privacy','marketing_email','product_updates')),
  locale            TEXT NOT NULL,
  text_sha256       TEXT NOT NULL,
  published_at      TEXT NOT NULL
);
CREATE TABLE consent_events (
  id                TEXT PRIMARY KEY,
  user_id           TEXT REFERENCES users(id),
  email_hmac        TEXT NOT NULL,                     -- HMAC-SHA256(lower(email), secret pepper): lookup key, still personal data, never published
  email_enc         BLOB,                              -- PII, AES-GCM under the subject key; unreadable after crypto-shred
  purpose           TEXT NOT NULL,
  action            TEXT NOT NULL CHECK (action IN ('granted','confirmed_doi','withdrawn','unsubscribed_one_click','bounced','complained')),
  consent_text_id   TEXT REFERENCES consent_texts(id),
  source            TEXT NOT NULL,                     -- signup_form | account_settings | list_unsubscribe_post | support
  ip_prefix         TEXT,
  user_agent_hash   TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX idx_consent_email_purpose ON consent_events(email_hmac, purpose, created_at);
CREATE TRIGGER consent_events_no_update BEFORE UPDATE ON consent_events BEGIN SELECT RAISE(ABORT,'append-only'); END;
CREATE TRIGGER consent_events_no_delete BEFORE DELETE ON consent_events BEGIN SELECT RAISE(ABORT,'append-only'); END;
CREATE VIEW marketing_status AS
  SELECT c.email_hmac, c.purpose, c.action AS last_action, c.created_at AS last_at
  FROM consent_events c
  WHERE c.created_at = (SELECT MAX(c2.created_at) FROM consent_events c2 WHERE c2.email_hmac = c.email_hmac AND c2.purpose = c.purpose);
  -- marketing is sendable only when last_action = 'confirmed_doi'

-- Agents
CREATE TABLE agents (
  id                TEXT PRIMARY KEY,
  name              TEXT NOT NULL,
  operator_user_id  TEXT REFERENCES users(id),
  operator_org_id   TEXT REFERENCES organizations(id),
  operator_email    TEXT NOT NULL,                     -- PII
  domain            TEXT NOT NULL,
  agent_card_url    TEXT,
  mcp_url           TEXT,
  payer_wallet      TEXT,                              -- public address
  auth_type         TEXT NOT NULL CHECK (auth_type IN ('api_key','oauth_client')),
  tier              TEXT NOT NULL DEFAULT 'free' CHECK (tier IN ('free','x402_metered','prepaid','enterprise')),
  status            TEXT NOT NULL DEFAULT 'pending_operator' CHECK (status IN ('pending_operator','pending_domain','active','suspended','revoked','expired')),
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  activated_at      TEXT
);
CREATE TABLE agent_domain_verifications (
  agent_id          TEXT NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  method            TEXT NOT NULL CHECK (method IN ('dns_txt','well_known')),
  token_hash        TEXT NOT NULL,
  attempts          INTEGER NOT NULL DEFAULT 0,
  last_checked_at   TEXT,
  verified_at       TEXT,
  expires_at        TEXT NOT NULL,
  PRIMARY KEY (agent_id, method)
);
CREATE TABLE api_keys (
  id                TEXT PRIMARY KEY,
  agent_id          TEXT REFERENCES agents(id) ON DELETE CASCADE,
  org_id            TEXT REFERENCES organizations(id) ON DELETE CASCADE,
  key_prefix        TEXT NOT NULL,
  key_sha256        TEXT NOT NULL UNIQUE,
  scopes            TEXT NOT NULL DEFAULT 'atlas:read',
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  last_used_at      TEXT,
  revoked_at        TEXT
);
CREATE TABLE price_tiers (
  sku               TEXT PRIMARY KEY,                  -- compare_lanes | export_layer | search_objects_over_100 | route_optimize
  protocol          TEXT NOT NULL CHECK (protocol IN ('x402v2','mpp','x402v1_legacy')),
  amount_usd        TEXT NOT NULL,
  network           TEXT NOT NULL DEFAULT 'base',
  asset             TEXT NOT NULL DEFAULT 'USDC',
  active            INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE payments (
  id                TEXT PRIMARY KEY,
  sku               TEXT NOT NULL REFERENCES price_tiers(sku),
  agent_id          TEXT REFERENCES agents(id),
  protocol          TEXT NOT NULL,
  amount_usd        TEXT NOT NULL,
  payer             TEXT,
  tx_hash           TEXT,
  receipt_json      TEXT,
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- Integrations
CREATE TABLE flexport_connections (
  id                TEXT PRIMARY KEY,
  org_id            TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id           TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status            TEXT NOT NULL CHECK (status IN ('pending','connected','revoked','error')),
  role_snapshot     TEXT CHECK (role_snapshot IN ('Admin','Billing','Member','Analyst','Tracker','unknown')),
  token_ref         TEXT NOT NULL,                     -- Durable Object id; tokens live encrypted in DO storage only
  connected_at      TEXT,
  revoked_at        TEXT,
  UNIQUE (org_id, user_id)
);
CREATE TABLE booking_confirmations (
  id                TEXT PRIMARY KEY,                  -- single-use confirm_id
  org_id            TEXT NOT NULL,
  user_id           TEXT NOT NULL,
  tool              TEXT NOT NULL CHECK (tool IN ('rates_instant_book','rates_book_without_rate','rates_request_rate')),
  payload_sha256    TEXT NOT NULL,
  expires_at        TEXT NOT NULL,
  confirmed_at      TEXT,
  consumed_at       TEXT
);

-- Durability and privacy
CREATE TABLE outbox (
  event_id          TEXT PRIMARY KEY,                  -- same ULID in Queue + R2
  event_type        TEXT NOT NULL,
  subject_key_id    TEXT,
  payload_enc       BLOB NOT NULL,                     -- AES-GCM under the subject key
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  enqueued_at       TEXT,
  archived_at       TEXT
);
CREATE INDEX idx_outbox_pending ON outbox(archived_at) WHERE archived_at IS NULL;

CREATE TABLE subject_keys (
  id                TEXT PRIMARY KEY,
  wrapped_key       BLOB,                              -- NULL after crypto-shred
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  shredded_at       TEXT
);

CREATE TABLE dsar_requests (
  id                TEXT PRIMARY KEY,
  user_id           TEXT REFERENCES users(id),
  kind              TEXT NOT NULL CHECK (kind IN ('export','erase','rectify')),
  status            TEXT NOT NULL CHECK (status IN ('received','verified','done','rejected')),
  created_at        TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  completed_at      TEXT
);

CREATE TABLE backup_runs (
  id                TEXT PRIMARY KEY,
  kind              TEXT NOT NULL CHECK (kind IN ('d1_export','r2_manifest','restore_drill')),
  object_key        TEXT NOT NULL,
  bytes             INTEGER,
  sha256_ciphertext TEXT NOT NULL,
  row_counts_json   TEXT NOT NULL,
  started_at        TEXT NOT NULL,
  finished_at       TEXT,
  ok                INTEGER NOT NULL DEFAULT 0
);

INSERT INTO price_tiers (sku, protocol, amount_usd) VALUES
  ('search_objects_over_100','x402v2','0.002'),
  ('compare_lanes','x402v2','0.05'),
  ('export_layer','x402v2','1.00'),
  ('route_optimize','x402v2','5.00');
```

---

## 7. Storage durability: "never lose an email or registration"

### 7.1 Write path (every registration, consent change, agent registration and payment)

1. The `id.` or `api.` Worker validates the input (Turnstile for humans, a signature or API key for agents).
2. **A single D1 `batch()` (atomic)** writes the domain row(s) **and** an `outbox` row holding the full event envelope `{event_id, type, occurred_at, subject_id, payload_enc}`. Personal fields in `payload_enc` are encrypted with the subject's data key (§7.4).
3. **Same request, after commit:** `env.EVENTS.send(envelope)` sends the event to a Cloudflare Queue (`atl-events`). If the send fails, the outbox row stays `pending`.
4. A **Queue consumer** writes one object per event to **R2 `atl-events`** at `events/YYYY/MM/DD/HH/{event_id}.json`. Writing on a key is idempotent. The bucket has a **bucket-lock retention rule of 400 days**, so objects cannot be deleted or overwritten during that period, even by an admin token. On success, the consumer marks `outbox.status='shipped'`.
5. **DLQ:** the queue is configured with `max_retries=10` and the dead-letter queue `atl-events-dlq`. A cron job alerts the owner when the DLQ depth is above 0.
6. **Reconciler (cron, every 5 minutes):** re-enqueues any `outbox` rows that have been `pending` for more than 5 minutes. It also compares D1 and R2 counts per hour bucket and writes the result to `backup_runs` (kind `reconcile`).
7. **Hourly compaction:** a Workflow concatenates the per-event objects from the previous hour into `jsonl/YYYY/MM/DD/HH.jsonl.gz`. The per-event objects are kept, so compaction only adds data and is never destructive.
8. **If D1 is down:** the Worker catches the error, sends the envelope straight to the Queue, *and* `PUT`s it to R2 `inbox/{event_id}.json`. It then returns **202 Accepted** with the message "we have your registration, confirmation email follows". When D1 is back, a replay job applies the inbox events in ULID order, idempotently by `event_id`.

So an accepted registration exists in at least two independent stores (D1 plus the Queue or R2) before the user sees "success".

### 7.2 Copies and retention

| Copy | Mechanism | RPO | Retention | Restores from |
|---|---|---|---|---|
| D1 primary | `atl-accounts`, location hint `weur` | 0 | live | — |
| D1 Time Travel | built in, always on | about 1 minute (any point in time) | 30 days (Workers Paid) | `wrangler d1 time-travel restore` |
| R2 event log | Queue → per-event JSON plus hourly JSONL, **bucket lock 400 days** | seconds | 400 days, then lifecycle to Infrequent Access | event replay |
| Nightly encrypted export | Workflow → D1 export API → **age-encrypted** (public key only in the Worker) → R2 `atl-backups` (separate bucket and token, EU jurisdiction, bucket lock 35 days) | 24 hours | 35 daily + 12 monthly | decrypt offline → `wrangler d1 execute --file` |
| Off-Cloudflare copy (optional, Phase 4) | weekly rclone of `atl-backups` ciphertext to a second provider (e.g. Backblaze B2 or Hetzner, EU) | 7 days | 12 weeks | same as above |
| Public GitHub | **stats only**: `docs/mvp/stats/YYYY-MM-DD.json` with counts plus the SHA-256 of each backup *ciphertext* | — | forever | integrity proof only, not a data copy |

### 7.3 Restore runbooks (keep them in the private ops repo)

- **Bad migration or accidental delete (< 30 days):** `wrangler d1 time-travel info atl-accounts` → **first run `wrangler d1 export` of the current state** (Time Travel restore is *in place* and overwrites the database) → `wrangler d1 time-travel restore atl-accounts --timestamp=<ISO>`. Then replay events from R2 that are newer than the restore point.
- **Database lost or older than 30 days:** download the newest nightly export → `age -d -i atl-backup.key` (offline machine) → create a new D1 → import → replay R2 events after the export timestamp → swap the binding.
- **Monthly restore drill (acceptance test):** restore the latest export into `atl-accounts-drill`. Row counts must match the `backup_runs` record within the replay window. Log the result in the issue tracker without any personal data.

### 7.4 Erasure versus immutable storage: crypto-shredding

- Each subject (user or agent operator) gets a 256-bit data key in `subject_keys`. The key is wrapped with a KEK held as a Worker secret.
- Personal fields in D1 `*_enc` columns, R2 events and exports are encrypted with this data key.
- **Erasure (GDPR Art. 17):** delete the personal data from live D1 rows, then destroy the subject key (`subject_keys.destroyed_at`). Locked R2 objects and old exports become unreadable for that subject, while the rest of the log stays intact. Exports age out after 35 days or 12 months, which is documented in the privacy notice.
- `consent_events` rows keep `email_hmac`, the purpose, the action and the text version as non-reversible proof of consent history. `email_enc` becomes undecryptable.

### 7.5 What goes to the public GitHub repo

- **Allowed:** the schema (`0001_init.sql`), docs, daily counts (registrations by type, verified orgs, agents, DOI confirmations, unsubscribes), backup run IDs and ciphertext SHA-256 values.
- **Never:** emails, names, domains of individual registrants, IPs, hashes or HMACs of emails (they can be reversed by dictionary attack), API keys, OAuth secrets, or the age private key.
- **CI guard:** a GitHub Action fails the push if any file under `docs/mvp/stats/` matches an email regex, a 64-hex value outside the `ciphertext_sha256` field, or a `sk_`/`atl_live_` key prefix. The stats JSON is generated by the Worker and committed by the Zo bot through a fine-grained token limited to `contents:write` on this repo.

---

## 8. Privacy and consent (GDPR / UK GDPR / 152-FZ-aware, neutral)

- **Controller:** Aleksei Dolgikh (ArcticTradeLanes.com), cto@arctictradelanes.com. A postal address is required on `/privacy` (manual step).
- **Lawful bases:** account and agent registration = contract (Art. 6(1)(b)). Security logs = legitimate interest. **Marketing email = consent only**, with **double opt-in**: an unticked checkbox, then a confirmation link valid for 72 hours. `consent_events` stores `granted` → `confirmed_doi`, the IP /24 truncated, the user agent hash and the `consent_text_id`.
- **Unsubscribe:** every marketing email carries `List-Unsubscribe: <https://id.arctictradelanes.com/u/{token}>, <mailto:unsubscribe@arctictradelanes.com?subject={token}>` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (RFC 8058). One click writes a `withdrawn` event, with no login required. Transactional emails (verification, receipts, booking confirmations) are separate and cannot carry marketing content.
- **Business emails:** org verification requires a mailbox at the org's domain. Free-mail domains (gmail.com, outlook.com, yandex.ru, mail.ru, qq.com, …) can create a *consumer* account but cannot claim an org or operate an agent.
- **DSAR:** `/account/data` exports JSON within 30 days, usually immediately. Deletion follows §7.4. Requests are tracked in `dsar_requests`.
- **Processors** (listed on `/privacy`): Cloudflare (hosting, D1, R2, Queues, Email Service, Turnstile); Google, Microsoft, LinkedIn, Apple and GitHub only as identity providers chosen by the user; Flexport only when a user connects their own account; the x402 facilitator (e.g. Coinbase CDP) for paid calls. Transfers rely on the providers' DPAs and SCCs.
- **Location:** D1 `--location=weur`. R2 buckets are created with **EU jurisdiction** (`--jurisdiction eu`). Logs are kept for 30 days.
- **Cookies:** strictly necessary only (`__Secure-atl_session` and the short-lived `__Host-atl_oauth`; HttpOnly, Secure, SameSite=Lax), so no banner is needed for them. Analytics stays cookieless (Cloudflare Web Analytics).
- **Minimisation:** no phone number, no date of birth, no ID documents. Agent operators provide a business email and a domain only.
- **Neutral-content lint** (applies to the whole platform): a build-time check fails on banned political or restrictive-list terminology in templates, fact pages, the brands strip and JSON-LD. The term list lives in the private ops repo, not in public docs. *Finding:* 14 legacy free-text hits exist in `atlas.4326.geojson` (13) and `atlas.manifest.json` (1). They need owner-approved cleanup (§13, step 11), and fact pages must not render those fields until then.

---

## 9. Endpoints (all NEW; existing endpoints unchanged)

### 9.1 `id.arctictradelanes.com` (Worker `atl-id`)

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/auth/start/:provider` | — | Start OIDC (`google`, `microsoft`, `linkedin`; later `apple`, `github`) |
| GET/POST | `/auth/callback/:provider` | state + PKCE | OIDC callback (Apple uses `form_post`) |
| POST | `/auth/email` | Turnstile | Send a magic link (`email_tokens`, 15 min, single use) |
| GET | `/auth/email/verify?t=` | token | Consume the magic link → session |
| POST | `/auth/logout` | session | Revoke the session |
| GET | `/account` | session | Profile, identities, orgs, consents |
| POST | `/account/business` | session + verified business email | Create or join an org (§4.2) |
| POST | `/account/org/:id/domain-verify` | org owner | Start a DNS TXT or well-known domain proof |
| POST | `/account/consents` | session | Grant or withdraw a purpose (marketing grant → DOI email) |
| GET | `/c/:token` | token | Double opt-in confirmation (72 h) |
| GET/POST | `/u/:token` | token | One-click unsubscribe (RFC 8058 POST, plus GET confirmation page) |
| GET | `/account/data` | session | DSAR JSON export |
| POST | `/account/delete` | session + re-auth | Erasure request (§7.4) |
| GET | `/integrations/flexport/connect` | session + org role | Start Flexport MCP OAuth (DCR + PKCE) |
| GET | `/integrations/flexport/callback` | state | Store encrypted Flexport tokens in `flexport_connections` |
| GET | `/healthz` | — | Liveness, including D1, Queue and R2 probes |

### 9.2 `api.arctictradelanes.com` (Worker `atl-api`)

| Method | Path | Auth / price | Purpose |
|---|---|---|---|
| POST | `/v1/agents/register` | operator business email (Turnstile-free, rate-limited per IP and domain) | Create a pending agent (§5.1) |
| GET | `/v1/agents/:id` | API key / OAuth | Status, verification state, tier |
| POST | `/v1/agents/:id/verify` | API key | Re-check DNS TXT or well-known proof now |
| POST | `/v1/agents/:id/keys` · DELETE `/v1/agents/:id/keys/:prefix` | operator session | Rotate or revoke API keys |
| GET | `/v1/objects?bbox=&layer=&q=` | free ≤100 results, then x402 v2 $0.002 | Atlas search |
| GET | `/v1/objects/:id` | free | Object facts (same data as the fact pages) |
| POST | `/v1/lanes/compare` | x402 v2 $0.05 | NSR vs Suez/Cape comparison |
| GET | `/v1/exports/:layer.geojson?crs=3996` | x402 v2 $1.00 | Bulk layer export |
| GET | `/v1/receipts` | API key / OAuth | Payment receipts (`payments` table) |
| POST | `/v1/orders` | AP2 mandate (Phase 6) | Report and data-pack purchase |
| POST/GET | `/acp/checkout_sessions[/:id]` | ACP (Phase 6) | Agentic Commerce checkout |
| POST | `/a2a` | per agent card | A2A JSON-RPC endpoint (`message/send`), mapped to the same skills |

### 9.3 `mcp.arctictradelanes.com` (Worker `atl-mcp`)

| Path | Purpose |
|---|---|
| `/.well-known/oauth-authorization-server`, `/.well-known/oauth-protected-resource` | OAuth metadata (workers-oauth-provider) |
| `/authorize`, `/token`, `/register` | OAuth 2.1 + PKCE + DCR (upstream login through `id.`) |
| `/mcp` | Streamable HTTP MCP: `search_objects`, `get_object`, `list_layers`, `compare_lanes`*, `export_layer`*, `route_optimize`*, and Phase 4 `flexport_*` proxies (* = x402 `paidTool`) |

### 9.4 Static discovery files (added by the Zo deploy bot as new files on the apex)

`/.well-known/agent-card.json` (canonical A2A), `/.well-known/agent.json` (identical alias), `/.well-known/x402-v2.json` (new sibling; **`/.well-known/x402.json` unchanged**), `/.well-known/mcp.json` (pointer to `https://mcp.arctictradelanes.com/mcp`), an `/llms.txt` appended section (§5.4), `/sitemaps/*.xml` (§11), `/privacy`, `/terms`.

---

## 10. Flexport MCP (summary; full plan in [`flexport-mcp-integration.md`](./flexport-mcp-integration.md))

- **Model:** bring your own account. A verified ATL business connects **its own** Flexport account through per-user Flexport OAuth (DCR + PKCE S256) from `id.…/integrations/flexport/connect`. ATL never uses a shared Flexport login. Tokens are encrypted with AES-GCM under a per-org data key and live only in the `FlexportBridge` Durable Object's storage. D1 `flexport_connections` keeps metadata only (`token_ref` = DO id). Before multi-tenant use, Flexport's written OK is required under its Software and Data Access Terms.
- **Server:** `https://mcp.flexport.com/mcp` (Streamable HTTP). A `FlexportBridge` Durable Object per connection acts as the MCP client, with Flexport's limits of about 60 requests/min per user and 300/min per account (ATL throttles itself to 50 and 250).
- **What ATL shows:** shipments (`browse_shipments`, `track_shipment`) drawn as **tracking overlays on the EPSG:3996 map**; an **exceptions queue** built as the union of two calls (`HAS_ACTIVE_EXCEPTION` ∪ `HAS_CUSTOMS_HOLD`, because flags in one call are ANDed); **NSR vs Suez lane comparison** that puts Flexport's instant price for the Suez/Cape lane next to ATL's NSR distance, transit and ice-window model.
- **Bookings:** `rates_instant_book`, `rates_book_without_rate` and `rates_request_rate` are **never auto-allowed**. Each one needs a human confirm in the ATL UI, recorded in `booking_confirmations` with an expiring nonce. Addresses come only from `network_search_addresses` (`flx::` IDs), never invented.
- **Doc discrepancies found** (details in the Flexport doc): the client-rate mode of `rates_instant_book` needs no token (the confirmation token applies to snapshot mode only); `rates_book_without_rate` also excludes Li-ion, magnets and batteries and rejects Google-address IDs; HS-code search and pricing are limited to Admin, Billing and Member roles; Flexport exposes 5 more tools than the summary listed (`rates_browse_quote_requests`, `rates_get_quote_request_details`, `rates_get_quote_details`, `network_search_google_addresses`, `list_active_company_users`).
- **Rollout:** Flexport admin enables MCP for the account (`app.flexport.com/integrations/mcp-connection`) → ATL pilot with 1–3 customers on read-only tools → role check → quotes → human-confirmed bookings → general availability.

---

## 11. SEO: programmatic fact pages (templates, zero per-page AI)

### 11.1 Inventory (from `public/data/atlas.4326.geojson` and the manifest, 2026-10-06)

| Layer | Objects | URL prefix | schema.org type |
|---|---:|---|---|
| Ports | 155 | `/port/{slug}` | `Place` (+ `additionalType` Seaport) / `CivicStructure` |
| Cities / settlements | 103 | `/city/{slug}` | `City` (`Place`) |
| Shipyards | 70 | `/shipyard/{slug}` | `Place` + operator `Organization` |
| Programs / projects | 713 | `/program/{slug}` | `Project` (`Organization` subtype) or `CreativeWork`; `Place` via `location` |
| Airports | 10 | `/airport/{slug}` | `Airport` |
| Industry sites | 110 | `/industry/{slug}` | `Place` + operator `Organization` |
| Rail | 14 | `/rail/{slug}` | `Place` (line / terminal) |
| Lanes | 27 | `/lane/{slug}` | `Place` with `geo` `GeoShape` line + `Dataset` |
| Tankers | 51 | `/vessel/{slug}` | `Vehicle` (additionalType Ship) |
| Icebreakers | 56 | `/vessel/{slug}` | `Vehicle` (additionalType Icebreaker) |
| Rescue centres | 7 | `/rescue/{slug}` | `EmergencyService` / `Place` |
| **Total** | **1,316** | × 22 locales | **≈ 28,952 URLs** (before the thin-content gate) |

Layer pages: `/ports`, `/shipyards`, … list all objects in a layer and link to the map layer. Each one is also a `Dataset` page.

### 11.2 URL scheme and slugs

- English at the root: `/port/murmansk`. Other locales: `/{lang}/port/murmansk` (the 21 non-EN codes already used by the site, e.g. `/ru/`, `/zh/`, `/no/`). **The slug stays the same in every locale** (Latin transliteration), so hreflang mapping is a straight join.
- Slug = `kebab(ascii_fold(name_en))`, de-duplicated with `-{country}` and then `-{n}`. Slugs are stored in `public/data/slugs.json` (`{atlas_id: slug}`) and **never change once published**. Renames add a 301 entry to `redirects.json`.
- `/object/{atlas_id}` (e.g. `/object/arc-…`, used by the brands CSV) → **301** to the canonical typed URL. This keeps brand-strip links stable even if a layer changes.
- Map deep link from each page: `/?focus={atlas_id}&layer={layer}#z=6` opens the EPSG:3996 hero with the object selected.

### 11.3 Rendering

- **Pre-render at build time** with `scripts/build-fact-pages.mjs` (Node, no network calls). It reads the atlas GeoJSON, manifest, `slugs.json` and `i18n/labels.{lang}.json`, and writes static HTML into the Zo site output. The deploy bot runs it as part of the normal Zo publish. No Worker is needed on `www`, which suits the grey-cloud setup.
- **Fallback (only if the static file count becomes a problem on Zo):** Worker SSR on an orange-clouded host, with the same template module and Cache API (`s-maxage=86400`).
- **i18n is label-only:** field labels, headings and units are translated (about 120 strings × 21 locales, a one-off DeepL or manual job). Object names use the `name:{lang}` property where present and fall back to English. **No per-page generated prose.** The intro sentence is a template, e.g. "{name} is a {type_label} in {country_label} on the {sea_label}, located at {lat}, {lon}."

### 11.4 Thin-content gate and page anatomy

- A page is indexed only if the object has **≥ 5 populated structured fields** (e.g. type, country, coordinates, operator, capacity/depth/year, source URL). Below that, the page is still rendered for users but carries `noindex,follow` and is left out of the sitemap.
- **Only structured fields** render. Free-text `notes`/`description` fields render **only** if they pass the neutral-content lint (§8). Until the 14 legacy hits are cleaned, those fields are hidden for the affected objects.
- **Anatomy:** H1 name → template intro → facts table (dl) → static mini-map (pre-rendered SVG in EPSG:3996, no JS needed) + "Open on the polar map" button → "Nearby on the atlas" (the 8 nearest objects by great-circle distance, computed at build time) → "Same operator" / "Same program" links → lanes passing within 50 nm → source links → last-updated date → breadcrumb.
- **Internal links:** every page links to its layer page, its country hub (`/country/{iso2}`), its sea hub (`/sea/{slug}`, e.g. Kara, Laptev, Barents) and the map. Hubs link down. Every page is therefore reachable within 3 clicks from the home page.

### 11.5 Structured data (JSON-LD, one `@graph` per page)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": ["Place", "CivicStructure"], "@id": "https://arctictradelanes.com/port/murmansk#place",
      "name": "Murmansk", "additionalType": "https://www.wikidata.org/wiki/Q44782",
      "geo": { "@type": "GeoCoordinates", "latitude": 68.97, "longitude": 33.05 },
      "address": { "@type": "PostalAddress", "addressCountry": "RU" },
      "containedInPlace": { "@type": "Place", "name": "Barents Sea" },
      "sameAs": ["https://www.wikidata.org/wiki/Q…"],
      "url": "https://arctictradelanes.com/port/murmansk",
      "hasMap": "https://arctictradelanes.com/?focus=arc-…&layer=ports" },
    { "@type": "Organization", "@id": "https://arctictradelanes.com/port/murmansk#operator", "name": "{operator}" },
    { "@type": "Dataset", "name": "ArcticTradeLanes atlas: ports layer", "url": "https://arctictradelanes.com/ports",
      "license": "{atlas license}", "creator": { "@type": "Organization", "name": "ArcticTradeLanes.com" },
      "spatialCoverage": { "@type": "Place", "geo": { "@type": "GeoShape", "box": "60 -180 90 180" } },
      "distribution": [{ "@type": "DataDownload", "encodingFormat": "application/geo+json", "contentUrl": "https://api.arctictradelanes.com/v1/exports/ports.geojson" }] },
    { "@type": "BreadcrumbList", "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Atlas", "item": "https://arctictradelanes.com/" },
      { "@type": "ListItem", "position": 2, "name": "Ports", "item": "https://arctictradelanes.com/ports" },
      { "@type": "ListItem", "position": 3, "name": "Murmansk" } ] }
  ]
}
```
Fields without data are **omitted**, never filled with placeholders. `sameAs` (Wikidata/Wikipedia) is set only when the atlas already holds the ID. A validator step in CI parses every generated JSON-LD block and checks the required properties.

### 11.6 hreflang, canonical, sitemaps, robots

- Each page: `<link rel="canonical">` to itself in its own locale, plus **23 `<link rel="alternate" hreflang>`** entries (22 locales + `x-default` → EN). Use `zh-CN` (not `zh`) if the site's Chinese is Simplified, and match the codes already in the live sitemap. Reciprocity is checked in CI.
- **Sharded sitemaps:** `/sitemaps/index.xml` → one file per layer per locale, e.g. `/sitemaps/port-ru.xml`, each under 50,000 URLs and 50 MB, with `<xhtml:link>` alternates and `<lastmod>` taken from the object's data timestamp (not the build time). Add `Sitemap: https://arctictradelanes.com/sitemaps/index.xml` to `robots.txt` as an **added line**. Keep the existing sitemap.
- AI crawlers: keep allowed (AEO). Do **not** enable Pay Per Crawl on fact pages.

### 11.7 SEO acceptance tests

1. Build produces ≥ 1 page per indexable object per locale. The page count equals the sitemap URL count.
2. 100 % of pages have a valid JSON-LD graph (schema.org validator in CI) and 23 reciprocal hreflang links.
3. No page contains banned neutral-content terms (lint = 0 hits).
4. Lighthouse SEO ≥ 95 and LCP < 2.5 s on a sample of 20 pages (static HTML, no map JS until the user clicks).
5. `/object/{id}` returns a 301 to the canonical URL. Unknown slugs return a real 404.
6. Google Search Console: sitemap index accepted. Two weeks after submission, ≥ 50 % of submitted EN port pages are indexed (monitored, not blocking).

---

## 12. Arctic brands strip (social proof, legally safe)

**Data:** [`arctic-brands.csv`](./arctic-brands.csv) has **50 brands** across shipping, energy, ports, logistics, icebreaker operators, shipbuilding, classification, insurance, mining and maritime tech. Each row has the country, the sector, a one-line Arctic relevance with a source URL, the Wikipedia/Wikidata ID, the official website, the logo source (Wikimedia Commons file page) with its licence, and the matching atlas object.

| `strip_status` | Count | Meaning |
|---|---:|---|
| `ready` | 22 | Commons logo with a free licence (21 public domain / CC0, 1 CC BY-SA 4.0) **and** an atlas object to link to |
| `needs_logo` | 22 | The atlas object exists, but no free Commons logo was found. Request one from the press or media kit (Aleksei) or show the text name only |
| `needs_atlas_object` | 6 | Logo or relevance is fine, but there is no atlas object yet (Vår Energi, Skuld, Wärtsilä, Lynden, Samsung Heavy Industries, Russian Maritime Register of Shipping). Add the objects first; the strip never links to a missing page |

**Ready now:** Novatek, Sovcomflot, Gazprom Neft, Nornickel, COSCO Shipping, Maersk, Equinor, Tschudi Shipping Company, Hurtigruten, DNV, Kongsberg Gruppen, Aker Arctic, Helsinki Shipyard, LKAB, Seaspan ULC, ConocoPhillips, Crowley, Hanwha Ocean, Mitsui O.S.K. Lines, TotalEnergies, DP World, Lloyd's Register.

**Presentation rules (legal guardrails):**
1. Heading: **"Arctic ecosystem: companies covered on the atlas"** (translated in all 22 locales). Small disclaimer below: *"Logos and names are trademarks of their owners and are shown only to identify companies profiled in the ArcticTradeLanes atlas. No affiliation, endorsement or business relationship is implied."*
2. **Forbidden wording** until a signed relationship exists: "partners", "trusted by", "customers", "clients", "used by", "powered by", "in collaboration with". The CI lint checks the strip component and its 22 translations for these terms.
3. **Each logo links to its atlas object page** (`/object/{atlas_id}` → 301 to the typed fact page), **never** to the company's own site. Alt text is "{Brand} on the ArcticTradeLanes atlas".
4. **Neutral profiles only.** The strip and the linked fact pages carry no political, legal-status or restrictive-list labels, badges or links.
5. Display: monochrome or greyscale logos (CSS `filter: grayscale(1)`, colour on hover), uniform height of 28 px, no resizing that distorts proportions, no recolouring beyond greyscale. Order alphabetically or rotate randomly per page load, so nobody gets "featured" placement.
6. **Self-host** the logo files in `/assets/brands/{slug}.svg` (downloaded once from Commons at the recorded file page). Do not hotlink. Keep an `ATTRIBUTION.md` next to them that lists each file, its source URL and its licence. **Tschudi (CC BY-SA 4.0)** needs visible attribution (author + licence link) in a tooltip or on a credits page.
7. Many Commons logos are tagged *PD-textlogo* (below the threshold of originality). That covers **copyright only, not trademark**. Nominative use under rules 1–5 is the safeguard. If a company objects, remove the logo within 48 hours (a `hidden` flag in the CSV).
8. Rows with `needs_logo` show the brand name in text (same height, small caps) until Aleksei gets a press-kit logo with written permission to use it.

---

## 13. What Aleksei must do himself (the bot cannot)

1. **Google OAuth client:** create the Google Cloud project, branding, publish the app, create the Web client with the §3.2 redirect URIs, and hand over the client ID and secret as Worker secrets.
2. **Microsoft Entra app:** register a multitenant + personal-account app, create a client secret (**put a calendar reminder before its 24-month expiry**), add optional claims and complete **publisher verification** (Microsoft AI Cloud Partner Program ID).
3. **LinkedIn:** create or confirm the ArcticTradeLanes **Company Page**, create the developer app, approve **app verification** as page admin, add the **"Sign In with LinkedIn using OpenID Connect"** product and the redirect URLs.
4. **Cloudflare account:**
   - Upgrade to **Workers Paid**.
   - Create D1 `atl-accounts` (`--location=weur`), R2 `atl-events` and `atl-backups` (**EU jurisdiction**, with **bucket-lock rules** of 400 and 35 days), Queues `atl-events` and `atl-events-dlq`, KV `OAUTH_KV`, and a Turnstile widget.
   - Add **orange-clouded** DNS records for `id.`, `api.` and `mcp.` (and `*-staging`).
   - Onboard the **Email Sending** domain (SPF/DKIM/DMARC).
   - Accept the Cloudflare **DPA**.
   - Create scoped API tokens for the deploy bot (no global key).
5. **Backup keys:** generate an **age keypair offline** (`age-keygen`). Only the **public** key goes to the bot or Worker. Keep the private key offline in two places (e.g. a password manager and a printed copy in a safe).
6. **Legal pages:** approve `/privacy` and `/terms` with the controller identity and a **postal address**, the processor list (§8) and the DOI and unsubscribe wording.
7. **Payments:**
   - Confirm the x402 v2 `payTo` (the existing wallet `0x211D…8Cea` or a new one).
   - Choose the facilitator (Coinbase **CDP** for Base mainnet: create CDP API keys) or apply for the Cloudflare **Monetization Gateway** beta.
   - Later: a **Stripe** account for MPP card payments, **OpenAI ACP** merchant onboarding, and AP2 evaluation.
8. **Flexport:** get Flexport's **written OK** for multi-tenant MCP use, ask about a sandbox account, and line up 1–3 **pilot customers** whose Flexport admins enable MCP.
9. **Brands:** approve the 22 `ready` logos, request press-kit logos for the 22 `needs_logo` rows (or accept text names), and approve the 6 new atlas objects.
10. **Search Console:** verify the domain property and submit `/sitemaps/index.xml` after Phase 1 ships.
11. **Data cleanup approval:** approve the data bot's neutral-content cleanup of the 14 legacy free-text hits (13 in `atlas.4326.geojson`, 1 in `atlas.manifest.json`).
12. **GitHub:** create a fine-grained token (`contents:write` on this repo only) for the daily stats commit, and enable branch protection with the PII-guard CI check required.

---

## 14. Phased MVP checklist with acceptance tests

**Phase 0: Foundations (no user-visible change)**
- [ ] Cloudflare resources from §13.4 created. `wrangler.toml` for `atl-id`, `atl-api` and `atl-mcp` with bindings `DB`, `EVENTS` (queue producer), `EVENTS_R2`, `BACKUPS_R2`, `OAUTH_KV`, `EMAIL`, `TURNSTILE_SECRET` and `RATE_LIMITER`.
- [ ] `0001_init.sql` applied (`wrangler d1 migrations apply atl-accounts`).
- [ ] Baseline SHA-256 snapshot of all existing endpoints (§1.1) stored in CI.
- **Accept:** `GET id.…/healthz` returns `{d1:"ok",queue:"ok",r2:"ok"}`. Existing endpoint hashes are unchanged.

**Phase 1: Durable email capture + magic link + consent (ships first; "never lose an email")**
- [ ] `/auth/email`, `/auth/email/verify`, sessions, the business-email gate, DOI (`/c/:token`) and one-click unsubscribe (`/u/:token`).
- [ ] Outbox → Queue → R2 per-event objects, DLQ, reconciler, hourly compaction, D1-down 202 fallback.
- [ ] Nightly encrypted export Workflow, `backup_runs`, daily stats JSON committed to `docs/mvp/stats/`, PII-guard CI.
- **Accept:**
  1. 1,000 synthetic sign-ups → 1,000 D1 rows = 1,000 R2 event objects = 1,000 Queue acks (reconciler diff = 0).
  2. Inject a D1 failure (binding pointed at a missing DB in staging) → sign-ups return 202 → after restore, replay yields 0 lost.
  3. Kill the consumer for 10 minutes → messages are retried or sent to the DLQ, the alert fires, and a re-drive gives 0 lost.
  4. Restore drill: Time Travel restore to T-1h on staging plus R2 replay matches the counts.
  5. Decrypt the nightly export offline and import it into a scratch D1 → the counts match.
  6. `UPDATE consent_events` fails (append-only trigger).
  7. RFC 8058 POST to `/u/:token` writes `withdrawn` without a session.
  8. The stats JSON passes the PII regex check.

**Phase 2: Social login + business accounts**
- [ ] Google, Microsoft and LinkedIn OIDC with PKCE, state and nonce. Account linking rule (§3.4). Orgs, memberships, domain verification (DNS TXT / well-known).
- **Accept:** each provider signs in on staging. A Workspace account with `hd=carrier.example` gets a business org. A gmail.com account is consumer-only. An unverified IdP email never auto-links. The DNS TXT proof verifies within 10 minutes. The login page offers Google, then Microsoft and LinkedIn, then email.

**Phase 3: Agent registry + discovery + x402 v2**
- [ ] `/v1/agents/register`, domain proof cron, API keys (hash only), OAuth clients (DCR), `price_tiers`.
- [ ] Static `agent-card.json` + `agent.json` alias, `x402-v2.json`, `mcp.json`, appended `llms.txt` section.
- [ ] `atl-mcp` with `OAuthProvider` and `withX402`. Paid tools `compare_lanes`, `export_layer` and `route_optimize` (wrapper only).
- **Accept:**
  1. An agent with the operator `ops@carrier.example` plus a TXT record becomes `active` and gets a key shown exactly once.
  2. An unpaid `POST /v1/lanes/compare` → 402 with a `PAYMENT-REQUIRED` header. A paid retry → 200 + `PAYMENT-RESPONSE` and a `payments` row.
  3. MCP Inspector connects with OAuth, lists the tools with correct annotations, and a paid tool triggers an x402 payment on Base Sepolia.
  4. The agent card validates against the A2A schema, and `agent.json` is byte-identical to it.
  5. **The legacy `/.well-known/x402.json` and `/api/x402/*` responses are unchanged** (hash test).

**Phase 4: SEO fact pages + brands strip**
- [ ] `scripts/build-fact-pages.mjs`, `slugs.json`, label i18n, JSON-LD, hreflang, sharded sitemaps, hubs, `/object/{id}` 301s.
- [ ] Brands strip component with the 22 `ready` logos self-hosted, `ATTRIBUTION.md`, disclaimer, lint for forbidden wording.
- **Accept:** §11.7 tests 1–5 pass. The strip shows exactly the `ready` rows, every logo resolves to a 200 atlas page, and the lint finds 0 occurrences of "partner", "trusted by" or the neutral-content terms in the strip or fact pages.

**Phase 5: Flexport pilot + MPP**
- [ ] `FlexportBridge` DO, connect flow, read-only tools (`browse_shipments`, `track_shipment`, network search), exceptions queue (two calls, union), map overlays, NSR vs Suez comparison panel.
- [ ] Quote → human confirm → book (`booking_confirmations`), with destructive tools never auto-allowed.
- [ ] MPP accepted alongside x402 on the paid routes.
- **Accept:** see the acceptance tests in `flexport-mcp-integration.md`. A booking attempt without a UI confirm is refused by ATL before any call to Flexport. An MPP card test payment settles in Stripe test mode.

**Phase 6: ACP, AP2, Apple, GitHub, enterprise SSO**
- [ ] ACP checkout endpoints + product feed (Arctic Intel $49/mo, data packs). AP2 mandate verification on `/v1/orders`. Sign in with Apple and GitHub. Per-org OIDC/SAML.
- **Accept:** ACP sandbox checkout completes. An AP2 cart mandate is verified and settles through x402. Apple private-relay users can sign in, but cannot claim an org.

---

## 15. Handoff notes for the Zo deploy bot

- Read this file, `0001_init.sql`, `flexport-mcp-integration.md` and `arctic-brands.csv` from `docs/mvp/` on `main`.
- **Additive only:** new Workers on `id.`, `api.` and `mcp.`. New static files on the apex. **Never** edit `/.well-known/x402.json`, `/api/x402/*`, `/api/alpha/*`, `/api/vessels` or the atlas data files without a separate owner-approved task.
- Secrets go in only via `wrangler secret put` (or the Cloudflare dashboard). Never commit them. Never print them in logs or PR comments.
- **No raw PII** in the public repo, CI logs or issue comments. Stats JSON only.
- Every phase ends with its acceptance tests run on **staging** (`*-staging` hosts, separate D1/R2) before production.
- Apply the neutral-content lint and the brand-wording lint to every generated page and component. A failing lint blocks the deploy.
- Report each phase to the tracking issue as a checklist update (counts only, no personal data).
