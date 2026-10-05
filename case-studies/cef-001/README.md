# Synthetic Vulnerability Evidence Pipeline (active project)

## Recruiter summary

This active Python project organizes vulnerability work into discovery, advisory correlation, applicability review, remediation, and retesting. It uses labeled synthetic JSON and a local advisory profile to prevent a product/version match from being reported as a confirmed live vulnerability. The implementation and documentation were AI-assisted under my direction; my independent review and live-system validation remain future checkpoints.

## Problem or objective

A service banner and a matching CVE can start an investigation, but they do not establish that the advisory applies to a particular host. The pipeline requires stronger evidence as a record moves through the lifecycle. It keeps uncertainty visible when a prerequisite or approval is missing.

## Environment and technologies

Python 3 standard library, local JSON fixtures, deterministic Markdown reports, and unit tests. There is no scanner, network request, credential test, exploitation step, or live target.

## My contribution and team context

I set the project direction and scope as owner. Codex produced the current code, tests, and documentation with AI assistance. No independent handwritten coding claim or professional assessment claim is made here. The private project record retains the detailed implementation and test evidence.

## Architecture and implementation

One validator checks whether each finding has the fields required for its lifecycle state. A collection reporter rejects empty, malformed, or duplicate records and renders a stable summary only after validation. A separate advisory assessor compares a synthetic product observation to a local profile with exact product, version, and condition checks. It can report `not_applicable`, `insufficient_evidence`, or `applicable_in_synthetic_model`; the last result deliberately says nothing about a real system.

## Validation procedure and result

The private test suite covers valid records, missing evidence, duplicates, malformed collections, mismatched products or versions, missing conditions, and rejection of non-synthetic input. The current local run passed 22 unit tests. A five-record fixture rendered one example for each lifecycle state. These are software behavior checks, not security measurements or real remediation results.

## Problems, troubleshooting, and resolution

The central design problem was avoiding overconfident applicability language. The resolution was to require explicit condition evidence and to return `insufficient_evidence` when a required condition is absent. The public overview does not claim a field troubleshooting incident for this synthetic project.

## Security significance and skills demonstrated

The workflow makes an analyst state what was observed, which advisory was consulted, which conditions match, what change was selected, and what comparable retest followed. It demonstrates an evidence model and tested Python validation logic. It does not demonstrate live vulnerability discovery or patch effectiveness.

## Evidence basis and limitations

The private source, fixtures, 22 tests, and generated reports support the implementation claims. Fixtures are invented. Advisory profiles can be incomplete, exact-version matching is intentionally narrow, and human review is required before any applicability or remediation decision on a real system.

## Production improvements

Future work would add an authorized target scope, authoritative advisory review, version parsing appropriate to each vendor, comparable pre/post evidence, and a reviewer sign-off. Those changes would require new tests and a clear data-handling plan.

## Interview talking points

- Explain why CVE correlation is not applicability.
- Identify the evidence needed to move from discovery to a supported applicability assessment.
- Explain why missing conditions return uncertainty rather than a positive result.
- Describe a comparable retest and why a schema-valid record cannot prove remediation.

## AI assistance

Codex created the current implementation and portfolio draft under my direction. See [AI assistance](../../AI_ASSISTANCE.md). My personal technical validation remains a **HUMAN CHECKPOINT** before I present this as independent coding experience.
