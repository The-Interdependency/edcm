# === CHECKS ===
# id: check_tarot_manifest_preserves_preontology_boundary
#   proves: tarot_manifest_preserves_preontology_boundary
#   call: self::test_committed_manifest_validates_without_tarot_ontology
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_tarot_fetch_authority_and_metadata_only_boundary
#   proves: tarot_acquisition_fetches_only_authorized_public_domain_bytes, tarot_metadata_only_sources_are_not_downloaded, tarot_acquisition_preserves_source_identity
#   call: self::test_acquisition_fetches_only_public_domain_and_seals_source_identity
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_completed_resume_fails_closed
#   proves: tarot_acquisition_resume_fails_closed
#   call: self::test_completed_resume_reuses_exact_state_and_rejects_tamper
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_interrupted_resume_checkpoint
#   proves: tarot_acquisition_resume_fails_closed, tarot_acquisition_preserves_source_identity
#   call: self::test_interrupted_resume_keeps_verified_completed_sources
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_auto_fetch_rights_gate
#   proves: tarot_acquisition_fetches_only_authorized_public_domain_bytes
#   call: self::test_manifest_rejects_auto_fetch_without_public_domain_rights
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from tools.acquire_tarot_corpus import (
    DOCTRINE,
    FetchMetadata,
    TarotCorpusError,
    acquire_manifest,
    load_manifest,
    validate_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "corpus" / "tarot" / "sources.v1.json"


def _source(
    source_id: str,
    *,
    policy: str,
    rights: str,
    artifact: str | None = None,
    content_url: str | None = None,
) -> dict:
    return {
        "source_id": source_id,
        "title": f"Source {source_id}",
        "authority": "Test archive",
        "source_date": "test",
        "locator_url": f"https://example.test/{source_id}",
        "retrieval_policy": policy,
        "content_url": content_url,
        "artifact_name": artifact,
        "rights_status": rights,
        "rights_url": f"https://example.test/{source_id}/rights",
        "media_type": "application/pdf",
        "curation_note": "Evidence fixture only.",
        "provenance_note": "Preserve exact test source identity.",
    }


def _manifest(sources: list[dict]) -> dict:
    return {
        "schema": "edcm.tarot-corpus-manifest",
        "version": "1.0.0",
        "scope": "tarot",
        "frozen_on": "2026-08-16",
        "doctrine": deepcopy(DOCTRINE),
        "sources": sources,
        "hmmm": ["fixture incompletion"],
    }


def _write_manifest(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def _fake_fetch(calls: list[str], payloads: dict[str, bytes]):
    def fetch(url: str, destination: Path, max_bytes: int) -> FetchMetadata:
        calls.append(url)
        data = payloads[url]
        assert len(data) <= max_bytes
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return FetchMetadata(
            final_url=url,
            content_type="application/pdf",
            bytes_written=len(data),
            sha256=sha256(data).hexdigest(),
        )

    return fetch


def test_committed_manifest_validates_without_tarot_ontology() -> None:
    manifest, _, _ = load_manifest(MANIFEST)
    assert manifest["scope"] == "tarot"
    assert manifest["doctrine"] == DOCTRINE
    assert manifest["doctrine"]["ontology_selected"] is False
    assert manifest["doctrine"]["canonical_deck_selected"] is False
    assert manifest["doctrine"]["canonical_card_count_selected"] is False
    assert manifest["doctrine"]["cross_source_card_identity_inference"] is False
    assert manifest["doctrine"]["i_ching_in_scope"] is False
    assert len({source["source_id"] for source in manifest["sources"]}) == len(manifest["sources"])
    assert len(manifest["sources"]) >= 12

    polluted = deepcopy(manifest)
    polluted["ontology"] = {"major_arcana": 22}
    with pytest.raises(TarotCorpusError):
        validate_manifest(polluted)


def test_acquisition_fetches_only_public_domain_and_seals_source_identity(tmp_path: Path) -> None:
    fetch_url = "https://example.test/public.pdf"
    manifest = _manifest(
        [
            _source(
                "public_primary",
                policy="fetch_bytes",
                rights="public_domain_mark",
                artifact="public.pdf",
                content_url=fetch_url,
            ),
            _source("metadata_secondary", policy="metadata_only", rights="in_copyright"),
            _source("manual_archive", policy="manual_review", rights="source_specific"),
        ]
    )
    manifest_path = tmp_path / "manifest.json"
    output = tmp_path / "out"
    _write_manifest(manifest_path, manifest)
    calls: list[str] = []
    receipt = acquire_manifest(
        manifest_path,
        output,
        fetcher=_fake_fetch(calls, {fetch_url: b"tarot evidence"}),
    )
    assert calls == [fetch_url]
    assert receipt["fetched_count"] == 1
    assert receipt["metadata_only_count"] == 1
    assert receipt["manual_review_count"] == 1
    assert receipt["ontology_selected"] is False
    index = json.loads((output / "evidence-index.json").read_bytes())
    rows = {row["source_id"]: row for row in index["sources"]}
    assert rows["public_primary"]["sha256"] == sha256(b"tarot evidence").hexdigest()
    assert rows["metadata_secondary"]["artifact_path"] is None
    assert rows["manual_archive"]["artifact_path"] is None
    assert all(row["entry_sha256"] for row in rows.values())


def test_completed_resume_reuses_exact_state_and_rejects_tamper(tmp_path: Path) -> None:
    fetch_url = "https://example.test/public.pdf"
    manifest = _manifest(
        [_source("public_primary", policy="fetch_bytes", rights="public_domain", artifact="public.pdf", content_url=fetch_url)]
    )
    manifest_path = tmp_path / "manifest.json"
    output = tmp_path / "out"
    _write_manifest(manifest_path, manifest)
    calls: list[str] = []
    first = acquire_manifest(manifest_path, output, fetcher=_fake_fetch(calls, {fetch_url: b"stable"}))
    assert calls == [fetch_url]

    def forbidden_fetch(url: str, destination: Path, max_bytes: int) -> FetchMetadata:  # pragma: no cover - should never run
        raise AssertionError("completed resume must not fetch")

    second = acquire_manifest(manifest_path, output, resume=True, fetcher=forbidden_fetch)
    assert second == first

    (output / "raw" / "public.pdf").write_bytes(b"tampered")
    with pytest.raises(TarotCorpusError):
        acquire_manifest(manifest_path, output, resume=True, fetcher=forbidden_fetch)


def test_interrupted_resume_keeps_verified_completed_sources(tmp_path: Path) -> None:
    first_url = "https://example.test/first.pdf"
    second_url = "https://example.test/second.pdf"
    manifest = _manifest(
        [
            _source("first_primary", policy="fetch_bytes", rights="public_domain_mark", artifact="first.pdf", content_url=first_url),
            _source("second_primary", policy="fetch_bytes", rights="public_domain_mark", artifact="second.pdf", content_url=second_url),
        ]
    )
    manifest_path = tmp_path / "manifest.json"
    output = tmp_path / "out"
    _write_manifest(manifest_path, manifest)
    calls: list[str] = []

    def fail_second(url: str, destination: Path, max_bytes: int) -> FetchMetadata:
        calls.append(url)
        if url == second_url:
            raise RuntimeError("simulated interruption")
        data = b"first complete"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return FetchMetadata(url, "application/pdf", len(data), sha256(data).hexdigest())

    with pytest.raises(RuntimeError):
        acquire_manifest(manifest_path, output, fetcher=fail_second)
    assert calls == [first_url, second_url]
    assert (output / "raw" / "first.pdf").is_file()
    assert (output / ".checkpoint.json").is_file()

    resume_calls: list[str] = []
    receipt = acquire_manifest(
        manifest_path,
        output,
        resume=True,
        fetcher=_fake_fetch(resume_calls, {second_url: b"second complete"}),
    )
    assert resume_calls == [second_url]
    assert receipt["fetched_count"] == 2
    assert not (output / ".checkpoint.json").exists()

    (output / "injected.txt").write_text("not evidence", encoding="utf-8")
    with pytest.raises(TarotCorpusError):
        acquire_manifest(manifest_path, output, resume=True)


def test_manifest_rejects_auto_fetch_without_public_domain_rights() -> None:
    manifest = _manifest(
        [
            _source(
                "restricted",
                policy="fetch_bytes",
                rights="in_copyright",
                artifact="restricted.pdf",
                content_url="https://example.test/restricted.pdf",
            )
        ]
    )
    with pytest.raises(TarotCorpusError):
        validate_manifest(manifest)
