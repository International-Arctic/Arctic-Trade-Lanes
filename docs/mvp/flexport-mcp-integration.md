# Flexport MCP integration plan for ArcticTradeLanes.com (ATL)

**Status:** spec only. Nothing has been built, connected or deployed.
**Date:** 2026-10-06 · **Owner:** Aleksei Dolgikh (@alexdolbun) · cto@arctictradelanes.com
**Companion spec:** [`ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md`](./ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md) (§10)

---

## 1. What we checked, and where

These were read on 2026-10-06 (all requests were read-only, with no authentication and no tool calls):

| Source | URL | What it confirmed |
|---|---|---|
| Flexport docs: Setup | https://apidocs.flexport.com/v3/tag/Setup/ | Server URL, how an admin enables MCP, per-user connection |
| Flexport docs: Permissions | https://apidocs.flexport.com/v3/tag/Permissions/ | The roles Admin, Billing, Member, Analyst and Tracker |
| Flexport docs: MCP Tools | https://apidocs.flexport.com/v3/tag/MCP-Tools/ | Each tool's schema, allowed roles, `destructive` annotations, token rules |
| Microsoft connector page (published by Flexport) | https://learn.microsoft.com/en-us/connectors/flexportmcp/ | Tool list, rate limits, common errors, admin URL |
| Flexport product page | https://www.flexport.com/technology/flexport-mcp/ | Admin enables once, then each user connects; separate rate limits from the REST API |
| Live OAuth metadata | `https://mcp.flexport.com/.well-known/oauth-authorization-server` and `/.well-known/oauth-protected-resource/mcp` | Auth server and scopes; DCR and PKCE supported |
| Live endpoint probe | `GET https://mcp.flexport.com/mcp` returns `401` with `WWW-Authenticate: Bearer … resource_metadata=…/.well-known/oauth-protected-resource/mcp, scope="openid profile email tool:*"` | Standard MCP OAuth 2.1 discovery |

Live OAuth metadata (abridged):

```json
{
  "issuer": "https://mcp.flexport.com",
  "authorization_endpoint": "https://mcp.flexport.com/authorize",
  "token_endpoint": "https://mcp.flexport.com/token",
  "registration_endpoint": "https://mcp.flexport.com/register",
  "scopes_supported": ["openid","profile","email","tool:*"],
  "grant_types_supported": ["authorization_code","refresh_token"],
  "token_endpoint_auth_methods_supported": ["client_secret_basic","client_secret_post","none"],
  "code_challenge_methods_supported": ["S256"],
  "client_id_metadata_document_supported": true
}
```

## 2. Owner's summary compared with the official docs

| # | Owner summary | Official docs | Verdict |
|---|---|---|---|
| 1 | Server `https://mcp.flexport.com/mcp`, Streamable HTTP | Same. **SSE transport is not supported.** | ✅ matches |
| 2 | Per-user Flexport OAuth | Same. Every call runs as the signed-in user. Users can revoke a connection under *User Settings → MCP Connections*. | ✅ matches |
| 3 | Roles Admin/Billing/Member/Analyst/Tracker | Same five roles. | ✅ matches |
| 4 | Visibility: `browse_shipments`, `track_shipment` | Same. Both are open to **all five roles**. `browse_shipments` returns up to 100 shipments per page. `track_shipment` returns up to 20 matches. | ✅ matches |
| 5 | Rates: `rates_search_instant_price`, `rates_evaluate_total_price_from_instant_price_search`, `rates_instant_book` | Same. These are limited to **Admin, Billing and Member**. Analyst and Tracker cannot price or book. Modes are Ocean FCL, Ocean LCL and Air. | ✅ with a role nuance |
| 6 | `rates_instant_book` is destructive and needs a confirmation token | **Partly right.** It is annotated `destructive`. It has two modes: **(a) snapshot mode** needs the `price_confirmation_token` returned by the *evaluate* tool for the same snapshot IDs, add-on flags and detention days, and a missing or mismatched token returns `REQUIRES_PRICE_CONFIRMATION` with no booking; **(b) client-rate mode** (`client_rate_id`) needs **no token**. Flexport says the token is "a workflow-consistency guard, **not an authentication credential**". | ⚠️ discrepancy: client-rate mode books with no token, so ATL must add its own human confirmation step in both modes |
| 7 | `rates_book_without_rate` is two-step with `booking_confirmation_token`, no hazmat, needs onboarded `flx::` addresses | Same two-step preflight and fingerprint flow, and any change needs a new preflight. It is broader than "no hazmat": **hazmat, lithium-ion, magnets and non-Li-ion batteries must all be `false`**, document uploads and automatic fulfillment-inbound creation are unsupported, and **Google-address results are rejected** (only `network_search_addresses` FIDs work). China-origin shipments need `description_for_export_customs` on every HS line. | ✅ plus extra limits |
| 8 | `rates_request_rate` is destructive | Same: annotated `destructive`, Admin/Billing/Member only. Addresses may come from `network_search_addresses` **or** `network_search_google_addresses` (`commerce_address_fid`). | ✅ matches |
| 9 | Network tools: ports, HS codes, addresses, company entities | Same. **`network_search_hs_codes` is Admin/Billing/Member only**, and the other network tools are open to all roles. | ✅ with a role nuance |
| 10 | Exceptions queue: union of `HAS_ACTIVE_EXCEPTION` and `HAS_CUSTOMS_HOLD` because flags are ANDed | Confirmed word for word: "flags are combined with AND… a complete search for held shipments also requires a separate HAS_ACTIVE_EXCEPTION query and a union". Also: `HAS_CUSTOMS_HOLD` *includes agency reviews that do not block cargo* and *misses holds recorded only as operational exceptions*. Relevant exceptions have category "Customs & regulatory holds" and an open status. RESOLVED and CANCELED history entries are not current holds. A third flag, `HAS_OPEN_TASK`, also exists. | ✅ plus filtering rules |
| 11 | (not in summary) | **More tools exist:** `rates_browse_quote_requests`, `rates_get_quote_request_details`, `rates_get_quote_details`, `network_search_google_addresses` (annotated `openWorld`) and `list_active_company_users`. | ➕ new information |
| 12 | (not in summary) | **Rate limits:** about 60 requests/min per user and 300/min per Flexport customer account. These are separate from the Flexport REST API limits. | ➕ new information |
| 13 | Rollout: admin enablement, pilot, role check, expansion | Admin enables it once, either at **Business Profile → Integrations → MCP Connection** (`app.flexport.com/integrations/mcp-connection`) or inline on first connect. Every company sees the same tool list, and calls fail with a permission error if the user's role is not allowed. | ✅ matches |
| 14 | (not in summary) | Data handling falls under Flexport's *Software and Data Access Terms and Conditions*. ATL acting as a multi-tenant intermediary needs Flexport's written OK (see §8). | ⚠️ legal gate |

### Tool and role matrix (from the official MCP Tools page)

| Tool | Admin | Billing | Member | Analyst | Tracker | Annotation | ATL policy |
|---|---|---|---|---|---|---|---|
| `track_shipment` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `browse_shipments` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `network_search_ports` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `network_search_addresses` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `network_search_google_addresses` | ✅ | ✅ | ✅ | ✅ | ✅ | openWorld | allow, but results are **never** used for `book_without_rate` |
| `network_search_company_entities` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `list_active_company_users` | ✅ | ✅ | ✅ | ✅ | ✅ | read | allow (shown to Admin only in the ATL UI) |
| `rates_get_quote_request_details` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `rates_get_quote_details` | ✅ | ✅ | ✅ | ✅ | ✅ | read | auto-allow |
| `rates_browse_quote_requests` | ✅ | ✅ | ✅ | ✅ | ❌ | read | auto-allow |
| `network_search_hs_codes` | ✅ | ✅ | ✅ | ❌ | ❌ | read | auto-allow |
| `rates_search_instant_price` | ✅ | ✅ | ✅ | ❌ | ❌ | read | auto-allow |
| `rates_evaluate_total_price_from_instant_price_search` | ✅ | ✅ | ✅ | ❌ | ❌ | read | auto-allow |
| `rates_instant_book` | ✅ | ✅ | ✅ | ❌ | ❌ | **destructive** | **human confirm, always** |
| `rates_book_without_rate` | ✅ | ✅ | ✅ | ❌ | ❌ | **destructive** | **human confirm, always** |
| `rates_request_rate` | ✅ | ✅ | ✅ | ❌ | ❌ | **destructive** | **human confirm, always** |

## 3. How ATL uses Flexport (product view)

1. **Bring your own Flexport.** A registered ATL **business** account (verified business email, see the main spec §4) can connect **its own** Flexport account. ATL never uses a shared ATL-owned Flexport login for customer data.
2. **Lane comparison on the polar map.** For an origin and destination pair (for example Busan to Rotterdam, or Shanghai to Felixstowe), the ATL agent:
   - calls `rates_search_instant_price` (and `evaluate` if a rate is selected) to get **live Suez or Cape** market pricing and transit from the customer's Flexport account;
   - combines it with ATL's own **NSR** model (the existing `/api/alpha/route-optimize`, distance and ice window from the atlas lanes layer `ARC-LANE-*`);
   - draws both tracks on the EPSG:3996 hero map. The NSR comes from ATL lane geometry. The Suez/Cape track is drawn from Flexport route stops (`network_search_ports` resolves UN/LOCODEs to atlas ports).
   - Every number has a source label: *"Flexport instant price (your account)"* or *"ATL NSR model estimate"*. ATL never presents an NSR price as a Flexport quote. Flexport instant pricing covers Flexport-served lanes, and NSR sailings will usually have **no** Flexport instant price. In that case the UI says so (`empty_reason`) and offers `rates_request_rate` (destructive, confirmation needed).
3. **Tracking overlay.** `browse_shipments` and `track_shipment` route stops become a per-tenant layer on the polar map. It is **private to that tenant**, never cached into public atlas pages, and never written to the public repo.
4. **Exceptions queue** (§5.1): a tenant dashboard card listing current customs holds and exceptions.
5. **Bookings are always human-confirmed** (§5.2 and §5.3). An ATL agent never books on its own.

## 4. Architecture

```
Browser / ATL agent (A2A, ATL MCP client)
        │
        ▼
mcp.arctictradelanes.com  (ATL Worker: McpAgent + workers-oauth-provider)
        │  ATL session → tenant (org) → flexport_connections row
        ▼
FlexportBridge (Durable Object per org×user)
        │  Agents SDK MCP client: this.addMcpServer("flexport", "https://mcp.flexport.com/mcp", { callbackPath: "/integrations/flexport/callback" })
        │  OAuth 2.1 + PKCE (S256), DCR at https://mcp.flexport.com/register  (or client_id metadata document)
        ▼
https://mcp.flexport.com/mcp  (Streamable HTTP)
```

- **Client registration:** Flexport supports Dynamic Client Registration and a client-ID metadata document. ATL hosts `https://id.arctictradelanes.com/.well-known/oauth-client/flexport.json` (client_name "ArcticTradeLanes", redirect_uris `["https://id.arctictradelanes.com/integrations/flexport/callback"]`, `token_endpoint_auth_method: "none"` with PKCE, or `client_secret_basic` if DCR issues a secret).
- **Scopes requested:** `openid profile email tool:*`. This is the only tool scope advertised, and ATL restricts tools on its side through the policy table above.
- **Token storage:** access and refresh tokens are encrypted with AES-GCM using a per-org data key (envelope encryption, main spec §7.4) and stored in the DO's SQLite. D1 keeps only `flexport_connections` metadata (status, connected_by, role_snapshot, connected_at, revoked_at). Tokens never go to logs, R2 events or GitHub.
- **Callback path:** use the Agents SDK `callbackPath` option (added in Agents SDK v0.4.0) so the instance name does not leak in callback URLs. Ref: https://developers.cloudflare.com/changelog/post/2026-02-09-agents-sdk-v0.4.0/
- **Rate limiting:** a token bucket per user (50/min) and per org (250/min), held in the DO and kept under Flexport's 60 and 300. On a 429 or limit error, retry with exponential backoff and jitter, at most 3 tries.
- **Role check:** after connecting, ATL makes one harmless call (`network_search_ports` with query "Rotterdam") and records whether `rates_search_instant_price` is permitted, using a no-op probe with an invalid payload that is expected to fail validation. A permission error tells us the role. If probing is not reliable, ATL asks the user to pick their Flexport role and treats permission errors as authoritative.

## 5. Flows

### 5.1 Exceptions queue (read-only)

```
A = browse_shipments(flags=[HAS_ACTIVE_EXCEPTION], status≠delivered, page through has_more)
B = browse_shipments(flags=[HAS_CUSTOMS_HOLD],      status≠delivered, page through has_more)
U = A ∪ B  (dedupe on flex_id)
for s in U:
   holds = s.exceptions where category == "Customs & regulatory holds" AND status is open   (ignore RESOLVED / CANCELED)
   reviews = s.customs[].agency_statuses[] where disposition is a review (not blocking)
   label: "Hold" if holds or a blocking disposition, else "Review"
```

- Never send both flags in one call, because that gives the intersection.
- Optional third pass: `HAS_OPEN_TASK` for a "Needs your action" tab.
- Refresh with Cron every 30 minutes for active tenants and on demand from the UI. Cache the results per tenant in DO storage for 15 minutes.

### 5.2 Quote, then book (instant price), with a human confirm

```
1. network_search_ports(origin), network_search_ports(dest)        → port ids  (or network_search_addresses → flx:: FIDs for door legs)
2. rates_search_instant_price(cargo, route, cargo_ready_date, incoterm, …)
      if empty_reason → show "No instant price" → offer request_rate (step 6)
3. user picks an option in the ATL UI (side by side with the ATL NSR estimate on the map)
4. rates_evaluate_total_price_from_instant_price_search(search_snapshot_id, item_snapshot_id, wants_* flags, detention_addon_free_days)
      → total, itemised charges, price_confirmation_token
5. ATL CONFIRMATION SCREEN (human): total price, currency, route, carrier/transit, cargo summary, incoterm, add-ons, detention days,
   "This creates a real, binding Flexport booking under <org legal name>." → [Confirm booking] (re-auth if the ATL session is older than 10 minutes)
      ATL mints its own single-use confirm_id (D1 row, TTL 10 min) bound to sha256(evaluate payload + user_id)
6. rates_instant_book(search_snapshot_id, item_snapshot_id, same flags, same detention days, price_confirmation_token)
      handle error_code: REQUIRES_PRICE_CONFIRMATION → back to step 4; RATE_EXPIRED / SNAPSHOT_NOT_FOUND → back to step 2
7. Write an audit event booking.created (flex_id, confirm_id, user, timestamp; no prices in the public logs)
```

**Client-rate mode** (`client_rate_id`) needs no Flexport token, so ATL **still requires** step 5. ATL builds its own preview from `rates_get_quote_details` or the customer's rate card and binds a `confirm_id` to `client_rate_id + cargo_ready_date + cargo_details`.

### 5.3 Supplier booking without a rate (two-step)

```
1. network_search_addresses(...)  → origin_address_fid (flx::…)   ← MUST come from this tool; Google-address results are rejected
2. network_search_hs_codes(...)   → hs_code_dbid lines (+ description_for_export_customs if origin is China)
3. Pre-validate in ATL: contains_hazmat = contains_li_ion = contains_magnets = contains_non_li_ion_battery = false; else stop and send the user to Flexport
4. rates_book_without_rate(… no booking_confirmation_token …)   → preflight: validation + fingerprint token
5. ATL CONFIRMATION SCREEN (human) showing the exact payload → [Submit booking]
6. rates_book_without_rate(identical payload + booking_confirmation_token)   → submitted for consignee acceptance
   any edit → discard the token and go back to step 4
```

### 5.4 Request a rate (destructive)

The ATL UI shows the lane, cargo profile and free-text note **before** sending. This step always needs a human confirmation. It is used for NSR lanes where no instant price exists.

## 6. Guardrails (non-negotiable)

1. **Destructive tools are never auto-allowed.** `rates_instant_book`, `rates_book_without_rate` and `rates_request_rate` sit behind ATL's own confirmation (a single-use `confirm_id`, a human click, and re-auth if the session is older than 10 minutes). This applies to ATL agents, A2A callers and MCP callers alike. A2A or MCP clients get a `confirmation_required` result containing a URL for a human to approve. They never get a direct booking.
2. **Never invent addresses or IDs.** Every `flx::` FID, port id, HS `dbid`, snapshot id and rate id must come from a tool response *in the same session*. ATL validates provenance by storing returned IDs per conversation in the DO and rejecting any ID it did not see. LLM-generated IDs are refused.
3. **No hazmat or battery cargo through `book_without_rate`** (the tool supports only `false`).
4. **Least privilege in the UI:** Analyst and Tracker users see the visibility features only. Pricing and booking buttons are hidden, and Flexport would refuse those calls anyway.
5. **Tenant isolation:** Flexport data is per org×user and never cached publicly, never used to train or enrich public atlas pages, and never shown to other tenants.
6. **Audit:** every tool call writes an event (tool, org, user, success/error_code, latency) to the append-only event log. Payload bodies with commercial terms are **not** logged, only their hashes.
7. **Kill switch:** an `FLEXPORT_ENABLED` flag per org plus a global flag in KV. Revoking in ATL deletes the tokens and tells the user to also revoke under *Flexport → User Settings → MCP Connections*.
8. **Neutral content:** lane comparisons show distance, transit, price and ice-season facts only.

## 7. Rollout

| Step | Gate | Acceptance test |
|---|---|---|
| 0. Legal | Written confirmation from the Flexport account team that a third-party platform (ATL) may connect on behalf of Flexport customers under the Software & Data Access T&Cs | Email on file |
| 1. Admin enablement | The pilot customer's Flexport **Admin** enables MCP (Business Profile → Integrations → MCP Connection) | Connecting no longer shows "MCP has not been enabled for your organization" |
| 2. Pilot (1–3 friendly orgs) | `FLEXPORT_ENABLED` only for pilot orgs; read-only tools only for 2 weeks | Exceptions queue matches the Flexport web app for 20 sampled shipments |
| 3. Role check | Capture the role per user. Bookings stay off until it is verified | An Analyst user cannot see booking buttons, and a forced call returns a Flexport permission error that ATL shows cleanly |
| 4. Quote then book (pilot) | Destructive tools enabled for pilot Admin/Member users | Booking without a confirm click is impossible (automated test); a REQUIRES_PRICE_CONFIRMATION path is exercised |
| 5. Expansion | All verified business orgs can self-connect | Error rate under 1%, no rate-limit breaches in 7 days |

## 8. Open questions for Aleksei and Flexport

1. Is Flexport fine with ATL acting as an MCP **client** for many customers (multi-tenant), or does each customer need to connect through their own AI workspace? *(This decides whether the plan is feasible.)*
2. Will Flexport register ATL as a **named client** (pre-registered client_id, branded consent), rather than anonymous DCR?
3. Does Flexport offer a sandbox or test tenant? The docs mention none. Without one, the pilot runs against real accounts using read-only tools first.
4. Can instant price ever return Arctic or NSR routings? If not, NSR always stays "ATL estimate" and Suez/Cape comes from Flexport.

## 9. ATL code touchpoints (for the deploy bot; all additive)

- New: `workers/mcp/flexport-bridge.ts` (Durable Object), `workers/id/integrations/flexport/*` (connect and callback), D1 table `flexport_connections` (main spec §6), UI `/app/integrations/flexport`, map layer `tenant-shipments` (private).
- **Untouched:** every existing `/api/x402/*`, `/api/alpha/*`, `/.well-known/x402.json`, the atlas files and the current home and map routes.
