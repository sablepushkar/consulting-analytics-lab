#!/usr/bin/env python3
"""Download one India indicator series from the official World Bank API."""
from __future__ import annotations
import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

COUNTRY = "IND"
INDICATOR = "SH.XPD.CHEX.GD.ZS"
BASE_URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"


def fetch_series(start_year: int, end_year: int, retries: int = 3) -> list[dict]:
    if start_year < 1960 or end_year < start_year or end_year > datetime.now(timezone.utc).year:
        raise ValueError("Use a valid year range between 1960 and the current year.")
    query = urlencode({"format": "json", "date": f"{start_year}:{end_year}", "per_page": max(100, end_year - start_year + 1)})
    request = Request(f"{BASE_URL}?{query}", headers={"User-Agent": "consulting-analytics-lab-student-project/1.0"})
    last_error = None
    for attempt in range(retries):
        try:
            with urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
                raise ValueError("World Bank API returned an unexpected response shape.")
            records = []
            for item in payload[1]:
                if not isinstance(item, dict) or item.get("countryiso3code") != COUNTRY or item.get("indicator", {}).get("id") != INDICATOR:
                    raise ValueError("World Bank response contains an unexpected country or indicator.")
                try:
                    year = int(item["date"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError("World Bank response contains an invalid year.") from exc
                value = item.get("value")
                if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
                    raise ValueError("World Bank response contains a non-numeric observation.")
                records.append({"year": year, "value": value, "country_code": COUNTRY, "indicator_code": INDICATOR, "unit": "% of GDP"})
            records.sort(key=lambda row: row["year"])
            if len({row["year"] for row in records}) != len(records):
                raise ValueError("World Bank response contains duplicate years.")
            return records
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(0.5 * (2 ** attempt))
    raise RuntimeError(f"Could not retrieve World Bank data after {retries} attempts: {last_error}")


def write_outputs(records: list[dict], output: Path, metadata_path: Path, start_year: int, end_year: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    csv_tmp = output.with_suffix(output.suffix + ".tmp")
    with csv_tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["year", "value", "country_code", "indicator_code", "unit"])
        writer.writeheader()
        for row in records:
            writer.writerow(row)
    csv_tmp.replace(output)
    metadata = {
        "publisher": "World Bank",
        "dataset": "World Development Indicators",
        "country": "India",
        "country_code": COUNTRY,
        "indicator": INDICATOR,
        "indicator_name": "Current health expenditure (% of GDP)",
        "unit": "% of GDP",
        "source_url": f"{BASE_URL}?{urlencode({'format': 'json', 'date': f'{start_year}:{end_year}'})}",
        "accessed_at_utc": datetime.now(timezone.utc).isoformat(),
        "requested_year_range": [start_year, end_year],
        "rows_returned": len(records),
        "observations_present": sum(row["value"] is not None for row in records),
        "missing_observations": sum(row["value"] is None for row in records),
        "interpretation_limit": "This indicator is national health expenditure as a share of GDP. It is not pharmaceutical company revenue, medicine demand, or profitability.",
    }
    meta_tmp = metadata_path.with_suffix(metadata_path.suffix + ".tmp")
    meta_tmp.write_text(json.dumps(metadata, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    meta_tmp.replace(metadata_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a traceable India health-expenditure indicator series.")
    parser.add_argument("--start-year", type=int, default=2000)
    parser.add_argument("--end-year", type=int, default=2023)
    parser.add_argument("--output", default="data/india_health_expenditure.csv")
    parser.add_argument("--metadata", default="data/india_health_expenditure.metadata.json")
    args = parser.parse_args()
    try:
        records = fetch_series(args.start_year, args.end_year)
        write_outputs(records, Path(args.output), Path(args.metadata), args.start_year, args.end_year)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(f"Wrote {len(records)} rows to {args.output}")
    print(f"Metadata saved to {args.metadata}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
