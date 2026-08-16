# === CHECKS ===
# id: check_tarot_discovery_complete_acquisition_and_determinism
#   proves: tarot_discovery_consumes_only_complete_sealed_acquisition, tarot_discovery_is_byte_deterministic
#   call: self::test_discovery_requires_sealed_acquisition_and_is_byte_deterministic
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_discovery_exact_order_values_and_absence
#   proves: tarot_discovery_preserves_exact_source_order_and_values, tarot_discovery_preserves_typed_absence_and_nonclaims
#   call: self::test_discovery_preserves_order_exact_values_and_typed_absence
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_discovery_mechanical_bounds
#   proves: tarot_discovery_relations_are_mechanical_and_bounded
#   call: self::test_discovery_emits_only_frozen_relations_and_enforces_bounds
#   requires: python3
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_tarot_discovery_documented_cli
#   proves: tarot_discovery_is_byte_deterministic
#   call: self::test_documented_direct_cli_executes
#   requires: python3, posix_shell
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest

from tools.acquire_tarot_corpus import DOCTRINE, FetchMetadata, acquire_manifest
from tools.discover_tarot_relations import (
    FIELD_ORDER,
    TarotRelationDiscoveryError,
    _canonical_bytes,
    discover_relations,
)


def _source(source_id: str, *, title: str, fetched: bool = False) -> dict:
    return {
        "source_id": source_id,
        "title": title,
        "authority": "Exact Archive",
        "source_date": "test",
        "locator_url": f"https://example.test/{source_id}",
        "retrieval_policy": "fetch_bytes" if fetched else "metadata_only",
        "content_url": f"https://example.test/{source_id}.pdf" if fetched else None,
        "artifact_name": f"{source_id}.pdf" if fetched else None,
        "rights_status": "public_domain" if fetched else "source_specific",
        "rights_url": f"https://example.test/{source_id}/rights",
        "media_type": "application/pdf",
        "curation_note": "Exact evidence.",
        "provenance_note": "Do not normalize.",
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


def _seal(tmp_path: Path, sources: list[dict]) -> tuple[Path, Path]:
    manifest = tmp_path / "manifest.json"
    acquisition = tmp_path / "acquisition"
    manifest.write_text(json.dumps(_manifest(sources), indent=2) + "\n", encoding="utf-8")

    def fetch(url: str, destination: Path, max_bytes: int) -> FetchMetadata:
        payload = b"exact public evidence"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        return FetchMetadata(url, "application/pdf", len(payload), sha256(payload).hexdigest())

    acquire_manifest(manifest, acquisition, fetcher=fetch)
    return manifest, acquisition


def test_discovery_requires_sealed_acquisition_and_is_byte_deterministic(tmp_path: Path) -> None:
    manifest, acquisition = _seal(
        tmp_path,
        [_source("first", title="Tarot", fetched=True), _source("second", title="tarot")],
    )
    first = discover_relations(manifest, acquisition)
    second = discover_relations(manifest, acquisition)
    assert _canonical_bytes(first) == _canonical_bytes(second)
    (acquisition / "injected.txt").write_text("not sealed", encoding="utf-8")
    with pytest.raises(TarotRelationDiscoveryError, match="validation failed"):
        discover_relations(manifest, acquisition)


def test_discovery_preserves_order_exact_values_and_typed_absence(tmp_path: Path) -> None:
    manifest, acquisition = _seal(
        tmp_path,
        [_source("z_source", title="Tarot", fetched=True), _source("a_source", title="tarot")],
    )
    report = discover_relations(manifest, acquisition)
    assert report["source_order"] == ["z_source", "a_source"]
    title_assertions = [row for row in report["assertions"] if row["field"] == "title"]
    assert [row["value"] for row in title_assertions] == ["Tarot", "tarot"]
    assert title_assertions[0]["value_identity"] != title_assertions[1]["value_identity"]
    assert {row["state"] for row in report["typed_absences"]} == {"NA"}
    assert report["status"] == "UNRESOLVED"
    assert report["ontology_selected"] is False
    assert report["cross_source_card_identity_inferred"] is False
    assert report["geometry_attached"] is False
    assert report["measurement_attached"] is False
    assert report["canon_selection"] is None


def test_discovery_emits_only_frozen_relations_and_enforces_bounds(tmp_path: Path) -> None:
    manifest, acquisition = _seal(
        tmp_path,
        [_source("first", title="One", fetched=True), _source("second", title="Two")],
    )
    report = discover_relations(manifest, acquisition)
    assert report["algorithm"]["field_order"] == list(FIELD_ORDER)
    assert report["algorithm"]["normalization"] == "none"
    assert report["algorithm"]["ocr"] == "not-run"
    assert report["algorithm"]["image_interpretation"] == "not-run"
    assert report["adjacency_relations"] == [{
        "relation": "next-source-in-manifest",
        "source": "first",
        "target": "second",
        "source_ordinal": 0,
        "target_ordinal": 1,
    }]
    assert len(report["artifact_bindings"]) == 1
    assert all(row["relation"] == "same-field-exact-value" for row in report["exact_value_agreements"])
    with pytest.raises(TarotRelationDiscoveryError, match="source resource bound"):
        discover_relations(manifest, acquisition, max_sources=1)
    with pytest.raises(TarotRelationDiscoveryError, match="assertion resource bound"):
        discover_relations(manifest, acquisition, max_assertions=1)


def test_documented_direct_cli_executes(tmp_path: Path) -> None:
    manifest, acquisition = _seal(tmp_path, [_source("first", title="One")])
    output = tmp_path / "relations.json"
    subprocess.run(
        [
            sys.executable,
            "tools/discover_tarot_relations.py",
            "--manifest",
            str(manifest),
            "--acquisition",
            str(acquisition),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(output.read_bytes())["counts"]["sources"] == 1
