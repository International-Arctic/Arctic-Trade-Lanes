# docs/mvp: ATL MVP build spec (2026-10-06)

This folder is a spec only. Nothing in it is deployed, and the live site and existing x402 endpoints are unchanged.

| File | What it is |
|---|---|
| [`ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md`](./ATL-MVP-REGISTRATION-AGENTIC-SPEC-20261006.md) | Main build spec: architecture, OAuth providers, agent registry, payment protocols (x402 v2, MPP, ACP, AP2), A2A, MCP, storage durability, privacy, endpoints, SEO fact pages, brands strip, phased checklist, owner's manual steps |
| [`0001_init.sql`](./0001_init.sql) | Cloudflare D1 schema (first migration), validated with SQLite |
| [`flexport-mcp-integration.md`](./flexport-mcp-integration.md) | Flexport MCP integration plan, checked against Flexport's public docs, with the discrepancies listed |
| [`arctic-brands.csv`](./arctic-brands.csv) | 50 Arctic ecosystem companies covered on the atlas (22 ready, 22 need a logo, 6 need an atlas object). Display label: "Arctic ecosystem: companies covered on the atlas". Never shown as partners. |

Privacy rule for this public repo: schema, docs, counts and ciphertext hashes only. Never commit emails, hashes of emails, or secrets.
