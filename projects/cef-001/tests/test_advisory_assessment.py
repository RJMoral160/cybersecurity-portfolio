import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from advisory_assessment import assess, render_markdown, validate_profile


PROFILE = {
    "cve": "CVE-20XX-0001", "vendor": "Example Vendor", "product": "Example Product",
    "affected_versions": ["1.0"], "fixed_version": "1.1",
    "source_url": "https://example.invalid/advisory",
    "required_conditions": {"feature_enabled": True, "access_control_present": False},
}


def observation(**updates):
    value = {
        "synthetic": True, "product": "Example Product", "version": "1.0",
        "conditions": {"feature_enabled": True, "access_control_present": False},
    }
    value.update(updates)
    return value


class AdvisoryAssessmentTests(unittest.TestCase):
    def test_complete_matching_synthetic_observation_is_model_applicable(self):
        self.assertEqual("applicable_in_synthetic_model", assess(PROFILE, observation())["conclusion"])

    def test_product_mismatch_is_not_applicable(self):
        self.assertEqual("not_applicable", assess(PROFILE, observation(product="Other Product"))["conclusion"])

    def test_version_outside_range_is_not_applicable(self):
        self.assertEqual("not_applicable", assess(PROFILE, observation(version="1.1"))["conclusion"])

    def test_missing_condition_preserves_uncertainty(self):
        result = assess(PROFILE, observation(conditions={"feature_enabled": True}))
        self.assertEqual("insufficient_evidence", result["conclusion"])
        self.assertIn("access_control_present", result["missing_conditions"])

    def test_condition_mismatch_is_not_applicable(self):
        result = assess(PROFILE, observation(conditions={"feature_enabled": True, "access_control_present": True}))
        self.assertEqual("not_applicable", result["conclusion"])

    def test_non_synthetic_observation_is_not_accepted(self):
        self.assertEqual("insufficient_evidence", assess(PROFILE, observation(synthetic=False))["conclusion"])

    def test_profile_requires_https_source_and_required_fields(self):
        errors = validate_profile({"source_url": "http://example.invalid"})
        self.assertIn("profile requires cve", errors)
        self.assertIn("profile source_url must be an HTTPS URL", errors)

    def test_report_states_limitation(self):
        report = render_markdown(PROFILE, assess(PROFILE, observation()))
        self.assertIn("does not replace human review", report)
        self.assertIn("applicable_in_synthetic_model", report)


if __name__ == "__main__":
    unittest.main()
