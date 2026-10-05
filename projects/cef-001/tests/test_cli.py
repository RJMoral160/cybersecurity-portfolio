"""Offline command-line and committed sample regression checks."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DATA = ROOT / "data" / "synthetic"
EXAMPLES = ROOT / "examples"


def cli(script, *args):
    return subprocess.run(
        [sys.executable, str(SRC / script), *[str(arg) for arg in args]],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )


class CLITests(unittest.TestCase):
    def test_committed_samples_match_generation(self):
        with tempfile.TemporaryDirectory() as scratch:
            collection = Path(scratch) / "collection.md"
            advisory = Path(scratch) / "advisory.md"
            first = cli("report_findings.py", DATA / "finding_collection.json", "--output", collection)
            second = cli("advisory_assessment.py", DATA / "apache_cve_2021_41773_profile.json", DATA / "apache_cve_2021_41773_observation.json", "--output", advisory)
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertEqual((EXAMPLES / "sample_report.md").read_text(), collection.read_text())
            self.assertEqual((EXAMPLES / "sample_advisory_assessment.md").read_text(), advisory.read_text())

    def test_bad_inputs_fail_without_overwriting_output(self):
        with tempfile.TemporaryDirectory() as scratch:
            directory = Path(scratch)
            output = directory / "existing.md"
            output.write_text("preserve", encoding="utf-8")
            cases = {
                "malformed": b"{bad",
                "wrong-top-level": b"{}",
                "wrong-status-type": json.dumps([{"synthetic": True, "finding_id": "x", "status": []}]).encode(),
                "bad-encoding": b"\xff\xfe",
            }
            for label, content in cases.items():
                with self.subTest(label=label):
                    path = directory / (label + ".json")
                    path.write_bytes(content)
                    result = cli("report_findings.py", path, "--output", output)
                    self.assertNotEqual(0, result.returncode)
                    self.assertEqual("preserve", output.read_text())
            self.assertNotEqual(0, cli("report_findings.py", directory / "absent.json").returncode)

    def test_invalid_output_path_fails_clearly(self):
        with tempfile.TemporaryDirectory() as scratch:
            result = cli("report_findings.py", DATA / "finding_collection.json", "--output", Path(scratch))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("could not write report", result.stderr)

    def test_advisory_bad_profile_and_input_fail(self):
        with tempfile.TemporaryDirectory() as scratch:
            path = Path(scratch) / "invalid.json"
            path.write_text("[]", encoding="utf-8")
            result = cli("advisory_assessment.py", path, DATA / "apache_cve_2021_41773_observation.json")
            self.assertNotEqual(0, result.returncode)
            path.write_text("{}", encoding="utf-8")
            result = cli("advisory_assessment.py", path, DATA / "apache_cve_2021_41773_observation.json")
            self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()
