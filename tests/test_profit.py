from safar_ads.profit import (
    classify_ad_cost,
    contribution_profit,
    max_remaining_other_costs,
    remaining_after_ad_cost,
)


def test_remaining_after_ad_cost_matches_plan_table():
    # Phase 4.2 table: 299 price, 75 physical cost.
    assert remaining_after_ad_cost(selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=60) == 164
    assert remaining_after_ad_cost(selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=75) == 149
    assert remaining_after_ad_cost(selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=90) == 134


def test_max_remaining_other_costs_matches_plan_table():
    assert max_remaining_other_costs(
        selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=60, profit_floor_inr=70
    ) == 94
    assert max_remaining_other_costs(
        selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=75, profit_floor_inr=70
    ) == 79
    assert max_remaining_other_costs(
        selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=90, profit_floor_inr=70
    ) == 64


def test_contribution_profit_full_formula():
    breakdown = contribution_profit(
        selling_price_inr=299,
        physical_cost_inr=75,
        ad_cost_per_order_inr=70,
        amazon_fees_inr=40,
        fulfilment_shipping_inr=20,
        coupons_promotions_inr=0,
        return_refund_allowance_inr=5,
        other_variable_costs_inr=2,
    )
    assert breakdown.net_contribution_inr == 299 - 75 - 40 - 20 - 70 - 0 - 5 - 2  # == 87
    assert breakdown.meets_profit_floor(70) is True


def test_meets_profit_floor_true_and_false():
    good = contribution_profit(selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=60)
    assert good.net_contribution_inr == 164
    assert good.meets_profit_floor(70) is True

    bad = contribution_profit(selling_price_inr=299, physical_cost_inr=75, ad_cost_per_order_inr=250)
    assert bad.meets_profit_floor(70) is False


def test_classify_ad_cost_traffic_light():
    assert classify_ad_cost(59) == "excellent"
    assert classify_ad_cost(75) == "target_range"
    assert classify_ad_cost(100) == "above_preferred"
    assert classify_ad_cost(150) == "wasteful"
