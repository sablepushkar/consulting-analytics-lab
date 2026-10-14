# Consulting Analytics Lab

[![Tests](https://github.com/sablepushkar/consulting-analytics-lab/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/sablepushkar/consulting-analytics-lab/actions/workflows/ci.yml)

I started this project to practise using numbers to answer business questions. I am combining consulting-style cases with public-data analysis in one repository, instead of making a separate project for each one.

## What works now

- Tested calculations for contribution per unit, break-even, margin and percentage change.
- A command that runs a fictional profitability case and prints the assumptions and result.
- A streaming CSV checker for row counts, missing values, invalid numeric cells, duplicate keys and summary statistics.
- A script to fetch India's health-expenditure indicator from the official World Bank API and save source details separately.
- Automated tests for calculations, case validation and CSV quality checks, including a generated 20,000-row test fixture.

## Quick start

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m analytics_lab.case_runner cases/profitability/case.json
```

## Public-data workflow

Download the dataset (internet required):

```bash
python scripts/fetch_world_bank.py --start-year 2000 --end-year 2023
```

Check the downloaded CSV without loading the full file into memory:

```bash
python scripts/analyze_csv.py data/india_health_expenditure.csv --numeric-column value --key-column year --required-column country_code --required-column indicator_code --output reports/health-expenditure-quality.json
```

See the [portfolio demo guide](docs/portfolio-demo.md), [operating guide](docs/operating_guide.md), [data pipeline](docs/data_pipeline.md), [data sources](docs/data_sources.md) and [metric definitions](docs/metric_definitions.md).

## Current gaps

The market-entry and operational-efficiency cases are outlines, not completed investigations. PharmaOps is a possible future extension for inventory, expiry, supplier performance and working capital; it is not implemented. The World Bank download needs internet access and should be checked for source metadata and row quality before analysis.

## Scope and limits

This is a student learning project, not a consulting firm's toolkit. The CSV scanner has configurable safety limits (1 GB input and 5 million rows by default); I have not benchmarked it on production-scale data. The public indicator measures national current health expenditure as a share of GDP; it does not measure pharmaceutical sales, medicine demand or company profitability. Results still need source checks and interpretation of assumptions.
