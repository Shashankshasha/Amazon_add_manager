"""Command-line entry point for work that does not need live API access.

    python -m safar_ads.cli plan          # Phase 7 dry-run plan
    python -m safar_ads.cli profit-table  # Phase 4.2 launch-economics table
    python -m safar_ads.cli check-budget  # validate config/campaigns.yaml against the hard cap

This is exactly the "dry-run plan the owner reviews before any write"
step in Phase 7 of the implementation plan, runnable today with zero
Amazon Ads credentials.
"""

from __future__ import annotations

import argparse
import json
import sys

from safar_ads.amazon_ads_client import AmazonAdsClient
from safar_ads.config import (
    load_business_constants,
    load_campaign_plan,
    planned_total_daily_budget_inr,
)
from safar_ads.profit import remaining_after_ad_cost, max_remaining_other_costs
from safar_ads.safety import SafetyMiddleware, SafetyViolation


def cmd_check_budget(_: argparse.Namespace) -> int:
    constants = load_business_constants()
    cap = constants.guardrails.max_total_daily_budget_inr
    total = planned_total_daily_budget_inr()
    print(f"Planned total daily budget: Rs.{total:.0f}")
    print(f"Hard cap (guardrails.max_total_daily_budget_inr): Rs.{cap:.0f}")
    if total > cap:
        print("FAIL: planned budget exceeds the hard cap.", file=sys.stderr)
        return 1
    print("OK: planned budget is within the hard cap.")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    """Build and print the exact dry-run plan Phase 7 asks the owner to
    review before any campaign is created."""
    rc = cmd_check_budget(args)
    if rc != 0:
        return rc

    client = AmazonAdsClient(dry_run=True, safety=SafetyMiddleware(kill_switch=False))
    plan = load_campaign_plan()
    results = []
    for campaign in plan["campaigns"]:
        other_budgets = tuple(
            c["daily_budget_inr"] for c in plan["campaigns"] if c["name"] != campaign["name"]
        )
        try:
            create_result = client.create_campaign(
                name=campaign["name"],
                daily_budget_inr=campaign["daily_budget_inr"],
                targeting_type=campaign["targeting_type"],
                other_active_daily_budgets_inr=other_budgets,
                state=campaign["state"],
            )
        except SafetyViolation as exc:
            create_result = {"blocked": True, "reason": str(exc)}
        results.append({"campaign": campaign["name"], "plan": create_result, "ad_groups": campaign["ad_groups"]})

    print(json.dumps({"marketplace": plan["marketplace"], "ad_product": plan["ad_product"], "campaigns": results}, indent=2))
    return 0


def cmd_profit_table(_: argparse.Namespace) -> int:
    constants = load_business_constants()
    econ = constants.economics
    print(f"Selling price: Rs.{econ.selling_price_inr:.0f}  Physical cost: Rs.{econ.physical_packed_cost_inr:.0f}  Profit floor: Rs.{econ.profit_floor_inr:.0f}\n")
    print(f"{'Ad cost/order':>15} | {'Remaining after cost+ads':>26} | {'Max other costs @ profit floor':>32}")
    for ad_cost in (60, 75, 90):
        remaining = remaining_after_ad_cost(
            selling_price_inr=econ.selling_price_inr,
            physical_cost_inr=econ.physical_packed_cost_inr,
            ad_cost_per_order_inr=ad_cost,
        )
        max_other = max_remaining_other_costs(
            selling_price_inr=econ.selling_price_inr,
            physical_cost_inr=econ.physical_packed_cost_inr,
            ad_cost_per_order_inr=ad_cost,
            profit_floor_inr=econ.profit_floor_inr,
        )
        print(f"{'Rs.' + str(ad_cost):>15} | {'Rs.' + f'{remaining:.0f}':>26} | {'Rs.' + f'{max_other:.0f}':>32}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="safar_ads.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan", help="Print the Phase 7 dry-run campaign plan").set_defaults(func=cmd_plan)
    sub.add_parser("check-budget", help="Validate config/campaigns.yaml against the hard daily cap").set_defaults(func=cmd_check_budget)
    sub.add_parser("profit-table", help="Print the Phase 4.2 launch-economics table").set_defaults(func=cmd_profit_table)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
