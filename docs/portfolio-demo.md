# Consulting Analytics Lab: portfolio demo

This walkthrough separates the supplied assumptions, calculations and public-data checks. Do not present fictional case numbers as real business results.

## 1. Run the included case

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m analytics_lab.case_runner cases/profitability/case.json
```

Show the case assumptions before the result. Explain contribution per unit and break-even in terms of those assumptions, and label the example as fictional.

## 2. Fetch and inspect a public indicator

```bash
python scripts/fetch_world_bank.py --start-year 2000 --end-year 2023
```

This step requires internet access. Check the saved source details and confirm the returned country, indicator, year range and row count before using the file. If the fetch fails or the source response is unexpected, report that rather than inventing a result.

## 3. Run data-quality checks

```bash
python scripts/analyze_csv.py data/india_health_expenditure.csv --numeric-column value --key-column year --required-column country_code --required-column indicator_code --output reports/health-expenditure-quality.json
```

Review missing values, invalid numeric cells, duplicate keys and summary statistics. Keep the generated report as evidence and record the commit and source date.

## What this demo establishes

It demonstrates the included calculations, a streaming CSV quality workflow and a public-data retrieval script. The 20,000-row test is a correctness fixture, not a production-scale performance benchmark. The World Bank indicator is national health expenditure as a share of GDP, not medicine demand or pharmaceutical-company performance.
