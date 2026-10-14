# Metric definitions

These are the first calculations in the project. I want to keep the definitions in plain language so I can explain them in an interview or spot a mistake.

- **Contribution per unit:** selling price minus variable cost per unit.
- **Break-even units:** fixed costs divided by contribution per unit, rounded up to the next whole unit. This calculation only works when contribution per unit is positive.
- **Profit margin:** (revenue minus costs) divided by revenue, multiplied by 100. Revenue must be greater than zero.
- **Percentage change:** (current value minus previous value) divided by previous value, multiplied by 100. The starting value must be positive in this first implementation.

The functions reject a few invalid inputs, but they are still basic helpers. A real case needs careful decisions about which costs, time periods and units belong in each calculation.
