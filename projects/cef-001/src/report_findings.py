#!/usr/bin/env python3
"""Validate synthetic finding collections and render a deterministic evidence report.

The tool is offline: it reads local JSON only. A structural pass does not prove
that a real system is vulnerable, remediated, or safely retested.
"""

from __future__ import annotations

import argparse
import json
import html
from collections import Counter
from pathlib import Path
from typing import Any

from validate_findings import REQUIRED_BY_STATUS, validate


def load_collection(path: Path) -> list[dict[str, Any]]:
    """Load a JSON array of finding objects or raise ValueError with context."""
    try:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("could not read JSON collection: {}".format(exc)) from exc
    if not isinstance(data, list):
        raise ValueError("collection must be a JSON array")
    if not all(isinstance(record, dict) for record in data):
        raise ValueError("every collection item must be a JSON object")
    return data


def validate_collection(records: list[dict[str, Any]]) -> list[str]:
    """Return all collection and record errors without stopping at the first."""
    errors: list[str] = []
    seen_ids: set[str] = set()
    for position, record in enumerate(records, start=1):
        finding_id = record.get("finding_id")
        label = "record {}".format(position)
        if not isinstance(finding_id, str) or not finding_id.strip():
            errors.append("{} requires a non-empty finding_id".format(label))
        elif finding_id in seen_ids:
            errors.append("duplicate finding_id: {}".format(finding_id))
        else:
            seen_ids.add(finding_id)
        errors.extend("{}: {}".format(label, error) for error in validate(record))
    if not records:
        errors.append("collection must contain at least one finding record")
    return errors


def _cell(value: object) -> str:
    """Keep untrusted JSON strings inside one Markdown table cell."""
    cleaned = str(value).replace("\r", " ").replace("\n", " ").strip()
    escaped = html.escape(cleaned, quote=True)
    for character, entity in (("\\", "&#92;"), ("|", "&#124;"), ("`", "&#96;"), ("*", "&#42;"), ("_", "&#95;"), ("[", "&#91;"), ("]", "&#93;"), ("!", "&#33;")):
        escaped = escaped.replace(character, entity)
    return escaped


def render_markdown(records: list[dict[str, Any]], source_name: str) -> str:
    """Render a stable report after validation has passed."""
    counts = Counter(record["status"] for record in records)
    lines = [
        "# Synthetic Finding Evidence Report",
        "",
        "- **Source:** {}".format(_cell(source_name)),
        "- **Records:** {}".format(len(records)),
        "- **Scope:** Offline synthetic-data validation only.",
        "- **Limitation:** A structural pass does not confirm a live vulnerability, remediation, or retest outcome.",
        "",
        "## Status summary",
        "",
    ]
    for status in REQUIRED_BY_STATUS:
        lines.append("- **{}:** {}".format(status, counts.get(status, 0)))
    lines.extend(["", "## Records", "", "| Finding ID | Status | Structural gate |", "|---|---|---|"])
    for record in sorted(records, key=lambda item: item["finding_id"]):
        lines.append("| {} | {} | Passed |".format(_cell(record["finding_id"]), _cell(record["status"])))
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Each record passed the local evidence-field gate for its declared status. Human review and authorized evidence remain required before any claim about a non-synthetic system.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", type=Path, help="path to a JSON array of finding records")
    parser.add_argument("--output", type=Path, help="write Markdown report to this local path")
    args = parser.parse_args()
    try:
        records = load_collection(args.collection)
    except ValueError as exc:
        parser.error(str(exc))
    errors = validate_collection(records)
    if errors:
        print("REJECTED")
        print("\n".join("- " + error for error in errors))
        return 1
    report = render_markdown(records, args.collection.name)
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
        except OSError as exc:
            parser.error("could not write report: {}".format(exc))
        print("WROTE: {}".format(args.output))
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
