"""Basic business calculations used in the practice cases."""
from __future__ import annotations
import math


def contribution_per_unit(selling_price: float, variable_cost_per_unit: float) -> float:
    """Return selling price minus variable cost for one unit."""
    if selling_price < 0 or variable_cost_per_unit < 0:
        raise ValueError("Price and variable cost must not be negative.")
    return selling_price - variable_cost_per_unit


def break_even_units(
    fixed_costs: float, selling_price: float, variable_cost_per_unit: float
) -> int:
    """Return the whole number of units needed to cover fixed costs."""
    if fixed_costs < 0:
        raise ValueError("Fixed costs must not be negative.")
    contribution = contribution_per_unit(selling_price, variable_cost_per_unit)
    if contribution <= 0:
        raise ValueError("Selling price must be greater than variable cost.")
    return math.ceil(fixed_costs / contribution)


def margin_percent(revenue: float, costs: float) -> float:
    """Return profit margin as a percentage of revenue."""
    if revenue <= 0:
        raise ValueError("Revenue must be greater than zero.")
    if costs < 0:
        raise ValueError("Costs must not be negative.")
    return ((revenue - costs) / revenue) * 100


def percentage_change(previous: float, current: float) -> float:
    """Return percentage change from a positive starting value."""
    if previous <= 0:
        raise ValueError("The previous value must be greater than zero.")
    return ((current - previous) / previous) * 100
