# Contributing to the arctic-brands registry

There are two ways to add a company or correct a row.

## 1. Contribution form (no account needed)

Use the form at https://arctictradelanes.com/#atlx-contribute and choose **business** (new company) or **correction**.
Behind it is `POST /api/contributions`:

```json
{ "type": "business", "name": "Example AS", "details": "What the company does in the Arctic, plus one public source URL.",
  "url": "https://example.no", "location": "Tromsø, NO", "consent": true }
```

Submissions go into a private review queue. Nothing is published automatically.

## 2. GitHub pull request

1. Edit `data/arctic-brands/brands.json`, plus `brands.csv` if you can (maintainers regenerate it otherwise).
2. Every fact needs a public `source_url` and a `date` (YYYY-MM-DD). Rows without a source are rejected.
3. Only add a `logo_url` when the file's license allows reuse (public domain, CC0, CC BY, CC BY-SA). Fill in
   `logo_license` and `logo_source` as well. Otherwise leave all three empty and a text wordmark is shown.
4. Don't name private individuals, and don't add prices, revenues or other figures without a dated source.
5. Inclusion rule: HQ at or north of 60°N, or a documented operating presence in the Arctic (a port, terminal, mine,
   field or route) with a source.

Pages update on the next deploy: `/company/<slug>`, `/companies`, `/country/<iso2>`, in 22 languages.
