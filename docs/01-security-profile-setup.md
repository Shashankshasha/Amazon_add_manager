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

- [x] Navigate to **Login with Amazon** → **Create a New Security
      Profile**.
- [x] Security Profile Name: `SAFAR Ads Manager`.
- [x] Security Profile Description: *"Internal application for Grace
      One to programmatically manage SAFAR's own Amazon Sponsored
      Products advertising: read performance, create and optimise
      campaigns, enforce spend guardrails."*
- [x] Consent Privacy Notice URL: `https://www.graceone.in/privacy-policy.html`
      (Grace One's real, dated privacy policy page).
- [x] **Confirmed, 15 Aug 2026:** profile created successfully —
      "Login with Amazon successfully enabled for Security Profile,"
      listed under Login with Amazon Configurations with a visible
      Client ID. This is the direct proof that the identity-verification
      failure does not block LWA/Ads API onboarding.

## Capture credentials securely

- [ ] Open the security profile (gear icon under "Manage") and go to
      **Web Settings** / **Credentials** tab.
- [ ] Copy the **Client Secret** (Client ID is already visible on the
      configurations list and isn't sensitive the same way).
- [ ] Store it in a password manager or secret vault immediately —
      **do not** paste it into chat, screenshots, SKILL.md, or any file
      that gets committed to this repo. `.env` is git-ignored for
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

Security profile creation is done. Remaining before moving on:
1. Retrieve and securely store the Client Secret (see "Capture
   credentials securely" above).
2. Then proceed to `docs/02-direct-advertiser-application.md` and
   submit the Direct Advertiser API application — the security profile
   it depends on now exists.

Identity verification is confirmed to only matter for Appstore
publishing and can stay parked indefinitely — resolving it is optional,
not a blocker for anything in this plan.
