#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_ocr_v7_runner
#   module_name: tarot_ocr_v7_runner
#   module_kind: experiment
#   summary: executes the frozen Tarot OCR v7 renderer-flag repair with the unchanged historic-print instrument
#   owner: Erin Spencer
#   public_surface: command-line interface
#   internal_surface: explicit TXT/TSV flags and v6 historic-model page producer
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_tarot_ocr_v7
#   rollout: explicit CLI only after protocol commit f57f639
#   rollback: remove this adapter without altering prior evidence or protocols
#   requires: edcm_tarot_ocr_v6_runner
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_ocr_v7_repairs_only_renderer_activation
#   given: a v7 page OCR request
#   then: explicit TXT and TSV booleans replace only the unavailable config filenames
#   class: evidence
#
# id: tarot_ocr_v7_retains_v6_instrument
#   given: a complete or resumed v7 run
#   then: the exact historic model and all inherited source, OCR, validation, evidence, and failure contracts remain active
#   class: correctness
# === END CONTRACTS ===

"""Execute the frozen Tarot OCR v7 renderer-flag repair.

Usage:
    python3 tools/run_tarot_ocr_v7.py \
      --acquisition artifacts/tarot/acquisition-v1 \
      --reference experiments/tarot/tarot-ocr-validation-reference-v4.json \
      --model artifacts/tarot/ocr-models/frak2021-0.905.traineddata \
      --output artifacts/tarot/ocr-v7/run-a
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys

try:
    from tools import run_tarot_ocr_v4 as core
    from tools import run_tarot_ocr_v6 as predecessor
except ModuleNotFoundError:  # Direct ``python tools/run_tarot_ocr_v7.py`` use.
    import run_tarot_ocr_v4 as core
    import run_tarot_ocr_v6 as predecessor


PROTOCOL_COMMIT = "f57f639c02f3f975c4bd7983d3a22cdf59592a77"
PROTOCOL_SHA256 = "43a1568c68ffad1052fa382b08ee8af7793cdc8ef289971707dc27aa0479eccd"
INSTRUMENT = {
    **predecessor.INSTRUMENT,
    "output_renderers": {
        "tessedit_create_txt": "1",
        "tessedit_create_tsv": "1",
        "config_files": "not-used",
    },
    "all_other_v6_fields": "unchanged",
}


def ocr_command(tesseract: Path, png: Path, base: Path, model: Path) -> list[str]:
    return [
        str(tesseract), str(png), str(base), "--tessdata-dir", str(model.parent),
        "-l", predecessor.MODEL_NAME, "--oem", "1", "--psm", "3", "-c",
        "thresholding_method=2", "-c", "tessedit_create_txt=1", "-c",
        "tessedit_create_tsv=1",
    ]


def run(acquisition: Path, reference: Path, model: Path, output: Path, resume: bool) -> dict[str, object]:
    predecessor.verify_model(model)

    def page_producer(*args):
        return predecessor.render_and_ocr(model, *args, command_builder=ocr_command)

    return core.run(
        acquisition,
        reference,
        output,
        resume,
        version="7.0.0",
        protocol_commit=PROTOCOL_COMMIT,
        page_producer=page_producer,
        instrument={**INSTRUMENT, "protocol_sha256": PROTOCOL_SHA256},
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
