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
