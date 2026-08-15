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

### Which Amazon account to log in with — corrected

**Important correction to earlier guidance in this repo:** an earlier
version of this doc said to log in as `graceragheshwari@gmail.com`
(the Ads/Seller Central account) to submit this application. That was
wrong. Amazon's own instructions are explicit:

> You must log in with the same email address that was used to create
> the Amazon Developer account in step 1.

That's **`hello@graceone.in`** — the Developer Console account that
holds the "SAFAR Ads Manager" LwA security profile. If any other Amazon
account is already logged into the browser, Amazon auto-redirects using
*that* session — check the account shown top-right before applying;
log out and back in as `hello@graceone.in` if it's wrong.

**Do not skip this.** Per the same docs page: *"Your LwA developer
registration will be associated to your Amazon Ads API permissions in
the next step of the process. This association cannot be changed once
it is set."* Applying under the wrong account risks permanently tying
API permissions to an account that doesn't hold the LwA client you
need.

`graceragheshwari@gmail.com` (Ads/Seller Central) comes back into play
later — at OAuth time (Phase 2), when that account authorizes the
"SAFAR Ads Manager" app to actually access its campaign data. That's a
separate step from this application.

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

## After submitting (per Amazon's docs)

- [ ] Complete the application form, click **Submit for review**.
- [ ] A confirmation email arrives at the address used to log in
      (`hello@graceone.in`).
- [ ] Review takes **up to 1 business day**. An email follows with the
      application status either way — approved, or (if not) information
      on how to resolve the issue.
- [ ] **Read "Assign API access to your LwA application" before
      clicking any link in that status email** — the LwA-to-permissions
      association it describes is permanent once set. Assign it to the
      "SAFAR Ads Manager" profile specifically.
- [ ] Only after assignment is confirmed do Phase 2 (OAuth) and populate
      `.env` from `.env.example`.
