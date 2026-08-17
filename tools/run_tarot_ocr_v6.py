#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_ocr_v6_runner
#   module_name: tarot_ocr_v6_runner
#   module_kind: experiment
#   summary: executes the frozen Tarot OCR v6 historic-print model protocol through the v4 evidence-preserving core
#   owner: Erin Spencer
#   public_surface: command-line interface
#   internal_surface: historic-model verification, frozen OCR command, and v4 resumable corpus core
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_tarot_ocr_v6
#   rollout: explicit CLI only after protocol commit c63ad40
#   rollback: remove this adapter without altering earlier evidence or protocols
#   requires: edcm_tarot_ocr_v4_runner
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_ocr_v6_verifies_historic_model
#   given: a v6 execution request
#   then: the external model filename, byte count, and SHA-256 must match before any producer runs
#   class: evidence
#
# id: tarot_ocr_v6_changes_only_frozen_model
#   given: a v6 page OCR request
#   then: the v5 command replaces only the language model and model directory while retaining Sauvola, OEM, PSM, TXT, and TSV
#   class: evidence
#
# id: tarot_ocr_v6_retains_v4_evidence_contracts
#   given: a complete or resumed v6 run
#   then: frozen sources, page evidence, validation, serialization, resources, and fail-closed resume use the shared core with v6 identities
#   class: correctness
# === END CONTRACTS ===

"""Execute the frozen Tarot OCR v6 historic-print model experiment.

Usage:
    python3 tools/run_tarot_ocr_v6.py \
      --acquisition artifacts/tarot/acquisition-v1 \
      --reference experiments/tarot/tarot-ocr-validation-reference-v4.json \
      --model artifacts/tarot/ocr-models/frak2021-0.905.traineddata \
      --output artifacts/tarot/ocr-v6/run-a

The command has no network path. Acquire the model from the content URL in
``tarot-ocr-model-frak2021.json`` first; this runner verifies its exact bytes.
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
except ModuleNotFoundError:  # Direct ``python tools/run_tarot_ocr_v6.py`` use.
    import run_tarot_ocr_v4 as core


PROTOCOL_COMMIT = "c63ad40d71b60a1d944ad6ce21e9d7e4cf8d2a3b"
PROTOCOL_SHA256 = "07c4540d4be3ab1affb30184d7eb6290361b5b470bb55ac23cc3adf64c34a216"
MODEL_NAME = "frak2021-0.905"
MODEL_FILENAME = f"{MODEL_NAME}.traineddata"
MODEL_BYTES = 3_421_140
MODEL_SHA256 = "1da2384254fa8462c776faf3b43307fe19ce51be0931c623b2fdd560f96e299a"
INSTRUMENT = {
    "language_model": MODEL_NAME,
    "model_sha256": MODEL_SHA256,
    "thresholding_method": "2",
    "thresholding_name": "Sauvola",
    "all_other_v5_fields": "unchanged",
}


def verify_model(path: Path) -> None:
    if path.name != MODEL_FILENAME:
        raise core.ProtocolBlocked("historic model filename mismatch")
    if not path.is_file() or path.stat().st_size != MODEL_BYTES or core.digest(path) != MODEL_SHA256:
        raise core.ProtocolBlocked("historic model identity mismatch")


def ocr_command(tesseract: Path, png: Path, base: Path, model: Path) -> list[str]:
    return [
        str(tesseract), str(png), str(base), "--tessdata-dir", str(model.parent),
        "-l", MODEL_NAME, "--oem", "1", "--psm", "3", "-c",
        "thresholding_method=2", "txt", "tsv",
    ]


def render_and_ocr(
    model: Path,
    mutool: Path,
    tesseract: Path,
    pdf: Path,
    output: Path,
    source: core.Source,
    page: int,
    *,
    command_builder=ocr_command,
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
        command_builder(tesseract, png, txt.with_suffix(""), model),
        capture_output=True,
        timeout=core.OCR_TIMEOUT,
        env=environment,
    )
    if ocr.returncode:
        raise core.ProtocolBlocked(f"OCR producer error: {source.source_id} page {page}")
    if not txt.is_file() or not tsv.is_file():
        raise core.ProtocolBlocked(f"missing OCR output: {source.source_id} page {page}")
    return core.record_for(source, page, png, txt, tsv)


def run(acquisition: Path, reference: Path, model: Path, output: Path, resume: bool) -> dict[str, object]:
    verify_model(model)

    def page_producer(*args):
        return render_and_ocr(model, *args)

    return core.run(
        acquisition,
        reference,
        output,
        resume,
        version="6.0.0",
        protocol_commit=PROTOCOL_COMMIT,
        page_producer=page_producer,
        instrument={**INSTRUMENT, "protocol_sha256": PROTOCOL_SHA256},
        model_sha256=MODEL_SHA256,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acquisition", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args.acquisition, args.reference, args.model, args.output, args.resume)
    except (core.ProtocolBlocked, subprocess.TimeoutExpired, UnicodeError, csv.Error, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "failure": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if result["status"] == "FALSIFIED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
