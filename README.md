# SAFAR Ads Manager

Programmatic, profit-guarded management of SAFAR's Amazon India
Sponsored Products advertising. Built from the *SAFAR Amazon Ads
Automation & Agent Implementation Plan* (v1.0, 15 Aug 2026), archived in
full at [`docs/00-implementation-plan.md`](docs/00-implementation-plan.md)
— see that document for the full roadmap; this README tracks what's
implemented here versus what's still pending.

## Current status

| Workstream | Status | Next action |
|---|---|---|
| Business constants / hard caps | **Done** | `config/business_constants.yaml` — review before launch. |
| Campaign structure / seed keywords | **Done** | `config/campaigns.yaml`, `config/keywords.yaml` — data-led revision after real performance exists. |
| Profit calculator | **Done, tested** | `src/safar_ads/profit.py` |
| Safety middleware (caps, kill switch, idempotency, audit log) | **Done, tested** | `src/safar_ads/safety.py` |
| Amazon Ads API client | **Dry-run/mock only** | `src/safar_ads/amazon_ads_client.py` — real HTTP paths are scaffolded but unverified against live credentials; re-check against current Amazon Ads API docs before first live write. |
| SAFAR Ads SKILL.md | **Done** | `skills/safar-ads-manager/SKILL.md` |
| Amazon Developer identity verification | **Failed, likely scoped to Appstore only** | First attempt failed with "cannot upload apps." Amazon Developer Community guidance says this verification gates Appstore app publishing specifically, not every Developer Console feature — see `docs/01-security-profile-setup.md` for the source. Untested whether it blocks LWA/Ads API; don't assume either way until Step 3 is attempted. |
| Login with Amazon security profile | **Not started — manual step, try now** | `docs/01-security-profile-setup.md` — worth attempting even with verification unresolved. |
| Direct Advertiser API application | **Not started** | `docs/02-direct-advertiser-application.md` (wording ready to paste, needs the security profile first) |
| Five SAFAR ASINs / GTINs | **Pending** | Outside this repo's scope — tracked in the plan's Phase 0. |
| Live campaign writes | **Blocked** | Requires live ASINs + approved, authenticated API access. Not possible yet. |

## What you can do today, with zero Amazon credentials

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"

python -m pytest                    # 22 tests: profit math, safety caps, dry-run client
python -m safar_ads.cli check-budget   # validates config/campaigns.yaml against the Rs.400/day cap
python -m safar_ads.cli profit-table   # reproduces the Phase 4.2 launch-economics table
python -m safar_ads.cli plan           # prints the exact Phase 7 dry-run campaign creation plan
```

Every write method on `AmazonAdsClient` (`create_campaign`, `set_bid`,
`set_budget`, etc.) works in dry-run mode: it runs the full
`SafetyMiddleware` validation — hard budget cap, bid/budget change %
caps, idempotency, kill switch — and returns exactly what *would* be
sent to Amazon, without any network call. This is how the guardrails get
tested before there's anything real to guard.

## Directory layout

```
config/                   Business constants, campaign plan, seed keywords (no secrets)
src/safar_ads/
  config.py                Loads config/*.yaml
  profit.py                Contribution-profit formula + traffic-light classifier
  safety.py                Hard caps, kill switch, idempotency store - SafetyMiddleware
  audit_log.py             Append-only JSONL log of every write attempt
  amazon_ads_client.py     Thin Ads API client: dry-run/mock now, real HTTP scaffolded
  cli.py                   `plan` / `check-budget` / `profit-table` commands
skills/safar-ads-manager/SKILL.md   Agent operating playbook (no secrets)
docs/                      Manual setup checklists + design rationale
tests/                     pytest suite for profit.py, safety.py, amazon_ads_client.py
.env.example               Credential placeholders - copy to .env, never commit .env
```

## What's next

1. **Manual, in-browser:** work through
   `docs/01-security-profile-setup.md` (Login with Amazon / security
   profile). Amazon Developer Community guidance suggests identity
   verification only gates Appstore app publishing, so this is worth
   attempting now rather than waiting on verification — report back
   whether it goes through cleanly or hits its own verification error.
2. Once the security profile exists, submit the Direct Advertiser
   application using `docs/02-direct-advertiser-application.md`.
3. In parallel, GTIN/ASIN and listing work (outside this repo) can
   proceed independently — see the plan's Phase 0 and Phase 14.
4. After live credentials exist, wire `AmazonAdsClient`'s live-mode HTTP
   calls against real Amazon Ads API responses (the dry-run interfaces
   are already the intended shape) and flip `SAFAR_ADS_DRY_RUN=false`
   only after a careful review.

## Safety principle

Everything here follows one rule from the plan: **the agent may make
bounded routine changes; total spend increases, major bid changes, and
changes to business constants require owner approval — enforced in
code, not just in a prompt.** See `docs/04-financial-guardrails.md` for
the full breakdown.
