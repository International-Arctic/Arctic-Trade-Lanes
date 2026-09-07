# Ship / icebreaker fleet densification (schematic)

ArcticTradeLanes atlas pins for **tankers** and **icebreakers** are **route-schematic**, not live AIS. Production builder (`build_atlas.py` on Zo) must:

1. Match `typical_arctic_route` / `primary_service_route` with **longest** `ROUTE_ANCHORS` substring.
2. Fall back to `COUNTRY_ANCHORS` by vessel `country` when no route key matches (prevents a single NSR centroid stack).
3. Emit `country` + `year_built` on every ship feature (dataset already has these columns).
4. Golden-angle spiral unstack co-route fleets; expand radius with stack size.
5. Mark `position_quality` as `schematic_route_anchor` | `route_anchor`.

## QA thresholds (client or CI)

- Every `layer=tankers|icebreakers` feature has non-empty `country`.
- Max `position_stack_size` ≤ 24 (alert if higher — anchors need densifying).
- Unique rounded lon/lat counts should equal fleet size after spiral (no exact pixel stacks).

See Issue #2 (projection / ships QA) and Issue #3 (attribute completeness).
