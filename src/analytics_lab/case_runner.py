"""Run the small profitability case from its JSON assumptions."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any
from .metrics import break_even_units, contribution_per_unit


def evaluate_profitability_case(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        case = json.load(handle)
    if not isinstance(case, dict) or case.get("data_type") != "synthetic_example":
        raise ValueError("This runner only accepts a case marked synthetic_example.")
    try:
        price = case["selling_price_per_unit"]
        variable_cost = case["variable_cost_per_unit"]
        fixed_costs = case["fixed_costs"]
    except KeyError as exc:
        raise ValueError(f"Missing required case field: {exc.args[0]}") from exc
    for name, value in (("selling_price_per_unit", price), ("variable_cost_per_unit", variable_cost), ("fixed_costs", fixed_costs)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number.")
    units = break_even_units(fixed_costs, price, variable_cost)
    return {
        "title": case.get("title", Path(path).stem),
        "data_type": "synthetic_example",
        "currency": case.get("currency", "unspecified"),
        "assumptions": {"selling_price_per_unit": price, "variable_cost_per_unit": variable_cost, "fixed_costs": fixed_costs},
        "contribution_per_unit": contribution_per_unit(price, variable_cost),
        "break_even_units": units,
        "break_even_revenue": units * price,
        "note": "This is arithmetic based on the supplied assumptions, not a forecast or real-company result.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic profitability example.")
    parser.add_argument("case", help="Path to a profitability case JSON file")
    parser.add_argument("--output", help="Optional path for a JSON result")
    args = parser.parse_args()
    result = evaluate_profitability_case(args.case)
    rendered = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(target)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
