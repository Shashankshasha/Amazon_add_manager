"""Contribution-profit calculator (Phase 4 of the implementation plan).

The agent optimises for business profit, not just Amazon ad metrics.
This module is the single place that formula lives - the agent and the
daily report both call into it rather than re-deriving it inline.
"""

from __future__ import annotations

from dataclasses import dataclass

from safar_ads.config import load_business_constants


@dataclass(frozen=True)
class ProfitBreakdown:
    selling_price_inr: float
    physical_cost_inr: float
    amazon_fees_inr: float
    fulfilment_shipping_inr: float
    ad_cost_per_order_inr: float
    coupons_promotions_inr: float
    return_refund_allowance_inr: float
    other_variable_costs_inr: float
    net_contribution_inr: float

    def meets_profit_floor(self, profit_floor_inr: float) -> bool:
        return self.net_contribution_inr >= profit_floor_inr


def contribution_profit(
    *,
    selling_price_inr: float,
    physical_cost_inr: float,
    ad_cost_per_order_inr: float,
    amazon_fees_inr: float = 0.0,
    fulfilment_shipping_inr: float = 0.0,
    coupons_promotions_inr: float = 0.0,
    return_refund_allowance_inr: float = 0.0,
    other_variable_costs_inr: float = 0.0,
) -> ProfitBreakdown:
    """Net contribution per completed order (Phase 4.1 core calculation).

    Net contribution = selling price - physical product/dispatch cost
      - Amazon variable charges - fulfilment/shipping
      - advertising spend allocated to that order - coupons/promotions
      - return/refund allowance - other variable selling costs.
    """
    net = (
        selling_price_inr
        - physical_cost_inr
        - amazon_fees_inr
        - fulfilment_shipping_inr
        - ad_cost_per_order_inr
        - coupons_promotions_inr
        - return_refund_allowance_inr
        - other_variable_costs_inr
    )
    return ProfitBreakdown(
        selling_price_inr=selling_price_inr,
        physical_cost_inr=physical_cost_inr,
        amazon_fees_inr=amazon_fees_inr,
        fulfilment_shipping_inr=fulfilment_shipping_inr,
        ad_cost_per_order_inr=ad_cost_per_order_inr,
        coupons_promotions_inr=coupons_promotions_inr,
        return_refund_allowance_inr=return_refund_allowance_inr,
        other_variable_costs_inr=other_variable_costs_inr,
        net_contribution_inr=net,
    )


def remaining_after_ad_cost(
    *, selling_price_inr: float, physical_cost_inr: float, ad_cost_per_order_inr: float
) -> float:
    """Amount left for every other variable cost after physical cost + ads.

    Matches the Phase 4.2 launch-economics table: at 299/75/60 this is 164.
    """
    return selling_price_inr - physical_cost_inr - ad_cost_per_order_inr


def max_remaining_other_costs(
    *,
    selling_price_inr: float,
    physical_cost_inr: float,
    ad_cost_per_order_inr: float,
    profit_floor_inr: float,
) -> float:
    """Ceiling on Amazon fees + fulfilment + returns + coupons + misc,
    if the profit floor must still be met. Matches the Phase 4.2 table:
    at 299/75/60/70 this is 94.
    """
    remaining = remaining_after_ad_cost(
        selling_price_inr=selling_price_inr,
        physical_cost_inr=physical_cost_inr,
        ad_cost_per_order_inr=ad_cost_per_order_inr,
    )
    return remaining - profit_floor_inr


def classify_ad_cost(ad_cost_per_order_inr: float) -> str:
    """Traffic-light classification per Phase 6.1 of the plan."""
    constants = load_business_constants()
    tl = constants.raw["economics"]["traffic_light"]
    if ad_cost_per_order_inr < tl["excellent_below_inr"]:
        return "excellent"
    if ad_cost_per_order_inr <= tl["target_range_inr"][1]:
        return "target_range"
    if ad_cost_per_order_inr <= tl["above_preferred_inr"][1]:
        return "above_preferred"
    return "wasteful"
