import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from report_findings import load_collection, render_markdown, validate_collection


def discovered(finding_id="SYN-001"):
    return {"synthetic": True, "finding_id": finding_id, "status": "discovered", "observation": "Synthetic observation"}


class ReportFindingsTests(unittest.TestCase):
    def test_valid_collection_has_no_errors(self):
        self.assertEqual([], validate_collection([discovered()]))

    def test_empty_collection_is_rejected(self):
        self.assertIn("collection must contain at least one finding record", validate_collection([]))

    def test_duplicate_ids_are_rejected(self):
        self.assertIn("duplicate finding_id: SYN-001", validate_collection([discovered(), discovered()]))

    def test_invalid_record_error_includes_position(self):
        errors = validate_collection([{"synthetic": True, "finding_id": "SYN-002", "status": "unknown"}])
        self.assertIn("record 1: status must be one of: discovered, correlated, applicable, remediated, retested", errors)

    def test_report_is_sorted_and_escapes_table_delimiters(self):
        report = render_markdown([discovered("Z|2"), discovered("A|1")], "synthetic.json")
        self.assertLess(report.index("A\\|1"), report.index("Z\\|2"))
        self.assertIn("- **discovered:** 2", report)
        self.assertIn("- **retested:** 0", report)

    def test_load_collection_rejects_object_instead_of_array(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(discovered()), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "collection must be a JSON array"):
                load_collection(path)

    def test_load_collection_rejects_non_object_item(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps(["not-a-record"]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "every collection item must be a JSON object"):
                load_collection(path)


if __name__ == "__main__":
    unittest.main()
