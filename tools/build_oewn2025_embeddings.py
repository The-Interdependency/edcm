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
import sqlite3
import subprocess
import sys
import tempfile
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
_PROGRESS_INTERVAL = 1_000


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


def _write_canonical_jsonl_gz(path: Path, rows: Iterable[str]) -> int:
    """Write rows already encoded by :func:`_canonical_json`.

    This preserves the historical bytes while letting full-corpus construction
    spill completed recursive objects to disk instead of retaining them all in
    Python dictionaries.
    """

    text, raw = _gzip_text_writer(path)
    count = 0
    try:
        for row in rows:
            if not isinstance(row, str):
                raise TypeError("canonical JSONL rows must be strings")
            text.write(row)
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


def _surface_dependency_counts(graph: MorphologyGraph) -> Counter[str]:
    """Count every generated child consumption across all alternatives."""

    counts: Counter[str] = Counter()
    for surface in graph.surfaces:
        for alternative in graph.immediate(surface):
            for part in alternative.parts:
                if part.startswith("surface:"):
                    counts[part.removeprefix("surface:")] += 1
    return counts


def _initialize_row_store(connection: sqlite3.Connection) -> None:
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA temp_store=FILE")
    connection.execute(
        """
        CREATE TABLE materialized (
            surface TEXT PRIMARY KEY,
            direct_json TEXT NOT NULL,
            generated_json TEXT NOT NULL,
            direct_hash TEXT NOT NULL,
            generated_hash TEXT NOT NULL,
            comparison_json TEXT NOT NULL,
            is_root INTEGER NOT NULL CHECK (is_root IN (0, 1))
        )
        """
    )


def _materialize_row_store(
    connection: sqlite3.Connection,
    graph: MorphologyGraph,
    surface_lexemes: Mapping[str, tuple[LexemeRecord, ...]],
    synset_map: Mapping[str, Any],
    affix_gonols: Mapping[str, Any],
) -> tuple[Counter[str], float, int]:
    """Build the complete branch into a bounded-memory, disk-backed row store.

    Morphology edges always point to a shorter surface, so increasing
    ``(len(surface), surface)`` order is topological. Generated objects remain
    live only until their final declared parent consumes them. Canonical JSON,
    stable hashes, and comparison rows are stored immediately; later writers
    recover them in the historical lexicographic row order.
    """

    _initialize_row_store(connection)
    remaining_uses = _surface_dependency_counts(graph)
    generated_cache: dict[str, Any] = {}
    relation_counts: Counter[str] = Counter()
    theta_total = 0.0
    peak_cache_size = 0
    ordered_surfaces = tuple(sorted(graph.surfaces, key=lambda value: (len(value), value)))

    for index, surface in enumerate(ordered_surfaces, start=1):
        alternatives = graph.immediate(surface)
        consumed_children: list[str] = []
        if not alternatives:
            generated = assign_root_gonol(surface, surface_lexemes[surface])
            is_root = 1
        else:
            branches = []
            for alternative in alternatives:
                parts = []
                for part in alternative.parts:
                    if part.startswith("affix:"):
                        parts.append(affix_gonols[part.removeprefix("affix:")])
                        continue
                    child_surface = part.removeprefix("surface:")
                    try:
                        child = generated_cache[child_surface]
                    except KeyError as exc:
                        raise RuntimeError(
                            "generated dependency was evicted before its final use: "
                            f"parent={surface!r}, child={child_surface!r}"
                        ) from exc
                    parts.append(child)
                    consumed_children.append(child_surface)
                branches.append(compose_gonols(parts))
            generated = superpose_gonols(branches)
            is_root = 0

        direct = assign_direct_atomic_gonol(
            surface,
            surface_lexemes[surface],
            synset_map,
        )
        comparison = compare_gonols(direct, generated)
        direct_hash = gonol_sha256(direct)
        generated_hash = gonol_sha256(generated)
        direct_json = _canonical_json(intrinsic_gonol_record(direct))
        generated_json = _canonical_json(intrinsic_gonol_record(generated))
        comparison_json = _canonical_json({"surface": surface, **comparison})

        connection.execute(
            """
            INSERT INTO materialized (
                surface,
                direct_json,
                generated_json,
                direct_hash,
                generated_hash,
                comparison_json,
                is_root
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                surface,
                direct_json,
                generated_json,
                direct_hash,
                generated_hash,
                comparison_json,
                is_root,
            ),
        )

        relation_counts["equivalent" if comparison["equivalent"] else "divergent"] += 1
        if comparison["carrier_equal"]:
            relation_counts["carrier_equal"] += 1
        if comparison["face_histogram_equal"]:
            relation_counts["face_histogram_equal"] += 1
        theta_total += float(comparison["theta_jaccard"])

        if remaining_uses[surface] > 0:
            generated_cache[surface] = generated
            peak_cache_size = max(peak_cache_size, len(generated_cache))

        for child_surface in consumed_children:
            remaining_uses[child_surface] -= 1
            if remaining_uses[child_surface] < 0:
                raise RuntimeError(f"negative dependency count for {child_surface!r}")
            if remaining_uses[child_surface] == 0:
                generated_cache.pop(child_surface, None)

        if index % _PROGRESS_INTERVAL == 0 or index == len(ordered_surfaces):
            connection.commit()
            print(
                "materialized "
                f"{index}/{len(ordered_surfaces)} surfaces; "
                f"active_generated={len(generated_cache)}; "
                f"peak_active_generated={peak_cache_size}",
                flush=True,
            )

    connection.commit()
    unresolved = {surface: count for surface, count in remaining_uses.items() if count != 0}
    if unresolved:
        sample = dict(list(sorted(unresolved.items()))[:10])
        raise RuntimeError(f"unresolved generated dependency counts: {sample!r}")
    if generated_cache:
        raise RuntimeError(
            "generated cache was not empty after the final dependency use: "
            f"{tuple(sorted(generated_cache)[:10])!r}"
        )
    return relation_counts, theta_total, peak_cache_size


def _stored_column_rows(
    connection: sqlite3.Connection,
    column: str,
    *,
    roots_only: bool = False,
) -> Iterator[str]:
    allowed = {
        "direct_json",
        "generated_json",
        "comparison_json",
    }
    if column not in allowed:
        raise ValueError(f"unsupported stored column: {column!r}")
    where = " WHERE is_root = 1" if roots_only else ""
    query = f"SELECT {column} FROM materialized{where} ORDER BY surface"
    for (value,) in connection.execute(query):
        yield str(value)


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

    with tempfile.TemporaryDirectory(prefix="oewn2025-row-store-", dir=output_root) as temporary:
        database_path = Path(temporary) / "materialized.sqlite3"
        connection = sqlite3.connect(database_path)
        try:
            relation_counts, theta_total, peak_cache_size = _materialize_row_store(
                connection,
                graph,
                surface_lexemes,
                synset_map,
                affix_gonols,
            )

            _write_jsonl_gz(
                target / "roots.metadata.jsonl.gz",
                (
                    {
                        "root": surface,
                        "lexical_entries": len(surface_lexemes[surface]),
                        "parts_of_speech": sorted(
                            {item.part_of_speech for item in surface_lexemes[surface]}
                        ),
                        "gonol_sha256": generated_hash,
                    }
                    for surface, generated_hash in connection.execute(
                        "SELECT surface, generated_hash FROM materialized "
                        "WHERE is_root = 1 ORDER BY surface"
                    )
                ),
            )
            _write_jsonl_gz(
                target / "morphology.metadata.jsonl.gz",
                (
                    {
                        "surface": surface,
                        "is_root": bool(is_root),
                        "primary_tree": _tree_record(graph.primary_tree(surface)),
                        "alternatives": [
                            _decomposition_record(item)
                            for item in graph.immediate(surface)
                        ],
                        "generated_gonol_sha256": generated_hash,
                    }
                    for surface, generated_hash, is_root in connection.execute(
                        "SELECT surface, generated_hash, is_root "
                        "FROM materialized ORDER BY surface"
                    )
                ),
            )
            _write_canonical_jsonl_gz(
                target / "comparison.metadata.jsonl.gz",
                _stored_column_rows(connection, "comparison_json"),
            )
            _write_jsonl_gz(
                target / "surface-index.jsonl.gz",
                (
                    {
                        "row": index,
                        "surface": surface,
                        "attestation": "attested",
                        "soundness": "sound",
                        "parts_of_speech": sorted(
                            {item.part_of_speech for item in surface_lexemes[surface]}
                        ),
                        "direct_gonol_sha256": direct_hash,
                        "generated_gonol_sha256": generated_hash,
                    }
                    for index, (surface, direct_hash, generated_hash) in enumerate(
                        connection.execute(
                            "SELECT surface, direct_hash, generated_hash "
                            "FROM materialized ORDER BY surface"
                        )
                    )
                ),
            )

            # Intrinsic-only lists. Their order is bound only by the separate index.
            _write_canonical_jsonl_gz(
                target / "atomic-direct.gonols.jsonl.gz",
                _stored_column_rows(connection, "direct_json"),
            )
            _write_canonical_jsonl_gz(
                target / "molecular.gonols.jsonl.gz",
                _stored_column_rows(connection, "generated_json"),
            )
            _write_canonical_jsonl_gz(
                target / "atomic-generated.gonols.jsonl.gz",
                _stored_column_rows(connection, "generated_json"),
            )
            _write_canonical_jsonl_gz(
                target / "roots.gonols.jsonl.gz",
                _stored_column_rows(connection, "generated_json", roots_only=True),
            )
            _write_jsonl_gz(
                target / "affixes.gonols.jsonl.gz",
                (intrinsic_gonol_record(affix_gonols[record.affix_id]) for record in affixes),
            )
        finally:
            connection.close()

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
        "peak_active_generated_cache": peak_cache_size,
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
