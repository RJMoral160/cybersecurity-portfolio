#!/usr/bin/env python3
"""Assess a synthetic observation against a local public-advisory profile.

This offline tool compares supplied fields only. It does not retrieve an
advisory, scan a host, or prove a real system is vulnerable.
"""

from __future__ import annotations

import argparse
import json
import html
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


PROFILE_FIELDS = (
    "cve", "vendor", "product", "affected_versions", "fixed_version",
    "source_url", "required_conditions",
)


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("could not read {}: {}".format(label, exc)) from exc
    if not isinstance(value, dict):
        raise ValueError("{} must be a JSON object".format(label))
    return value


def validate_profile(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in PROFILE_FIELDS:
        if field not in profile:
            errors.append("profile requires {}".format(field))
    for field in ("cve", "vendor", "product", "fixed_version"):
        if field in profile and (not isinstance(profile[field], str) or not profile[field].strip()):
            errors.append("profile {} must be non-empty text".format(field))
    versions = profile.get("affected_versions")
    if not isinstance(versions, list) or not versions or any(not isinstance(v, str) or not v.strip() for v in versions):
        errors.append("profile affected_versions must be a non-empty array of non-empty strings")
    conditions = profile.get("required_conditions")
    if not isinstance(conditions, dict):
        errors.append("profile required_conditions must be an object")
    elif not conditions:
        errors.append("profile required_conditions must not be empty; use a separately reviewed no-prerequisite profile")
    elif any(not isinstance(k, str) or not k.strip() or type(v) is not bool for k, v in conditions.items()):
        errors.append("profile required_conditions must map non-empty names to booleans")
    source = profile.get("source_url")
    try:
        parsed = urlparse(source) if isinstance(source, str) else None
        valid_url = bool(parsed and parsed.scheme == "https" and parsed.hostname and "." in parsed.hostname and parsed.path not in ("", "/") and not parsed.username and not parsed.password and not any(character.isspace() for character in source))
        if parsed:
            _ = parsed.port  # Invalid port syntax raises ValueError.
    except ValueError:
        valid_url = False
    if not valid_url:
        errors.append("profile source_url must be an HTTPS URL")
    return errors


def assess(profile: dict[str, Any], observation: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative applicability conclusion and its evidence gaps."""
    result: dict[str, Any] = {
        "cve": profile.get("cve"),
        "conclusion": "insufficient_evidence",
        "reasons": [],
        "missing_conditions": [],
        "limitations": [
            "Synthetic/offline assessment only; no system was contacted.",
            "A matching profile does not replace human review or authorized validation.",
        ],
    }
    if observation.get("synthetic") is not True:
        result["reasons"].append("observation is not labeled synthetic")
        return result
    product = observation.get("product")
    if not isinstance(product, str) or not product.strip():
        result["reasons"].append("observed product identity is missing or invalid")
        return result
    if product != profile.get("product"):
        result["conclusion"] = "not_applicable"
        result["reasons"].append("observed product does not match advisory profile")
        return result
    version = observation.get("version")
    if not isinstance(version, str) or not version.strip():
        result["reasons"].append("observed version is missing")
        return result
    if version not in profile.get("affected_versions", []):
        result["conclusion"] = "not_applicable"
        result["reasons"].append("observed version is outside the profile's affected versions")
        return result
    conditions = observation.get("conditions")
    if not isinstance(conditions, dict):
        result["reasons"].append("observed conditions are missing")
        return result
    mismatches = []
    for name, expected in profile.get("required_conditions", {}).items():
        if name not in conditions:
            result["missing_conditions"].append(name)
        elif type(conditions[name]) is not bool:
            result["missing_conditions"].append(name)
        elif conditions[name] != expected:
            mismatches.append(name)
    if result["missing_conditions"]:
        result["reasons"].append("required configuration evidence is incomplete")
        return result
    if mismatches:
        result["conclusion"] = "not_applicable"
        result["reasons"].append("one or more required conditions do not match")
        result["mismatched_conditions"] = mismatches
        return result
    result["conclusion"] = "applicable_in_synthetic_model"
    result["reasons"].append("affected version and required synthetic conditions match")
    return result


def render_markdown(profile: dict[str, Any], result: dict[str, Any]) -> str:
    def safe(value: object) -> str:
        return html.escape(str(value), quote=True).replace("\\", "&#92;").replace("`", "&#96;").replace("*", "&#42;").replace("[", "&#91;").replace("]", "&#93;").replace("\n", " ").replace("\r", " ")

    reasons = result["reasons"] or ["No additional reason recorded."]
    lines = [
        "# Synthetic Advisory Assessment",
        "",
        "- **CVE:** {}".format(safe(result["cve"])),
        "- **Product:** {}".format(safe(profile["product"])),
        "- **Authoritative advisory:** {}".format(safe(profile["source_url"])),
        "- **Conclusion:** {}".format(safe(result["conclusion"])),
        "",
        "## Reasons",
        "",
    ]
    lines.extend("- {}".format(safe(reason)) for reason in reasons)
    if result["missing_conditions"]:
        lines.extend(["", "## Missing evidence", ""])
        lines.extend("- {}".format(safe(item)) for item in result["missing_conditions"])
    if result.get("mismatched_conditions"):
        lines.extend(["", "## Mismatched conditions", ""])
        lines.extend("- {}".format(safe(item)) for item in result["mismatched_conditions"])
    lines.extend(["", "## Limitations", ""])
    lines.extend("- {}".format(safe(item)) for item in result["limitations"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("observation", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        profile = load_object(args.profile, "profile")
        observation = load_object(args.observation, "observation")
    except ValueError as exc:
        parser.error(str(exc))
    errors = validate_profile(profile)
    if errors:
        print("REJECTED PROFILE")
        print("\n".join("- " + error for error in errors))
        return 1
    report = render_markdown(profile, assess(profile, observation))
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
