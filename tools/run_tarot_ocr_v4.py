#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_ocr_v4_runner
#   module_name: tarot_ocr_v4_runner
#   module_kind: experiment
#   summary: executes the frozen Tarot OCR v4 protocol with exact producer identities, resumable raw outputs, deterministic manifests, and independent-reference scoring
#   owner: Erin Spencer
#   public_surface: command-line interface
#   internal_surface: producer verification, render/OCR execution, checkpoint verification, TSV reconstruction, CER/WER scoring
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_tarot_ocr_v4
#   rollout: explicit CLI only after validation reference commit aed1cf7de3df80da104daf2b3c46246ff5c3fe39
#   rollback: remove this runner without altering frozen protocol or result receipts
#   requires: edcm_tarot_corpus_acquirer
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_ocr_v4_verifies_every_frozen_identity
#   given: a protocol execution request
#   then: both PDFs, renderer, OCR executable, French model, versions, page counts, and reference bytes must match before a producer runs
#   class: evidence
#
# id: tarot_ocr_v4_preserves_raw_page_evidence
#   given: an admitted PDF page
#   then: exact grayscale PNG, raw UTF-8 TXT, raw TSV, hashes, bytes, confidences, page identity, and typed unavailable alternatives are retained
#   class: evidence
#
# id: tarot_ocr_v4_resume_fails_closed
#   given: an interrupted or completed output directory
#   then: only checkpoint-bound exact files are reused and any missing, injected, or changed file blocks continuation
#   class: correctness
#
# id: tarot_ocr_v4_applies_frozen_accuracy_rule
#   given: the sealed independent reference and complete OCR outputs
#   then: inherited normalization, CER/WER thresholds, replacement check, and exact-empty rule produce only FALSIFIED, UNRESOLVED, or BLOCKED for one run
#   class: evidence
#
# id: tarot_ocr_v4_serialization_is_deterministic
#   given: identical producer outputs and inputs
#   then: canonical manifest, checkpoint, and evaluation bytes are identical
#   class: correctness
# === END CONTRACTS ===

"""Execute the frozen Tarot OCR v4 experiment.

Usage:
    python3 tools/run_tarot_ocr_v4.py \
      --acquisition artifacts/tarot/acquisition-v1 \
      --reference experiments/tarot/tarot-ocr-validation-reference-v4.json \
      --output artifacts/tarot/ocr-v4/run-a

The command has no network path and never interprets content. It verifies all
frozen producer/input identities, writes one page at a time, and checkpoints
after each complete PNG/TXT/TSV triplet. Reuse requires ``--resume`` and exact
checkpoint/file agreement. One passing run is UNRESOLVED pending a second
byte-identical complete run. Any frozen accuracy failure is FALSIFIED.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata


MUTOOL_SHA256 = "9203440040cc38ee412aeedbfe57f452d6b85709c5b1600ca6ab2aa05478ab73"
TESSERACT_SHA256 = "9f831cab7525c3dab04af41bda35182af7ea1df9dceeaaa2f3bf207ac45c06a5"
MODEL_PATH = Path("/usr/share/tesseract-ocr/5/tessdata/fra.traineddata")
MODEL_SHA256 = "ced037562e8c80c13122dece28dd477d399af80911a28791a66a63ac1e3445ca"
REFERENCE_SHA256 = "2832183c54b34f8275057faf61d20b6139d54dbb140bd38ae9c89b4583dc1e4e"
MAX_RENDERED_BYTES = 2_147_483_648
MAX_OCR_BYTES = 1_073_741_824
RENDER_TIMEOUT = 20
OCR_TIMEOUT = 60
CROP_BOX = (248, 1052, 2233, 1930)
BOOK_VALIDATION_PAGES = {25, 75, 125, 175, 225, 275, 325, 375}


@dataclass(frozen=True)
class Source:
    source_id: str
    filename: str
    pages: int
    bytes: int
    digest: str


SOURCES = (
    Source("wellcome_etteilla_1783_1785", "wellcome_etteilla_1783_1785.pdf", 401, 77_852_106, "d44fc8bf81e5356fa1f05d11a9e92723ee36efe94b3af2def5c1c97e80ff5c0f"),
    Source("wellcome_etteilla_tableau_1780s", "wellcome_etteilla_tableau_1780s.pdf", 6, 869_817, "d3a2e8e82c79e9a109e662e53ff034dcabc7f2902c52dcde10fec9d3529f5381"),
)


class ProtocolBlocked(RuntimeError):
    pass


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_canonical(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(canonical_bytes(value))
    temporary.replace(path)


def command_identity(command: str, expected_digest: str) -> Path:
    found = shutil.which(command)
    if found is None:
        raise ProtocolBlocked(f"missing producer: {command}")
    path = Path(found).resolve()
    if digest(path) != expected_digest:
        raise ProtocolBlocked(f"producer identity mismatch: {command}")
    return path


def verify_inputs(acquisition: Path, reference: Path) -> tuple[Path, Path, dict[str, object]]:
    mutool = command_identity("mutool", MUTOOL_SHA256)
    tesseract = command_identity("tesseract", TESSERACT_SHA256)
    if not MODEL_PATH.is_file() or digest(MODEL_PATH) != MODEL_SHA256:
        raise ProtocolBlocked("French model identity mismatch")
    if not reference.is_file() or digest(reference) != REFERENCE_SHA256:
        raise ProtocolBlocked("validation reference identity mismatch")
    mutool_version = subprocess.run([str(mutool), "version"], capture_output=True, text=True, timeout=5)
    mutool_lines = mutool_version.stderr.splitlines()
    if mutool_version.returncode != 1 or mutool_version.stdout or not mutool_lines or mutool_lines[0] != "mutool version 1.23.10":
        raise ProtocolBlocked("MuPDF version output mismatch")
    tess_version = subprocess.run([str(tesseract), "--version"], capture_output=True, text=True, timeout=5)
    lines = tess_version.stdout.splitlines()
    if tess_version.returncode or len(lines) < 2 or lines[0] != "tesseract 5.3.4" or lines[1].strip() != "leptonica-1.82.0":
        raise ProtocolBlocked("Tesseract version output mismatch")
    raw = acquisition / "raw"
    for source in SOURCES:
        path = raw / source.filename
        if not path.is_file() or path.stat().st_size != source.bytes or digest(path) != source.digest:
            raise ProtocolBlocked(f"input identity mismatch: {source.source_id}")
    return mutool, tesseract, json.loads(reference.read_text(encoding="utf-8"))


def page_paths(output: Path, source: Source, page: int) -> tuple[Path, Path, Path]:
    base = output / "raw" / source.source_id / f"page-{page:04d}"
    return base.with_suffix(".png"), base.with_suffix(".txt"), base.with_suffix(".tsv")


def record_for(source: Source, page: int, png: Path, txt: Path, tsv: Path) -> dict[str, object]:
    confidences: list[str] = []
    with tsv.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"level", "page_num", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height", "conf", "text"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ProtocolBlocked(f"missing TSV fields: {source.source_id} page {page}")
        for row in reader:
            if row["level"] == "5" and row["text"].strip():
                confidences.append(row["conf"])
    return {
        "source_id": source.source_id,
        "source_sha256": source.digest,
        "page": page,
        "png": {"bytes": png.stat().st_size, "sha256": digest(png)},
        "txt": {"bytes": txt.stat().st_size, "sha256": digest(txt)},
        "tsv": {"bytes": tsv.stat().st_size, "sha256": digest(tsv), "word_confidences": confidences},
    }


def verify_record(output: Path, source: Source, record: dict[str, object]) -> bool:
    page = int(record["page"])
    png, txt, tsv = page_paths(output, source, page)
    for key, path in (("png", png), ("txt", txt), ("tsv", tsv)):
        expected = record[key]
        if not path.is_file() or path.stat().st_size != expected["bytes"] or digest(path) != expected["sha256"]:
            return False
    return record_for(source, page, png, txt, tsv) == record


def render_and_ocr(mutool: Path, tesseract: Path, pdf: Path, output: Path, source: Source, page: int) -> dict[str, object]:
    png, txt, tsv = page_paths(output, source, page)
    png.parent.mkdir(parents=True, exist_ok=True)
    render = subprocess.run(
        [str(mutool), "draw", "-q", "-N", "-r", "300", "-c", "gray", "-F", "png", "-o", str(png), str(pdf), str(page)],
        capture_output=True,
        timeout=RENDER_TIMEOUT,
    )
    if render.returncode or render.stdout or render.stderr:
        raise ProtocolBlocked(f"renderer output/error: {source.source_id} page {page}")
    environment = dict(os.environ)
    environment["OMP_THREAD_LIMIT"] = "1"
    base = txt.with_suffix("")
    ocr = subprocess.run(
        [str(tesseract), str(png), str(base), "-l", "fra", "--oem", "1", "--psm", "3", "txt", "tsv"],
        capture_output=True,
        timeout=OCR_TIMEOUT,
        env=environment,
    )
    if ocr.returncode:
        raise ProtocolBlocked(f"OCR producer error: {source.source_id} page {page}")
    if not txt.is_file() or not tsv.is_file():
        raise ProtocolBlocked(f"missing OCR output: {source.source_id} page {page}")
    return record_for(source, page, png, txt, tsv)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    lines = []
    for line in text.split("\n"):
        collapsed = re.sub(r"\s+", " ", line.strip())
        if collapsed:
            lines.append(collapsed)
    return "\n".join(lines)


def tsv_text(path: Path, crop: tuple[int, int, int, int] | None) -> str:
    lines: dict[tuple[int, int, int, int], list[tuple[int, str]]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            text = row["text"].strip()
            if row["level"] != "5" or not text:
                continue
            if crop is not None:
                cx = int(row["left"]) + int(row["width"]) / 2
                cy = int(row["top"]) + int(row["height"]) / 2
                if not (crop[0] <= cx < crop[2] and crop[1] <= cy < crop[3]):
                    continue
            key = tuple(int(row[name]) for name in ("page_num", "block_num", "par_num", "line_num"))
            lines.setdefault(key, []).append((int(row["word_num"]), text))
    return "\n".join(" ".join(text for _, text in sorted(words)) for _, words in sorted(lines.items()))


def levenshtein(left: list[str] | str, right: list[str] | str) -> int:
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def score(reference_text: str, candidate_text: str) -> dict[str, object]:
    reference_normalized = normalize(reference_text)
    candidate_normalized = normalize(candidate_text)
    if not reference_normalized:
        return {"reference_characters": 0, "candidate_characters": len(candidate_normalized), "exact_empty": not candidate_normalized}
    ref_words = reference_normalized.split()
    candidate_words = candidate_normalized.split()
    char_distance = levenshtein(reference_normalized, candidate_normalized)
    word_distance = levenshtein(ref_words, candidate_words)
    return {
        "reference_characters": len(reference_normalized),
        "candidate_characters": len(candidate_normalized),
        "character_distance": char_distance,
        "cer": char_distance / len(reference_normalized),
        "reference_words": len(ref_words),
        "candidate_words": len(candidate_words),
        "word_distance": word_distance,
        "wer": word_distance / len(ref_words),
    }


def evaluate(output: Path, reference: dict[str, object], *, version: str = "4.0.0") -> dict[str, object]:
    results: list[dict[str, object]] = []
    totals = {"characters": 0, "character_distance": 0, "words": 0, "word_distance": 0}
    source_totals: dict[str, dict[str, int]] = {}
    failed = False
    for group, source in (("book", SOURCES[0]), ("tableau", SOURCES[1])):
        source_total = {"characters": 0, "character_distance": 0, "words": 0, "word_distance": 0}
        for entry in reference[group]:
            page = int(entry["page"])
            _, txt, tsv = page_paths(output, source, page)
            candidate = tsv_text(tsv, CROP_BOX if group == "book" else None)
            page_score = score(entry["text"], candidate)
            page_score.update({"source": group, "page": page, "candidate_sha256": sha256(normalize(candidate).encode()).hexdigest()})
            if "exact_empty" in page_score:
                if not page_score["exact_empty"]:
                    failed = True
            else:
                if page_score["cer"] > 0.20:
                    failed = True
                for total_key, score_key in (("characters", "reference_characters"), ("character_distance", "character_distance"), ("words", "reference_words"), ("word_distance", "word_distance")):
                    source_total[total_key] += int(page_score[score_key])
                    totals[total_key] += int(page_score[score_key])
            if "�" in txt.read_text(encoding="utf-8"):
                page_score["ocr_replacement_character"] = True
                failed = True
            else:
                page_score["ocr_replacement_character"] = False
            results.append(page_score)
        source_total["cer"] = source_total["character_distance"] / source_total["characters"]
        source_total["wer"] = source_total["word_distance"] / source_total["words"]
        if source_total["cer"] > 0.10:
            failed = True
        source_totals[group] = source_total
    aggregate_cer = totals["character_distance"] / totals["characters"]
    aggregate_wer = totals["word_distance"] / totals["words"]
    if aggregate_cer > 0.08 or aggregate_wer > 0.20:
        failed = True
    return {
        "schema": "edcm.tarot-ocr-validation",
        "version": version,
        "status": "FALSIFIED" if failed else "UNRESOLVED",
        "aggregate": {**totals, "cer": aggregate_cer, "wer": aggregate_wer},
        "sources": source_totals,
        "pages": results,
        "replay": "not-run",
        "nonclaims": ["Tarot ontology", "card equivalence", "semantic normalization", "UCNS geometry", "EDCM interpretation", "Platonic-card construction", "canon"],
    }


def run(
    acquisition: Path,
    reference_path: Path,
    output: Path,
    resume: bool,
    *,
    version: str = "4.0.0",
    protocol_commit: str = "5d20d70a3b2b9d91fefbfc5142294b262a125223",
    page_producer=render_and_ocr,
    instrument: dict[str, object] | None = None,
    model_sha256: str = MODEL_SHA256,
) -> dict[str, object]:
    mutool, tesseract, reference = verify_inputs(acquisition, reference_path)
    output.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output / "checkpoint.json"
    if checkpoint_path.exists():
        if not resume:
            raise ProtocolBlocked("output checkpoint exists; use --resume")
        checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    else:
        unexpected = list(output.iterdir())
        if unexpected:
            raise ProtocolBlocked("nonempty output without checkpoint")
        checkpoint = {"schema": "edcm.tarot-ocr-checkpoint", "version": version, "records": []}
    if checkpoint.get("version") != version:
        raise ProtocolBlocked("checkpoint protocol version mismatch")
    records = checkpoint["records"]
    expected_sequence = [(source, page) for source in SOURCES for page in range(1, source.pages + 1)]
    if len(records) > len(expected_sequence):
        raise ProtocolBlocked("checkpoint has excess records")
    for index, record in enumerate(records):
        source, page = expected_sequence[index]
        if record["source_id"] != source.source_id or record["page"] != page or not verify_record(output, source, record):
            raise ProtocolBlocked("checkpoint/file mismatch")
    rendered_bytes = sum(int(record["png"]["bytes"]) for record in records)
    ocr_bytes = sum(int(record["txt"]["bytes"]) + int(record["tsv"]["bytes"]) for record in records)
    for source, page in expected_sequence[len(records):]:
        record = page_producer(mutool, tesseract, acquisition / "raw" / source.filename, output, source, page)
        records.append(record)
        rendered_bytes += int(record["png"]["bytes"])
        ocr_bytes += int(record["txt"]["bytes"]) + int(record["tsv"]["bytes"])
        if rendered_bytes > MAX_RENDERED_BYTES or ocr_bytes > MAX_OCR_BYTES:
            raise ProtocolBlocked("artifact byte limit exceeded")
        write_canonical(checkpoint_path, checkpoint)
    manifest = {
        "schema": "edcm.tarot-ocr-corpus-manifest",
        "version": version,
        "protocol_commit": protocol_commit,
        "reference_commit": "aed1cf7de3df80da104daf2b3c46246ff5c3fe39",
        "reference_sha256": REFERENCE_SHA256,
        "renderer_sha256": MUTOOL_SHA256,
        "ocr_sha256": TESSERACT_SHA256,
        "model_sha256": model_sha256,
        "pages": records,
        "alternatives": {"status": "NA", "reason": "Tesseract txt/tsv interface exposes no character alternatives"},
        "ontology_selected": False,
        "semantic_normalization": False,
        "geometry_attached": False,
        "measurement_attached": False,
        "canon_selection": None,
    }
    if instrument is not None:
        manifest["instrument"] = instrument
    write_canonical(output / "manifest.json", manifest)
    evaluation = evaluate(output, reference, version=version)
    write_canonical(output / "validation.json", evaluation)
    return evaluation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acquisition", type=Path, required=True)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    try:
        result = run(args.acquisition, args.reference, args.output, args.resume)
    except (ProtocolBlocked, subprocess.TimeoutExpired, UnicodeError, csv.Error, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "failure": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if result["status"] == "FALSIFIED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
