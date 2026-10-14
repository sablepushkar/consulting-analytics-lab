import csv
import tempfile
import unittest
from pathlib import Path
from analytics_lab.data_pipeline import analyze_csv


class DataPipelineTests(unittest.TestCase):
    def write_csv(self, directory, rows, headers=("year", "value", "note")):
        path = Path(directory) / "sample.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def test_summary_quality_and_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, [
                {"year": "2020", "value": "2", "note": "a"},
                {"year": "2021", "value": "4", "note": ""},
                {"year": "2021", "value": "bad", "note": "c"},
                {"year": "", "value": "", "note": "d"},
            ])
            result = analyze_csv(path, numeric_column="value", key_column="year")
            self.assertEqual(result["rows_read"], 4)
            self.assertEqual(result["valid_numeric_values"], 2)
            self.assertEqual(result["missing_numeric_values"], 1)
            self.assertEqual(result["invalid_numeric_values"], 1)
            self.assertEqual(result["duplicate_keys"], 1)
            self.assertEqual(result["missing_keys"], 1)
            self.assertEqual(result["numeric_summary"]["mean"], 3.0)
            self.assertEqual(result["status"], "review_required")

    def test_streams_many_rows_and_respects_row_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "many.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["id", "value"])
                for number in range(20000):
                    writer.writerow([number, number % 10])
            result = analyze_csv(path, numeric_column="value", key_column="id", max_rows=20000)
            self.assertEqual(result["rows_read"], 20000)
            self.assertEqual(result["duplicate_keys"], 0)
            with self.assertRaisesRegex(ValueError, "row limit"):
                analyze_csv(path, numeric_column="value", max_rows=100)

    def test_rejects_missing_required_columns_and_oversize_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, [{"year": "2020", "value": "2", "note": "a"}])
            with self.assertRaisesRegex(ValueError, "missing"):
                analyze_csv(path, numeric_column="value", required_columns=("country",))
            with self.assertRaisesRegex(ValueError, "byte limit"):
                analyze_csv(path, numeric_column="value", max_bytes=2)

    def test_empty_file_has_no_numeric_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_csv(directory, [])
            result = analyze_csv(path, numeric_column="value")
            self.assertEqual(result["rows_read"], 0)
            self.assertIsNone(result["numeric_summary"]["mean"])


if __name__ == "__main__":
    unittest.main()
