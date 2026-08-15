# SAFAR Amazon Ads Automation & Agent Implementation Plan

*From manual launch to API-driven, profit-controlled advertising.*
Prepared for Grace One / SAFAR. Version 1.0 — 15 August 2026.

> Archived here as the source-of-truth reference for everything else in
> this repo. Extracted from the original `.docx`; content is unchanged,
> reformatted as markdown. If this ever disagrees with `config/*.yaml`
> or `SKILL.md`, treat those as the current implementation and this file
> as the plan they were built from.

**Purpose:** This document turns the current SAFAR Amazon Ads idea into
a complete implementation roadmap: prepare the listing, obtain Amazon
Ads API access, create campaigns programmatically, connect an AI agent,
enforce hard financial controls, launch safely, and scale only when the
economics work.

**Working principle:** automate the repeatable work, but keep spending
limits and financial guardrails outside the AI model.

## 1. Executive Summary

The goal is to build a SAFAR Amazon advertising system that can create
and manage Sponsored Products campaigns programmatically, while an AI
agent uses business rules to decide what to optimise. Amazon Ads API is
the execution layer; the agent is the decision layer; SKILL.md is the
operating playbook; backend code is the safety layer.

| Item | Working decision |
|---|---|
| Commercial objective | Launch SAFAR as a premium 10 ml dual-use car air freshener (hang + AC vent clip), build traffic and sales efficiently, and scale only when unit economics are acceptable. |
| Launch price discussed | Rs.299 introductory price, subject to final fee/profit validation before launch. |
| Product claim | Up to 45 days. Do not use 60 days in listings, ads, packaging, or comparison copy. |
| Working physical cost | Use Rs.75 per unit as the conservative fully packed physical cost until the final cost sheet is locked (roughly Rs.65 product cost plus about Rs.10 dispatch packaging). |
| Desired mature profit floor | Target at least Rs.70 net contribution per completed unit after all variable selling costs. |
| Advertising target | Approximately Rs.60-Rs.90 advertising cost per completed order during the controlled launch, then improve over time. |
| Initial ad ceiling | Working starting ceiling: about Rs.400/day across controlled Sponsored Products campaigns. Launch guardrail, not a permanent budget. |
| Automation objective | Programmatically create campaigns, read performance, optimise bids/keywords/budgets, harvest winning search terms, add negatives, pause waste, and report results. |
| Human-control principle | Agent may make bounded routine changes; total spend increases, major bid changes, and changes to business constants require owner approval. |

**Important finance check:** At a Rs.299 selling price and Rs.75
physical cost, reserving Rs.70 net profit leaves Rs.154 for every other
variable cost combined. If advertising costs Rs.60-Rs.90 per order, only
Rs.94-Rs.64 remains for Amazon fees, fulfilment/shipping, tax on fees,
return allowance, coupons and other variable charges. Therefore the
Rs.299 price must be validated against the actual Amazon fee preview
before treating Rs.70 profit as guaranteed.

## 2. Current Project Status

| Workstream | Status | Current position | Next action |
|---|---|---|---|
| Amazon Seller Central India | COMPLETE | Seller account is available and accessible. | Keep account compliant and ready for listings. |
| Amazon Advertising / Campaign Manager | COMPLETE | Campaign Manager is accessible. A Rs.1,000 promotional ad-credit message was visible; terms/eligibility should be checked before relying on it. | No campaign should be launched until the product listing is ready. |
| Business email | COMPLETE | hello@graceone.in selected for developer/API administration. | Keep access secure and enable strong account security. |
| GTIN / GS1 barcodes | PENDING | Five fragrance-specific GTINs are not yet available. | Obtain/allocate GTINs for Musk, Lavender, Sandalwood, Vanilla and Jasmine. |
| SAFAR Amazon listings / ASINs | PENDING | Listings are deferred until GTINs are ready. | Create listings and capture each ASIN/SKU. |
| Amazon Developer account | IN PROGRESS | Developer registration was started using business details. | Resolve identity verification issue before depending on this account for API onboarding. |
| Developer identity verification | ISSUE | First verification attempt failed. Amazon documentation states there are three verification attempts. | Check exact legal-name match, accepted ID, country selection and image quality; contact Developer Support if appropriate before consuming attempts. |
| Login with Amazon (LwA) app | NOT STARTED | Not yet completed. | Create after developer-account access is in a healthy state. |
| Amazon Ads API access | NOT STARTED | No Direct Advertiser API application submitted yet. | Apply after LwA app/security profile is available. |
| SAFAR Ads Agent | NOT STARTED | Architecture defined conceptually only. | Build after API read access works. |
| SAFAR Ads SKILL.md | NOT STARTED | Rules discussed but not packaged as a skill yet. | Create after financial constants and campaign rules are locked. |

## 3. Target System Architecture

The final system separates strategy, execution, security, and financial
controls, so the AI never has unrestricted authority over advertising
spend:

```
OWNER / BUSINESS RULES         Price, cost, profit floor, max daily/monthly ad spend, approval thresholds
        |
SAFAR ADS AGENT                Reads data, reasons about performance, chooses bounded optimisation actions
        |
SAFAR SKILL.md                 Reusable operating instructions: metrics, decision rules, escalation, naming, reporting
        |
SAFETY MIDDLEWARE / BACKEND     Hard caps, validation, credentials, approval checks, idempotency, audit log
        |
AMAZON ADS API CLIENT          Campaigns, ad groups, ads, targeting, bids, budgets, reports, profiles, auth
        |
AMAZON ADS                     Sponsored Products campaigns on Amazon India
        |
PRODUCT DETAIL PAGES           SAFAR Musk, Lavender, Sandalwood, Vanilla and Jasmine ASINs
```

**Why this structure matters:** A prompt such as "never spend more than
Rs.400/day" is not a sufficient financial safeguard by itself. The
backend should calculate and reject any API update that would exceed
the configured hard cap, even if the agent requests it.

## 4. Phase 0 — Product, Listing and Economics Readiness

The Ads API can create traffic, but it cannot compensate for a weak or
incomplete product listing. Complete the commercial foundation before
paying for clicks.

### 4.1 Lock the SAFAR product facts
- [x] Brand: SAFAR under Grace One.
- [x] Product: 10 ml premium car air freshener.
- [x] Core differentiator: dual-use format — hang from the mirror or use
      with the AC vent clip.
- [x] Fragrances: Musk, Lavender, Sandalwood, Vanilla and Jasmine.
- [x] Longevity claim: "up to 45 days" only, with suitable qualification
      where needed.
- [x] Packaging and listing claims must match the actual product and
      supporting documentation.

### 4.2 Obtain GTINs and create ASINs
- [ ] Obtain or allocate five valid GS1/GTIN identifiers — one per
      fragrance/SKU.
- [ ] Create the five Amazon product listings in the correct category.
- [ ] Capture ASIN, SKU, fragrance name, selling price, fulfilment
      method and inventory in a master product table.
- [ ] Where Amazon supports compliant variation relationships for the
      category, evaluate presenting fragrances as variations.
- [ ] Confirm product detail pages are active and buyable before
      advertising them.

### 4.3 Build a conversion-focused listing before ads
- [ ] Main image: clean, accurate bottle and retail box; no alteration
      of real product appearance.
- [ ] Secondary image: explicitly demonstrate "HANG IT" and "CLIP IT"
      with the included hardware.
- [ ] Feature image: 10 ml, dual-use format, up to 45 days, fragrance
      identity, and formulation claims only where substantiated.
- [ ] Comparison image: show the value of two installation methods
      without unsupported "only/first in India" claims.
- [ ] Title, bullets, backend search terms and description based on
      actual search behaviour and Amazon policy.
- [ ] Ensure launch stock is sufficient so ads don't drive traffic to an
      unavailable listing.

### 4.4 Lock the unit economics

| Input | Working value | Action before launch |
|---|---|---|
| Selling price | Rs.299 launch price discussed | Validate with actual Amazon fee preview. |
| Physical packed cost | Rs.75 conservative assumption | Replace with final audited cost if different. |
| Desired mature net contribution | Rs.70/unit | Use as long-term guardrail after launch phase. |
| Target ad cost/order | Rs.60-Rs.90 | Treat as target range, not a guaranteed result. |
| Initial daily ad cap | Rs.400/day | Enforce in backend, not only in the agent prompt. |
| Launch-profit sacrifice | Optional, not yet numerically fixed | If used, define a temporary minimum profit and maximum number of units/days in writing. |

## 5. Phase 1 — Obtain Amazon Ads API Access

Amazon Ads states that API access requires application and approval;
direct advertisers are eligible. Official onboarding sequence: create a
Login with Amazon client → apply for Ads API access → assign the
approved access to that LwA application.

### 5.1 Resolve the current developer identity issue
- [ ] Verify the full legal name in Developer Console > Company Profile
      matches the government-issued ID exactly, including middle names.
- [ ] Use an accepted ID type and the correct ID-issuing country.
- [ ] Use clear, uncropped images with no glare/blur per Amazon's upload
      requirements.
- [ ] Do not casually consume repeat attempts — documentation states
      there are three verification attempts.
- [ ] If the account reaches a failed state or the reason is unclear,
      use Amazon Developer Support rather than repeatedly retrying.

**Current issue:** One identity-verification attempt has already
failed. This does not stop planning, listing, or agent-specification
work, but should be resolved before the project depends on developer/API
credentials.

### 5.2 Create the Login with Amazon (LwA) application
- [ ] Use the verified/usable Amazon Developer account.
- [ ] Create a security profile / LwA application for the internal tool.
- [ ] Use a clear name such as "SAFAR Ads Manager" or "Grace One Ads
      Manager".
- [ ] Use business-controlled contact details where possible.
- [ ] Capture the LwA Client ID and Client Secret securely.
- [ ] Never place the Client Secret in SKILL.md, a public Git
      repository, browser JavaScript, screenshots, or ordinary chat
      prompts.

### 5.3 Apply as a Direct Advertiser

Request API access as a Direct Advertiser in the Amazon Ads Partner
Network / API Applications area, because the application manages Grace
One's own SAFAR advertising, not an agency service.

**Suggested use-case description:**

> We are a direct advertiser selling our own branded products on Amazon
> India. We are developing an internal advertising management
> application to create, monitor and optimise Sponsored Products
> campaigns for our own advertiser account. The application will
> retrieve campaign performance metrics and manage campaigns, budgets,
> bids, targeting, keywords and negative targeting within predefined
> spending and profitability controls. It will not provide advertising
> management services to third-party advertisers.

### 5.4 Assign API access after approval
- [ ] Wait for Amazon Ads approval of the API application.
- [ ] Use the approval flow/link to assign approved API access to the
      LwA application created earlier.
- [ ] Confirm the application is the intended internal SAFAR/Grace One
      tool before completing assignment.

## 6. Phase 2 — Authentication and Technical Foundation

### 6.1 Complete OAuth authorisation
- [ ] Create the Amazon authorisation grant/consent flow for the
      business account that manages SAFAR advertising.
- [ ] Exchange the authorisation result for access credentials per
      Amazon's LwA/OAuth flow.
- [ ] Store the refresh token and client secret in a server-side secret
      store or environment-managed vault.
- [ ] Generate short-lived access tokens only when required.
- [ ] Do not log secrets or return them to the agent as ordinary text.

### 6.2 Retrieve and lock the India advertiser profile
- [ ] Call the Amazon Ads Profiles resource after authentication.
- [ ] Identify the correct India advertiser profile for the SAFAR
      advertising account.
- [ ] Store the profile ID in configuration and validate it before
      every write action.
- [ ] Prevent the agent from choosing an arbitrary advertiser profile.

### 6.3 Build a thin Amazon Ads API client

| Function | Purpose | Write permission at first |
|---|---|---|
| get_profiles | Confirm advertiser profile and marketplace | Read-only |
| get_campaigns | Read campaign configuration and status | Read-only |
| get_performance | Read impressions, clicks, spend, orders, sales, CPC, ACoS/ROAS inputs | Read-only |
| get_search_terms | Read actual customer search terms where reporting supports it | Read-only |
| create_campaign | Create Sponsored Products campaign | Approval-gated |
| create_ad_group | Create campaign structure | Approval-gated |
| add_product_ad | Attach SAFAR ASIN/SKU to ad group | Approval-gated |
| add_keyword_or_target | Create keyword/product/auto target | Approval-gated |
| set_bid | Change CPC bid | Bounded automation later |
| set_budget | Change daily budget | Strictly bounded; total cap enforced in code |
| add_negative | Prevent irrelevant traffic | Bounded automation later |
| pause_target_or_campaign | Stop waste or emergency pause | Bounded automation later |

### 6.4 Engineering safeguards
- [ ] Idempotency: the same agent instruction must not accidentally
      create duplicate campaigns or repeat a budget change.
- [ ] Rate-limit handling and retries: respect Amazon API limits, safe
      backoff.
- [ ] Audit log: record every read, recommendation, write request,
      Amazon response, old value, new value and approval decision.
- [ ] Environment separation: test/dry-run mode before production
      writes.
- [ ] Kill switch: one owner-controlled setting disables all write
      calls immediately.
- [ ] Secret isolation: the agent calls tools but never receives raw
      secrets.

## 7. Phase 3 — Build the SAFAR Ads Agent and SKILL.md

### 7.1 What SKILL.md should contain
- [ ] Purpose and scope: manage only SAFAR Amazon advertising for the
      authorised account.
- [ ] Product facts: 10 ml, dual-use hang + vent clip, five fragrances,
      "up to 45 days".
- [ ] Commercial constants: launch price, conservative cost, profit
      floor, approved daily/monthly limits.
- [ ] Campaign naming convention and structure.
- [ ] Metrics to monitor: impressions, clicks, CPC, spend, orders,
      attributed sales, cost/order, conversion rate, ACoS/ROAS, and
      calculated contribution profit.
- [ ] Decision rules: when to maintain, reduce, scale, pause, add
      negatives or harvest winners.
- [ ] Minimum-data rules: avoid overreacting to one or two clicks or one
      day of noisy data.
- [ ] Approval rules: automatic, approval-gated, or prohibited actions.
- [ ] Daily report format and exception reporting.
- [ ] Escalation rules for API errors, spend anomalies, out-of-stock
      listings, suppressed ASINs or profit deterioration.

### 7.2 What SKILL.md must NOT contain
- [ ] Amazon Client Secret.
- [ ] Refresh tokens or access tokens.
- [ ] Bank/payment information.
- [ ] Any instruction allowing the agent to bypass backend spending
      caps.
- [ ] Unsupported product claims or competitor claims presented as
      facts.

### 7.3 Recommended permission levels

| Level | Agent authority | When to use |
|---|---|---|
| 0 — Read only | Read campaigns/reports and produce recommendations; no write calls. | First integration and validation. |
| 1 — Controlled writes | Small bid changes, negatives, pausing obvious waste, bounded reallocations within a hard total cap. | After recommendations have been checked against actual outcomes. |
| 2 — Semi-autonomous | Create/modify campaigns and redistribute budgets within strict encoded limits; major changes require owner approval. | After several weeks of reliable operation. |
| 3 — Broad autonomy | Not recommended for initial SAFAR launch. | Only after strong monitoring, testing and owner confidence. |

## 8. Phase 4 — Encode Financial Guardrails

### 8.1 Profit formula

**Net contribution per completed order** = Selling price − physical
product/dispatch cost − Amazon variable charges − fulfilment/shipping −
advertising spend allocated to that order − coupons/promotions −
return/refund allowance − other variable selling costs.

### 8.2 Launch economics at Rs.299 using the conservative Rs.75 physical cost

| Ad cost/order | Amount left after Rs.75 physical cost and ads | Max remaining cost if Rs.70 profit must still be kept |
|---|---|---|
| Rs.60 | Rs.164 | Rs.94 |
| Rs.75 | Rs.149 | Rs.79 |
| Rs.90 | Rs.134 | Rs.64 |

This is why the exact Amazon fee and fulfilment preview matters. If
non-ad variable charges exceed these envelopes, either the price, ad
target, fulfilment method, or temporary profit expectation must change.

### 8.3 Hard-coded safety controls
- [ ] MAX_TOTAL_DAILY_BUDGET = Rs.400 during the initial launch unless
      the owner explicitly approves a change.
- [ ] MAX_MONTHLY_AD_SPEND = explicit monthly value derived from the
      daily cap and owner decision.
- [ ] MAX_SINGLE_BID_CHANGE_PCT = 10%-15% per optimisation cycle unless
      owner-approved.
- [ ] MAX_CAMPAIGN_BUDGET_CHANGE_PCT = bounded per cycle.
- [ ] Do not permit price changes through the Ads agent.
- [ ] Do not allow the agent to alter payment, bank, tax, account
      ownership or developer credentials.
- [ ] If API data is incomplete, delayed or inconsistent, default to no
      increase in spend.

## 9. Phase 5 — Programmatically Create the Launch Campaigns

| Campaign | Initial role | Working launch budget |
|---|---|---|
| SAFAR_AUTO_DISCOVERY | Automatic targeting to discover relevant customer searches and product contexts. | Rs.150/day |
| SAFAR_MANUAL_RESEARCH | High-intent manual keyword testing using carefully selected phrase/exact targets. | Rs.150/day |
| SAFAR_EXACT_WINNERS | Proven search terms moved into tightly controlled exact targeting. Can begin small/empty and receive winners. | Rs.100/day |

**Total initial ceiling:** Rs.400/day across all campaigns combined. The
backend must reject any update that would make the configured total
exceed the hard cap.

### 9.1 Starting campaign rules
- [ ] Use Sponsored Products first — the objective is product-detail-page
      traffic and sales.
- [ ] Conservative bidding during learning; no aggressive placement
      multipliers or automatic budget expansion on day one.
- [ ] Begin with a manageable set of highly relevant keywords rather
      than hundreds of broad terms.
- [ ] Separate discovery from proven exact winners so budget moves
      toward evidence rather than intuition.
- [ ] Clear naming that includes marketplace, fragrance (where
      separated), targeting type and lifecycle stage.

### 9.2 Suggested first keyword themes

| Theme | Examples to test — final list should be data-led |
|---|---|
| Core category | car perfume; car air freshener; car freshener; car fragrance |
| Format/use | hanging car perfume; AC vent car perfume; vent clip car freshener; 2 in 1 car freshener |
| Value/quality | premium car perfume; luxury car fragrance; long lasting car freshener |
| Size | 10 ml car perfume |
| Fragrance-specific | musk car perfume; sandalwood car perfume; lavender car freshener; vanilla car perfume; jasmine car perfume |

## 10. Phase 6 — Agent Optimisation Logic

### 10.1 Working traffic-light rules

| Observed ad cost/order | Interpretation | Default action |
|---|---|---|
| Below Rs.60 | Excellent relative to the working acquisition target. | Maintain; consider a small increase only after adequate data and if profit remains acceptable. |
| Rs.60-Rs.90 | Target launch range. | Maintain; optimise search terms and conversion. |
| Rs.90-Rs.110 | Above preferred range. | Reduce bids selectively; investigate conversion, relevance and listing quality. |
| Above Rs.110 | Potentially wasteful at a Rs.299 launch price. | Reduce/pause after sufficient evidence; do not keep increasing spend blindly. |

### 10.2 Search-term harvesting
- [ ] Identify search terms that generate multiple profitable orders.
- [ ] Move strong search terms into exact-target campaigns so bids and
      budget can be controlled directly.
- [ ] Add suitable negatives to discovery campaigns to reduce internal
      competition and waste, where structure allows.
- [ ] Identify irrelevant/repeatedly non-converting searches and add
      negative targeting only after enough evidence.
- [ ] Retain a discovery campaign at a smaller budget so the system
      keeps finding new terms.

### 10.3 Fragrance-level allocation

The agent should not force equal budget across all five fragrances. If
Musk or Sandalwood converts materially better than another fragrance,
budget should gradually move toward the stronger SKU while preserving
enough discovery spend to avoid prematurely abandoning the others.

### 10.4 Minimum-data rule

Do not overreact: a target should not be paused merely because it had
one or two clicks without a sale. Require a minimum amount of
spend/click evidence, consider attribution/reporting delay, and compare
performance over a sensible lookback window before a strong action.

## 11. Phase 7 — Safe Launch Sequence

1. Run all API calls in read-only mode and confirm the correct India
   profile, ASINs, campaigns and currency.
2. Create a dry-run plan that shows exactly what campaigns, ad groups,
   budgets, bids and targets would be created without sending writes.
3. Owner reviews the dry-run plan.
4. Create campaigns programmatically with conservative budgets and keep
   them paused initially.
5. Read back the campaign configuration from Amazon and compare it to
   the intended configuration.
6. Enable campaigns in a controlled window.
7. Monitor the first 24-72 hours closely for spend anomalies, listing
   issues and irrelevant traffic.
8. Keep the agent in read-only/recommendation mode during the first
   evidence-gathering period.
9. Enable bounded writes only after recommendations have been manually
   checked.

### 11.1 Daily launch report

| Metric / section | What the owner should see |
|---|---|
| Spend | Total and by campaign/fragrance. |
| Sales/orders | Ad-attributed orders and sales, plus organic sales where separately available. |
| Cost/order | Spend divided by attributed completed orders. |
| CPC | Average cost per click. |
| Conversion rate | Orders divided by clicks. |
| ACoS / ROAS | Advertising efficiency, interpreted alongside real profit. |
| Estimated contribution | Selling price less all known variable costs. |
| Actions taken | Every bid/budget/negative/pause action and reason. |
| Exceptions | Out-of-stock, listing suppression, report delays, API errors or spend anomalies. |

## 12. Phase 8 — Scaling Rules
- [ ] Increase spend only when conversion, cost/order and contribution
      profit remain acceptable across a meaningful sample.
- [ ] Increase budgets gradually rather than doubling them abruptly.
- [ ] Prioritise exact winners and high-converting fragrances before
      expanding generic discovery spend.
- [ ] Test price movement from Rs.299 upward only after review/rating
      strength and conversion are established, measuring the effect on
      conversion rather than assuming a higher price always improves
      profit.
- [ ] Introduce 2-pack, 3-pack and fragrance-collection offers only
      after fulfilment economics and listing structure are calculated
      separately.
- [ ] Use organic ranking and branded search growth as secondary
      indicators, but continue to manage advertising on true profit.

### 12.1 When to raise the overall Rs.400/day cap

**Owner approval required:** the initial total daily cap should only be
increased after the owner sees a period of stable conversion, acceptable
contribution profit, sufficient inventory, no material return problem,
and no unexplained reporting/attribution issue. The agent can recommend
a new cap but should not approve it itself.

## 13. Risks, Failure Modes and Controls

| Risk | Why it matters | Control |
|---|---|---|
| Identity verification failure | Can delay developer/API onboarding. | Resolve legal-name/ID issue carefully; avoid wasting remaining attempts; use Developer Support if needed. |
| GTIN/ASIN delay | No product to advertise. | Complete GS1/GTIN and listing work in parallel with developer onboarding. |
| Wrong advertiser profile | Could read or modify the wrong account. | Hard-code/allow-list the India SAFAR profile ID after manual verification. |
| Credential leakage | Could expose advertising account access. | Server-side secret storage; never expose raw tokens to the agent or skill. |
| Runaway budget | AI or logic bug could overspend. | Hard backend cap, kill switch, bounded changes and owner approval. |
| Duplicate writes | Retries could create duplicate campaigns/keywords. | Idempotency keys/state checks before writes. |
| Noisy early data | Premature pausing/scaling can harm learning. | Minimum-data and lookback-window rules. |
| Attribution/report delay | Today's results may be incomplete. | Use conservative decisions when data is incomplete; avoid instant large reactions. |
| Unsupported claims | Can create policy or trust problems. | Use "up to 45 days" only and keep listing claims evidence-based. |
| Out of stock | Paid traffic cannot convert and ranking momentum can be lost. | Inventory check before campaign launch and before scale increases. |
| Revenue without profit | High sales can hide weak economics. | Calculate contribution profit per order/channel and use it as the primary guardrail. |

## 14. Parallel Workstreams While API Access Is Pending

The identity-verification issue does not mean the whole project must
stop. Work can continue in parallel so the launch is not delayed once
API access becomes available.

| Workstream | Can proceed now? | Next deliverable |
|---|---|---|
| GS1 / GTIN | Yes | Five unique fragrance GTINs. |
| Amazon listings | Partially | Prepare content now; publish when GTINs are ready. |
| Product images | Yes | Final compliant image set showing actual product and dual-use feature. |
| Cost/fee model | Yes | Amazon profit calculator using actual package weight/dimensions and fulfilment method. |
| Campaign design | Yes | Final campaign names, seed keywords, bids and caps ready for API creation. |
| SKILL.md drafting | Yes | Draft skill without credentials; finalise constants after fee model. |
| API client code | Yes, with mocks | Build tool interfaces and dry-run behaviour before credentials exist. |
| Developer/API authorisation | Limited | Resolve verification and then complete LwA/API onboarding. |
| Live campaign writes | No | Requires live ASINs, API access and approved authentication. |

## 15. One-Step-at-a-Time Master Checklist

**A. Seller & product readiness**
- [x] Amazon Seller Central India account ready.
- [x] Amazon Campaign Manager accessible.
- [x] Business developer/API email selected: hello@graceone.in.
- [ ] Obtain five GTINs.
- [ ] Create five SAFAR listings/ASINs.
- [ ] Confirm each listing is active/buyable.
- [ ] Complete listing images, title, bullets and search terms.
- [ ] Lock actual packed weight, dimensions and fulfilment method.
- [ ] Run exact Amazon fee preview at Rs.299 and confirm allowed ad
      CPA/profit.

**B. Developer & Ads API access**
- [ ] Resolve Amazon Developer identity verification.
- [ ] Create LwA/security profile for SAFAR Ads Manager.
- [ ] Store Client ID/Secret securely.
- [ ] Apply for Amazon Ads API access as Direct Advertiser.
- [ ] Receive approval.
- [ ] Assign API access to the LwA application.
- [ ] Complete OAuth authorisation.
- [ ] Retrieve and verify the Amazon India advertiser profile ID.

**C. Software foundation**
- [x] Build read-only Amazon Ads API client. *(dry-run/mock — see README status table)*
- [ ] Validate campaign/report data against live Amazon responses.
- [x] Add write functions with backend validation.
- [x] Implement hard Rs.400/day launch cap.
- [x] Implement bid-change limit and approval gates.
- [x] Implement audit log, idempotency and kill switch. *(rate-limit/retry handling still open)*

**D. Agent & skill**
- [x] Create SAFAR Ads SKILL.md.
- [ ] Create agent with Amazon Ads functions as tools.
- [ ] Run in recommendation-only mode.
- [ ] Compare agent recommendations with manual decisions.
- [ ] Enable bounded low-risk write actions.

**E. Launch**
- [ ] Programmatically create Auto Discovery campaign. *(dry-run plan ready — `python -m safar_ads.cli plan`)*
- [ ] Programmatically create Manual Research campaign.
- [ ] Programmatically create Exact Winners campaign.
- [ ] Read back and verify all campaign settings.
- [ ] Enable campaigns with total daily cap <= Rs.400.
- [ ] Monitor first 24-72 hours closely.
- [ ] Start keyword harvesting and negative-target control.
- [ ] Scale only after profitability is demonstrated.

## 16. Immediate Next Actions

| Priority | Action | Why |
|---|---|---|
| 1 | Resolve or support-escalate the Amazon Developer identity verification failure before using more attempts casually. | API onboarding should not depend on a developer account in a failed verification state. |
| 2 | Obtain five GTINs and create the five SAFAR ASINs. | The advertising system ultimately needs live products to advertise. |
| 3 | Measure final packed weight and package dimensions and select the fulfilment method. | This allows the real Rs.299 profit envelope to be calculated. |
| 4 | Create the final Amazon listing content and dual-use product images. | Conversion quality directly affects advertising cost per order. |
| 5 | Draft the SAFAR Ads SKILL.md and API tool schemas in dry-run mode. | This work can proceed before live credentials are ready. |

## 17. Definition of Done
- [ ] Five SAFAR ASINs are live, accurate, in stock and ready to advertise.
- [ ] Amazon Ads API access is approved and securely authenticated for
      the correct India advertiser profile.
- [x] The application can create/read/update Sponsored Products
      campaigns through validated API tools. *(dry-run only until live credentials exist)*
- [x] The agent can read performance and calculate business contribution
      profit using configured costs.
- [x] SKILL.md contains the operating strategy and no secrets.
- [x] Hard spend and bid-change limits are enforced by backend code and
      cannot be overridden by the agent.
- [x] Every write action is logged and can be traced to a reason/approval.
- [ ] The first campaigns are created programmatically and operate
      within the approved budget. *(blocked on live API access)*
- [ ] Owner receives a daily report with spend, orders, cost/order,
      profitability, actions and exceptions. *(report generator not yet built — see "Open items" below)*
- [ ] Scaling occurs only after the actual economics demonstrate that
      higher spend remains profitable.

## 18. Official References

- Amazon Ads API onboarding overview: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/overview
- Amazon Ads — Create a Login with Amazon application: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/create-lwa-app
- Amazon Ads — Apply for API access: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/apply-for-access
- Amazon Ads — Assign API access to LwA application: https://advertising.amazon.com/API/docs/en-us/guides/onboarding/assign-api-access
- Amazon Ads API getting started: https://advertising.amazon.com/API/docs/en-us/guides/get-started/overview
- Amazon Ads API authorization overview: https://advertising.amazon.com/API/docs/en-us/guides/account-management/authorization/overview
- Amazon Sponsored Products: https://advertising.amazon.com/solutions/products/sponsored-products
- Amazon Ads — Sponsored Products auto campaigns: https://advertising.amazon.com/API/docs/en-us/guides/sponsored-products/get-started/auto-campaigns
- Amazon Ads — Sponsored Products keyword targeting: https://advertising.amazon.com/API/docs/en-us/guides/sponsored-products/keywords/overview
- Amazon Developer — Identity verification: https://developer.amazon.com/docs/app-submission/identity-verification.html
- OpenAI API — Function calling: https://developers.openai.com/api/docs/guides/function-calling
- OpenAI API — Agents SDK: https://developers.openai.com/api/docs/guides/agents
- OpenAI API — Skills: https://developers.openai.com/api/docs/guides/tools-skills

**Implementation note:** This is a project/engineering plan, not a
guarantee of Amazon Ads API approval, ad performance, ranking, sales, or
profit. Final campaign economics must use the actual Amazon fee preview,
fulfilment method, package dimensions/weight, taxes, returns and live
CPC/conversion data.
