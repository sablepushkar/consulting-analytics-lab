import json
import tempfile
import unittest
from pathlib import Path
from analytics_lab.case_runner import evaluate_profitability_case


class CaseRunnerTests(unittest.TestCase):
    def test_existing_profitability_case_runs(self):
        case = Path(__file__).resolve().parents[1] / "cases" / "profitability" / "case.json"
        result = evaluate_profitability_case(case)
        self.assertEqual(result["contribution_per_unit"], 45)
        self.assertEqual(result["break_even_units"], 23)
        self.assertEqual(result["break_even_revenue"], 2760)
        self.assertEqual(result["data_type"], "synthetic_example")

    def test_outline_is_not_treated_as_calculable_case(self):
        case = Path(__file__).resolve().parents[1] / "cases" / "market_entry" / "case.json"
        with self.assertRaisesRegex(ValueError, "synthetic_example"):
            evaluate_profitability_case(case)

    def test_non_finite_assumption_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "case.json"
            path.write_text(json.dumps({"data_type": "synthetic_example", "selling_price_per_unit": float("inf"), "variable_cost_per_unit": 1, "fixed_costs": 2}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "finite number"):
                evaluate_profitability_case(path)


if __name__ == "__main__":
    unittest.main()
