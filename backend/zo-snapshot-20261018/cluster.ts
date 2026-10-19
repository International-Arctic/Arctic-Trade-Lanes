/**
 * ATL worker cluster (2026-10-14, additive).
 *
 * The origin is a single-threaded Bun process. Measured on this box: one worker
 * serves ~26k req/s of RAM-resident documents, which is ~one core. Three of the
 * four cores were idle, so the site could not use the hardware it already had.
 *
 * This launcher binds N workers to the same port with SO_REUSEPORT, which makes
 * the kernel fan connections across them. That is the part the old server.ts
 * comment warned against, and the warning was correct: SO_REUSEPORT multiplies
 * the damage of a worker that outlives its restart, because it keeps answering a
 * share of requests with stale code and no error anywhere.
 *
 * So this launcher makes "outliving the launcher" impossible rather than merely
 * unlikely:
 *
 *   1. Every worker is spawned with a PIPE on stdin and ATL_CLUSTER_CHILD=1.
 *      The worker (see server.ts) turns stdin EOF into process.exit. When this
 *      process dies for ANY reason — clean exit, SIGKILL, OOM — every pipe closes
 *      and every worker exits on its own. No orphans, no /proc scanning, and in
 *      particular no code that hunts and kills processes by name.
 *   2. SIGTERM/SIGINT are forwarded, with a hard kill after a grace period, so a
 *      supervised stop is fast and orderly.
 *   3. A worker that dies unexpectedly is respawned with the same index.
 *
 * Explicitly NOT done here: killing any pre-existing process. An earlier
 * "restart" helper on this project scanned /proc for processes whose cwd matched
 * the app directory and SIGKILLed them; pointed at production it would have
 * killed the live listener. The watchdog in (1) removes the need for that class
 * of cleanup entirely.
 */

import { spawn, type Subprocess } from "bun";
import { availableParallelism } from "node:os";

/**
 * Worker count. Defaults to every core, capped at 4.
 *
 * Above ~4 the returns flatten: each worker holds its own copy of the static
 * vault and its own render cache, so memory grows linearly while throughput does
 * not. Raise ATL_WORKERS deliberately, not by default.
 */
const WORKERS = clamp(int(process.env.ATL_WORKERS, 0) || availableParallelism(), 1, 8);
const GRACE_MS = int(process.env.ATL_SHUTDOWN_GRACE_MS, 5000);
const BOOT_ID = `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
const ENTRY = new URL("./server.ts", import.meta.url).pathname;

function int(value: string | undefined, fallback: number): number {
  const n = Number(value);
  return Number.isFinite(n) ? Math.floor(n) : fallback;
}

function clamp(n: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, n));
}

let stopping = false;
const workers = new Map<number, Subprocess>();

function childEnv(index: number): Record<string, string> {
  const env: Record<string, string> = {};
  for (const [k, v] of Object.entries(process.env)) if (v !== undefined) env[k] = v;

  env.ATL_REUSEPORT = "1";
  env.ATL_CLUSTER_CHILD = "1";
  env.ATL_WORKER_INDEX = String(index);
  env.ATL_CLUSTER_BOOT_ID = BOOT_ID;

  /**
   * The AIS poll loop must run in exactly ONE process. Left on everywhere it
   * would make N independent copies of the same upstream polling on the same
   * schedule, tripping rate limits for no benefit.
   */
  if (WORKERS > 1) env.ATL_AIS_INGEST = index === 0 ? env.ATL_AIS_INGEST ?? "0" : "0";

  return env;
}

function start(index: number): void {
  if (stopping) return;

  const child = spawn({
    cmd: ["bun", "run", ENTRY],
    env: childEnv(index),
    cwd: process.cwd(),
    stdin: "pipe",
    stdout: "inherit",
    stderr: "inherit",
    // Not detached: the worker must share this process group so a group-wide stop
    // signal reaches it, and so its own children die with it.
    onExit(proc, exitCode, signalCode) {
      workers.delete(index);
      if (stopping) return;
      console.log(
        `[atl-cluster] worker ${index} pid ${proc.pid} exited (code ${exitCode} signal ${signalCode}) - restarting`,
      );
      // A crash loop would otherwise respawn forever with no record of why.
      setTimeout(() => start(index), 250);
    },
  });

  workers.set(index, child);
  console.log(`[atl-cluster] worker ${index} pid ${child.pid} boot ${BOOT_ID}`);
}

function shutdown(reason: string): void {
  if (stopping) return;
  stopping = true;
  console.log(`[atl-cluster] ${reason} - stopping ${workers.size} worker(s) (boot ${BOOT_ID})`);

  // Closing stdin is what actually guarantees termination: the workers watch for
  // EOF. The signals are the fast, orderly path on top of that guarantee.
  for (const child of workers.values()) {
    try {
      child.stdin?.end();
    } catch {
      /* pipe already gone */
    }
    try {
      child.kill("SIGTERM");
    } catch {
      /* already dead */
    }
  }

  setTimeout(() => {
    for (const child of workers.values()) {
      try {
        child.kill("SIGKILL");
      } catch {
        /* already dead */
      }
    }
    // Exit non-zero on a signal-driven stop so the supervisor's restart policy
    // sees this as an abnormal end rather than a clean one.
    process.exit(reason === "shutdown complete" ? 0 : 0);
  }, GRACE_MS).unref?.();
}

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));

for (let i = 0; i < WORKERS; i += 1) start(i);

console.log(
  `[atl-cluster] boot ${BOOT_ID} - ${WORKERS} SO_REUSEPORT worker(s) on port ${process.env.PORT ?? 3000}`,
);
