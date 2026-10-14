"""Offline tests for the World Bank fetch and output helpers."""
from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import fetch_world_bank as world_bank


def api_response(records: list[dict]) -> bytes:
    return json.dumps([{"page": 1, "pages": 1, "total": len(records)}, records]).encode("utf-8")


def observation(year: str, value: float | None, *, country: str = "IND", indicator: str = "SH.XPD.CHEX.GD.ZS") -> dict:
    return {
        "countryiso3code": country,
        "date": year,
        "value": value,
        "indicator": {"id": indicator},
    }


class WorldBankFetchTests(unittest.TestCase):
    def test_fetch_validates_source_and_sorts_years(self):
        payload = api_response([observation("2022", 3.4), observation("2020", None), observation("2021", 3.2)])
        with patch.object(world_bank, "urlopen", return_value=io.BytesIO(payload)):
            rows = world_bank.fetch_series(2020, 2022)
        self.assertEqual([row["year"] for row in rows], [2020, 2021, 2022])
        self.assertEqual(rows[0]["value"], None)
        self.assertTrue(all(row["country_code"] == "IND" for row in rows))
        self.assertTrue(all(row["indicator_code"] == "SH.XPD.CHEX.GD.ZS" for row in rows))

    def test_rejects_unexpected_country_or_indicator(self):
        for record in [observation("2020", 3.1, country="USA"), observation("2020", 3.1, indicator="WRONG")]:
            with self.subTest(record=record):
                with patch.object(world_bank, "urlopen", return_value=io.BytesIO(api_response([record]))):
                    with self.assertRaisesRegex(ValueError, "unexpected country or indicator"):
                        world_bank.fetch_series(2020, 2020)

    def test_rejects_duplicate_years_and_non_numeric_values(self):
        duplicate = api_response([observation("2020", 3.1), observation("2020", 3.2)])
        with patch.object(world_bank, "urlopen", return_value=io.BytesIO(duplicate)):
            with self.assertRaisesRegex(ValueError, "duplicate years"):
                world_bank.fetch_series(2020, 2020)
        non_numeric = api_response([observation("2020", "not-a-number")])
        with patch.object(world_bank, "urlopen", return_value=io.BytesIO(non_numeric)):
            with self.assertRaisesRegex(ValueError, "non-numeric observation"):
                world_bank.fetch_series(2020, 2020)

    def test_rejects_invalid_year_range_without_network_access(self):
        with patch.object(world_bank, "urlopen") as mocked_urlopen:
            with self.assertRaisesRegex(ValueError, "valid year range"):
                world_bank.fetch_series(2022, 2020)
        mocked_urlopen.assert_not_called()

    def test_writes_csv_and_traceable_metadata(self):
        rows = [
            {"year": 2020, "value": None, "country_code": "IND", "indicator_code": "SH.XPD.CHEX.GD.ZS", "unit": "% of GDP"},
            {"year": 2021, "value": 3.2, "country_code": "IND", "indicator_code": "SH.XPD.CHEX.GD.ZS", "unit": "% of GDP"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "data" / "series.csv"
            metadata_path = Path(tmp) / "data" / "series.metadata.json"
            world_bank.write_outputs(rows, csv_path, metadata_path, 2020, 2021)
            with csv_path.open(encoding="utf-8", newline="") as handle:
                written_rows = list(csv.DictReader(handle))
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertEqual([row["year"] for row in written_rows], ["2020", "2021"])
        self.assertEqual(metadata["rows_returned"], 2)
        self.assertEqual(metadata["observations_present"], 1)
        self.assertEqual(metadata["missing_observations"], 1)
        self.assertIn("not pharmaceutical company revenue", metadata["interpretation_limit"])


if __name__ == "__main__":
    unittest.main()
