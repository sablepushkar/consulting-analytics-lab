# Data pipeline notes

I added a CSV scan that reads one row at a time instead of loading a whole file into a dataframe. It checks the header, required columns, blank cells, numeric values, duplicate keys and basic summary statistics. Numeric summaries are calculated as the file is read. Duplicate-key tracking uses a temporary SQLite database, which can use disk space as the number of keys grows.

The defaults are a 1 GB input-file limit and 5 million rows. They are guardrails, not a benchmark. The pipeline has not been benchmarked on a production server, and disk space, CSV shape and SQLite speed still affect runtime. If a row has a bad numeric value, the report is marked `review_required` instead of silently treating that value as zero.

Example:

```bash
python scripts/analyze_csv.py data/india_health_expenditure.csv --numeric-column value --key-column year --required-column country_code --required-column indicator_code --output reports/health-expenditure-quality.json
```

The JSON report records the file name and size, row count, missing and invalid values, duplicate keys and numeric summary. It does not modify the input file. Keep the source file and its metadata next to any result so another person can trace the analysis.
