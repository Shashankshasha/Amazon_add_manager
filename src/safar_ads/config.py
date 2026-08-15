"""Loads the business constants and campaign plan from config/*.yaml.

Nothing in this module reads secrets - see amazon_ads_client.py for that.
Keeping business numbers in YAML (not scattered through code or prompts)
is what lets the safety middleware enforce them without trusting the agent.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"


def _load_yaml(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@dataclass(frozen=True)
class Guardrails:
    max_total_daily_budget_inr: float
    max_monthly_ad_spend_inr: float
    max_single_bid_change_pct: float
    max_campaign_budget_change_pct: float
    prohibited_actions: tuple[str, ...]


@dataclass(frozen=True)
class Economics:
    selling_price_inr: float
    physical_packed_cost_inr: float
    profit_floor_inr: float
    target_ad_cost_per_order_min_inr: float
    target_ad_cost_per_order_max_inr: float


@dataclass(frozen=True)
class BusinessConstants:
    economics: Economics
    guardrails: Guardrails
    permission_level: int
    raw: dict[str, Any]


@functools.lru_cache(maxsize=1)
def load_business_constants() -> BusinessConstants:
    data = _load_yaml("business_constants.yaml")
    econ = data["economics"]
    guard = data["guardrails"]
    return BusinessConstants(
        economics=Economics(
            selling_price_inr=econ["selling_price_inr"],
            physical_packed_cost_inr=econ["physical_packed_cost_inr"],
            profit_floor_inr=econ["profit_floor_inr"],
            target_ad_cost_per_order_min_inr=econ["target_ad_cost_per_order_min_inr"],
            target_ad_cost_per_order_max_inr=econ["target_ad_cost_per_order_max_inr"],
        ),
        guardrails=Guardrails(
            max_total_daily_budget_inr=guard["max_total_daily_budget_inr"],
            max_monthly_ad_spend_inr=guard["max_monthly_ad_spend_inr"],
            max_single_bid_change_pct=guard["max_single_bid_change_pct"],
            max_campaign_budget_change_pct=guard["max_campaign_budget_change_pct"],
            prohibited_actions=tuple(guard["prohibited_actions"]),
        ),
        permission_level=data["permission_level"]["current"],
        raw=data,
    )


@functools.lru_cache(maxsize=1)
def load_campaign_plan() -> dict[str, Any]:
    return _load_yaml("campaigns.yaml")


@functools.lru_cache(maxsize=1)
def load_keyword_themes() -> dict[str, Any]:
    return _load_yaml("keywords.yaml")


def planned_total_daily_budget_inr() -> float:
    plan = load_campaign_plan()
    return sum(c["daily_budget_inr"] for c in plan["campaigns"])
