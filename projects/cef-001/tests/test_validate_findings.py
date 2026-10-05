import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validate_findings import validate


class ValidateFindingsTests(unittest.TestCase):
    def test_discovery_requires_observation(self):
        self.assertIn("discovered status requires non-empty observation", validate({"synthetic": True, "status": "discovered"}))

    def test_correlation_is_not_applicability(self):
        self.assertEqual([], validate({"synthetic": True, "status": "correlated", "observation": "Synthetic banner", "correlation": "Possible CVE correlation"}))

    def test_applicability_requires_human_and_authoritative_evidence(self):
        errors = validate({"synthetic": True, "status": "applicable", "observation": "Synthetic banner", "correlation": "Possible CVE correlation"})
        self.assertIn("applicable status requires non-empty authoritative_source", errors)
        self.assertIn("applicable status requires non-empty human_approval", errors)

    def test_complete_applicability_record_passes(self):
        record = {
            "synthetic": True, "status": "applicable", "observation": "Synthetic banner",
            "correlation": "Possible CVE correlation", "authoritative_source": "https://example.invalid/advisory",
            "product_identity": "Example Product", "affected_range_evidence": "Synthetic range",
            "prerequisite_evidence": "Synthetic prerequisite", "human_approval": "approved",
        }
        self.assertEqual([], validate(record))

    def test_remediation_requires_validation(self):
        record = {
            "synthetic": True, "status": "remediated", "observation": "Synthetic banner",
            "correlation": "Possible CVE correlation", "authoritative_source": "https://example.invalid/advisory",
            "product_identity": "Example Product", "affected_range_evidence": "Synthetic range",
            "prerequisite_evidence": "Synthetic prerequisite", "human_approval": "approved",
            "remediation": "Synthetic patch",
        }
        self.assertIn("remediated status requires non-empty remediation_validation", validate(record))

    def test_retest_requires_prior_lifecycle_and_retest_evidence(self):
        record = {
            "synthetic": True, "status": "retested", "observation": "Synthetic observation",
            "correlation": "Synthetic correlation", "authoritative_source": "https://example.invalid/advisory",
            "product_identity": "Example Product", "affected_range_evidence": "Synthetic range",
            "prerequisite_evidence": "Synthetic prerequisite", "human_approval": "approved",
            "remediation": "Synthetic patch action", "remediation_validation": "Synthetic change check",
            "retest_method": "Repeat synthetic check", "baseline_reference": "SYN-BASELINE-001",
            "retest_result": "Synthetic result",
        }
        self.assertEqual([], validate(record))

    def test_non_synthetic_records_are_rejected_during_startup(self):
        self.assertIn("synthetic must be true during the startup phase", validate({"synthetic": False, "status": "discovered", "observation": "x"}))

    def test_non_string_status_is_rejected_cleanly(self):
        for status in ([], {}, None, 1):
            with self.subTest(status=status):
                self.assertTrue(any("status must be one of" in error for error in validate({"synthetic": True, "status": status})))


if __name__ == "__main__":
    unittest.main()
