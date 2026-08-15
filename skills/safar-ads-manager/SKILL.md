---
name: safar-ads-manager
description: Operating playbook for managing SAFAR's Amazon India Sponsored Products advertising through the safar_ads API client. Use when reading SAFAR campaign performance, recommending or making bounded optimisation changes (bids, budgets, negatives, pausing), harvesting search terms, or producing the daily SAFAR ads report. Do not use for pricing, payments, account ownership, or developer-credential changes - those are permanently out of scope for this skill.
---

# SAFAR Ads Manager

Operating instructions for the agent that manages SAFAR's Amazon India
Sponsored Products advertising. This skill contains strategy and
decision rules only - no credentials. Credentials live in environment
variables and are read directly by `safar_ads.amazon_ads_client`; this
skill's tools never receive raw secrets.

## 1. Purpose and scope

Manage Sponsored Products advertising for the SAFAR brand (Grace One)
on Amazon.in only. In scope: campaigns, ad groups, keywords/targets,
bids, budgets, negatives, pausing, and reporting for the five SAFAR
ASINs. Out of scope, always: product price, payment/bank details, tax
settings, account ownership, developer credentials, and any advertiser
account other than SAFAR's own.

## 2. Product facts

- Brand: SAFAR (Grace One). 10 ml, dual-use car air freshener - hang
  from the mirror or clip to the AC vent.
- Fragrances: Musk, Lavender, Sandalwood, Vanilla, Jasmine.
- Longevity claim: **"up to 45 days" only**. Never use "60 days" in any
  generated copy, keyword rationale, or report commentary.

## 3. Commercial constants

Read these from `config/business_constants.yaml` at runtime - never
hard-code a number here that could drift from that file:

- Selling price, physical packed cost, profit floor per unit.
- Target ad cost per order range.
- `guardrails.max_total_daily_budget_inr`, `max_monthly_ad_spend_inr`,
  `max_single_bid_change_pct`, `max_campaign_budget_change_pct`.

These are enforced in code by `safar_ads.safety.SafetyMiddleware`. If a
recommended action would violate one, the client raises
`SafetyViolation` before any request reaches Amazon - treat that as a
hard stop, not a retry-with-different-wording signal.

## 4. Campaign naming convention

`SAFAR-IN-SP-<ROLE>-<STAGE>` where `ROLE` is `AUTO-DISCOVERY`,
`MANUAL-RESEARCH`, or `EXACT-WINNERS`, and `STAGE` is `LAUNCH` (initial)
or `SCALE` (after the owner approves scaling, Phase 8). Ad group and
target names should stay traceable to the campaign name. Full structure
lives in `config/campaigns.yaml` and `docs/03-campaign-structure.md`.

## 5. Metrics to monitor

Impressions, clicks, CPC, spend, orders, attributed sales,
cost/order, conversion rate, ACoS/ROAS, and **calculated contribution
profit** via `safar_ads.profit.contribution_profit()`. Contribution
profit is the primary guardrail - a campaign can look efficient on ACoS
and still fail the owner's net-profit target once fees, fulfilment,
returns and promotions are included.

## 6. Decision rules (traffic-light, Phase 6.1)

Use `safar_ads.profit.classify_ad_cost()` against observed ad cost per
completed order:

| Classification | Ad cost/order | Default action |
|---|---|---|
| `excellent` | below Rs.60 | Maintain; consider a small increase only with adequate data and if profit holds. |
| `target_range` | Rs.60-90 | Maintain; optimise search terms and conversion. |
| `above_preferred` | Rs.90-110 | Reduce bids selectively; investigate conversion, relevance, listing quality. |
| `wasteful` | above Rs.110 | Reduce/pause after sufficient evidence. Do not keep increasing spend blindly. |

## 7. Search-term harvesting (Phase 6.2)

- Move search terms with multiple profitable orders from
  `SAFAR-IN-SP-MANUAL-RESEARCH-*` (or auto-discovery) into
  `SAFAR-IN-SP-EXACT-WINNERS-*` as exact targets.
- Add negatives to discovery/research campaigns for terms that are
  irrelevant or repeatedly non-converting, only after enough evidence.
- Keep a discovery campaign funded at all times so new terms keep
  surfacing - never harvest it down to zero.

## 8. Fragrance-level allocation

Do not force equal budget across Musk, Lavender, Sandalwood, Vanilla,
and Jasmine. If one fragrance converts materially better, gradually
shift budget toward it while preserving enough discovery spend that the
others aren't prematurely abandoned.

## 9. Minimum-data rule

Never pause or scale a target off one or two clicks. Require a minimum
spend/click sample, account for attribution/reporting delay, and
compare over a sensible lookback window before a strong action.
Default to **no increase in spend** if data is incomplete, delayed, or
inconsistent.

## 10. Permission levels

| Level | Authority | When |
|---|---|---|
| 0 - Read only | Read campaigns/reports, produce recommendations. No writes. | First integration and validation. **Current default - see `permission_level.current` in business_constants.yaml.** |
| 1 - Controlled writes | Small bid changes, negatives, pausing obvious waste, bounded reallocation within the hard total cap. | After recommendations have been checked against real outcomes. |
| 2 - Semi-autonomous | Create/modify campaigns, redistribute budget within strict encoded limits. Major changes still need owner approval. | After several weeks of reliable operation. |
| 3 - Broad autonomy | Not recommended for initial SAFAR launch. | Only after strong monitoring, testing, and owner confidence. |

The agent reads the current level from config; it never raises its own
permission level.

## 11. Approval rules

- **Automatic** (within the current permission level and hard caps):
  bid changes within `max_single_bid_change_pct`, budget changes within
  `max_campaign_budget_change_pct` and the total daily cap, adding
  negatives, pausing targets with clear evidence of waste.
- **Approval-gated**: any change exceeding the bid/budget % caps, raising
  the total daily cap, creating new campaigns beyond the launch set,
  moving to a higher permission level.
- **Prohibited, always**: price changes, payment/bank/tax/account-ownership
  changes, developer-credential changes, bypassing the kill switch,
  exceeding `max_total_daily_budget_inr`.

## 12. Daily report format

Produce, in this order: spend (total + by campaign/fragrance),
orders/sales (ad-attributed + organic where available), cost/order,
CPC, conversion rate, ACoS/ROAS, estimated contribution profit, every
action taken with its reason, and exceptions (out-of-stock, listing
suppression, report delay, API errors, spend anomalies).

## 13. Escalation rules

Escalate to the owner rather than acting automatically when: an Amazon
Ads API error persists across retries, spend deviates sharply from the
expected pattern, a SAFAR ASIN goes out of stock or gets suppressed,
contribution profit trends below the profit floor for a sustained
period, or a recommended action would require exceeding any hard cap in
`config/business_constants.yaml`.

## 14. What this skill must NOT contain or do

- No Amazon Client Secret, refresh token, or access token, ever.
- No bank/payment information.
- No instruction that lets the agent bypass a backend spending cap.
- No unsupported product or competitor claims presented as fact -
  "up to 45 days" is the only longevity claim.
