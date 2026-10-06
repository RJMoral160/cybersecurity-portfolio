#!/usr/bin/env python3
"""Offline links, fixture, diagram, address, and privacy checks.

Static Mermaid inspection is not rendering. Pass --render only when the
official Mermaid CLI (`mmdc`) is installed; output goes to a temp directory.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
ADDRESS = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
PRIVATE_NETS = [ipaddress.ip_network(v) for v in (
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "127.0.0.0/8",
    "192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24",
)]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b44\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
]
DENIED_SUFFIXES = {".docx", ".pdf", ".p12", ".pfx", ".pem", ".key", ".private", ".pcap", ".pcapng"}


def files():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    return sorted({ROOT / name for name in result.stdout.splitlines() if (ROOT / name).is_file()})


def slug(heading):
    heading = re.sub(r"<[^>]+>", "", heading).lower().strip()
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def check_links(path, body):
    failures = []
    for raw in MARKDOWN_LINK.findall(body):
        url = raw.split(" ", 1)[0].strip("<>")
        if "://" in url or url.startswith(("mailto:", "#")) and not url.startswith("#"):
            continue
        target, _, fragment = url.partition("#")
        destination = (path.parent / unquote(target)).resolve() if target else path
        if not destination.is_relative_to(ROOT) or not destination.exists():
            failures.append("{}: broken local link {}".format(path.relative_to(ROOT), raw))
        elif fragment and destination.is_file() and destination.suffix == ".md":
            headings = {slug(line.lstrip("# ")) for line in destination.read_text(encoding="utf-8").splitlines() if line.startswith("#")}
            if unquote(fragment).lower() not in headings:
                failures.append("{}: missing anchor {}".format(path.relative_to(ROOT), raw))
    return failures


def check_diagrams(path, body, render, tempdir, mmdc, puppeteer_config):
    failures = []
    openings = body.count("```mermaid")
    blocks = MERMAID_BLOCK.findall(body)
    if openings != len(blocks):
        failures.append("{}: unclosed Mermaid fence".format(path.relative_to(ROOT)))
    for index, diagram in enumerate(blocks, 1):
        if not re.match(r"\s*(flowchart|graph|sequenceDiagram)\b", diagram):
            failures.append("{}: unknown Mermaid start in block {}".format(path.relative_to(ROOT), index))
        if render:
            source = tempdir / (path.stem + "-" + str(index) + "-" + str(abs(hash(str(path)))) + ".mmd")
            output = source.with_suffix(".svg")
            source.write_text(diagram, encoding="utf-8")
            command = [mmdc, "-i", str(source), "-o", str(output)]
            if puppeteer_config:
                command.extend(["-p", str(puppeteer_config)])
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode or not output.is_file():
                failures.append("{}: Mermaid render failed block {}: {}".format(path.relative_to(ROOT), index, result.stderr[:1000]))
    return failures, len(blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true", help="render all Mermaid blocks using installed mmdc")
    parser.add_argument("--mmdc", default="mmdc", help="path to Mermaid CLI, used with --render")
    parser.add_argument("--puppeteer-config", type=Path, help="Mermaid CLI browser configuration for --render")
    args = parser.parse_args()
    if args.render and not shutil.which(args.mmdc):
        parser.error("--render requires Mermaid CLI (mmdc)")
    failures = []
    diagram_count = 0
    with tempfile.TemporaryDirectory(prefix="portfolio-diagrams-") as temporary:
        for path in files():
            relative = path.relative_to(ROOT)
            if path.suffix.lower() in DENIED_SUFFIXES or any(part.lower() in {"coursework", "transcripts", "resumes", "private", "source-reports"} for part in relative.parts):
                failures.append("{}: private/binary artifact in tree".format(relative))
                continue
            if path.suffix == ".json":
                try:
                    json.loads(path.read_text(encoding="utf-8"))
                except (ValueError, UnicodeError) as exc:
                    failures.append("{}: invalid JSON: {}".format(relative, exc))
            if path.suffix not in {".md", ".cfg", ".conf", ".zone", ".json", ".py", ".yml", ".yaml"} and path.name != ".gitignore":
                continue
            try:
                body = path.read_text(encoding="utf-8")
            except UnicodeError:
                failures.append("{}: non-UTF-8 text".format(relative))
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(body):
                    failures.append("{}: forbidden secret/address pattern".format(relative))
            if path.suffix == ".md":
                failures.extend(check_links(path, body))
                diagram_errors, count = check_diagrams(path, body, args.render, Path(temporary), args.mmdc, args.puppeteer_config)
                failures.extend(diagram_errors)
                diagram_count += count
            for match in ADDRESS.finditer(body):
                candidate = match.group()
                try:
                    address = ipaddress.ip_address(candidate)
                except ValueError:
                    failures.append("{}: invalid IPv4 {}".format(relative, candidate))
                    continue
                if not any(address in network for network in PRIVATE_NETS) and not candidate.startswith(("255.", "0.0.0.")) and candidate != "0.0.0.0":
                    failures.append("{}: non-documentation public IPv4 {}".format(relative, candidate))
    for error in failures:
        print("FAIL:", error)
    print("Checked repository files; Mermaid blocks: {}; rendered: {}; failures: {}".format(diagram_count, args.render, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
