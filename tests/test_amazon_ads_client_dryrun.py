import pytest

from safar_ads.amazon_ads_client import AmazonAdsClient, NotAuthenticatedError
from safar_ads.audit_log import AuditLog
from safar_ads.safety import IdempotencyStore, SafetyMiddleware, SafetyViolation


@pytest.fixture()
def client(tmp_path):
    safety = SafetyMiddleware(
        kill_switch=False,
        audit_log=AuditLog(path=tmp_path / "audit.jsonl"),
        idempotency_store=IdempotencyStore(path=tmp_path / "idempotency.json"),
    )
    return AmazonAdsClient(dry_run=True, safety=safety)


def test_get_profiles_returns_mock_without_network(client):
    profiles = client.get_profiles()
    assert profiles[0]["countryCode"] == "IN"


def test_get_campaigns_reflects_config(client):
    campaigns = client.get_campaigns()
    names = {c["name"] for c in campaigns}
    assert "SAFAR-IN-SP-AUTO-DISCOVERY-LAUNCH" in names
    assert "SAFAR-IN-SP-EXACT-WINNERS-LAUNCH" in names


def test_create_campaign_dry_run_does_not_touch_network(client):
    result = client.create_campaign(
        name="SAFAR-IN-SP-AUTO-DISCOVERY-LAUNCH",
        daily_budget_inr=150,
        targeting_type="auto",
        other_active_daily_budgets_inr=(150, 100),
    )
    assert result["dryRun"] is True
    assert result["wouldCreate"]["dailyBudget"] == 150


def test_create_campaign_rejected_when_it_would_breach_total_cap(client):
    with pytest.raises(SafetyViolation):
        client.create_campaign(
            name="SAFAR-IN-SP-EXTRA",
            daily_budget_inr=50,
            targeting_type="auto",
            other_active_daily_budgets_inr=(150, 150, 100),  # already at the 400 cap
        )


def test_set_bid_over_cap_without_approval_is_rejected(client):
    with pytest.raises(SafetyViolation):
        client.set_bid(target_id="t1", old_bid_inr=10, new_bid_inr=20)  # 100% change


def test_set_bid_within_cap_succeeds(client):
    result = client.set_bid(target_id="t1", old_bid_inr=10, new_bid_inr=11)
    assert result["newBid"] == 11


def test_live_call_without_credentials_raises_not_authenticated():
    live_client = AmazonAdsClient(dry_run=False)
    with pytest.raises(NotAuthenticatedError):
        live_client.get_campaigns()


def test_repeat_idempotency_key_is_rejected(client):
    client.pause_target_or_campaign(entity_type="campaign", entity_id="c1", idempotency_key="fixed-key")
    with pytest.raises(SafetyViolation, match="already used"):
        client.pause_target_or_campaign(entity_type="campaign", entity_id="c1", idempotency_key="fixed-key")
