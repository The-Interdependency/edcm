#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: edcm_tarot_corpus_acquirer
#   module_name: tarot_corpus_acquirer
#   module_kind: instrument
#   summary: validates a provenance-only Tarot source manifest, acquires only explicitly authorized public-domain bytes, and seals deterministic evidence receipts without defining Tarot ontology
#   owner: Erin Spencer
#   public_surface: validate_manifest, acquire_manifest, main
#   internal_surface: _fetch_https, _write_checkpoint, _validate_completed_run, _canonical_bytes
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: external
#   user_data_boundary: none; public cultural and archival evidence only
#   admin_only: false
#   tests: tests.test_tarot_corpus_acquisition
#   rollout: explicit CLI only; no automatic embedding or corpus download
#   rollback: remove this tool and its corpus/artifact documentation; generated artifacts are reproducible caches and remain noncanonical
#   requires: none
#   since: 2026-08-16
#   unresolved: source-specific item licensing and child-object identities beyond pinned public-domain downloads; OCR, transcription, semantic extraction, and EDCM embedding remain separate stages
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: tarot_manifest_preserves_preontology_boundary
#   given: a Tarot corpus manifest is loaded
#   then: only the frozen evidence-envelope schema is accepted and ontology, canonical-deck, canonical-card-count, cross-source card identity, and I Ching inclusion remain explicitly unselected
#   class: safety
#   since: 2026-08-16
#
# id: tarot_acquisition_fetches_only_authorized_public_domain_bytes
#   given: a source requests automatic byte acquisition
#   then: the source must declare an HTTPS content URL, a safe artifact name, expected media type, and public-domain or Public Domain Mark rights before any network request occurs
#   class: safety
#   since: 2026-08-16
#
# id: tarot_acquisition_preserves_source_identity
#   given: a Tarot source is admitted to an acquisition run
#   then: its exact manifest entry digest, locator, retrieval policy, rights state, and any fetched byte digest are recorded without semantic normalization
#   class: evidence
#   since: 2026-08-16
#
# id: tarot_acquisition_resume_fails_closed
#   given: a completed or interrupted Tarot acquisition is resumed
#   then: manifest identity, checkpoint entries, byte digests, and the exact output file set are validated; altered, missing, stale, or injected state is rejected
#   class: safety
#   since: 2026-08-16
#
# id: tarot_metadata_only_sources_are_not_downloaded
#   given: a source is metadata_only or manual_review
#   then: no content request is issued and the source remains a provenance-bearing locator in the evidence index
#   class: correctness
#   since: 2026-08-16
# === END CONTRACTS ===

"""Acquire a provenance-first Tarot evidence corpus without defining Tarot.

Usage:
    python tools/acquire_tarot_corpus.py --dry-run
    python tools/acquire_tarot_corpus.py --output artifacts/tarot/acquisition-v1
    python tools/acquire_tarot_corpus.py --output artifacts/tarot/acquisition-v1 --resume

Only manifest entries whose retrieval policy is ``fetch_bytes`` and whose rights
state is explicitly ``public_domain`` or ``public_domain_mark`` are downloaded.
All other sources remain locators. The runner records evidence identity only; it
performs no OCR, image interpretation, card matching, semantic normalization,
EDCM embedding, UCNS construction, or Tarot ontology selection.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
from typing import Any, Callable
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MANIFEST_SCHEMA = "edcm.tarot-corpus-manifest"
MANIFEST_VERSION = "1.0.0"
INDEX_SCHEMA = "edcm.tarot-corpus-evidence-index"
RECEIPT_SCHEMA = "edcm.tarot-corpus-acquisition-receipt"
CHECKPOINT_SCHEMA = "edcm.tarot-corpus-acquisition-checkpoint"
OUTPUT_VERSION = "1.0.0"

TOP_LEVEL_KEYS = {"schema", "version", "scope", "frozen_on", "doctrine", "sources", "hmmm"}
DOCTRINE = {
    "ontology_selected": False,
    "canonical_deck_selected": False,
    "canonical_card_count_selected": False,
    "cross_source_card_identity_inference": False,
    "source_provenance_required": True,
    "semantic_normalization": "forbidden_before_edcm_discovery",
    "corpus_closure": "open",
    "i_ching_in_scope": False,
}
SOURCE_KEYS = {
    "source_id",
    "title",
    "authority",
    "source_date",
    "locator_url",
    "retrieval_policy",
    "content_url",
    "artifact_name",
    "rights_status",
    "rights_url",
    "media_type",
    "curation_note",
    "provenance_note",
}
RETRIEVAL_POLICIES = {"fetch_bytes", "metadata_only", "manual_review"}
RIGHTS_STATES = {"public_domain", "public_domain_mark", "in_copyright", "source_specific", "unknown"}
AUTO_FETCH_RIGHTS = {"public_domain", "public_domain_mark"}
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9_]{1,95}$")
SAFE_ARTIFACT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
DEFAULT_MANIFEST = Path("corpus/tarot/sources.v1.json")
DEFAULT_OUTPUT = Path("artifacts/tarot/acquisition-v1")
DEFAULT_MAX_BYTES = 268_435_456


class TarotCorpusError(RuntimeError):
    """Raised when an evidence or acquisition boundary fails closed."""


@dataclass(frozen=True)
class FetchMetadata:
    final_url: str
    content_type: str
    bytes_written: int
    sha256: str


Fetcher = Callable[[str, Path, int], FetchMetadata]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"


def _sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_https(url: str, *, field: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise TarotCorpusError(f"{field} must be an absolute HTTPS URL: {url!r}")


def validate_manifest(manifest: Any) -> dict[str, Any]:
    """Validate and return a strict Tarot evidence manifest."""
    if not isinstance(manifest, dict):
        raise TarotCorpusError("manifest must be a JSON object")
    extra = set(manifest) - TOP_LEVEL_KEYS
    missing = TOP_LEVEL_KEYS - set(manifest)
    if extra or missing:
        raise TarotCorpusError(f"manifest keys mismatch; missing={sorted(missing)} extra={sorted(extra)}")
    if manifest["schema"] != MANIFEST_SCHEMA or manifest["version"] != MANIFEST_VERSION:
        raise TarotCorpusError("unsupported Tarot corpus manifest schema/version")
    if manifest["scope"] != "tarot":
        raise TarotCorpusError("manifest scope must be exactly 'tarot'")
    if manifest["doctrine"] != DOCTRINE:
        raise TarotCorpusError("pre-ontology doctrine changed; refuse implicit Tarot schema selection")
    if not isinstance(manifest["frozen_on"], str) or not manifest["frozen_on"]:
        raise TarotCorpusError("frozen_on must be a non-empty string")
    if not isinstance(manifest["hmmm"], list) or not all(isinstance(item, str) and item for item in manifest["hmmm"]):
        raise TarotCorpusError("hmmm must be a list of non-empty strings")
    sources = manifest["sources"]
    if not isinstance(sources, list) or not sources:
        raise TarotCorpusError("sources must be a non-empty list")

    seen_ids: set[str] = set()
    seen_artifacts: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise TarotCorpusError(f"source[{index}] must be an object")
        extra = set(source) - SOURCE_KEYS
        missing = SOURCE_KEYS - set(source)
        if extra or missing:
            raise TarotCorpusError(
                f"source[{index}] keys mismatch; missing={sorted(missing)} extra={sorted(extra)}"
            )
        source_id = source["source_id"]
        if not isinstance(source_id, str) or not SAFE_ID.fullmatch(source_id):
            raise TarotCorpusError(f"invalid source_id: {source_id!r}")
        if source_id in seen_ids:
            raise TarotCorpusError(f"duplicate source_id: {source_id}")
        seen_ids.add(source_id)
        for field in ("title", "authority", "source_date", "curation_note", "provenance_note"):
            if not isinstance(source[field], str) or not source[field].strip():
                raise TarotCorpusError(f"{source_id}.{field} must be non-empty text")
        _require_https(source["locator_url"], field=f"{source_id}.locator_url")
        _require_https(source["rights_url"], field=f"{source_id}.rights_url")
        policy = source["retrieval_policy"]
        if policy not in RETRIEVAL_POLICIES:
            raise TarotCorpusError(f"unsupported retrieval policy for {source_id}: {policy!r}")
        if source["rights_status"] not in RIGHTS_STATES:
            raise TarotCorpusError(f"unsupported rights status for {source_id}: {source['rights_status']!r}")
        if not isinstance(source["media_type"], str) or "/" not in source["media_type"]:
            raise TarotCorpusError(f"invalid media_type for {source_id}")

        content_url = source["content_url"]
        artifact = source["artifact_name"]
        if policy == "fetch_bytes":
            if source["rights_status"] not in AUTO_FETCH_RIGHTS:
                raise TarotCorpusError(f"automatic fetch lacks public-domain authority: {source_id}")
            if not isinstance(content_url, str):
                raise TarotCorpusError(f"fetch_bytes source lacks content_url: {source_id}")
            _require_https(content_url, field=f"{source_id}.content_url")
            if not isinstance(artifact, str) or not SAFE_ARTIFACT.fullmatch(artifact):
                raise TarotCorpusError(f"unsafe artifact_name for {source_id}: {artifact!r}")
            if artifact in seen_artifacts:
                raise TarotCorpusError(f"duplicate artifact_name: {artifact}")
            seen_artifacts.add(artifact)
        elif content_url is not None or artifact is not None:
            raise TarotCorpusError(
                f"{source_id}: {policy} entries must not carry downloadable content_url/artifact_name"
            )
    return manifest


def load_manifest(path: Path) -> tuple[dict[str, Any], str, str]:
    raw = path.read_bytes()
    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TarotCorpusError(f"invalid manifest JSON: {exc}") from exc
    manifest = validate_manifest(decoded)
    return manifest, _sha256_bytes(raw), _sha256_bytes(_canonical_bytes(manifest))


def _fetch_https(url: str, destination: Path, max_bytes: int) -> FetchMetadata:
    """Stream one HTTPS object to ``destination`` with a hard byte ceiling."""
    _require_https(url, field="content_url")
    if max_bytes <= 0:
        raise TarotCorpusError("max_bytes must be positive")
    request = Request(url, headers={"User-Agent": "edcm-tarot-corpus/1.0 (+https://github.com/The-Interdependency/edcm)"})
    temp = destination.with_name(destination.name + ".part")
    temp.parent.mkdir(parents=True, exist_ok=True)
    digest = sha256()
    total = 0
    try:
        with urlopen(request, timeout=60) as response, temp.open("wb") as handle:  # noqa: S310 - HTTPS is enforced above
            final_url = response.geturl()
            _require_https(final_url, field="final_url")
            content_type = (response.headers.get_content_type() or "application/octet-stream").lower()
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise TarotCorpusError(f"download exceeds max_bytes={max_bytes}: {url}")
                handle.write(chunk)
                digest.update(chunk)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    return FetchMetadata(final_url=final_url, content_type=content_type, bytes_written=total, sha256=digest.hexdigest())


def _source_entry_sha(source: dict[str, Any]) -> str:
    return _sha256_bytes(_canonical_bytes(source))


def _checkpoint_path(output: Path) -> Path:
    return output / ".checkpoint.json"


def _write_checkpoint(
    output: Path,
    manifest_file_sha: str,
    manifest_canonical_sha: str,
    fetched: dict[str, dict[str, Any]],
) -> None:
    checkpoint = {
        "schema": CHECKPOINT_SCHEMA,
        "version": OUTPUT_VERSION,
        "manifest_file_sha256": manifest_file_sha,
        "manifest_canonical_sha256": manifest_canonical_sha,
        "fetched": fetched,
    }
    _checkpoint_path(output).write_bytes(_canonical_bytes(checkpoint))


def _load_checkpoint(
    output: Path,
    manifest: dict[str, Any],
    manifest_file_sha: str,
    manifest_canonical_sha: str,
) -> dict[str, dict[str, Any]]:
    path = _checkpoint_path(output)
    if not path.exists():
        return {}
    try:
        checkpoint = json.loads(path.read_bytes())
    except json.JSONDecodeError as exc:
        raise TarotCorpusError(f"invalid acquisition checkpoint: {exc}") from exc
    if checkpoint.get("schema") != CHECKPOINT_SCHEMA or checkpoint.get("version") != OUTPUT_VERSION:
        raise TarotCorpusError("checkpoint schema/version mismatch")
    if checkpoint.get("manifest_file_sha256") != manifest_file_sha:
        raise TarotCorpusError("checkpoint manifest file identity mismatch")
    if checkpoint.get("manifest_canonical_sha256") != manifest_canonical_sha:
        raise TarotCorpusError("checkpoint canonical manifest identity mismatch")
    fetched = checkpoint.get("fetched")
    if not isinstance(fetched, dict):
        raise TarotCorpusError("checkpoint fetched map is malformed")

    by_id = {source["source_id"]: source for source in manifest["sources"]}
    allowed_files = {".checkpoint.json"}
    for source_id, record in fetched.items():
        source = by_id.get(source_id)
        if source is None or source["retrieval_policy"] != "fetch_bytes":
            raise TarotCorpusError(f"checkpoint names invalid source: {source_id}")
        if not isinstance(record, dict) or record.get("entry_sha256") != _source_entry_sha(source):
            raise TarotCorpusError(f"checkpoint entry identity mismatch: {source_id}")
        artifact = source["artifact_name"]
        relative = f"raw/{artifact}"
        if record.get("artifact_path") != relative:
            raise TarotCorpusError(f"checkpoint artifact path mismatch: {source_id}")
        path_on_disk = output / relative
        if not path_on_disk.is_file():
            raise TarotCorpusError(f"checkpoint artifact missing: {relative}")
        if record.get("sha256") != _sha256_file(path_on_disk) or record.get("bytes") != path_on_disk.stat().st_size:
            raise TarotCorpusError(f"checkpoint artifact altered: {relative}")
        allowed_files.add(relative)

    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    if actual != allowed_files:
        raise TarotCorpusError(
            f"incomplete resume file set mismatch; expected={sorted(allowed_files)} actual={sorted(actual)}"
        )
    return fetched


def _index_row(source: dict[str, Any], fetched: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_id = source["source_id"]
    base = {
        "source_id": source_id,
        "entry_sha256": _source_entry_sha(source),
        "title": source["title"],
        "authority": source["authority"],
        "source_date": source["source_date"],
        "locator_url": source["locator_url"],
        "retrieval_policy": source["retrieval_policy"],
        "rights_status": source["rights_status"],
        "rights_url": source["rights_url"],
        "declared_media_type": source["media_type"],
        "curation_note": source["curation_note"],
        "provenance_note": source["provenance_note"],
        "artifact_path": None,
        "sha256": None,
        "bytes": None,
        "content_type": None,
        "final_url": None,
    }
    if source["retrieval_policy"] == "fetch_bytes":
        record = fetched.get(source_id)
        if record is None:
            raise TarotCorpusError(f"missing fetched record for {source_id}")
        base.update(
            artifact_path=record["artifact_path"],
            sha256=record["sha256"],
            bytes=record["bytes"],
            content_type=record["content_type"],
            final_url=record["final_url"],
        )
    return base


def _final_receipt_path(output: Path) -> Path:
    return output / "run-receipt.json"


def _validate_completed_run(
    output: Path,
    manifest_file_sha: str,
    manifest_canonical_sha: str,
) -> dict[str, Any]:
    receipt_path = _final_receipt_path(output)
    if not receipt_path.is_file():
        raise TarotCorpusError("completed receipt is missing")
    try:
        receipt = json.loads(receipt_path.read_bytes())
    except json.JSONDecodeError as exc:
        raise TarotCorpusError(f"invalid completed receipt: {exc}") from exc
    if receipt.get("schema") != RECEIPT_SCHEMA or receipt.get("version") != OUTPUT_VERSION:
        raise TarotCorpusError("completed receipt schema/version mismatch")
    if receipt.get("manifest_file_sha256") != manifest_file_sha:
        raise TarotCorpusError("completed receipt manifest file identity mismatch")
    if receipt.get("manifest_canonical_sha256") != manifest_canonical_sha:
        raise TarotCorpusError("completed receipt canonical manifest identity mismatch")
    files = receipt.get("files")
    if not isinstance(files, list):
        raise TarotCorpusError("completed receipt files list is malformed")
    expected = {"run-receipt.json"}
    for record in files:
        if not isinstance(record, dict) or set(record) != {"path", "sha256", "bytes"}:
            raise TarotCorpusError("completed receipt file record is malformed")
        relative = record["path"]
        if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
            raise TarotCorpusError(f"unsafe completed file path: {relative!r}")
        path = output / relative
        if not path.is_file():
            raise TarotCorpusError(f"completed artifact missing: {relative}")
        if record["sha256"] != _sha256_file(path) or record["bytes"] != path.stat().st_size:
            raise TarotCorpusError(f"completed artifact altered: {relative}")
        expected.add(relative)
    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    if actual != expected:
        raise TarotCorpusError(f"completed output file set mismatch; expected={sorted(expected)} actual={sorted(actual)}")
    index_path = output / "evidence-index.json"
    if receipt.get("evidence_index_sha256") != _sha256_file(index_path):
        raise TarotCorpusError("evidence index digest mismatch")
    return receipt


def acquire_manifest(
    manifest_path: Path,
    output: Path,
    *,
    resume: bool = False,
    max_bytes: int = DEFAULT_MAX_BYTES,
    fetcher: Fetcher | None = None,
) -> dict[str, Any]:
    """Acquire approved bytes, preserve all source locators, and seal a receipt."""
    manifest, manifest_file_sha, manifest_canonical_sha = load_manifest(manifest_path)
    fetcher = fetcher or _fetch_https
    if max_bytes <= 0:
        raise TarotCorpusError("max_bytes must be positive")

    if output.exists() and _final_receipt_path(output).exists():
        if not resume:
            raise TarotCorpusError("completed output exists; use --resume to verify and reuse it")
        return _validate_completed_run(output, manifest_file_sha, manifest_canonical_sha)

    if output.exists() and any(output.iterdir()) and not resume:
        raise TarotCorpusError("output directory is non-empty; use --resume only for a valid checkpoint")
    output.mkdir(parents=True, exist_ok=True)
    (output / "raw").mkdir(exist_ok=True)

    if resume:
        fetched = _load_checkpoint(output, manifest, manifest_file_sha, manifest_canonical_sha)
        if not fetched:
            actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
            if actual:
                raise TarotCorpusError("resume requested but no valid checkpoint or completed receipt exists")
    else:
        fetched = {}
        _write_checkpoint(output, manifest_file_sha, manifest_canonical_sha, fetched)

    for source in manifest["sources"]:
        if source["retrieval_policy"] != "fetch_bytes":
            continue
        source_id = source["source_id"]
        if source_id in fetched:
            continue
        destination = output / "raw" / source["artifact_name"]
        meta = fetcher(source["content_url"], destination, max_bytes)
        if meta.content_type != source["media_type"].lower():
            destination.unlink(missing_ok=True)
            raise TarotCorpusError(
                f"media type mismatch for {source_id}: expected {source['media_type']!r}, got {meta.content_type!r}"
            )
        if not destination.is_file():
            raise TarotCorpusError(f"fetcher did not materialize artifact: {source_id}")
        disk_sha = _sha256_file(destination)
        disk_bytes = destination.stat().st_size
        if meta.sha256 != disk_sha or meta.bytes_written != disk_bytes:
            destination.unlink(missing_ok=True)
            raise TarotCorpusError(f"fetch metadata does not match materialized bytes: {source_id}")
        fetched[source_id] = {
            "entry_sha256": _source_entry_sha(source),
            "artifact_path": f"raw/{source['artifact_name']}",
            "sha256": disk_sha,
            "bytes": disk_bytes,
            "content_type": meta.content_type,
            "final_url": meta.final_url,
        }
        _write_checkpoint(output, manifest_file_sha, manifest_canonical_sha, fetched)

    rows = [_index_row(source, fetched) for source in manifest["sources"]]
    index = {
        "schema": INDEX_SCHEMA,
        "version": OUTPUT_VERSION,
        "scope": "tarot",
        "manifest_file_sha256": manifest_file_sha,
        "manifest_canonical_sha256": manifest_canonical_sha,
        "ontology_selected": False,
        "sources": rows,
        "hmmm": manifest["hmmm"],
    }
    index_path = output / "evidence-index.json"
    index_path.write_bytes(_canonical_bytes(index))

    data_files = [index_path]
    data_files.extend(output / record["artifact_path"] for record in fetched.values())
    file_records = [
        {
            "path": path.relative_to(output).as_posix(),
            "sha256": _sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(data_files, key=lambda p: p.relative_to(output).as_posix())
    ]
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "version": OUTPUT_VERSION,
        "scope": "tarot",
        "status": "complete",
        "manifest_file_sha256": manifest_file_sha,
        "manifest_canonical_sha256": manifest_canonical_sha,
        "source_count": len(rows),
        "fetched_count": sum(row["retrieval_policy"] == "fetch_bytes" for row in rows),
        "metadata_only_count": sum(row["retrieval_policy"] == "metadata_only" for row in rows),
        "manual_review_count": sum(row["retrieval_policy"] == "manual_review" for row in rows),
        "evidence_index_sha256": _sha256_file(index_path),
        "files": file_records,
        "ontology_selected": False,
        "authority_transfer": False,
        "measurement_status_transfer": False,
        "hmmm": manifest["hmmm"],
    }
    _final_receipt_path(output).write_bytes(_canonical_bytes(receipt))
    _checkpoint_path(output).unlink(missing_ok=True)
    return _validate_completed_run(output, manifest_file_sha, manifest_canonical_sha)


def _summary(manifest: dict[str, Any]) -> str:
    counts = {policy: 0 for policy in sorted(RETRIEVAL_POLICIES)}
    for source in manifest["sources"]:
        counts[source["retrieval_policy"]] += 1
    return (
        f"Tarot sources: {len(manifest['sources'])}; "
        f"fetch_bytes={counts['fetch_bytes']}; metadata_only={counts['metadata_only']}; "
        f"manual_review={counts['manual_review']}; ontology_selected=false"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="validate manifest and print acquisition scope without network or writes")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="hard per-source byte ceiling")
    args = parser.parse_args(argv)

    manifest, _, _ = load_manifest(args.manifest)
    if args.dry_run:
        print(_summary(manifest))
        return 0
    receipt = acquire_manifest(args.manifest, args.output, resume=args.resume, max_bytes=args.max_bytes)
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
