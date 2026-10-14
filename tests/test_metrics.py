import unittest
from analytics_lab.metrics import break_even_units, contribution_per_unit, margin_percent, percentage_change


class MetricsTests(unittest.TestCase):
    def test_contribution_per_unit(self):
        self.assertEqual(contribution_per_unit(120, 75), 45)

    def test_break_even_rounds_up_to_whole_unit(self):
        self.assertEqual(break_even_units(1000, 120, 75), 23)

    def test_break_even_rejects_no_contribution(self):
        with self.assertRaises(ValueError):
            break_even_units(1000, 75, 75)

    def test_negative_cost_is_rejected(self):
        with self.assertRaises(ValueError):
            contribution_per_unit(100, -2)

    def test_non_finite_and_boolean_values_are_rejected(self):
        for value in (float("nan"), float("inf"), True, "120"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                contribution_per_unit(value, 75)

    def test_margin_percent(self):
        self.assertAlmostEqual(margin_percent(200, 150), 25.0)

    def test_margin_requires_positive_revenue(self):
        with self.assertRaises(ValueError):
            margin_percent(0, 10)

    def test_percentage_change(self):
        self.assertAlmostEqual(percentage_change(80, 100), 25.0)

    def test_percentage_change_requires_positive_start(self):
        with self.assertRaises(ValueError):
            percentage_change(0, 10)


if __name__ == "__main__":
    unittest.main()
