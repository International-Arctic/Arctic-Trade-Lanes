// atl-id (id.arctictradelanes.com) — Phase 1: durable email capture, magic link, consent, outbox. NOT deployed.
// Written against docs/mvp/ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md §6 (schema), §7 (durability), §8 (consent), §9.1.
import {
  ulid, nowIso, plusMinutes, randomToken, sha256Hex, hmacHex, normEmail, isBusinessEmail, ipPrefix,
  newSubjectKey, unwrapSubjectKey, seal, b64url, json, LOCALES,
} from '../../shared/util';

export interface Env {
  DB: D1Database;
  EVENTS: Queue<Envelope>;
  EVENTS_R2: R2Bucket;
  BACKUPS_R2: R2Bucket;
  OAUTH_KV: KVNamespace;
  EMAIL: { send(msg: { to: string; from: string; subject: string; text: string; html?: string; headers?: Record<string, string> }): Promise<unknown> };
  RATE_LIMITER: { limit(o: { key: string }): Promise<{ success: boolean }> };
  TURNSTILE_SECRET: string; // secret
  KEK_B64: string;          // secret
  EMAIL_PEPPER: string;     // secret
  SESSION_SECRET: string;   // secret
  ATL_ORIGIN: string;
  ATL_ID_ORIGIN: string;
  MAIL_FROM: string;
  ATL_ENV: string;
}

export interface Envelope { event_id: string; type: string; occurred_at: string; subject_id: string | null; payload_enc: string }

const SESSION_COOKIE = '__Secure-atl_session';
const SESSION_DAYS = 30;
const LOGIN_TTL_MIN = 15;
const DOI_TTL_MIN = 72 * 60;

// ---------- helpers ----------
const clientIp = (req: Request) => req.headers.get('cf-connecting-ip');
const uaHash = async (req: Request) => (req.headers.get('user-agent') ? (await sha256Hex(req.headers.get('user-agent')!)).slice(0, 32) : null);

async function turnstileOk(env: Env, token: unknown, ip: string | null): Promise<boolean> {
  if (typeof token !== 'string' || !token) return false;
  const body = new FormData();
  body.set('secret', env.TURNSTILE_SECRET); body.set('response', token); if (ip) body.set('remoteip', ip);
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body });
  const j = (await r.json()) as { success?: boolean };
  return !!j.success;
}

/** Build an encrypted event envelope + the outbox INSERT for the same atomic batch (spec §7.1 step 2). */
async function outboxEvent(env: Env, key: CryptoKey, subjectKeyId: string, type: string, payload: unknown) {
  const event_id = ulid();
  const enc = await seal(key, payload);
  const env_: Envelope = { event_id, type, occurred_at: nowIso(), subject_id: subjectKeyId, payload_enc: b64url(enc) };
  const stmt = env.DB.prepare('INSERT INTO outbox (event_id, event_type, subject_key_id, payload_enc) VALUES (?1, ?2, ?3, ?4)').bind(event_id, type, subjectKeyId, enc);
  return { envelope: env_, stmt };
}

/** After commit: ship to the Queue; mark enqueued. A failure leaves the row for the reconciler (step 3/6). */
async function ship(env: Env, ctx: ExecutionContext, envelopes: Envelope[]) {
  ctx.waitUntil((async () => {
    for (const e of envelopes) {
      try {
        await env.EVENTS.send(e);
        await env.DB.prepare('UPDATE outbox SET enqueued_at = ?1 WHERE event_id = ?2').bind(nowIso(), e.event_id).run();
      } catch { /* reconciler re-enqueues */ }
    }
  })());
}

/** D1 unavailable: Queue + R2 inbox, then 202 (spec §7.1 step 8). */
async function d1DownFallback(env: Env, envelopes: Envelope[]): Promise<Response> {
  for (const e of envelopes) {
    await Promise.allSettled([env.EVENTS.send(e), env.EVENTS_R2.put(`inbox/${e.event_id}.json`, JSON.stringify(e), { httpMetadata: { contentType: 'application/json' } })]);
  }
  return json({ ok: true, status: 'accepted', message: 'We have your request; the confirmation email follows.' }, 202);
}

async function subjectKeyFor(env: Env, subjectKeyId: string): Promise<CryptoKey | null> {
  const row = await env.DB.prepare('SELECT wrapped_key FROM subject_keys WHERE id = ?1 AND shredded_at IS NULL').bind(subjectKeyId).first<{ wrapped_key: ArrayBuffer }>();
  return row?.wrapped_key ? unwrapSubjectKey(env, row.wrapped_key) : null;
}

function cookie(name: string, value: string, maxAge: number) {
  return `${name}=${value}; Max-Age=${maxAge}; Path=/; Domain=.arctictradelanes.com; HttpOnly; Secure; SameSite=Lax`;
}

async function sessionUser(env: Env, req: Request): Promise<{ user_id: string; session_id: string } | null> {
  const m = /(?:^|;\s*)__Secure-atl_session=([A-Za-z0-9_-]{20,})/.exec(req.headers.get('cookie') || '');
  if (!m) return null;
  const sid = await sha256Hex(m[1]);
  const row = await env.DB.prepare('SELECT user_id FROM sessions WHERE id = ?1 AND revoked_at IS NULL AND expires_at > ?2').bind(sid, nowIso()).first<{ user_id: string }>();
  return row ? { user_id: row.user_id, session_id: sid } : null;
}

/** Unsubscribe token = b64url(email_hmac|purpose).hmac — stateless, no login needed (RFC 8058). */
async function unsubToken(env: Env, emailHmac: string, purpose: string) {
  const body = b64url(new TextEncoder().encode(`${emailHmac}|${purpose}`));
  return `${body}.${(await hmacHex(env.SESSION_SECRET, body)).slice(0, 32)}`;
}
async function readUnsubToken(env: Env, t: string): Promise<{ emailHmac: string; purpose: string } | null> {
  const [body, sig] = t.split('.');
  if (!body || !sig || (await hmacHex(env.SESSION_SECRET, body)).slice(0, 32) !== sig) return null;
  const [emailHmac, purpose] = new TextDecoder().decode(Uint8Array.from(atob(body.replace(/-/g, '+').replace(/_/g, '/')), (c) => c.charCodeAt(0))).split('|');
  return emailHmac && purpose ? { emailHmac, purpose } : null;
}

const page = (title: string, body: string, status = 200) =>
  new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${title} · ArcticTradeLanes</title></head><body style="font:16px system-ui;max-width:560px;margin:48px auto;padding:0 16px"><h1>${title}</h1>${body}</body></html>`,
    { status, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });

// ---------- handlers ----------

/** POST /auth/email {email, turnstile, locale?, marketing?, consent_text_id?, return_to?} → magic link (15 min, single use). */
async function postAuthEmail(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  const ip = clientIp(req);
  if (!(await env.RATE_LIMITER.limit({ key: `auth-email:${ipPrefix(ip)}` })).success) return json({ error: 'rate_limited' }, 429);
  const body = (await req.json().catch(() => ({}))) as Record<string, unknown>;
  const email = normEmail(body.email);
  if (!email) return json({ error: 'invalid_email' }, 400);
  if (!(await turnstileOk(env, body.turnstile, ip))) return json({ error: 'turnstile_failed' }, 400);
  const locale = LOCALES.includes(body.locale as any) ? String(body.locale) : 'en';

  const token = randomToken();
  const tokenHash = await sha256Hex(token);
  const emailHmac = await hmacHex(env.EMAIL_PEPPER, email);
  const envelopes: Envelope[] = [];
  const stmts: D1PreparedStatement[] = [];
  // Reuse the subject key of a known user so crypto-shredding covers every event; otherwise mint one.
  let existing: { subject_key_id: string } | null = null;
  try { existing = await env.DB.prepare('SELECT subject_key_id FROM users WHERE email = ?1').bind(email).first(); } catch { /* D1 down: handled below */ }
  let key: CryptoKey | null = existing ? await subjectKeyFor(env, existing.subject_key_id).catch(() => null) : null;
  let subjectKeyId = existing?.subject_key_id ?? '';
  if (!key) {
    const fresh = await newSubjectKey(env);
    key = fresh.key; subjectKeyId = ulid();
    stmts.push(env.DB.prepare('INSERT INTO subject_keys (id, wrapped_key) VALUES (?1, ?2)').bind(subjectKeyId, fresh.wrapped));
  }
  stmts.push(env.DB.prepare("INSERT INTO email_tokens (token_hash, email, purpose, ref_id, expires_at) VALUES (?1, ?2, 'login', ?3, ?4)").bind(tokenHash, email, subjectKeyId, plusMinutes(LOGIN_TTL_MIN)));
  const ev = await outboxEvent(env, key, subjectKeyId, 'email.captured', { email, locale, business_email: isBusinessEmail(email), source: 'magic_link' });
  stmts.push(ev.stmt); envelopes.push(ev.envelope);

  // Marketing consent: unticked by default; a tick records 'granted' and triggers double opt-in (spec §8).
  let doiToken: string | null = null;
  if (body.marketing === true) {
    doiToken = randomToken();
    const emailEnc = await seal(key, { email });
    stmts.push(env.DB.prepare("INSERT INTO consent_events (id, email_hmac, email_enc, purpose, action, consent_text_id, source, ip_prefix, user_agent_hash) VALUES (?1, ?2, ?3, 'marketing_email', 'granted', ?4, 'signup_form', ?5, ?6)")
      .bind(ulid(), emailHmac, emailEnc, typeof body.consent_text_id === 'string' ? body.consent_text_id : null, ipPrefix(ip), await uaHash(req)));
    stmts.push(env.DB.prepare("INSERT INTO email_tokens (token_hash, email, purpose, ref_id, expires_at) VALUES (?1, ?2, 'marketing_doi', ?3, ?4)").bind(await sha256Hex(doiToken), email, subjectKeyId, plusMinutes(DOI_TTL_MIN)));
    const ce = await outboxEvent(env, key, subjectKeyId, 'consent.granted', { email_hmac: emailHmac, purpose: 'marketing_email', source: 'signup_form' });
    stmts.push(ce.stmt); envelopes.push(ce.envelope);
  }

  try {
    await env.DB.batch(stmts); // atomic: domain rows + outbox
  } catch {
    return d1DownFallback(env, envelopes);
  }
  await ship(env, ctx, envelopes);

  const link = `${env.ATL_ID_ORIGIN}/auth/email/verify?t=${token}`;
  ctx.waitUntil(env.EMAIL.send({
    to: email, from: env.MAIL_FROM, subject: 'Your ArcticTradeLanes sign-in link',
    text: `Sign in to ArcticTradeLanes: ${link}\n\nThe link works once and expires in ${LOGIN_TTL_MIN} minutes. If you did not request it, ignore this email.`,
  }));
  if (doiToken) {
    const c = `${env.ATL_ID_ORIGIN}/c/${doiToken}`;
    ctx.waitUntil(env.EMAIL.send({
      to: email, from: env.MAIL_FROM, subject: 'Confirm ArcticTradeLanes email updates',
      text: `Please confirm that you want ArcticTradeLanes email updates: ${c}\n\nThe link expires in 72 hours. Without confirmation we send no updates.`,
    }));
  }
  // Same answer whether or not the address is known (no account enumeration).
  return json({ ok: true, status: 'sent' }, 202);
}

/** GET /auth/email/verify?t= → consume token, create/link user, start session. */
async function getAuthVerify(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  const t = new URL(req.url).searchParams.get('t') || '';
  if (!/^[A-Za-z0-9_-]{30,}$/.test(t)) return page('Link not valid', '<p>Request a new sign-in link.</p>', 400);
  const tokenHash = await sha256Hex(t);
  const tok = await env.DB.prepare("SELECT email, ref_id FROM email_tokens WHERE token_hash = ?1 AND purpose = 'login' AND used_at IS NULL AND expires_at > ?2").bind(tokenHash, nowIso()).first<{ email: string; ref_id: string }>();
  if (!tok) return page('Link expired', '<p>This sign-in link was already used or has expired. Request a new one.</p>', 400);

  const existing = await env.DB.prepare('SELECT id, subject_key_id FROM users WHERE email = ?1').bind(tok.email).first<{ id: string; subject_key_id: string }>();
  const userId = existing?.id ?? ulid();
  const subjectKeyId = existing?.subject_key_id ?? tok.ref_id;
  const key = await subjectKeyFor(env, subjectKeyId);
  if (!key) return page('Account unavailable', '<p>Please contact support.</p>', 409);

  const sessionToken = randomToken();
  const sid = await sha256Hex(sessionToken);
  const expires = new Date(Date.now() + SESSION_DAYS * 864e5).toISOString();
  const stmts: D1PreparedStatement[] = [
    env.DB.prepare('UPDATE email_tokens SET used_at = ?1 WHERE token_hash = ?2 AND used_at IS NULL').bind(nowIso(), tokenHash),
  ];
  if (!existing) {
    stmts.push(env.DB.prepare('INSERT INTO users (id, email, email_verified_at, subject_key_id) VALUES (?1, ?2, ?3, ?4)').bind(userId, tok.email, nowIso(), subjectKeyId));
    stmts.push(env.DB.prepare("INSERT INTO identities (id, user_id, provider, provider_subject, email_at_idp, email_verified) VALUES (?1, ?2, 'email', ?3, ?3, 1)").bind(ulid(), userId, tok.email));
  } else {
    stmts.push(env.DB.prepare('UPDATE users SET email_verified_at = COALESCE(email_verified_at, ?1), updated_at = ?1 WHERE id = ?2').bind(nowIso(), userId));
  }
  stmts.push(env.DB.prepare('INSERT INTO sessions (id, user_id, expires_at, ip_prefix, user_agent_hash) VALUES (?1, ?2, ?3, ?4, ?5)').bind(sid, userId, expires, ipPrefix(clientIp(req)), await uaHash(req)));
  const ev = await outboxEvent(env, key, subjectKeyId, existing ? 'user.signed_in' : 'user.registered', { user_id: userId, method: 'email', business_email: isBusinessEmail(tok.email) });
  stmts.push(ev.stmt);
  const res = await env.DB.batch(stmts);
  if (!res[0].meta.changes) return page('Link expired', '<p>This sign-in link was already used.</p>', 400); // lost a race
  await ship(env, ctx, [ev.envelope]);

  return new Response(null, { status: 303, headers: { Location: `${env.ATL_ORIGIN}/account`, 'Set-Cookie': cookie(SESSION_COOKIE, sessionToken, SESSION_DAYS * 86400), 'Cache-Control': 'no-store' } });
}

/** POST /auth/logout */
async function postLogout(req: Request, env: Env): Promise<Response> {
  const s = await sessionUser(env, req);
  if (s) await env.DB.prepare('UPDATE sessions SET revoked_at = ?1 WHERE id = ?2').bind(nowIso(), s.session_id).run();
  return json({ ok: true }, 200, { 'Set-Cookie': cookie(SESSION_COOKIE, '', 0) });
}

/** POST /account/consents {purpose, action: 'grant'|'withdraw', consent_text_id?} (session). Marketing grant → DOI email. */
async function postConsents(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
  const s = await sessionUser(env, req);
  if (!s) return json({ error: 'unauthenticated' }, 401);
  const body = (await req.json().catch(() => ({}))) as Record<string, unknown>;
  const purpose = String(body.purpose || '');
  if (!['marketing_email', 'product_updates'].includes(purpose) || !['grant', 'withdraw'].includes(String(body.action))) return json({ error: 'invalid' }, 400);
  const u = await env.DB.prepare('SELECT email, subject_key_id FROM users WHERE id = ?1').bind(s.user_id).first<{ email: string; subject_key_id: string }>();
  if (!u) return json({ error: 'unauthenticated' }, 401);
  const key = await subjectKeyFor(env, u.subject_key_id);
  if (!key) return json({ error: 'unavailable' }, 409);
  const emailHmac = await hmacHex(env.EMAIL_PEPPER, u.email);
  const action = body.action === 'grant' ? 'granted' : 'withdrawn';
  const stmts: D1PreparedStatement[] = [
    env.DB.prepare("INSERT INTO consent_events (id, user_id, email_hmac, email_enc, purpose, action, consent_text_id, source, ip_prefix, user_agent_hash) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, 'account_settings', ?8, ?9)")
      .bind(ulid(), s.user_id, emailHmac, await seal(key, { email: u.email }), purpose, action, typeof body.consent_text_id === 'string' ? body.consent_text_id : null, ipPrefix(clientIp(req)), await uaHash(req)),
  ];
  let doi: string | null = null;
  if (action === 'granted') {
    doi = randomToken();
    stmts.push(env.DB.prepare("INSERT INTO email_tokens (token_hash, email, purpose, ref_id, expires_at) VALUES (?1, ?2, 'marketing_doi', ?3, ?4)").bind(await sha256Hex(doi), u.email, `${s.user_id}|${purpose}`, plusMinutes(DOI_TTL_MIN)));
  }
  const ev = await outboxEvent(env, key, u.subject_key_id, `consent.${action}`, { user_id: s.user_id, email_hmac: emailHmac, purpose, source: 'account_settings' });
  stmts.push(ev.stmt);
  await env.DB.batch(stmts);
  await ship(env, ctx, [ev.envelope]);
  if (doi) ctx.waitUntil(env.EMAIL.send({ to: u.email, from: env.MAIL_FROM, subject: 'Confirm ArcticTradeLanes email updates', text: `Please confirm: ${env.ATL_ID_ORIGIN}/c/${doi}\n\nThe link expires in 72 hours.` }));
  return json({ ok: true, action, double_opt_in: !!doi });
}

/** GET /c/:token → confirmed_doi (72 h). */
async function getDoi(req: Request, env: Env, ctx: ExecutionContext, token: string): Promise<Response> {
  const th = await sha256Hex(token);
  const tok = await env.DB.prepare("SELECT email, ref_id FROM email_tokens WHERE token_hash = ?1 AND purpose = 'marketing_doi' AND used_at IS NULL AND expires_at > ?2").bind(th, nowIso()).first<{ email: string; ref_id: string }>();
  if (!tok) return page('Link expired', '<p>This confirmation link was already used or has expired.</p>', 400);
  const purpose = tok.ref_id?.includes('|') ? tok.ref_id.split('|')[1] : 'marketing_email';
  const user = await env.DB.prepare('SELECT id, subject_key_id FROM users WHERE email = ?1').bind(tok.email).first<{ id: string; subject_key_id: string }>();
  const subjectKeyId = user?.subject_key_id ?? tok.ref_id;
  const key = await subjectKeyFor(env, subjectKeyId);
  if (!key) return page('Unavailable', '<p>Please contact support.</p>', 409);
  const emailHmac = await hmacHex(env.EMAIL_PEPPER, tok.email);
  const ev = await outboxEvent(env, key, subjectKeyId, 'consent.confirmed_doi', { email_hmac: emailHmac, purpose });
  await env.DB.batch([
    env.DB.prepare('UPDATE email_tokens SET used_at = ?1 WHERE token_hash = ?2').bind(nowIso(), th),
    env.DB.prepare("INSERT INTO consent_events (id, user_id, email_hmac, email_enc, purpose, action, source, ip_prefix, user_agent_hash) VALUES (?1, ?2, ?3, ?4, ?5, 'confirmed_doi', 'signup_form', ?6, ?7)")
      .bind(ulid(), user?.id ?? null, emailHmac, await seal(key, { email: tok.email }), purpose, ipPrefix(clientIp(req)), await uaHash(req)),
    ev.stmt,
  ]);
  await ship(env, ctx, [ev.envelope]);
  const unsub = `${env.ATL_ID_ORIGIN}/u/${await unsubToken(env, emailHmac, purpose)}`;
  return page('Confirmed', `<p>Thank you. You can unsubscribe at any time: <a href="${unsub}">unsubscribe</a>.</p>`);
}

/** GET /u/:token (confirmation page) · POST /u/:token (RFC 8058 one-click; no session). */
async function unsubscribe(req: Request, env: Env, ctx: ExecutionContext, token: string): Promise<Response> {
  const t = await readUnsubToken(env, token);
  if (!t) return page('Link not valid', '<p>This unsubscribe link is not valid.</p>', 400);
  if (req.method === 'GET') {
    return page('Unsubscribe', `<form method="post"><input type="hidden" name="List-Unsubscribe" value="One-Click"><button type="submit">Unsubscribe from ArcticTradeLanes emails</button></form>`);
  }
  const oneClick = 'list_unsubscribe_post';
  await env.DB.prepare("INSERT INTO consent_events (id, email_hmac, purpose, action, source, ip_prefix, user_agent_hash) VALUES (?1, ?2, ?3, 'withdrawn', ?4, ?5, ?6)")
    .bind(ulid(), t.emailHmac, t.purpose, oneClick, ipPrefix(clientIp(req)), await uaHash(req)).run();
  // No subject key is needed here: the event carries only the HMAC (never published).
  const e: Envelope = { event_id: ulid(), type: 'consent.withdrawn', occurred_at: nowIso(), subject_id: null, payload_enc: b64url(new TextEncoder().encode(JSON.stringify({ purpose: t.purpose, source: oneClick }))) };
  ctx.waitUntil(env.EVENTS.send(e).catch(() => env.EVENTS_R2.put(`inbox/${e.event_id}.json`, JSON.stringify(e))));
  return page('Unsubscribed', '<p>You will not receive these emails any more.</p>');
}

/** GET /healthz → {d1, queue, r2} (spec §14 Phase 0 acceptance). */
async function healthz(env: Env): Promise<Response> {
  const out: Record<string, string> = {};
  try { await env.DB.prepare('SELECT 1').first(); out.d1 = 'ok'; } catch { out.d1 = 'error'; }
  try { await env.EVENTS.send({ event_id: ulid(), type: 'health.probe', occurred_at: nowIso(), subject_id: null, payload_enc: '' }); out.queue = 'ok'; } catch { out.queue = 'error'; }
  try { await env.EVENTS_R2.head('health/probe'); out.r2 = 'ok'; } catch { out.r2 = 'error'; }
  return json(out, Object.values(out).every((v) => v === 'ok') ? 200 : 503);
}

// ---------- entry points ----------
export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(req.url);
    const p = url.pathname;
    try {
      if (p === '/healthz' && req.method === 'GET') return healthz(env);
      if (p === '/auth/email' && req.method === 'POST') return postAuthEmail(req, env, ctx);
      if (p === '/auth/email/verify' && req.method === 'GET') return getAuthVerify(req, env, ctx);
      if (p === '/auth/logout' && req.method === 'POST') return postLogout(req, env);
      if (p === '/account/consents' && req.method === 'POST') return postConsents(req, env, ctx);
      let m = /^\/c\/([A-Za-z0-9_-]{30,})$/.exec(p);
      if (m && req.method === 'GET') return getDoi(req, env, ctx, m[1]);
      m = /^\/u\/([A-Za-z0-9_.-]{20,})$/.exec(p);
      if (m && (req.method === 'GET' || req.method === 'POST')) return unsubscribe(req, env, ctx, m[1]);
      return json({ error: 'not_found' }, 404);
    } catch (err) {
      console.error('atl-id error', (err as Error)?.name); // never log request bodies or emails
      return json({ error: 'internal' }, 500);
    }
  },

  /** Queue consumer: one R2 object per event (idempotent key), then mark the outbox row archived (spec §7.1 step 4). */
  async queue(batch: MessageBatch<Envelope>, env: Env): Promise<void> {
    for (const msg of batch.messages) {
      const e = msg.body;
      if (e.type === 'health.probe') { msg.ack(); continue; }
      const d = new Date(e.occurred_at);
      const k = `events/${d.getUTCFullYear()}/${String(d.getUTCMonth() + 1).padStart(2, '0')}/${String(d.getUTCDate()).padStart(2, '0')}/${String(d.getUTCHours()).padStart(2, '0')}/${e.event_id}.json`;
      try {
        await env.EVENTS_R2.put(k, JSON.stringify(e), { httpMetadata: { contentType: 'application/json' } });
        await env.DB.prepare('UPDATE outbox SET archived_at = ?1 WHERE event_id = ?2 AND archived_at IS NULL').bind(nowIso(), e.event_id).run().catch(() => {});
        msg.ack();
      } catch {
        msg.retry(); // max_retries=10, then atl-events-dlq
      }
    }
  },

  /** Cron reconciler: re-enqueue outbox rows not enqueued after 5 minutes (spec §7.1 step 6). */
  async scheduled(_c: ScheduledController, env: Env, ctx: ExecutionContext): Promise<void> {
    const cutoff = new Date(Date.now() - 5 * 60_000).toISOString();
    const { results } = await env.DB.prepare('SELECT event_id, event_type, subject_key_id, payload_enc, created_at FROM outbox WHERE archived_at IS NULL AND (enqueued_at IS NULL OR enqueued_at < ?1) AND created_at < ?1 LIMIT 500')
      .bind(cutoff).all<{ event_id: string; event_type: string; subject_key_id: string | null; payload_enc: ArrayBuffer; created_at: string }>();
    const envs: Envelope[] = results.map((r) => ({ event_id: r.event_id, type: r.event_type, occurred_at: r.created_at, subject_id: r.subject_key_id, payload_enc: b64url(new Uint8Array(r.payload_enc)) }));
    await ship(env, ctx, envs);
    // TODO(Phase 1): replay R2 inbox/ (D1-down fallback) in ULID order; hourly JSONL compaction Workflow; nightly age-encrypted export.
  },
} satisfies ExportedHandler<Env, Envelope>;
