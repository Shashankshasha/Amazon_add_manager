# SAFAR launch campaign structure

Source of truth: `config/campaigns.yaml` (machine-readable) and
`config/keywords.yaml` (seed keyword themes). This document explains the
*why* behind that config; if the two ever disagree, the YAML is correct
and this doc needs updating.

## Why three campaigns

| Campaign | Role | Why separate |
|---|---|---|
| `SAFAR-IN-SP-AUTO-DISCOVERY-LAUNCH` | Automatic targeting | Lets Amazon surface real customer search behaviour and product contexts we haven't thought of yet, across all five fragrances. Cheapest way to generate harvestable data. |
| `SAFAR-IN-SP-MANUAL-RESEARCH-LAUNCH` | Manual phrase/exact testing | Tests our own hypotheses (category, format, value, size, fragrance-specific terms from `config/keywords.yaml`) with controlled bids, independent of what auto-targeting finds. |
| `SAFAR-IN-SP-EXACT-WINNERS-LAUNCH` | Tightly controlled exact targeting | Once a search term proves profitable in either of the above, it graduates here so its bid and budget can be managed precisely, without competing against broader discovery spend. Starts empty by design. |

Total launch budget: Rs.150 + Rs.150 + Rs.100 = **Rs.400/day**, matching
`guardrails.max_total_daily_budget_inr`. `python -m safar_ads.cli
check-budget` fails loudly if this ever drifts out of sync.

## Naming convention

`SAFAR-IN-SP-<ROLE>-<STAGE>`

- `SAFAR` — brand.
- `IN` — marketplace (Amazon.in). Add a second segment if SAFAR ever
  expands to another marketplace, rather than overloading this one.
- `SP` — ad product (Sponsored Products). Reserve `SB`/`SD` prefixes if
  Sponsored Brands/Display are added later.
- `ROLE` — `AUTO-DISCOVERY`, `MANUAL-RESEARCH`, or `EXACT-WINNERS`.
- `STAGE` — `LAUNCH` initially; bump to `SCALE` only after the owner
  approves raising the Rs.400/day cap (Phase 8.1 of the plan).

Ad group and target names should stay traceable to their campaign name
(see `config/campaigns.yaml` for the `-AG1` suffix convention).

## Starting rules (Phase 9.1)

- Sponsored Products only at launch — the objective is product-detail-page
  traffic and sales, not brand awareness.
- Conservative bidding: no aggressive placement multipliers or automatic
  budget expansion on day one.
- Start with the seed keyword themes in `config/keywords.yaml`, not
  hundreds of broad terms.
- Every campaign is created in `state: paused` — see Phase 7 (safe
  launch sequence): dry-run plan → owner review → create paused → verify
  → enable in a controlled window.

## Fragrance handling

Fragrances (Musk, Lavender, Sandalwood, Vanilla, Jasmine) are not split
into five separate campaigns at launch — that would fragment the budget
too thin to generate meaningful data per fragrance. Instead:

- `config/keywords.yaml` includes fragrance-specific keyword themes
  inside the shared manual-research campaign.
- Once ASINs exist and real performance data comes in, the agent
  reallocates budget toward stronger-converting fragrances per
  `SKILL.md` §8 (fragrance-level allocation) — without starving the
  weaker ones of all discovery spend.
- Revisit whether per-fragrance campaigns make sense only after there's
  enough data to justify the added complexity.

## What's still pending before any of this can go live

Per `docs/README` (project status) — five ASINs must exist and be
buyable, and Amazon Ads API access must be approved and authenticated.
Until then, `python -m safar_ads.cli plan` is the closest thing to
"running" this structure: it prints exactly what would be created.
