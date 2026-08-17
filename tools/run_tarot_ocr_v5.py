#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_ocr_v5_runner
#   module_name: tarot_ocr_v5_runner
#   module_kind: experiment
#   summary: executes the frozen Tarot OCR v5 adaptive-threshold protocol through the v4 evidence-preserving core
#   owner: Erin Spencer
#   public_surface: command-line interface
#   internal_surface: frozen Sauvola OCR command and v4 resumable corpus core
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_tarot_ocr_v5
#   rollout: explicit CLI only after protocol commit 9199f2d
#   rollback: remove this adapter without altering v4 evidence or protocols
#   requires: edcm_tarot_ocr_v4_runner
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_ocr_v5_changes_only_frozen_thresholding
#   given: a v5 page OCR request
#   then: the exact v4 command gains only thresholding_method=2 and retains raw TXT/TSV evidence
#   class: evidence
#
# id: tarot_ocr_v5_retains_v4_evidence_contracts
#   given: a complete or resumed v5 run
#   then: frozen identities, page evidence, validation, deterministic serialization, and fail-closed resume use the v4 core with v5 identities
#   class: correctness
# === END CONTRACTS ===

"""Execute the frozen Tarot OCR v5 adaptive-threshold experiment.

Usage:
    python3 tools/run_tarot_ocr_v5.py \
      --acquisition artifacts/tarot/acquisition-v1 \
      --reference experiments/tarot/tarot-ocr-validation-reference-v4.json \
      --output artifacts/tarot/ocr-v5/run-a

V5 changes only Tesseract's thresholding method to fixed-default Sauvola. The
command has no network path. It preserves every v4 source, producer, raw-page,
validation, resource, resume, and nonclaim boundary.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys

try:
    from tools import run_tarot_ocr_v4 as core
except ModuleNotFoundError:  # Direct ``python tools/run_tarot_ocr_v5.py`` use.
    import run_tarot_ocr_v4 as core


PROTOCOL_COMMIT = "9199f2dc3830bab11486c359b5e1f9e9974b36fb"
PROTOCOL_SHA256 = "625acfea972dfe882afd4742db3608cf67f7828d898b6725678e19b2b586661c"
INSTRUMENT = {
    "thresholding_method": "2",
    "thresholding_name": "Sauvola",
    "thresholding_window_size": "0.33",
    "thresholding_kfactor": "0.34",
    "all_other_v4_fields": "unchanged",
}


def ocr_command(tesseract: Path, png: Path, base: Path) -> list[str]:
    return [
        str(tesseract), str(png), str(base), "-l", "fra", "--oem", "1",
        "--psm", "3", "-c", "thresholding_method=2", "txt", "tsv",
    ]


def render_and_ocr(
    mutool: Path,
    tesseract: Path,
    pdf: Path,
    output: Path,
    source: core.Source,
    page: int,
) -> dict[str, object]:
    png, txt, tsv = core.page_paths(output, source, page)
    png.parent.mkdir(parents=True, exist_ok=True)
    render = subprocess.run(
        [str(mutool), "draw", "-q", "-N", "-r", "300", "-c", "gray", "-F", "png", "-o", str(png), str(pdf), str(page)],
        capture_output=True,
        timeout=core.RENDER_TIMEOUT,
    )
    if render.returncode or render.stdout or render.stderr:
        raise core.ProtocolBlocked(f"renderer output/error: {source.source_id} page {page}")
    environment = dict(os.environ)
    environment["OMP_THREAD_LIMIT"] = "1"
    ocr = subprocess.run(
        ocr_command(tesseract, png, txt.with_suffix("")),
        capture_output=True,
        timeout=core.OCR_TIMEOUT,
        env=environment,
    )
    if ocr.returncode:
        raise core.ProtocolBlocked(f"OCR producer error: {source.source_id} page {page}")
    if not txt.is_file() or not tsv.is_file():
        raise core.ProtocolBlocked(f"missing OCR output: {source.source_id} page {page}")
    return core.record_for(source, page, png, txt, tsv)


def run(acquisition: Path, reference: Path, output: Path, resume: bool) -> dict[str, object]:
    return core.run(
        acquisition,
        reference,
        output,
        resume,
        version="5.0.0",
        protocol_commit=PROTOCOL_COMMIT,
        page_producer=render_and_ocr,
        instrument={**INSTRUMENT, "protocol_sha256": PROTOCOL_SHA256},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acquisition", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args.acquisition, args.reference, args.output, args.resume)
    except (core.ProtocolBlocked, subprocess.TimeoutExpired, UnicodeError, csv.Error, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "failure": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if result["status"] == "FALSIFIED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
