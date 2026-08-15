# Direct Advertiser API application wording

Use this once the "SAFAR Ads Manager" LwA security profile exists
(`docs/01-security-profile-setup.md`). Submit in the Amazon Ads Partner
Network / API Applications area, applying as a **Direct Advertiser** —
Grace One is managing its own SAFAR advertising, not offering an agency
service to other advertisers.

## Which Amazon account to log in with

**Confirmed, 15 Aug 2026:** two separate Amazon accounts are involved,
and they stay separate on purpose:

- `hello@graceone.in` — Developer Console account. Already used to
  create the "SAFAR Ads Manager" LwA security profile
  (`docs/01-security-profile-setup.md`). Not needed again until you
  manage that security profile's settings.
- `graceragheshwari@gmail.com` — Advertising Console / Seller Central /
  Campaign Manager account. This is the account that actually owns the
  SAFAR advertiser profile and campaign data. **Log into
  advertising.amazon.com with this account** to submit the application
  below — the request needs to be tied to the account whose data the
  API will access.

Later (Phase 5.4 → 6.1), after Amazon approves the application, you'll
log back in as `graceragheshwari@gmail.com` to authorize the "SAFAR Ads
Manager" app (identified by its LwA Client ID from the other account)
to access this advertiser's campaigns via the OAuth consent screen.
That's the step that actually links the two accounts together.

## Application type

**Direct Advertiser** (not Agency / Software Partner). Grace One only
manages its own SAFAR advertiser account.

## Use-case description (ready to paste)

> We are a direct advertiser selling our own branded products on Amazon
> India. We are developing an internal advertising management
> application to create, monitor and optimise Sponsored Products
> campaigns for our own advertiser account. The application will
> retrieve campaign performance metrics and manage campaigns, budgets,
> bids, targeting, keywords and negative targeting within predefined
> spending and profitability controls. It will not provide advertising
> management services to third-party advertisers.

## If Amazon asks for more detail, expand with

> The application (internally named "SAFAR Ads Manager") will operate
> under hard-coded financial guardrails maintained outside of any AI or
> automated decision layer: a maximum total daily budget, bounded
> per-cycle bid and budget change limits, and an owner-controlled kill
> switch that can immediately disable all write access. All API write
> actions are logged with the before/after value and the reason for the
> change. The application manages Sponsored Products campaigns
> exclusively for Grace One's own SAFAR-branded ASINs on the Amazon.in
> marketplace.

## Fields to have ready

- [ ] Company/business name: **Grace One**
- [ ] Brand: **SAFAR**
- [ ] Contact email: `hello@graceone.in` is fine as the *business*
      contact address on the form even though you're logged in as
      `graceragheshwari@gmail.com` — those don't have to match.
- [ ] Marketplace(s): **Amazon.in (India)**
- [ ] Ad product(s): **Sponsored Products**
- [ ] LwA Client ID (from `docs/01-security-profile-setup.md`) — do
      **not** paste the Client Secret into any application form field
      that isn't the designated secret field, and never into a support
      ticket or chat.

## After submitting

- [ ] Note the submission date — Amazon's approval timeline varies;
      don't resubmit duplicate applications while one is pending.
- [ ] Once approved, follow the "assign API access to the LwA
      application" flow (Phase 5.4 of the plan) and confirm you're
      assigning to the correct "SAFAR Ads Manager" profile, not a
      different one if you have multiple.
- [ ] Only after assignment is confirmed do Phase 2 (OAuth) and populate
      `.env` from `.env.example`.
