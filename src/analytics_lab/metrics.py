"""Basic business calculations used in the practice cases."""
from __future__ import annotations
import math


def _number(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number.")
    return float(value)


def contribution_per_unit(selling_price: float, variable_cost_per_unit: float) -> float:
    """Return selling price minus variable cost for one unit."""
    selling_price = _number("Selling price", selling_price)
    variable_cost_per_unit = _number("Variable cost", variable_cost_per_unit)
    if selling_price < 0 or variable_cost_per_unit < 0:
        raise ValueError("Price and variable cost must not be negative.")
    return selling_price - variable_cost_per_unit


def break_even_units(fixed_costs: float, selling_price: float, variable_cost_per_unit: float) -> int:
    """Return the whole number of units needed to cover fixed costs."""
    fixed_costs = _number("Fixed costs", fixed_costs)
    if fixed_costs < 0:
        raise ValueError("Fixed costs must not be negative.")
    contribution = contribution_per_unit(selling_price, variable_cost_per_unit)
    if contribution <= 0:
        raise ValueError("Selling price must be greater than variable cost.")
    return math.ceil(fixed_costs / contribution)


def margin_percent(revenue: float, costs: float) -> float:
    """Return profit margin as a percentage of revenue."""
    revenue = _number("Revenue", revenue)
    costs = _number("Costs", costs)
    if revenue <= 0:
        raise ValueError("Revenue must be greater than zero.")
    if costs < 0:
        raise ValueError("Costs must not be negative.")
    return ((revenue - costs) / revenue) * 100


def percentage_change(previous: float, current: float) -> float:
    """Return percentage change from a positive starting value."""
    previous = _number("Previous value", previous)
    current = _number("Current value", current)
    if previous <= 0:
        raise ValueError("The previous value must be greater than zero.")
    return ((current - previous) / previous) * 100
