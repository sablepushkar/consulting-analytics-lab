# How I run the project

## 1. Run the tests

```bash
python -m unittest discover -s tests -v
```

## 2. Run the fictional profitability example

```bash
PYTHONPATH=src python -m analytics_lab.case_runner cases/profitability/case.json
```

The current example uses a selling price of ₹120, variable cost of ₹75 and fixed costs of ₹1,000. Contribution is ₹45 per unit. Break-even is 23 whole units, so the break-even revenue at the assumed price is ₹2,760. These are only arithmetic results for fictional assumptions.

## 3. Download the public-data example

```bash
python scripts/fetch_world_bank.py --start-year 2000 --end-year 2023
```

This uses the World Bank API and writes a CSV plus a separate metadata JSON file. It needs internet access. A missing value stays blank; the script does not fill it with zero.

The indicator is India's current health expenditure as a percentage of GDP. It is a national health-spending measure, not medicine demand or the revenue of any pharmaceutical company.

## 4. Check the downloaded file

```bash
python scripts/analyze_csv.py data/india_health_expenditure.csv --numeric-column value --key-column year --required-column country_code --required-column indicator_code --output reports/health-expenditure-quality.json
```

Exit code `0` means no malformed numeric values were found, `1` means the report was produced but needs review, and `2` means the input could not be analysed under the configured checks. Read the report instead of relying only on the exit code.

## Current limits

The CSV scanner is streaming and includes file/row limits, but it is not a distributed data platform. There is no live dashboard, no automatic business recommendation, and no production performance benchmark yet. The market-entry and operational-efficiency folders remain case outlines until I add evidence and calculations for them.
