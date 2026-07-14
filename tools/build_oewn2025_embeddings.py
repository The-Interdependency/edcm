#!/usr/bin/env python3
"""Build the complete Open English WordNet 2025 atomic/molecular run.

The script consumes a local checkout of the exact upstream release commit and
writes deterministic, compressed artifacts. Pure gonol lists contain intrinsic
UCNS data only; every word, index, provenance, parse, and comparison field lives
in separate metadata artifacts.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import gzip
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterable, Iterator, Mapping, Sequence, TextIO

from edcm.language.affixes import affix_inventory_record, load_affix_inventory
from edcm.language.artifacts import intrinsic_gonol_record
from edcm.language.composition import compose_gonols
from edcm.language.morphology import Decomposition, MorphologyGraph, build_morphology_graph
from edcm.language.placement import (
    assign_affix_gonol,
    assign_direct_atomic_gonol,
    assign_root_gonol,
    compare_gonols,
    gonol_sha256,
    superpose_gonols,
)
from edcm.language.rendering import normalize_lemma, transformation_inventory
from edcm.language.source import (
    OEWN_COMMIT,
    OEWN_EXPECTED_RELATION_COUNT,
    OEWN_EXPECTED_SYNSET_COUNT,
    OEWN_EXPECTED_WORD_COUNT,
    OEWN_LICENSE,
    OEWN_RELEASE_DATE,
    OEWN_REPOSITORY,
    OEWN_TAG,
    LexemeRecord,
    load_oewn_2025,
)

SCHEMA_VERSION = "1.0.0"
ARTIFACT_DIRECTORY = "oewn2025"


def _git(repo: Path, *arguments: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *arguments],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _gzip_text_writer(path: Path) -> tuple[TextIO, io.BufferedWriter]:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = path.open("wb")
    compressed = gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9)
    text = io.TextIOWrapper(compressed, encoding="utf-8", newline="\n")
    return text, raw


def _write_jsonl_gz(path: Path, rows: Iterable[Any]) -> int:
    text, raw = _gzip_text_writer(path)
    count = 0
    try:
        for row in rows:
            text.write(_canonical_json(row))
            text.write("\n")
            count += 1
        text.flush()
        text.close()
    finally:
        if not raw.closed:
            raw.close()
    return count


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_record(node: Any) -> dict[str, Any]:
    if node.leaf_id is not None:
        return {"leaf": node.leaf_id}
    return {"children": [_tree_record(child) for child in node.children]}


def _decomposition_record(value: Decomposition) -> dict[str, Any]:
    return asdict(value)


def _surface_lexeme_map(snapshot: Any) -> dict[str, tuple[LexemeRecord, ...]]:
    grouped: dict[str, list[LexemeRecord]] = defaultdict(list)
    for lexeme in snapshot.lexemes:
        surfaces = {normalize_lemma(lexeme.lemma)}
        surfaces.update(normalize_lemma(form) for form in lexeme.forms)
        for surface in surfaces:
            if surface:
                grouped[surface].append(lexeme)
    return {
        surface: tuple(sorted(values, key=lambda item: (item.lemma, item.part_of_speech)))
        for surface, values in sorted(grouped.items())
    }


def _materializer(
    graph: MorphologyGraph,
    root_gonols: Mapping[str, Any],
    affix_gonols: Mapping[str, Any],
):
    primary_cache: dict[str, Any] = {}
    all_cache: dict[str, Any] = {}

    def resolve_part(part: str, *, all_alternatives: bool) -> Any:
        if part.startswith("affix:"):
            return affix_gonols[part.removeprefix("affix:")]
        surface = part.removeprefix("surface:")
        return materialize_all(surface) if all_alternatives else materialize_primary(surface)

    def materialize_primary(surface: str) -> Any:
        if surface in primary_cache:
            return primary_cache[surface]
        alternatives = graph.immediate(surface)
        if not alternatives:
            result = root_gonols[surface]
        else:
            selected_tree = graph.primary_tree(surface)

            def materialize_tree(node: Any) -> Any:
                if node.leaf_id is not None:
                    if node.leaf_id.startswith("affix:"):
                        return affix_gonols[node.leaf_id.removeprefix("affix:")]
                    return root_gonols[node.leaf_id.removeprefix("root:")]
                return compose_gonols(materialize_tree(child) for child in node.children)

            result = materialize_tree(selected_tree)
        primary_cache[surface] = result
        return result

    def materialize_all(surface: str) -> Any:
        if surface in all_cache:
            return all_cache[surface]
        alternatives = graph.immediate(surface)
        if not alternatives:
            result = root_gonols[surface]
        else:
            branch_gonols = []
            for alternative in alternatives:
                branch_gonols.append(
                    compose_gonols(
                        resolve_part(part, all_alternatives=True)
                        for part in alternative.parts
                    )
                )
            result = superpose_gonols(branch_gonols)
        all_cache[surface] = result
        return result

    return materialize_primary, materialize_all


def _artifact_manifest(root: Path, paths: Sequence[Path]) -> dict[str, Any]:
    records = []
    for path in sorted(paths):
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": _file_sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    return {"files": records}


def build(source_repo: Path, output_root: Path) -> dict[str, Any]:
    source_repo = source_repo.resolve()
    output_root = output_root.resolve()
    source_commit = _git(source_repo, "rev-parse", "HEAD")
    if source_commit != OEWN_COMMIT:
        raise RuntimeError(f"source commit mismatch: expected {OEWN_COMMIT}, got {source_commit}")
    exact_tag_commit = _git(source_repo, "rev-list", "-n", "1", OEWN_TAG)
    if exact_tag_commit != OEWN_COMMIT:
        raise RuntimeError(f"tag {OEWN_TAG} no longer resolves to the pinned commit")

    snapshot = load_oewn_2025(source_repo / "src" / "yaml")
    # The release table's "Words" count is lexical entries, not unique strings.
    if len(snapshot.lexemes) != OEWN_EXPECTED_WORD_COUNT:
        raise RuntimeError(
            f"lexical-entry count mismatch: expected {OEWN_EXPECTED_WORD_COUNT}, got {len(snapshot.lexemes)}"
        )
    if len(snapshot.synsets) != OEWN_EXPECTED_SYNSET_COUNT:
        raise RuntimeError(
            f"synset count mismatch: expected {OEWN_EXPECTED_SYNSET_COUNT}, got {len(snapshot.synsets)}"
        )

    target = output_root / ARTIFACT_DIRECTORY
    target.mkdir(parents=True, exist_ok=True)
    surface_lexemes = _surface_lexeme_map(snapshot)
    surfaces = tuple(surface_lexemes)
    synset_map = snapshot.synset_map()

    affixes = load_affix_inventory()
    graph = build_morphology_graph(surfaces, affixes)

    affix_gonols = {record.affix_id: assign_affix_gonol(record) for record in affixes}
    root_gonols = {
        root: assign_root_gonol(root, surface_lexemes[root])
        for root in graph.roots
    }
    direct_gonols = {
        surface: assign_direct_atomic_gonol(surface, surface_lexemes[surface], synset_map)
        for surface in surfaces
    }
    materialize_primary, materialize_all = _materializer(graph, root_gonols, affix_gonols)

    # Force the complete generated branch in increasing length order so every
    # dependency is already memoized when possible.
    generated_gonols: dict[str, Any] = {}
    for surface in sorted(surfaces, key=lambda value: (len(value), value)):
        generated_gonols[surface] = materialize_all(surface)

    _write_json(target / "source-manifest.json", {
        "schema": "edcm.oewn-source-manifest",
        "version": SCHEMA_VERSION,
        "repository": OEWN_REPOSITORY,
        "tag": OEWN_TAG,
        "commit": OEWN_COMMIT,
        "release_date": OEWN_RELEASE_DATE,
        "license": OEWN_LICENSE,
        "source_tree_sha256": snapshot.source_tree_sha256,
        "source_file_count": snapshot.source_file_count,
        "lexical_entry_count": len(snapshot.lexemes),
        "unique_lemma_count": len(snapshot.lemmas),
        "materialized_surface_count": len(surfaces),
        "sense_count": snapshot.sense_count,
        "synset_count": len(snapshot.synsets),
        "observed_relation_count": snapshot.relation_count,
        "release_reported_relation_count": OEWN_EXPECTED_RELATION_COUNT,
    })
    _write_json(target / "affixes.json", affix_inventory_record(affixes))
    _write_json(target / "transformations.json", transformation_inventory())

    _write_jsonl_gz(
        target / "roots.metadata.jsonl.gz",
        (
            {
                "root": root,
                "lexical_entries": len(surface_lexemes[root]),
                "parts_of_speech": sorted({item.part_of_speech for item in surface_lexemes[root]}),
                "gonol_sha256": gonol_sha256(root_gonols[root]),
            }
            for root in graph.roots
        ),
    )
    _write_jsonl_gz(
        target / "morphology.metadata.jsonl.gz",
        (
            {
                "surface": surface,
                "is_root": surface in root_gonols,
                "primary_tree": _tree_record(graph.primary_tree(surface)),
                "alternatives": [_decomposition_record(item) for item in graph.immediate(surface)],
                "generated_gonol_sha256": gonol_sha256(generated_gonols[surface]),
            }
            for surface in surfaces
        ),
    )

    comparisons: dict[str, dict[str, Any]] = {}
    relation_counts: Counter[str] = Counter()
    theta_total = 0.0
    for surface in surfaces:
        comparison = compare_gonols(direct_gonols[surface], generated_gonols[surface])
        comparisons[surface] = comparison
        relation_counts["equivalent" if comparison["equivalent"] else "divergent"] += 1
        if comparison["carrier_equal"]:
            relation_counts["carrier_equal"] += 1
        if comparison["face_histogram_equal"]:
            relation_counts["face_histogram_equal"] += 1
        theta_total += float(comparison["theta_jaccard"])

    _write_jsonl_gz(
        target / "comparison.metadata.jsonl.gz",
        ({"surface": surface, **comparisons[surface]} for surface in surfaces),
    )
    _write_jsonl_gz(
        target / "surface-index.jsonl.gz",
        (
            {
                "row": index,
                "surface": surface,
                "attestation": "attested",
                "soundness": "sound",
                "parts_of_speech": sorted({item.part_of_speech for item in surface_lexemes[surface]}),
                "direct_gonol_sha256": gonol_sha256(direct_gonols[surface]),
                "generated_gonol_sha256": gonol_sha256(generated_gonols[surface]),
            }
            for index, surface in enumerate(surfaces)
        ),
    )

    # Intrinsic-only lists. Their order is bound only by the separate index.
    _write_jsonl_gz(
        target / "atomic-direct.gonols.jsonl.gz",
        (intrinsic_gonol_record(direct_gonols[surface]) for surface in surfaces),
    )
    _write_jsonl_gz(
        target / "molecular.gonols.jsonl.gz",
        (intrinsic_gonol_record(generated_gonols[surface]) for surface in surfaces),
    )
    _write_jsonl_gz(
        target / "atomic-generated.gonols.jsonl.gz",
        (intrinsic_gonol_record(generated_gonols[surface]) for surface in surfaces),
    )
    _write_jsonl_gz(
        target / "roots.gonols.jsonl.gz",
        (intrinsic_gonol_record(root_gonols[root]) for root in graph.roots),
    )
    _write_jsonl_gz(
        target / "affixes.gonols.jsonl.gz",
        (intrinsic_gonol_record(affix_gonols[record.affix_id]) for record in affixes),
    )

    summary = {
        "schema": "edcm.oewn-atomic-molecular-run-summary",
        "version": SCHEMA_VERSION,
        "surface_count": len(surfaces),
        "root_count": len(graph.roots),
        "affix_count": len(affixes),
        "decomposed_surface_count": len(graph.alternatives),
        "ambiguous_surface_count": sum(1 for values in graph.alternatives.values() if len(values) > 1),
        "molecular_alternative_count": sum(len(values) for values in graph.alternatives.values()),
        "fork_counts": dict(sorted(relation_counts.items())),
        "mean_theta_jaccard": 0.0 if not surfaces else theta_total / len(surfaces),
        "direct_assignment": "whole-word OEWN sense and relation topology",
        "molecular_assignment": "public 157-glyph components plus universal UCNS composition",
        "generated_atomic_materialization": "complete alternative superposition",
    }
    _write_json(target / "summary.json", summary)

    notice = f"""# Open English WordNet 2025 embedding artifacts

Generated from `{OEWN_REPOSITORY}` tag `{OEWN_TAG}` at commit `{OEWN_COMMIT}`.

Open English WordNet is derived from Princeton WordNet under the WordNet
License and further developed under the Creative Commons Attribution 4.0
International License. Attribution is due to Princeton WordNet and the Open
English WordNet team. See the upstream `LICENSE.md` and `WNDB_License.txt`.

The `*.gonols.jsonl.gz` files contain intrinsic UCNS data only. They deliberately
contain no words, labels, provenance, soundness, attestation, or embedding names.
`surface-index.jsonl.gz` supplies the external row correspondence.
"""
    (target / "README.md").write_text(notice, encoding="utf-8")

    generated_paths = tuple(path for path in target.rglob("*") if path.is_file())
    artifact_records = _artifact_manifest(output_root, generated_paths)
    final_manifest = {
        "schema": "edcm.oewn-embedding-artifact-set",
        "version": SCHEMA_VERSION,
        "summary": summary,
        **artifact_records,
    }
    _write_json(target / "manifest.json", final_manifest)
    return final_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", required=True, type=Path)
    parser.add_argument("--output-root", default="artifacts", type=Path)
    args = parser.parse_args()
    manifest = build(args.source_repo, args.output_root)
    print(json.dumps(manifest["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
