#!/usr/bin/env python3
"""Run the streaming CSV quality and summary checks."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from analytics_lab.data_pipeline import analyze_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a CSV without loading all rows into memory.")
    parser.add_argument("input", help="CSV file to analyse")
    parser.add_argument("--numeric-column", required=True, help="Column to summarise as numbers")
    parser.add_argument("--key-column", help="Optional column used to find duplicate keys")
    parser.add_argument("--required-column", action="append", default=[], help="Required column; can be repeated")
    parser.add_argument("--max-bytes", type=int, default=1_000_000_000)
    parser.add_argument("--max-rows", type=int, default=5_000_000)
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()
    try:
        report = analyze_csv(args.input, numeric_column=args.numeric_column, key_column=args.key_column,
                             required_columns=tuple(args.required_column), max_bytes=args.max_bytes, max_rows=args.max_rows)
    except (OSError, ValueError) as exc:
        print(f"CSV analysis failed: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        temporary.replace(target)
    print(rendered, end="")
    return 1 if report["status"] != "ok" else 0


if __name__ == "__main__":
    raise SystemExit(main())
