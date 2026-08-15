# Step 3: Create the "SAFAR Ads Manager" security profile / Login with Amazon app

This is a manual, browser-only step — nobody can do it programmatically on
your behalf, including this repo's code. Amazon's official sequence is:
create a Login with Amazon (LwA) security profile → apply for Ads API
access → assign the approved access to that LwA profile
(see `18. Official References` in the plan document).

Work through this checklist in the Amazon Developer Console. Screenshot
each step if you want a second pair of eyes before submitting anything.

## Before you start

- [ ] Confirm which Amazon Developer account you're in (the one
      registered with `hello@graceone.in`).
- [ ] Do **not** treat this step as separate from identity verification —
      if the console still shows "Account Identity Verification Failed"
      in the area you need, note exactly which sections are blocked vs.
      still accessible. Amazon sometimes restricts only *some* developer
      capabilities (e.g. app submission) while still allowing security
      profile creation. Confirm rather than assume.

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
1. Whether "Login with Amazon" was fully accessible or partially
   blocked by the identity-verification issue.
2. Confirmation the security profile was created (name is enough — not
   the Client ID/Secret).
3. Any error messages Amazon showed, verbatim.

That tells us exactly where the verification failure does and doesn't
block progress, and whether Phase 1 can continue or needs Developer
Support first.
