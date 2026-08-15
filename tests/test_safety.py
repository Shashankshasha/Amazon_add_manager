import pytest

from safar_ads.audit_log import AuditLog
from safar_ads.safety import IdempotencyStore, SafetyMiddleware, SafetyViolation, WriteRequest


@pytest.fixture()
def middleware(tmp_path):
    return SafetyMiddleware(
        kill_switch=False,
        audit_log=AuditLog(path=tmp_path / "audit.jsonl"),
        idempotency_store=IdempotencyStore(path=tmp_path / "idempotency.json"),
    )


def test_kill_switch_blocks_every_write(tmp_path):
    m = SafetyMiddleware(
        kill_switch=True,
        audit_log=AuditLog(path=tmp_path / "audit.jsonl"),
        idempotency_store=IdempotencyStore(path=tmp_path / "idempotency.json"),
    )
    with pytest.raises(SafetyViolation, match="KILL_SWITCH"):
        m.validate_write(WriteRequest(action="pause_target_or_campaign", idempotency_key="k1"))


def test_prohibited_action_always_blocked(middleware):
    with pytest.raises(SafetyViolation, match="prohibited"):
        middleware.validate_write(WriteRequest(action="change_product_price", idempotency_key="k1"))


def test_idempotency_blocks_duplicate_write(middleware):
    req = WriteRequest(action="pause_target_or_campaign", idempotency_key="dup-key")
    middleware.validate_write(req)  # first time succeeds
    with pytest.raises(SafetyViolation, match="already used"):
        middleware.validate_write(req)  # replay of the same key is rejected


def test_bid_change_within_cap_allowed(middleware):
    middleware.validate_bid_change(old_bid=10, new_bid=11)  # 10% <= 15% cap


def test_bid_change_over_cap_blocked_without_approval(middleware):
    with pytest.raises(SafetyViolation, match="exceeds the 15"):
        middleware.validate_bid_change(old_bid=10, new_bid=15)  # 50% > 15% cap


def test_bid_change_over_cap_allowed_with_owner_approval(middleware):
    middleware.validate_bid_change(old_bid=10, new_bid=15, owner_approved=True)


def test_total_daily_budget_cap_enforced(middleware):
    # 150 + 150 already active; adding 101 more would exceed the 400 cap.
    with pytest.raises(SafetyViolation, match="hard cap"):
        middleware.validate_total_daily_budget(
            proposed_campaign_budget=101, other_active_daily_budgets_inr=(150, 150)
        )
    # Exactly at the cap is fine.
    middleware.validate_total_daily_budget(
        proposed_campaign_budget=100, other_active_daily_budgets_inr=(150, 150)
    )


def test_set_budget_write_rejected_when_it_breaches_total_cap(middleware):
    with pytest.raises(SafetyViolation):
        middleware.validate_write(
            WriteRequest(
                action="set_budget",
                idempotency_key="budget-1",
                old_value=100,
                new_value=101,
                other_active_daily_budgets_inr=(150, 150),
            )
        )


def test_idempotency_store_persists_across_instances(tmp_path):
    path = tmp_path / "idempotency.json"
    store_a = IdempotencyStore(path=path)
    store_a.mark("persisted-key")

    store_b = IdempotencyStore(path=path)
    assert store_b.seen("persisted-key") is True
