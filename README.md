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
| Amazon Developer identity verification | **Failed, confirmed scoped to Appstore only** | Confirmed by direct test: the "SAFAR Ads Manager" security profile below was created successfully despite the failed verification. Parked indefinitely — resolving it is optional unless a future step proves otherwise. |
| Login with Amazon security profile | **Done** | Created 15 Aug 2026 as "SAFAR Ads Manager." Client ID confirmed; Client Secret to be retrieved from Web Settings and stored in a password manager (never in this repo, never in chat). Redirect/return URL for OAuth still needs to be set once the backend has a real callback URL (Phase 2). |
| Amazon Ads advertiser account | **Done** | "Grace One / Sponsored ads, India" registered 15 Aug 2026 under `graceragheshwari@gmail.com`, linked to the existing Grace One Seller Central account. Business details (legal name, address, GSTIN `05AXTPS7154F1ZY`) verified against the official GST REG-06 certificate before submission. |
| Direct Advertiser API application | **Ready to submit** | `docs/02-direct-advertiser-application.md` — wording is ready to paste; both prerequisites (LwA security profile, Ads advertiser account) now exist. Locating the exact "API Applications" entry point in the console is in progress. |
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

1. ~~Create the "SAFAR Ads Manager" Login with Amazon security profile~~ — **done**.
2. ~~Register the "Grace One" Amazon Ads (Sponsored ads) advertiser account and link it to Seller Central~~ — **done**.
3. **Manual, in-browser:** retrieve the Client Secret from the security
   profile's Web Settings tab and store it in a password manager (see
   `docs/01-security-profile-setup.md`). Never commit it, never paste it
   into chat.
4. Find the API Applications / Ads API access entry point in the
   Advertising Console (likely under Settings) and submit the Direct
   Advertiser application using `docs/02-direct-advertiser-application.md`
   (wording ready to paste).
5. In parallel, GTIN/ASIN and listing work (outside this repo) can
   proceed independently — see the plan's Phase 0 and Phase 14.
6. After the Direct Advertiser application is approved and OAuth is
   complete, wire `AmazonAdsClient`'s live-mode HTTP calls against real
   Amazon Ads API responses (the dry-run interfaces are already the
   intended shape) and flip `SAFAR_ADS_DRY_RUN=false` only after a
   careful review.

## Safety principle

Everything here follows one rule from the plan: **the agent may make
bounded routine changes; total spend increases, major bid changes, and
changes to business constants require owner approval — enforced in
code, not just in a prompt.** See `docs/04-financial-guardrails.md` for
the full breakdown.
