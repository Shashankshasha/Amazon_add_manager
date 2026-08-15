# Financial guardrails

The core principle from the implementation plan: **spending limits and
financial guardrails live outside the AI model.** A prompt instruction
like "never spend more than Rs.400/day" is not a safeguard by itself —
the backend must reject any API call that would breach it, even if the
agent (or a person prompting it) asks for an exception. That's what
`src/safar_ads/safety.py` (`SafetyMiddleware`) implements, and
`config/business_constants.yaml` is its only source of numbers.

## Contribution-profit formula (Phase 4.1)

```
Net contribution per completed order
  = Selling price
  - Physical product/dispatch cost
  - Amazon variable charges
  - Fulfilment/shipping
  - Advertising spend allocated to that order
  - Coupons/promotions
  - Return/refund allowance
  - Other variable selling costs
```

Implemented in `safar_ads.profit.contribution_profit()`. This is the
number the agent should treat as the real success metric — not ACoS or
ROAS in isolation, which can look healthy while contribution profit is
negative once fees, fulfilment, and returns are included.

## Launch economics at Rs.299 / Rs.75 physical cost (Phase 4.2)

| Ad cost/order | Remaining after cost + ads | Max other costs if Rs.70 profit must hold |
|---|---|---|
| Rs.60 | Rs.164 | Rs.94 |
| Rs.75 | Rs.149 | Rs.79 |
| Rs.90 | Rs.134 | Rs.64 |

Reproduce this anytime with `python -m safar_ads.cli profit-table` — it
reads live from `config/business_constants.yaml`, so it stays correct
if the price or cost assumption changes.

**This table is why Rs.70 profit is not yet guaranteed at Rs.299.** If
Amazon fees + fulfilment + returns + coupons exceed the "max other
costs" column for the ad cost you're actually seeing, either the price,
the ad-cost target, the fulfilment method, or the temporary profit
expectation has to change. Run the real Amazon fee preview before
treating any of these numbers as locked.

## Hard-coded caps (Phase 4.3 / 8.3)

All enforced by `SafetyMiddleware`, read from
`config/business_constants.yaml` → `guardrails`:

| Cap | Value | Enforced by |
|---|---|---|
| `max_total_daily_budget_inr` | Rs.400 | `validate_total_daily_budget()` — checked on every `create_campaign` and `set_budget` call, summed across *all* active campaigns, not just the one being changed. |
| `max_monthly_ad_spend_inr` | Rs.12,000 (derived: 400 × 30) | Owner should confirm explicitly rather than treat the derived value as final. |
| `max_single_bid_change_pct` | 15% | `validate_bid_change()` — blocks any `set_bid` call whose % change exceeds this, unless `owner_approved=True` is passed explicitly. |
| `max_campaign_budget_change_pct` | 15% | `validate_budget_change()` — same pattern for `set_budget`. |

Raising the Rs.400/day cap itself requires the owner to see stable
conversion, acceptable contribution profit, sufficient inventory, no
material return problem, and no unexplained reporting/attribution issue
first (Phase 12.1). The agent may *recommend* a new cap; it cannot
approve one.

## Permanently prohibited actions

Listed in `guardrails.prohibited_actions` and rejected unconditionally
by `SafetyMiddleware.check_prohibited()` regardless of owner-approval
flags: changing product price, payment/bank details, tax settings,
account ownership, or developer credentials; exceeding the total daily
budget cap; bypassing the kill switch. There is no code path that lets
the agent request an exception to this list — it would require editing
`config/business_constants.yaml` directly.

## Kill switch

`SAFAR_ADS_KILL_SWITCH` (env var, defaults to `true` per
`.env.example`) blocks every write call immediately when engaged,
checked first in `SafetyMiddleware.validate_write()` before any other
logic runs. This is the owner's single point of control to stop all
automated spending changes without touching code.

## Idempotency and audit log

- Every write requires a unique `idempotency_key`. `IdempotencyStore`
  persists used keys to disk (`data/idempotency_keys.json`, git-ignored)
  so a retried or replayed instruction can't create duplicate campaigns
  or repeat a budget change.
- Every write attempt — allowed or blocked — is recorded by `AuditLog`
  to `data/audit_log.jsonl` (git-ignored) with the action, old/new
  value, approval flag, and result. This is what the daily report's
  "Actions taken" section should be built from.

## Minimum-data rule

Not a spend cap, but a guardrail against noisy decisions: don't pause
or scale a target based on one or two clicks. `SKILL.md` §9 encodes
this for the agent; enforcing a numeric minimum (e.g. "at least N clicks
or Rs.X spend before acting") should be added to `safar_ads.safety` once
real performance data exists to calibrate N and X sensibly — recorded
here as an open item, not yet implemented.
