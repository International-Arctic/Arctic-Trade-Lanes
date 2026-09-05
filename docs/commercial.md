# Commercial overview

Live pricing UI: https://arctictradelanes.com/pricing

| Tier | Price | Notes |
|------|-------|-------|
| Arctic Watch | Free | Atlas + map; 10 route runs/day/IP |
| Arctic Intel | $49/mo or 5 USDC/run | x402 USDC on Base; DeepSeek route reasoning when key set |
| Arctic Command | Custom | States / corporates; SLA 99.9% |

Multi-currency display is indicative FX; **settlement is always USDC on Base**.

Agent discovery: `GET /.well-known/x402.json`  
Fulfill: `GET /api/x402/fulfill` or `POST /api/x402/upload` with `x402-payment` header.
