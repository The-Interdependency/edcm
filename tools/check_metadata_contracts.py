#!/usr/bin/env python3
"""Validate EDCM-native MODULE_BUILD declarations.

Usage:

    python tools/check_metadata_contracts.py

The checker is intentionally repository-specific. Canonical block parsing and
collection remain owned by skill-lib/msdmd; this gate enforces EDCM's declared
native-module policy and verifies that metadata test references resolve to real
files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

BLOCK_RE = re.compile(
    r"^[ \t]*# === MODULE_BUILD ===\s*$"
    r"(?P<body>.*?)"
    r"^[ \t]*# === END MODULE_BUILD ===\s*$",
    re.MULTILINE | re.DOTALL,
)
ID_RE = re.compile(r"^[ \t]*# id:\s*(?P<value>.+?)\s*$", re.MULTILINE)
FIELD_RE = re.compile(
    r"^[ \t]*#\s{3}(?P<key>[a-zA-Z0-9_]+):\s*(?P<value>.*?)\s*$",
    re.MULTILINE,
)

REQUIRED_FIELDS = (
    "module_name",
    "module_kind",
    "summary",
    "owner",
    "public_surface",
    "internal_surface",
    "auth_boundary",
    "storage_boundary",
    "network_boundary",
    "user_data_boundary",
    "admin_only",
    "tests",
    "rollout",
    "rollback",
    "requires",
    "since",
    "unresolved",
)

NON_HMMM_FIELDS = tuple(field for field in REQUIRED_FIELDS if field != "unresolved")


@dataclass(frozen=True)
class Finding:
    path: str
    code: str
    detail: str


@dataclass(frozen=True)
class Report:
    passed: bool
    modules_checked: int
    findings: tuple[Finding, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "modules_checked": self.modules_checked,
            "findings": [asdict(finding) for finding in self.findings],
        }


def native_modules(root: Path) -> tuple[Path, ...]:
    paths = list((root / "edcm").glob("*.py"))
    paths.extend((root / "edcm" / "edcmucns").rglob("*.py"))
    return tuple(sorted(path for path in paths if path.is_file()))


def parse_module_build(path: Path) -> tuple[str | None, dict[str, str], list[Finding]]:
    text = path.read_text(encoding="utf-8")
    matches = list(BLOCK_RE.finditer(text))
    findings: list[Finding] = []
    relative = path.as_posix()
    if len(matches) != 1:
        findings.append(
            Finding(
                relative,
                "MODULE_BUILD_COUNT",
                f"expected exactly one MODULE_BUILD block, found {len(matches)}",
            )
        )
        return None, {}, findings

    body = matches[0].group("body")
    id_match = ID_RE.search(body)
    block_id = id_match.group("value").strip() if id_match else None
    if not block_id:
        findings.append(Finding(relative, "MISSING_ID", "MODULE_BUILD id is missing"))

    fields = {match.group("key"): match.group("value").strip() for match in FIELD_RE.finditer(body)}
    for field in REQUIRED_FIELDS:
        if field not in fields or not fields[field]:
            findings.append(
                Finding(relative, "MISSING_FIELD", f"required field {field!r} is missing")
            )
    for field in NON_HMMM_FIELDS:
        if fields.get(field, "").lower() == "hmmm":
            findings.append(
                Finding(
                    relative,
                    "UNRESOLVED_REQUIRED_FIELD",
                    f"required operational field {field!r} remains hmmm",
                )
            )
    return block_id, fields, findings


def candidate_test_paths(reference: str, root: Path) -> Iterable[Path]:
    clean = reference.strip().strip("`")
    if not clean:
        return ()
    clean = clean.split("::", 1)[0].strip()
    if clean.endswith(".py") or "/" in clean:
        return (root / clean,)
    if clean.startswith("tests."):
        return (root / Path(*clean.split(".")).with_suffix(".py"),)
    if clean.startswith("test_"):
        return (root / "tests" / f"{clean}.py",)
    return ()


def verify_test_references(path: Path, tests_field: str, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    relative = path.relative_to(root).as_posix()
    references = [value.strip() for value in tests_field.split(",") if value.strip()]
    if not references:
        return [Finding(relative, "EMPTY_TESTS", "tests field contains no references")]

    for reference in references:
        candidates = tuple(candidate_test_paths(reference, root))
        if not candidates:
            findings.append(
                Finding(
                    relative,
                    "UNPARSEABLE_TEST_REFERENCE",
                    f"cannot resolve test reference {reference!r}",
                )
            )
            continue
        if not any(candidate.is_file() for candidate in candidates):
            findings.append(
                Finding(
                    relative,
                    "MISSING_TEST_REFERENCE",
                    f"test reference {reference!r} does not resolve to a file",
                )
            )
    return findings


def run(root: Path) -> Report:
    root = root.resolve()
    findings: list[Finding] = []
    seen_ids: dict[str, str] = {}
    modules = native_modules(root)

    for path in modules:
        block_id, fields, module_findings = parse_module_build(path)
        normalized_findings = [
            Finding(path.relative_to(root).as_posix(), finding.code, finding.detail)
            for finding in module_findings
        ]
        findings.extend(normalized_findings)
        if block_id:
            previous = seen_ids.get(block_id)
            if previous:
                findings.append(
                    Finding(
                        path.relative_to(root).as_posix(),
                        "DUPLICATE_ID",
                        f"MODULE_BUILD id {block_id!r} already used by {previous}",
                    )
                )
            else:
                seen_ids[block_id] = path.relative_to(root).as_posix()
        tests_field = fields.get("tests")
        if tests_field and tests_field.lower() != "hmmm":
            findings.extend(verify_test_references(path, tests_field, root))

    return Report(
        passed=not findings,
        modules_checked=len(modules),
        findings=tuple(findings),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="EDCM repository root")
    args = parser.parse_args()
    report = run(Path(args.root))
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
