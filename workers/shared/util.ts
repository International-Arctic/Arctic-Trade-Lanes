// Shared helpers for ATL Workers (spec §6/§7). No secrets here; everything comes from env bindings.
export const LOCALES = ['en','ru','zh','ja','ko','el','de','nl','fr','es','it','pt','tr','ar','hi','vi','id','da','fi','sv','nb','is'] as const;

// Free-mail domains can create a consumer account but cannot claim an org or operate an agent (spec §8).
export const FREE_MAIL = new Set([
  'gmail.com','googlemail.com','outlook.com','hotmail.com','live.com','msn.com','yahoo.com','icloud.com','me.com','aol.com',
  'proton.me','protonmail.com','gmx.com','gmx.de','web.de','mail.com','yandex.ru','yandex.com','ya.ru','mail.ru','bk.ru','inbox.ru','list.ru',
  'qq.com','163.com','126.com','sina.com','naver.com','daum.net','privaterelay.appleid.com',
]);

const ENC = new TextEncoder();
const B32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

/** ULID (time-ordered, Crockford base32). */
export function ulid(now = Date.now()): string {
  let t = now, time = '';
  for (let i = 0; i < 10; i++) { time = B32[t % 32] + time; t = Math.floor(t / 32); }
  const r = crypto.getRandomValues(new Uint8Array(16));
  let rand = '';
  for (let i = 0; i < 16; i++) rand += B32[r[i] % 32];
  return time + rand;
}

export const nowIso = () => new Date().toISOString();
export const plusMinutes = (m: number) => new Date(Date.now() + m * 60_000).toISOString();

export function b64url(buf: ArrayBuffer | Uint8Array): string {
  const b = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
  let s = ''; for (const x of b) s += String.fromCharCode(x);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
export function b64dec(s: string): Uint8Array {
  const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

export function randomToken(bytes = 32): string { return b64url(crypto.getRandomValues(new Uint8Array(bytes))); }

export async function sha256Hex(s: string): Promise<string> {
  const d = await crypto.subtle.digest('SHA-256', ENC.encode(s));
  return [...new Uint8Array(d)].map((x) => x.toString(16).padStart(2, '0')).join('');
}

export async function hmacHex(secret: string, msg: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', ENC.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, ENC.encode(msg));
  return [...new Uint8Array(sig)].map((x) => x.toString(16).padStart(2, '0')).join('');
}

export function normEmail(raw: unknown): string | null {
  const e = String(raw ?? '').trim().toLowerCase();
  if (e.length > 254 || !/^[^\s@]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(e)) return null;
  return e;
}
export const emailDomain = (e: string) => e.split('@')[1] || '';
export const isBusinessEmail = (e: string) => !FREE_MAIL.has(emailDomain(e));

/** /24 for IPv4, /48 for IPv6 (spec §6: never store full IPs). */
export function ipPrefix(ip: string | null): string | null {
  if (!ip) return null;
  if (ip.includes('.')) return ip.split('.').slice(0, 3).join('.') + '.0/24';
  return ip.split(':').slice(0, 3).join(':') + '::/48';
}

// ---- Crypto-shredding (spec §7.4): per-subject AES-GCM data key wrapped with KEK (AES-KW) ----
async function kek(env: { KEK_B64: string }): Promise<CryptoKey> {
  return crypto.subtle.importKey('raw', b64dec(env.KEK_B64), 'AES-KW', false, ['wrapKey', 'unwrapKey']);
}
export async function newSubjectKey(env: { KEK_B64: string }): Promise<{ key: CryptoKey; wrapped: Uint8Array }> {
  const key = (await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt'])) as CryptoKey;
  const wrapped = new Uint8Array(await crypto.subtle.wrapKey('raw', key, await kek(env), 'AES-KW'));
  return { key, wrapped };
}
export async function unwrapSubjectKey(env: { KEK_B64: string }, wrapped: ArrayBuffer): Promise<CryptoKey> {
  return crypto.subtle.unwrapKey('raw', wrapped, await kek(env), 'AES-KW', { name: 'AES-GCM' }, false, ['encrypt', 'decrypt']);
}
export async function seal(key: CryptoKey, obj: unknown): Promise<Uint8Array> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, ENC.encode(JSON.stringify(obj))));
  const out = new Uint8Array(12 + ct.length); out.set(iv); out.set(ct, 12);
  return out;
}

export function json(data: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', ...headers } });
}
