"""Streaming CSV checks for datasets that are too large to load all at once."""
from __future__ import annotations

import csv
import math
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

DEFAULT_MAX_BYTES = 1_000_000_000
DEFAULT_MAX_ROWS = 5_000_000


def analyze_csv(
    path: str | Path,
    *,
    numeric_column: str,
    key_column: str | None = None,
    required_columns: tuple[str, ...] = (),
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_rows: int = DEFAULT_MAX_ROWS,
) -> dict[str, Any]:
    """Scan a CSV one row at a time and return auditable quality/statistics data.

    Rows are not accumulated in Python memory. If a key column is supplied,
    duplicate detection uses a temporary SQLite file so the key index can spill
    to disk. Limits are intentional safeguards, not claims of unlimited scale.
    """
    source = Path(path)
    if not source.is_file():
        raise ValueError(f"CSV file does not exist: {source}")
    if max_bytes < 1 or max_rows < 1:
        raise ValueError("max_bytes and max_rows must be positive integers.")
    if source.stat().st_size > max_bytes:
        raise ValueError(f"CSV exceeds the configured byte limit ({max_bytes}).")

    rows_read = valid_numbers = missing_numbers = invalid_numbers = 0
    missing_keys = duplicate_keys = 0
    minimum = maximum = mean = m2 = None
    missing_by_column: dict[str, int] = {}
    duplicate_db = tempfile.TemporaryDirectory(prefix="analytics-lab-keys-") if key_column else None
    connection = None
    try:
        if duplicate_db:
            connection = sqlite3.connect(str(Path(duplicate_db.name) / "keys.sqlite3"))
            connection.execute("CREATE TABLE seen_keys (key TEXT PRIMARY KEY)")
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, strict=True)
            headers = reader.fieldnames
            if not headers or any(not h or not h.strip() for h in headers):
                raise ValueError("CSV must have a header row with non-empty column names.")
            if len(set(headers)) != len(headers):
                raise ValueError("CSV contains duplicate column names.")
            required = set(required_columns) | {numeric_column}
            if key_column:
                required.add(key_column)
            absent = sorted(required - set(headers))
            if absent:
                raise ValueError("Required column(s) missing: " + ", ".join(absent))
            missing_by_column = {name: 0 for name in headers}

            for row in reader:
                if row is None or None in row:
                    raise ValueError(f"Malformed CSV row near record {rows_read + 2}: column count does not match header.")
                rows_read += 1
                if rows_read > max_rows:
                    raise ValueError(f"CSV exceeds the configured row limit ({max_rows}).")
                for name in headers:
                    if row.get(name) is None or not str(row[name]).strip():
                        missing_by_column[name] += 1
                if key_column:
                    key = (row.get(key_column) or "").strip()
                    if not key:
                        missing_keys += 1
                    else:
                        try:
                            connection.execute("INSERT INTO seen_keys(key) VALUES (?)", (key,))
                        except sqlite3.IntegrityError:
                            duplicate_keys += 1
                raw = (row.get(numeric_column) or "").strip()
                if not raw:
                    missing_numbers += 1
                    continue
                try:
                    value = float(raw)
                except (TypeError, ValueError):
                    invalid_numbers += 1
                    continue
                if not math.isfinite(value):
                    invalid_numbers += 1
                    continue
                valid_numbers += 1
                if minimum is None or value < minimum:
                    minimum = value
                if maximum is None or value > maximum:
                    maximum = value
                if mean is None:
                    mean = value
                    m2 = 0.0
                else:
                    delta = value - mean
                    mean += delta / valid_numbers
                    m2 += delta * (value - mean)
        variance = (m2 / valid_numbers) if valid_numbers else None
        return {
            "report_schema_version": 1,
            "source_file": source.name,
            "file_size_bytes": source.stat().st_size,
            "rows_read": rows_read,
            "numeric_column": numeric_column,
            "key_column": key_column,
            "valid_numeric_values": valid_numbers,
            "missing_numeric_values": missing_numbers,
            "invalid_numeric_values": invalid_numbers,
            "missing_values_by_column": missing_by_column,
            "missing_keys": missing_keys,
            "duplicate_keys": duplicate_keys,
            "numeric_summary": {
                "min": minimum,
                "max": maximum,
                "mean": mean,
                "population_stddev": math.sqrt(variance) if variance is not None else None,
            },
            "status": "ok" if invalid_numbers == 0 else "review_required",
            "limits": {"max_bytes": max_bytes, "max_rows": max_rows},
        }
    except csv.Error as exc:
        raise ValueError(f"CSV parsing failed: {exc}") from exc
    finally:
        if connection is not None:
            connection.close()
        if duplicate_db is not None:
            duplicate_db.cleanup()
