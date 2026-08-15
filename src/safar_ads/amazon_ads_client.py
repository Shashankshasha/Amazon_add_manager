"""Thin Amazon Ads API client (Phase 2.3 of the implementation plan).

Two modes:

- dry_run=True (default, and the ONLY mode usable today): no network calls
  are made. Read methods return structured mock data; write methods run
  through SafetyMiddleware and return a simulated response describing
  exactly what WOULD have been sent. This is what powers `safar_ads.cli`
  dry-run plans while Amazon Developer identity verification is unresolved.

- dry_run=False: performs real HTTP calls. This requires
  AMAZON_ADS_CLIENT_ID / _SECRET / _REFRESH_TOKEN / _PROFILE_ID to be set
  (Phase 1/2 of the plan) and SAFAR_ADS_KILL_SWITCH=false. Endpoint paths
  below follow the Amazon Ads API v3 Sponsored Products resources as of
  this plan's reference docs - re-verify exact paths/content-types against
  https://advertising.amazon.com/API/docs/ before the first live write.

Every write call - dry-run or live - goes through SafetyMiddleware first
and is recorded in the audit log. The agent never sees a raw secret: this
client reads credentials from the environment, not from agent input.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import requests

from safar_ads.safety import SafetyMiddleware, SafetyViolation, WriteRequest

__all__ = ["AmazonAdsClient", "AmazonAdsError", "NotAuthenticatedError", "SafetyViolation"]


class AmazonAdsError(Exception):
    """Base class for errors returned by (or about) the Amazon Ads API."""


class NotAuthenticatedError(AmazonAdsError):
    """Raised when a live (non-dry-run) call is attempted without full
    Login with Amazon credentials - i.e. before Phase 1/2 are complete."""


def _env_true(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


class AmazonAdsClient:
    def __init__(
        self,
        *,
        dry_run: bool = True,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        profile_id: str | None = None,
        api_base_url: str = "https://advertising-api-eu.amazon.com",
        lwa_token_url: str = "https://api.amazon.com/auth/o2/token",
        safety: SafetyMiddleware | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.dry_run = dry_run
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.profile_id = profile_id
        self.api_base_url = api_base_url.rstrip("/")
        self.lwa_token_url = lwa_token_url
        self.safety = safety or SafetyMiddleware(kill_switch=not dry_run and True)
        self.session = session or requests.Session()
        self._access_token: str | None = None
        self._access_token_expires_at: float = 0.0

    @classmethod
    def from_env(cls) -> "AmazonAdsClient":
        dry_run = _env_true("SAFAR_ADS_DRY_RUN", True)
        kill_switch = _env_true("SAFAR_ADS_KILL_SWITCH", True)
        client = cls(
            dry_run=dry_run,
            client_id=os.environ.get("AMAZON_ADS_CLIENT_ID") or None,
            client_secret=os.environ.get("AMAZON_ADS_CLIENT_SECRET") or None,
            refresh_token=os.environ.get("AMAZON_ADS_REFRESH_TOKEN") or None,
            profile_id=os.environ.get("AMAZON_ADS_PROFILE_ID") or None,
            api_base_url=os.environ.get("AMAZON_ADS_API_BASE_URL", "https://advertising-api-eu.amazon.com"),
            lwa_token_url=os.environ.get("AMAZON_LWA_TOKEN_URL", "https://api.amazon.com/auth/o2/token"),
            safety=SafetyMiddleware(kill_switch=kill_switch),
        )
        return client

    # -- authentication -------------------------------------------------

    def _ensure_configured_for_live_calls(self) -> None:
        missing = [
            name
            for name, val in (
                ("AMAZON_ADS_CLIENT_ID", self.client_id),
                ("AMAZON_ADS_CLIENT_SECRET", self.client_secret),
                ("AMAZON_ADS_REFRESH_TOKEN", self.refresh_token),
                ("AMAZON_ADS_PROFILE_ID", self.profile_id),
            )
            if not val
        ]
        if missing:
            raise NotAuthenticatedError(
                "Cannot make a live Amazon Ads API call - missing: "
                f"{', '.join(missing)}. Complete Phase 1 (LwA app + Direct "
                "Advertiser approval) and Phase 2 (OAuth) first, or keep "
                "dry_run=True."
            )

    def _get_access_token(self) -> str:
        self._ensure_configured_for_live_calls()
        if self._access_token and time.time() < self._access_token_expires_at - 60:
            return self._access_token
        resp = self.session.post(
            self.lwa_token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=30,
        )
        resp.raise_for_status()
        payload = resp.json()
        self._access_token = payload["access_token"]
        self._access_token_expires_at = time.time() + payload.get("expires_in", 3600)
        return self._access_token

    def _headers(self, *, content_type: str | None = None) -> dict[str, str]:
        headers = {
            "Amazon-Advertising-API-ClientId": self.client_id or "",
            "Authorization": f"Bearer {self._get_access_token()}",
            "Amazon-Advertising-API-Scope": self.profile_id or "",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        self._ensure_configured_for_live_calls()
        url = f"{self.api_base_url}{path}"
        resp = self.session.request(method, url, headers=self._headers(), timeout=30, **kwargs)
        if not resp.ok:
            raise AmazonAdsError(f"{method} {path} -> {resp.status_code}: {resp.text}")
        return resp.json() if resp.content else None

    # -- read-only methods ------------------------------------------------

    def get_profiles(self) -> list[dict]:
        if self.dry_run:
            return [
                {
                    "profileId": "MOCK-IN-PROFILE-0001",
                    "countryCode": "IN",
                    "currencyCode": "INR",
                    "accountInfo": {"marketplaceStringId": "A21TJRUUN4KGV", "type": "seller"},
                }
            ]
        return self._request("GET", "/v2/profiles")

    def get_campaigns(self) -> list[dict]:
        if self.dry_run:
            from safar_ads.config import load_campaign_plan

            plan = load_campaign_plan()
            return [
                {
                    "campaignId": f"MOCK-{c['name']}",
                    "name": c["name"],
                    "state": c["state"],
                    "dailyBudget": c["daily_budget_inr"],
                    "targetingType": c["targeting_type"],
                }
                for c in plan["campaigns"]
            ]
        return self._request("GET", "/sp/campaigns/list", json={})

    def get_performance(self, *, start_date: str, end_date: str) -> dict:
        if self.dry_run:
            return {
                "startDate": start_date,
                "endDate": end_date,
                "note": "MOCK data - no live reporting connection yet.",
                "impressions": 0,
                "clicks": 0,
                "spend": 0.0,
                "orders": 0,
                "sales": 0.0,
            }
        # Amazon Ads reporting v3 is an async request/poll/download flow -
        # this stub covers only the request step; polling and report
        # download should be added once live credentials exist.
        return self._request(
            "POST",
            "/reporting/reports",
            json={"startDate": start_date, "endDate": end_date, "adProduct": "SPONSORED_PRODUCTS"},
        )

    def get_search_terms(self, *, start_date: str, end_date: str) -> dict:
        if self.dry_run:
            return {"startDate": start_date, "endDate": end_date, "searchTerms": [], "note": "MOCK - dry run"}
        return self._request(
            "POST",
            "/reporting/reports",
            json={"startDate": start_date, "endDate": end_date, "reportTypeId": "spSearchTerm"},
        )

    # -- gated write methods ------------------------------------------------
    # Every write builds a WriteRequest and validates it through
    # SafetyMiddleware BEFORE touching the network, dry-run or not.

    def _new_idempotency_key(self, action: str, name: str) -> str:
        return f"{action}:{name}:{uuid.uuid4().hex[:12]}"

    def create_campaign(
        self, *, name: str, daily_budget_inr: float, targeting_type: str,
        other_active_daily_budgets_inr: tuple[float, ...] = (),
        state: str = "paused", idempotency_key: str | None = None,
    ) -> dict:
        key = idempotency_key or self._new_idempotency_key("create_campaign", name)
        self.safety.validate_write(
            WriteRequest(
                action="create_campaign",
                idempotency_key=key,
                new_value=daily_budget_inr,
                other_active_daily_budgets_inr=other_active_daily_budgets_inr,
            )
        )
        if self.dry_run:
            return {
                "dryRun": True,
                "wouldCreate": {
                    "name": name,
                    "dailyBudget": daily_budget_inr,
                    "targetingType": targeting_type,
                    "state": state,
                },
                "idempotencyKey": key,
            }
        return self._request(
            "POST",
            "/sp/campaigns",
            json=[{"name": name, "dailyBudget": daily_budget_inr, "targetingType": targeting_type, "state": state}],
        )

    def create_ad_group(self, *, campaign_id: str, name: str, default_bid_inr: float, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or self._new_idempotency_key("create_ad_group", name)
        self.safety.validate_write(WriteRequest(action="create_ad_group", idempotency_key=key))
        if self.dry_run:
            return {"dryRun": True, "wouldCreate": {"campaignId": campaign_id, "name": name, "defaultBid": default_bid_inr}, "idempotencyKey": key}
        return self._request("POST", "/sp/adGroups", json=[{"campaignId": campaign_id, "name": name, "defaultBid": default_bid_inr, "state": "enabled"}])

    def add_product_ad(self, *, ad_group_id: str, asin: str, sku: str | None = None, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or self._new_idempotency_key("add_product_ad", asin)
        self.safety.validate_write(WriteRequest(action="add_product_ad", idempotency_key=key))
        if self.dry_run:
            return {"dryRun": True, "wouldCreate": {"adGroupId": ad_group_id, "asin": asin, "sku": sku}, "idempotencyKey": key}
        return self._request("POST", "/sp/productAds", json=[{"adGroupId": ad_group_id, "asin": asin, "sku": sku, "state": "enabled"}])

    def add_keyword_or_target(
        self, *, ad_group_id: str, match_type: str, value: str, bid_inr: float, idempotency_key: str | None = None,
    ) -> dict:
        key = idempotency_key or self._new_idempotency_key("add_keyword_or_target", value)
        self.safety.validate_write(WriteRequest(action="add_keyword_or_target", idempotency_key=key))
        if self.dry_run:
            return {
                "dryRun": True,
                "wouldCreate": {"adGroupId": ad_group_id, "matchType": match_type, "value": value, "bid": bid_inr},
                "idempotencyKey": key,
            }
        path = "/sp/targets" if match_type == "auto" else "/sp/keywords"
        return self._request("POST", path, json=[{"adGroupId": ad_group_id, "matchType": match_type, "keywordText": value, "bid": bid_inr, "state": "enabled"}])

    def set_bid(self, *, target_id: str, old_bid_inr: float, new_bid_inr: float, owner_approved: bool = False, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or self._new_idempotency_key("set_bid", target_id)
        self.safety.validate_write(
            WriteRequest(action="set_bid", idempotency_key=key, old_value=old_bid_inr, new_value=new_bid_inr, owner_approved=owner_approved)
        )
        if self.dry_run:
            return {"dryRun": True, "targetId": target_id, "oldBid": old_bid_inr, "newBid": new_bid_inr, "idempotencyKey": key}
        return self._request("PUT", "/sp/keywords", json=[{"keywordId": target_id, "bid": new_bid_inr}])

    def set_budget(
        self, *, campaign_id: str, old_budget_inr: float, new_budget_inr: float,
        other_active_daily_budgets_inr: tuple[float, ...] = (), owner_approved: bool = False,
        idempotency_key: str | None = None,
    ) -> dict:
        key = idempotency_key or self._new_idempotency_key("set_budget", campaign_id)
        self.safety.validate_write(
            WriteRequest(
                action="set_budget",
                idempotency_key=key,
                old_value=old_budget_inr,
                new_value=new_budget_inr,
                owner_approved=owner_approved,
                other_active_daily_budgets_inr=other_active_daily_budgets_inr,
            )
        )
        if self.dry_run:
            return {"dryRun": True, "campaignId": campaign_id, "oldBudget": old_budget_inr, "newBudget": new_budget_inr, "idempotencyKey": key}
        return self._request("PUT", "/sp/campaigns", json=[{"campaignId": campaign_id, "dailyBudget": new_budget_inr}])

    def add_negative(self, *, ad_group_id: str, match_type: str, value: str, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or self._new_idempotency_key("add_negative", value)
        self.safety.validate_write(WriteRequest(action="add_negative", idempotency_key=key))
        if self.dry_run:
            return {"dryRun": True, "wouldCreate": {"adGroupId": ad_group_id, "matchType": match_type, "value": value}, "idempotencyKey": key}
        return self._request("POST", "/sp/negativeKeywords", json=[{"adGroupId": ad_group_id, "matchType": match_type, "keywordText": value, "state": "enabled"}])

    def pause_target_or_campaign(self, *, entity_type: str, entity_id: str, idempotency_key: str | None = None) -> dict:
        key = idempotency_key or self._new_idempotency_key("pause", entity_id)
        self.safety.validate_write(WriteRequest(action="pause_target_or_campaign", idempotency_key=key))
        if self.dry_run:
            return {"dryRun": True, "entityType": entity_type, "entityId": entity_id, "newState": "paused", "idempotencyKey": key}
        path = {"campaign": "/sp/campaigns", "keyword": "/sp/keywords", "target": "/sp/targets"}[entity_type]
        return self._request("PUT", path, json=[{"campaignId" if entity_type == "campaign" else f"{entity_type}Id": entity_id, "state": "paused"}])
