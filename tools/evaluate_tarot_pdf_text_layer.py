#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_pdf_text_layer_gate
#   module_name: tarot_pdf_text_layer_gate
#   module_kind: experiment
#   summary: executes the frozen MuPDF embedded-text adequacy gate over the two exact acquired Wellcome PDFs without OCR or semantic inspection
#   owner: Erin Spencer
#   public_surface: evaluate_pages, run_gate, main
#   internal_surface: _verify_backend, _extract_pages, _canonical_bytes
#   auth_boundary: none
#   storage_boundary: read exact acquired PDFs, temporary extracted pages, and one caller-selected report
#   network_boundary: none
#   user_data_boundary: none; public-domain archival evidence only
#   admin_only: false
#   tests: tests.test_tarot_pdf_text_layer_gate
#   rollout: explicit CLI after frozen preregistration only
#   rollback: remove experiment tool, tests, reports, and protocol without changing source evidence
#   requires: edcm_tarot_corpus_acquirer
#   since: 2026-08-16
#   unresolved: OCR backend and accuracy law if embedded text is insufficient
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_text_gate_uses_exact_frozen_inputs_and_backend
#   given: the embedded-text gate runs
#   then: both PDF digests, page counts, MuPDF version, executable digest, command, and timeout match the preregistration
#   class: evidence
#   since: 2026-08-16
#
# id: tarot_text_gate_applies_frozen_adequacy_rule
#   given: exact per-page text bytes are extracted
#   then: only preregistered non-whitespace, alphanumeric, replacement, coverage, and total thresholds determine the verdict
#   class: correctness
#   since: 2026-08-16
#
# id: tarot_text_gate_retains_nonclaims_and_failure
#   given: the gate completes or fails
#   then: FALSIFIED, SURVIVED, or BLOCKED is recorded without OCR fallback, semantic inspection, ontology, geometry, measurement, or canon escalation
#   class: doctrine
#   since: 2026-08-16
# === END CONTRACTS ===

"""Execute the preregistered Tarot PDF embedded-text adequacy gate."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Any

BACKEND_VERSION = "mutool version 1.23.10"
BACKEND_SHA256 = "9203440040cc38ee412aeedbfe57f452d6b85709c5b1600ca6ab2aa05478ab73"
TIMEOUT_SECONDS = 300
INPUTS = (
    ("wellcome_etteilla_1783_1785", "wellcome_etteilla_1783_1785.pdf", "d44fc8bf81e5356fa1f05d11a9e92723ee36efe94b3af2def5c1c97e80ff5c0f", 401, 361, 100_000),
    ("wellcome_etteilla_tableau_1780s", "wellcome_etteilla_tableau_1780s.pdf", "d3a2e8e82c79e9a109e662e53ff034dcabc7f2902c52dcde10fec9d3529f5381", 6, 5, 500),
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode() + b"\n"


def _sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def evaluate_pages(pages: list[str], *, required_pages: int, required_total: int) -> dict[str, Any]:
    rows = []
    for index, text in enumerate(pages, 1):
        nonspace = sum(not char.isspace() for char in text)
        alphanumeric = sum(char.isalnum() for char in text)
        replacement = text.count("\ufffd")
        rows.append({"page": index, "non_whitespace": nonspace, "alphanumeric": alphanumeric, "replacement": replacement, "sha256": sha256(text.encode()).hexdigest()})
    total = sum(row["non_whitespace"] for row in rows)
    alpha = sum(row["alphanumeric"] for row in rows)
    replacement = sum(row["replacement"] for row in rows)
    populated = sum(row["non_whitespace"] >= 100 for row in rows)
    checks = {
        "populated_pages": populated >= required_pages,
        "total_non_whitespace": total >= required_total,
        "alphanumeric_fraction": total > 0 and alpha * 2 >= total,
        "replacement_fraction": total > 0 and replacement * 100 <= total,
    }
    return {"pages": rows, "totals": {"pages": len(rows), "populated_pages": populated, "non_whitespace": total, "alphanumeric": alpha, "replacement": replacement}, "checks": checks, "passed": all(checks.values())}


def run_gate(raw_dir: Path) -> dict[str, Any]:
    backend = shutil.which("mutool")
    if backend is None:
        return {"schema": "edcm.tarot-pdf-text-layer-gate", "version": "1.0.0", "status": "BLOCKED", "failure": "mutool missing"}
    backend_path = Path(backend)
    version = subprocess.run(
        [backend, "-v"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).stdout.strip()
    if version != BACKEND_VERSION or _sha(backend_path) != BACKEND_SHA256:
        return {"schema": "edcm.tarot-pdf-text-layer-gate", "version": "1.0.0", "status": "BLOCKED", "failure": "backend identity mismatch"}
    results = []
    with tempfile.TemporaryDirectory(prefix="edcm-tarot-text-") as temporary:
        root = Path(temporary)
        for source_id, filename, digest, page_count, required_pages, required_total in INPUTS:
            source = raw_dir / filename
            if not source.is_file() or _sha(source) != digest:
                return {"schema": "edcm.tarot-pdf-text-layer-gate", "version": "1.0.0", "status": "BLOCKED", "failure": f"input identity mismatch: {source_id}"}
            output = root / source_id / "page-%04d.txt"
            output.parent.mkdir()
            subprocess.run([backend, "draw", "-q", "-F", "txt", "-o", str(output), str(source)], check=True, timeout=TIMEOUT_SECONDS)
            paths = sorted(output.parent.glob("page-*.txt"))
            if len(paths) != page_count:
                return {"schema": "edcm.tarot-pdf-text-layer-gate", "version": "1.0.0", "status": "BLOCKED", "failure": f"page count mismatch: {source_id}"}
            evaluation = evaluate_pages([path.read_text(encoding="utf-8") for path in paths], required_pages=required_pages, required_total=required_total)
            evaluation["source_id"] = source_id
            evaluation["input_sha256"] = digest
            results.append(evaluation)
    verdict = "SURVIVED" if all(item["passed"] for item in results) else "FALSIFIED"
    return {"schema": "edcm.tarot-pdf-text-layer-gate", "version": "1.0.0", "backend": {"version": version, "sha256": BACKEND_SHA256, "command": "mutool draw -q -F txt -o page-%04d.txt INPUT.pdf"}, "results": results, "status": verdict, "ocr": "not-run", "semantic_inspection": "not-run", "ontology_selected": False, "geometry_attached": False, "measurement_attached": False, "canon_selection": None}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = run_gate(args.raw_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(_canonical_bytes(report))
    print(json.dumps({"status": report["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
