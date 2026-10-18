import { upgradeWebSocket, websocket as honoBunWebSocket } from "hono/bun";
import type { Hono } from "hono";
import type { WSContext } from "hono/ws";

/**
 * ATL WebSocket server (restored 2026-10-14).
 *
 * Exposes the live atlas change-feed used by the map client:
 *   /ws        and  /api/ws
 *
 * Messages are JSON: { type: "hello" | "atlas" | "ais" | "pong", ... }.
 * The channel is read-mostly; inbound `{"type":"ping"}` and
 * `{"type":"subscribe","layer":"ports"}` are accepted. Nothing here mutates
 * the atlas — broadcasts are driven by the caller through `broadcast()`.
 */

type Client = { socket: WSContext; layers: Set<string>; connectedAt: number };

const clients = new Set<Client>();
const startedAt = Date.now();

function safeSend(client: Client, payload: unknown): void {
  try {
    client.socket.send(JSON.stringify(payload));
  } catch {
    clients.delete(client);
  }
}

export function broadcast(payload: Record<string, unknown>): number {
  let sent = 0;
  for (const client of clients) {
    safeSend(client, payload);
    sent += 1;
  }
  return sent;
}

export function wsStats() {
  return {
    ok: true,
    clients: clients.size,
    startedAt,
    uptimeMs: Date.now() - startedAt,
    paths: ["/ws", "/api/ws"],
    protocol: "json",
  };
}

const upgradeHandler = upgradeWebSocket((c) => {
  const requested = c.req.query("layers");
  const layers = new Set(
    (requested ? requested.split(",") : []).map((v) => v.trim()).filter(Boolean),
  );

  return {
    onOpen(_event, socket) {
      const client: Client = { socket, layers, connectedAt: Date.now() };
      clients.add(client);
      safeSend(client, {
        type: "hello",
        service: "ArcticTradeLanes.com",
        protocol: "json",
        layers: [...layers],
        clients: clients.size,
        ts: Date.now(),
      });
      console.log(`[WS Server] Connection for session: ${c.req.query("session") || "default"}`);
    },
    onMessage(event, socket) {
      const client = [...clients].find((entry) => entry.socket === socket);
      if (!client) return;
      let parsed: any = null;
      try {
        parsed = JSON.parse(String(event.data));
      } catch {
        safeSend(client, { type: "error", error: "invalid json" });
        return;
      }
      if (parsed?.type === "ping") {
        safeSend(client, { type: "pong", ts: Date.now() });
        return;
      }
      if (parsed?.type === "subscribe" && typeof parsed.layer === "string") {
        client.layers.add(parsed.layer);
        safeSend(client, { type: "subscribed", layer: parsed.layer });
        return;
      }
      if (parsed?.type === "unsubscribe" && typeof parsed.layer === "string") {
        client.layers.delete(parsed.layer);
        safeSend(client, { type: "unsubscribed", layer: parsed.layer });
        return;
      }
      safeSend(client, { type: "error", error: "unknown message type" });
    },
    onClose(_event, socket) {
      for (const client of clients) {
        if (client.socket === socket) clients.delete(client);
      }
      console.log(`[WS Server] Client disconnected from session ${c.req.query("session") || "default"}.`);
    },
    onError(_event, socket) {
      for (const client of clients) {
        if (client.socket === socket) clients.delete(client);
      }
    },
  };
});

export const webSocketServer = {
  configureRoutes(app: Hono): void {
    const mount = (path: string) => {
      app.get(path, async (c, next) => {
        if (c.req.header("upgrade")?.toLowerCase() !== "websocket") {
          return c.json(wsStats());
        }
        try {
          const response = await upgradeHandler(c, next);
          return response ?? c.json(wsStats());
        } catch (error) {
          console.error(
            `[WS Server] upgrade failed: ${error instanceof Error ? error.message : String(error)}`,
          );
          return c.json(
            { ok: false, error: "websocket upgrade unavailable", ...wsStats() },
            503,
          );
        }
      });
    };
    mount("/ws");
    mount("/api/ws");
  },
  broadcast,
  stats: wsStats,
};

/** Bun needs this handler object on the server export for ws callbacks to fire. */
export const bunWebSocketHandler = honoBunWebSocket;

export default webSocketServer;
