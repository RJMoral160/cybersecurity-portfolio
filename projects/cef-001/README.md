# Vulnerability Evidence Pipeline

## Overview

An offline Python workflow validates synthetic vulnerability records and renders Markdown reports. It separates service discovery, advisory correlation, applicability assessment, remediation, and retest as distinct states. The advisory module compares a synthetic observation with a local profile instead of treating a CVE match as an automatic conclusion.

## Objectives

- Require the evidence fields appropriate to each lifecycle state.
- Reject empty, malformed, duplicate, or non-synthetic collections.
- Compare product, exact version, and required conditions against a local advisory profile.
- Produce stable human-readable reports without contacting a target.

## Architecture

```text
data/synthetic/finding_collection.json
  → src/validate_findings.py
  → src/report_findings.py
  → examples/sample_report.md

data/synthetic/*profile.json + *observation.json
  → src/advisory_assessment.py
  → examples/sample_advisory_assessment.md
```

The modules use only the Python standard library. [Dependencies](DEPENDENCIES.md) records the runtime requirement.

## Implemented Components

| Component | Function |
|---|---|
| [Finding validator](src/validate_findings.py) | Applies state-specific required-field gates |
| [Collection reporter](src/report_findings.py) | Checks JSON collection shape and IDs, then renders a deterministic report |
| [Advisory assessor](src/advisory_assessment.py) | Compares a synthetic observation to a local product/version/condition profile |
| [Unit tests](tests/) | Covers valid paths, malformed input, missing prerequisites, and mismatches |

## Configuration

Inputs are local JSON. The [synthetic finding collection](data/synthetic/finding_collection.json) has one record per lifecycle state. The [advisory profile](data/synthetic/apache_cve_2021_41773_profile.json) and [observation](data/synthetic/apache_cve_2021_41773_observation.json) demonstrate the comparison interface. Profile contents are maintained data and must be reviewed against the cited advisory before any new use.

## Traffic or Data Flow

There is no network traffic. The collection command parses local JSON, runs schema and evidence-field checks, and writes a Markdown report only if all records pass. The advisory command reads two local objects and returns `not_applicable`, `insufficient_evidence`, or `applicable_in_synthetic_model`. A missing required condition preserves uncertainty.

## Validation

From this directory, run:

```sh
python3 -m unittest discover -s tests -v
python3 src/report_findings.py data/synthetic/finding_collection.json --output /tmp/cef001-report.md
python3 src/advisory_assessment.py data/synthetic/apache_cve_2021_41773_profile.json data/synthetic/apache_cve_2021_41773_observation.json --output /tmp/cef001-advisory.md
```

The current suite contains 22 tests. See [validation details](validation/README.md) and compare local output with the [sample collection report](examples/sample_report.md) and [sample advisory report](examples/sample_advisory_assessment.md).

## Troubleshooting

If a collection is rejected, the command prints all structural errors with record positions. A duplicate `finding_id` or absent evidence field prevents report generation. If the advisory result is `insufficient_evidence`, compare the observation's `conditions` object to the profile's `required_conditions`. Do not fill a missing field with a guessed value; record how that condition would be verified.

## Reproduction Guide

1. Clone the repository and enter `projects/cef-001`; Python 3.9+ is the only runtime dependency.
2. Run the unit-test command above in a clean directory. It needs no network or credentials.
3. Run the collection and advisory commands. Open the two generated `/tmp` reports and compare status/count/conclusion with the included samples.
4. Copy a fixture to a local scratch path, remove one required condition, and rerun the advisory command. The expected result is `insufficient_evidence`.
5. For rollback, delete only local scratch output and restore the copied fixture. Keep original synthetic fixtures unchanged so test results remain comparable.

## Project Completion

The local validator, reporter, advisory comparator, synthetic fixtures, generated samples, and 22 unit tests are implemented. The tests cover the stated local behavior. The project remains active: no live target is scanned, no real remediation is performed, and no actual post-change retest is recorded. A later authorized workflow would need independent advisory review, vendor-specific version handling, and comparable pre/post system observations.

## Limitations

Exact-version matching is narrow by design. A syntactically valid record cannot establish that an observed product is truly present or vulnerable. The `applicable_in_synthetic_model` result describes only the supplied fixture and profile. The sample reports are `synthetic-example` artifacts.

## Repository Contents

- [`src/`](src/) — Python implementation.
- [`tests/`](tests/) — unit tests.
- [`data/synthetic/`](data/synthetic/) — local fixtures.
- [`examples/`](examples/) — generated sample Markdown reports.
- [`validation/`](validation/README.md) — test coverage and pass/fail expectations.
- [`DEPENDENCIES.md`](DEPENDENCIES.md) — runtime and dependency notes.
