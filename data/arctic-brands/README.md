# ATL arctic-brands registry

Open registry of companies headquartered in the Arctic and sub-Arctic, published by
[Arctic Trade Lanes](https://arctictradelanes.com/companies). Snapshot: **2026-10-18**.

* **1326 rows**: 1270 from Wikidata, 56 operators listed in the ATL atlas.
* **321 logos** whose reuse is allowed (Wikimedia Commons: Public domain 274, CC BY-SA 4.0 27, CC BY-SA 3.0 13, CC BY 4.0 2, CC0 2, CC BY 2.5 1, Copyrighted free use 1, FAL 1).
  Every other row has an empty `logo_url`, and the site renders a text wordmark instead.
* Countries: FI 609, NO 408, SE 111, RU 77, IS 49, US 25, GL 14, CA 13, FO 9, CN 3, IN 2, SG 1, GB 1, DE 1, IT 1, DK 1, CH 1.

## Files

| file | content |
|---|---|
| `brands.json` | full records (array) |
| `brands.csv` | same rows, `facts` as a JSON string |
| `labels.json` | Wikidata labels (22 languages) for HQ / industry / exchange items used in facts |

## Fields

`id` (Wikidata QID or `atl-op-<slug>`), `name`, `logo_url`, `logo_license`, `logo_source`, `country` (ISO 3166-1 alpha-2),
`sector` (ATL bucket), `hq_lat`, `hq_lon`, `arctic_geo_lat`, `arctic_geo_lon`, `website`,
`facts` (`[{fact, source_url, date}]`), `currency` (ISO 4217 of the country). The JSON adds `slug`, `names` (localized labels), `source`, `wikidata`, `sitelinks`.

## How rows were selected (reproducible)

1. Wikidata items that are an instance of business / company / enterprise / public company / corporation /
   subsidiary / privately held company / state-owned enterprise / limited company, are not dissolved (no P576), and have a
   headquarters (P159) whose own coordinates are at or north of **60°N**. Countries, regions and other first-level
   divisions don't count as an HQ.
2. Notability: at least 2 Wikipedia sitelinks, or 1 sitelink plus an official website (P856).
3. Facts are **only** statements on the Wikidata item: inception (P571), headquarters (P159), industry (P452) and stock
   exchange (P414). Each fact's `source_url` is the Wikidata item and its `date` is the retrieval date. **No people are named**
   (no CEO, founder or owner fields).
4. ATL atlas operators of ports, shipyards, icebreakers, tankers, industry, rail and airports are added when the operator
   name is a single organisation not already present. Their facts link to the ATL atlas page, dated with the atlas snapshot (2026-10-14).
5. Logos come from Wikidata P154. The Commons file license is read through the Commons API (`extmetadata.LicenseShortName`).
   We keep public domain, CC0, CC BY, CC BY-SA, FAL and "Copyrighted free use"; anything else is dropped. Trademark rights
   are separate from copyright, and logos identify the company only.

Inclusion is not an endorsement, partnership or customer relationship.

## License

Wikidata-derived data: CC0 1.0. Atlas-derived rows: same terms as the Arctic Trade Lanes repository. Logos: each file's own license, linked in `logo_source`.

Build scripts: `site/v2/build_brands.py` and `site/v2/build_hubs.py`.
