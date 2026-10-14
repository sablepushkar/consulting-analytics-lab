# Consulting Analytics Lab

I started this project to practise using numbers to answer business questions. I am combining consulting-style cases with analysis of public datasets in one repository, instead of making a separate project for each one.

## What works now

- Small, tested calculations for contribution per unit, break-even, margin and percentage change.
- A command that runs the fictional profitability case and prints the assumptions and result.
- A streaming CSV checker for row counts, missing values, invalid numeric cells, duplicate keys and summary statistics.
- A script to download India's health-expenditure indicator from the official World Bank API and save the source details separately.
- Automated tests for calculations, case validation and CSV quality checks, including a 20,000-row test fixture.

## Try it

Run tests:

```bash
python -m unittest discover -s tests -v
```

Run the fictional case:

```bash
PYTHONPATH=src python -m analytics_lab.case_runner cases/profitability/case.json
```

Download the public dataset (internet required):

```bash
python scripts/fetch_world_bank.py --start-year 2000 --end-year 2023
```

Check it without loading the full CSV into memory:

```bash
python scripts/analyze_csv.py data/india_health_expenditure.csv --numeric-column value --key-column year --required-column country_code --required-column indicator_code --output reports/health-expenditure-quality.json
```

See `docs/operating_guide.md` and `docs/data_pipeline.md` for the steps and limitations.

## What is still in progress

The market-entry and operational-efficiency cases are outlines, not completed investigations. PharmaOps is a possible later extension for inventory, expiry, supplier performance and working capital; it is not implemented yet.

## Scope and limits

This is a student learning project, not a consulting firm's toolkit. The CSV scanner has practical limits (1 GB by default and 5 million rows by default), and I have not benchmarked it on production-scale data. The public indicator measures national current health expenditure as a share of GDP; it does not measure pharmaceutical sales, medicine demand or company profitability. Results still need interpretation and checking of assumptions.
