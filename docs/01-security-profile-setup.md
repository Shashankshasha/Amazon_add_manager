# Step 3: Create the "SAFAR Ads Manager" security profile / Login with Amazon app

This is a manual, browser-only step — nobody can do it programmatically on
your behalf, including this repo's code. Amazon's official sequence is:
create a Login with Amazon (LwA) security profile → apply for Ads API
access → assign the approved access to that LwA profile
(see `18. Official References` in the plan document).

Work through this checklist in the Amazon Developer Console. Screenshot
each step if you want a second pair of eyes before submitting anything.

## Before you start

- [x] Confirm which Amazon Developer account you're in (the one
      registered with `hello@graceone.in`).
- [x] **Confirmed, 15 Aug 2026:** the actual error banner reads *"Your
      identity verification has failed. You cannot upload apps. Please
      contact us under Appstore -> Appstore Identity Verification for
      further assistance if required."* — scoped by name to Appstore
      app publishing. It appears on the Appstore "App List" screen
      specifically. Just below it, a separate green banner reads
      *"Your account review is complete."* — the Developer account
      itself passed review; only the Appstore app-upload sub-feature is
      flagged. Login with Amazon lives in a different section of the
      same console and is not shown as blocked anywhere. Proceed with
      Step 3 below; there is no remaining reason to expect it's gated by
      this error.
      Background: https://community.amazondeveloper.com/t/account-identity-verification-failed-you-cannot-upload-apps/12149

## Create the security profile

- [ ] Navigate to **Login with Amazon** (bottom-left nav, per your
      screenshot) → **Create a New Security Profile**.
- [ ] Security Profile Name: `SAFAR Ads Manager` (or `Grace One Ads
      Manager` if you prefer the parent-company name — pick one and stay
      consistent with `config/campaigns.yaml` naming going forward).
- [ ] Security Profile Description: something like — *"Internal
      application for Grace One to programmatically manage SAFAR's own
      Amazon Sponsored Products advertising: read performance, create
      and optimise campaigns, enforce spend guardrails."*
- [ ] Consent Privacy Notice URL: use a real, business-controlled URL
      (can be a simple hosted privacy note if Grace One doesn't have a
      full site yet — Amazon requires *something* reachable here).
- [ ] Business contact details: use `hello@graceone.in` and Grace One's
      real business info, not a personal placeholder.

## Capture credentials securely

- [ ] Once created, open the security profile and go to **Web
      Settings** / **Credentials** tab.
- [ ] Copy the **Client ID** and **Client Secret**.
- [ ] Store them in a password manager or secret vault immediately —
      **do not** paste them into chat, screenshots, SKILL.md, or any
      file that gets committed to this repo. `.env` is git-ignored for
      exactly this reason (see `.env.example`).
- [ ] If you ever paste a secret into a chat window by accident, rotate
      it in the Developer Console immediately — treat it as compromised.

## Set the allowed return/redirect URL (for OAuth later)

- [ ] Under **Web Settings**, add the redirect URL your OAuth flow will
      use once Phase 2 (authentication) is built — e.g.
      `https://<your-backend-domain>/oauth/amazon/callback`. A
      placeholder like `http://localhost:8000/oauth/amazon/callback` is
      fine for now if the backend isn't deployed yet; you'll need to
      update this before going live.

## What NOT to do yet

- [ ] Do not submit the Direct Advertiser API application until you've
      reviewed `docs/02-direct-advertiser-application.md` — it needs the
      security profile to exist first, per Amazon's sequence.
- [ ] Do not put real credentials in `config/*.yaml` — those files are
      committed to git and contain no secrets by design.

## After this step

Report back with:
1. Confirmation the security profile was created (name is enough — not
   the Client ID/Secret).
2. Any error messages Amazon showed, verbatim, if you hit one.

If the security profile creates cleanly (expected, per the confirmation
above), identity verification only matters for Appstore publishing and
can stay parked indefinitely — resolving it becomes optional, not a
blocker for Phase 1. Move straight on to
`docs/02-direct-advertiser-application.md`. If Step 3 itself throws a
verification error, that would be new information (verification
blocking more than Appstore uploads on this account) and worth a
Developer Support ticket at that point, not before.
