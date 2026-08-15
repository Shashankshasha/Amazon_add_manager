"""Safety middleware: the hard financial guardrails from Phase 2.4 / 4.3.

This is the layer the plan insists on: "The backend should calculate and
reject any API update that would exceed the configured hard cap, even if
the agent requests it." Nothing in amazon_ads_client.py performs a write
without going through SafetyMiddleware.validate_write() first, and every
check here reads its numbers from config/business_constants.yaml - never
from a value the agent supplies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from safar_ads.audit_log import AuditLog
from safar_ads.config import BusinessConstants, load_business_constants

DEFAULT_IDEMPOTENCY_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "idempotency_keys.json"
)


class SafetyViolation(Exception):
    """Raised when a proposed action would breach a hard guardrail.

    The agent (or anything calling the Amazon Ads client) must treat this
    as non-negotiable - it is not a suggestion to retry with different
    wording, it is a rejected write.
    """


@dataclass
class WriteRequest:
    action: str
    idempotency_key: str
    owner_approved: bool = False
    old_value: float | None = None
    new_value: float | None = None
    # For budget writes: the daily budgets of every OTHER active campaign,
    # so the total-cap check considers the whole account, not just this one.
    other_active_daily_budgets_inr: tuple[float, ...] = ()


class IdempotencyStore:
    """Tracks idempotency keys already consumed, persisted to disk so a
    process restart cannot replay a write that already went through."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_IDEMPOTENCY_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._keys: set[str] = set(self._load())

    def _load(self) -> list[str]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(sorted(self._keys), f)

    def seen(self, key: str) -> bool:
        return key in self._keys

    def mark(self, key: str) -> None:
        self._keys.add(key)
        self._save()


class SafetyMiddleware:
    def __init__(
        self,
        *,
        kill_switch: bool,
        constants: BusinessConstants | None = None,
        audit_log: AuditLog | None = None,
        idempotency_store: IdempotencyStore | None = None,
    ) -> None:
        self.kill_switch = kill_switch
        self.constants = constants or load_business_constants()
        self.audit_log = audit_log or AuditLog()
        self.idempotency_store = idempotency_store or IdempotencyStore()

    # -- individual checks -------------------------------------------------

    def check_kill_switch(self) -> None:
        if self.kill_switch:
            raise SafetyViolation(
                "SAFAR_ADS_KILL_SWITCH is engaged - all write calls are blocked."
            )

    def check_prohibited(self, action: str) -> None:
        if action in self.constants.guardrails.prohibited_actions:
            raise SafetyViolation(f"Action '{action}' is permanently prohibited for the agent.")

    def check_idempotency(self, key: str) -> None:
        if not key:
            raise SafetyViolation("Write calls require a non-empty idempotency_key.")
        if self.idempotency_store.seen(key):
            raise SafetyViolation(f"Idempotency key '{key}' already used - refusing duplicate write.")

    def validate_bid_change(self, *, old_bid: float, new_bid: float, owner_approved: bool = False) -> None:
        if old_bid <= 0:
            raise SafetyViolation("old_bid must be positive to evaluate a % change.")
        pct_change = abs(new_bid - old_bid) / old_bid * 100
        cap = self.constants.guardrails.max_single_bid_change_pct
        if pct_change > cap and not owner_approved:
            raise SafetyViolation(
                f"Bid change of {pct_change:.1f}% exceeds the {cap}% per-cycle cap "
                "without owner approval."
            )

    def validate_budget_change(self, *, old_budget: float, new_budget: float, owner_approved: bool = False) -> None:
        if old_budget <= 0:
            raise SafetyViolation("old_budget must be positive to evaluate a % change.")
        pct_change = abs(new_budget - old_budget) / old_budget * 100
        cap = self.constants.guardrails.max_campaign_budget_change_pct
        if pct_change > cap and not owner_approved:
            raise SafetyViolation(
                f"Budget change of {pct_change:.1f}% exceeds the {cap}% per-cycle cap "
                "without owner approval."
            )

    def validate_total_daily_budget(self, *, proposed_campaign_budget: float, other_active_daily_budgets_inr: tuple[float, ...]) -> None:
        total = proposed_campaign_budget + sum(other_active_daily_budgets_inr)
        cap = self.constants.guardrails.max_total_daily_budget_inr
        if total > cap:
            raise SafetyViolation(
                f"Total daily budget would be Rs.{total:.0f}, exceeding the "
                f"Rs.{cap:.0f} hard cap across all active campaigns."
            )

    # -- combined entry point used by the Ads client ------------------------

    def validate_write(self, request: WriteRequest) -> None:
        """Run every applicable check for a write request, logging the
        outcome either way. Raises SafetyViolation on the first failure."""
        try:
            self.check_kill_switch()
            self.check_prohibited(request.action)
            self.check_idempotency(request.idempotency_key)

            if request.action == "set_bid" and request.old_value is not None and request.new_value is not None:
                self.validate_bid_change(
                    old_bid=request.old_value,
                    new_bid=request.new_value,
                    owner_approved=request.owner_approved,
                )
            elif request.action == "set_budget" and request.old_value is not None and request.new_value is not None:
                self.validate_budget_change(
                    old_budget=request.old_value,
                    new_budget=request.new_value,
                    owner_approved=request.owner_approved,
                )
                self.validate_total_daily_budget(
                    proposed_campaign_budget=request.new_value,
                    other_active_daily_budgets_inr=request.other_active_daily_budgets_inr,
                )
            elif request.action == "create_campaign" and request.new_value is not None:
                self.validate_total_daily_budget(
                    proposed_campaign_budget=request.new_value,
                    other_active_daily_budgets_inr=request.other_active_daily_budgets_inr,
                )
        except SafetyViolation as exc:
            self.audit_log.log(
                action=request.action,
                dry_run=True,
                old_value=request.old_value,
                new_value=request.new_value,
                idempotency_key=request.idempotency_key,
                approved=request.owner_approved,
                result="blocked",
                reason=str(exc),
            )
            raise

        self.idempotency_store.mark(request.idempotency_key)
        self.audit_log.log(
            action=request.action,
            dry_run=True,
            old_value=request.old_value,
            new_value=request.new_value,
            idempotency_key=request.idempotency_key,
            approved=request.owner_approved,
            result="ok",
        )
