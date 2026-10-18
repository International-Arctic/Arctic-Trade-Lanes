import { readFileSync } from "node:fs";

const AGENT_CARD_CANDIDATES = [
  "./public/.well-known/agent-card.json",
  "./dist/.well-known/agent-card.json",
  "./mvp-static/.well-known/agent-card.json",
];

const FALLBACK = {
  name: "ArcticTradeLanes Atlas Agent",
  description:
    "Arctic GIS OSINT for the Northern Sea Route and the Polar Silk Road: ports, lanes, vessels, programmes, shipyards and industry sites on an EPSG:3996 polar map. Live today: free atlas lookups (GeoJSON downloads and static fact pages in 22 languages) and the paid NSR route-optimize HTTP endpoint (legacy x402 v1, 5 USDC on Base, or a free tier of 10 runs per day per IP).",
  supportedInterfaces: [
    {
      url: "https://arctictradelanes.com/api",
      protocolBinding: "https://arctictradelanes.com/.well-known/x402.json",
      protocolVersion: "1.0",
    },
  ],
  provider: { organization: "ArcticTradeLanes.com", url: "https://arctictradelanes.com" },
  version: "1.0.0",
  documentationUrl: "https://arctictradelanes.com/llms.txt",
  iconUrl: "https://arctictradelanes.com/favicon.svg",
  capabilities: { streaming: false, pushNotifications: false, extendedAgentCard: false },
};

let cached: unknown | null = null;

function loadAgentCard(): unknown {
  if (cached) return cached;
  for (const candidate of AGENT_CARD_CANDIDATES) {
    try {
      cached = JSON.parse(readFileSync(candidate, "utf8"));
      return cached;
    } catch {
      /* try the next location */
    }
  }
  cached = FALLBACK;
  return cached;
}

export function agentCardDocument(): unknown {
  return loadAgentCard();
}

export function agentJsonDocument(): unknown {
  return loadAgentCard();
}
