#!/usr/bin/env python3
"""Validate local, synthetic vulnerability-evidence lifecycle records.

This tool is offline. It validates claims supplied in JSON; it does not scan
hosts, confirm CVEs, or substitute for human review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_BY_STATUS = {
    "discovered": ("observation",),
    "correlated": ("observation", "correlation"),
    "applicable": (
        "observation", "correlation", "authoritative_source", "product_identity",
        "affected_range_evidence", "prerequisite_evidence", "human_approval",
    ),
    "remediated": ("remediation", "remediation_validation"),
    "retested": ("retest_method", "baseline_reference", "retest_result"),
}


def validate(record: dict[str, Any]) -> list[str]:
    """Return structural-evidence errors; an empty list passes the gate."""
    errors: list[str] = []
    if record.get("synthetic") is not True:
        errors.append("synthetic must be true during the startup phase")
    status = record.get("status")
    if status not in REQUIRED_BY_STATUS:
        return errors + ["status must be one of: {}".format(", ".join(REQUIRED_BY_STATUS))]
    stages = list(REQUIRED_BY_STATUS)
    for stage in stages[: stages.index(status) + 1]:
        for field in REQUIRED_BY_STATUS[stage]:
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append("{} status requires non-empty {}".format(status, field))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="path to one JSON finding record")
    args = parser.parse_args()
    try:
        with args.record.open(encoding="utf-8") as handle:
            record = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error("could not read JSON record: {}".format(exc))
    if not isinstance(record, dict):
        parser.error("record must be a JSON object")
    errors = validate(record)
    if errors:
        print("REJECTED")
        print("\n".join("- " + error for error in errors))
        return 1
    print("ACCEPTED: structural evidence gate passed for {}".format(record["status"]))
    print("This does not confirm a live vulnerability or remediation outcome.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
