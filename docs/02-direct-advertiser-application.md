# Direct Advertiser API application wording

Use this once the "SAFAR Ads Manager" LwA security profile exists
(`docs/01-security-profile-setup.md`).

## Confirmed process, 15 Aug 2026 (from Amazon's current Advanced Tools
## Center docs — Onboarding → 2. Apply for API access)

The application form is **not** in the regular Ads console (confirmed
by exhaustively checking Administration, Tools & resources, and the
full "All tools" mega-menu — nothing there). It lives in Amazon's
developer documentation site instead, under Advanced Tools Center →
Developer guides → Onboarding → "2. Apply for API access." Two
categories are offered there:

- **Partner** — agencies/software providers managing *other*
  advertisers' accounts, via the Amazon Ads Partner Network. **Not us**
  — this is the "Partner Network / API Applications" language the
  original implementation plan used, and it does not apply to a Direct
  Advertiser managing its own account.
- **Direct Advertiser** — Grace One's actual category. Reach it via
  either "Apply for API access as a Direct Advertiser" (direct link on
  that docs page) or the Amazon Ads API web page → "Request API
  Access" → choose **Direct Advertiser**.

### Which Amazon account to log in with — corrected, again, 15 Aug 2026

**There is only one real Amazon account in this entire setup:
`graceragheshwari@gmail.com`.** This doc previously went back and forth
on this and got it wrong twice, so here's the settled fact, confirmed
by direct test:

- `graceragheshwari@gmail.com` is a real Amazon login. It's the account
  behind Seller Central, the Grace One Ads advertiser registration, and
  — it turns out — the Developer Console session that created the
  "SAFAR Ads Manager" LwA security profile too. One account, used
  everywhere.
- `hello@graceone.in` is **not** a real Amazon account. Attempting to
  sign in with it fails with "We cannot find an account with that
  e-mail address." It only ever appeared as *text typed into form
  fields* — the security profile's business contact details, and the
  suggested contact email below — never as an actual login. Keep using
  it that way (a contact address on forms), never as a sign-in.

So: Amazon's instruction to "log in with the same email used to create
the Developer account" is satisfied by `graceragheshwari@gmail.com`,
because that's the account that was actually authenticated when the
security profile was created — `hello@graceone.in` was never a
separate login to begin with. Sign in with
`graceragheshwari@gmail.com` for this application.

**Still true and still important:** per Amazon's docs, *"Your LwA
developer registration will be associated to your Amazon Ads API
permissions in the next step of the process. This association cannot
be changed once it is set."* — so get the account right before
submitting, which is now confirmed as `graceragheshwari@gmail.com`.

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

- [ ] Company/business name: **Grace One** (or the legal name
      `Grace Ragheshwari` if the field asks for the GST legal name
      specifically — match whichever the field is actually asking for,
      as with the Ads advertiser account registration).
- [ ] Brand: **SAFAR**
- [ ] Contact email: `hello@graceone.in` is fine as the *business*
      contact address typed into the form, even though you're logged in
      as `graceragheshwari@gmail.com` — those don't have to match.
- [ ] Marketplace(s): **Amazon.in (India)**
- [ ] Ad product(s): **Sponsored Products**
- [ ] LwA Client ID (from `docs/01-security-profile-setup.md`) — do
      **not** paste the Client Secret into any application form field
      that isn't the designated secret field, and never into a support
      ticket or chat.

## Submitted — 15 Aug 2026

- [x] Application form completed and submitted for review, logged in as
      `graceragheshwari@gmail.com`.
- [x] Confirmation shown on-screen: *"Thank you, your Amazon Ads API
      request has been successfully submitted. Expect a follow up email
      in 72 hours regarding next steps."* (Amazon's own docs page said
      "up to 1 business day" elsewhere — go with the on-screen figure,
      72 hours, as the real expectation; ~mid-day 18 Aug 2026.)
- [ ] Watch `graceragheshwari@gmail.com` for Amazon's decision email.
- [ ] **Read "Assign API access to your LwA application" in full before
      clicking any link in that status email** — the LwA-to-permissions
      association it describes is permanent once set. Assign it to the
      "SAFAR Ads Manager" profile specifically, not any other client if
      more than one exists.
- [ ] Only after assignment is confirmed do Phase 2 (OAuth) and populate
      `.env` from `.env.example`.

## While waiting on the 72-hour review

Good parallel work, none of it blocked by this pending application:

- [ ] Retrieve the "SAFAR Ads Manager" Client Secret from Web Settings
      and store it securely — see `docs/01-security-profile-setup.md`.
      Needed the moment OAuth (Phase 2) becomes possible.
- [ ] Invite `hello@graceone.in` as an Admin user via Seller Central →
      User Permissions, so business-critical Amazon access isn't tied
      to one person's personal Gmail long-term. Doesn't touch anything
      already built; purely additive.
- [ ] GTIN/ASIN and listing work (Phase 0) — see the plan's Phase 14
      "Parallel Workstreams" table.
