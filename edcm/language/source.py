"""Pinned Open English WordNet 2025 source ingestion.

The full dataset is never inferred from a moving branch. Builders must check out
``globalwordnet/english-wordnet`` at the exact release tag and commit declared
below, then pass the ``src/yaml`` directory to :func:`load_oewn_2025`.
"""

# === MODULE_BUILD ===
# id: edcm_language_oewn_source
#   module_name: source
#   module_kind: adapter
#   summary: loads the exact Open English WordNet 2025 YAML release into deterministic lemma, sense, synset, and relation records and computes a source-tree digest
#   owner: Erin Spencer
#   public_surface: OEWN_REPOSITORY, OEWN_TAG, OEWN_COMMIT, OEWN_LICENSE, LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot, load_oewn_2025
#   internal_surface: _load_yaml, _source_tree_digest, _relation_values
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_full_run
#   rollout: builder_only
#   rollback: remove loader and generated artifacts before publishing another source manifest
#   requires: PyYAML only during artifact construction
#   since: 2026-07-13
#   unresolved: none
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

OEWN_REPOSITORY = "globalwordnet/english-wordnet"
OEWN_TAG = "2025-edition"
OEWN_COMMIT = "dc343f2683279ecbb13fab4e2fd778d7b162d287"
OEWN_LICENSE = "Princeton WordNet License plus CC BY 4.0"
OEWN_RELEASE_DATE = "2025-12-31"
OEWN_EXPECTED_WORD_COUNT = 135_969
OEWN_EXPECTED_SYNSET_COUNT = 107_519
OEWN_EXPECTED_RELATION_COUNT = 355_064

_ENTRY_KEYS = {"form", "sense", "pronunciation"}
_SENSE_NON_RELATION_KEYS = {"id", "synset", "sent", "subcat", "adjposition"}
_SYNSET_NON_RELATION_KEYS = {
    "ili",
    "partOfSpeech",
    "definition",
    "example",
    "members",
    "source",
    "wikidata",
}


@dataclass(frozen=True, slots=True)
class SenseRecord:
    """One OEWN sense as represented in an entry YAML file."""

    sense_id: str
    synset_id: str
    relations: tuple[tuple[str, tuple[str, ...]], ...]
    subcategories: tuple[str, ...] = ()
    adjective_position: str | None = None


@dataclass(frozen=True, slots=True)
class LexemeRecord:
    """One lemma/POS entry. A surface lemma can own several records."""

    lemma: str
    part_of_speech: str
    forms: tuple[str, ...]
    senses: tuple[SenseRecord, ...]


@dataclass(frozen=True, slots=True)
class SynsetRecord:
    """The whole-word semantic context used by direct atomic placement."""

    synset_id: str
    part_of_speech: str
    members: tuple[str, ...]
    definitions: tuple[str, ...]
    relations: tuple[tuple[str, tuple[str, ...]], ...]


@dataclass(frozen=True, slots=True)
class WordnetSnapshot:
    """Deterministically ordered, dictionary-bounded source snapshot."""

    lexemes: tuple[LexemeRecord, ...]
    synsets: tuple[SynsetRecord, ...]
    source_tree_sha256: str
    source_file_count: int

    @property
    def lemmas(self) -> tuple[str, ...]:
        return tuple(sorted({record.lemma for record in self.lexemes}))

    @property
    def sense_count(self) -> int:
        return sum(len(record.senses) for record in self.lexemes)

    @property
    def relation_count(self) -> int:
        return sum(
            len(targets)
            for synset in self.synsets
            for _, targets in synset.relations
        ) + sum(
            len(targets)
            for lexeme in self.lexemes
            for sense in lexeme.senses
            for _, targets in sense.relations
        )

    def synset_map(self) -> dict[str, SynsetRecord]:
        return {record.synset_id: record for record in self.synsets}

    def lexemes_by_lemma(self) -> dict[str, tuple[LexemeRecord, ...]]:
        grouped: dict[str, list[LexemeRecord]] = {}
        for record in self.lexemes:
            grouped.setdefault(record.lemma, []).append(record)
        return {
            lemma: tuple(sorted(records, key=lambda item: item.part_of_speech))
            for lemma, records in grouped.items()
        }


def _load_yaml(path: Path) -> Mapping[str, Any]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - exercised by builder environment
        raise RuntimeError("PyYAML is required to construct OEWN artifacts") from exc
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"expected a YAML mapping in {path}")
    return value


def _source_tree_digest(paths: Iterable[Path], root: Path) -> str:
    digest = sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _relation_values(
    payload: Mapping[str, Any],
    excluded: set[str],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    relations: list[tuple[str, tuple[str, ...]]] = []
    for key, value in payload.items():
        if key in excluded or not isinstance(value, list):
            continue
        targets = tuple(sorted(str(item) for item in value if isinstance(item, (str, int))))
        if targets:
            relations.append((str(key), targets))
    return tuple(sorted(relations))


def _iter_entry_files(root: Path) -> Iterator[Path]:
    yield from sorted(root.rglob("entries-*.yaml"))


def _iter_synset_files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*.yaml")):
        if path.name == "frames.yaml" or path.name.startswith("entries-"):
            continue
        yield path


def load_oewn_2025(source_root: str | Path) -> WordnetSnapshot:
    """Load the exact core 2025 YAML tree.

    Parameters
    ----------
    source_root:
        Path to the checked-out ``src/yaml`` directory from ``OEWN_COMMIT``.
        The caller is responsible for proving the Git commit; the resulting
        source-tree digest proves the exact bytes consumed by this run.
    """

    root = Path(source_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    frames = root / "frames.yaml"
    if not frames.is_file():
        raise ValueError(f"{root} is not an OEWN YAML source directory")

    all_yaml = tuple(sorted(root.rglob("*.yaml")))
    lexemes: list[LexemeRecord] = []
    for path in _iter_entry_files(root):
        document = _load_yaml(path)
        for raw_lemma, raw_pos_map in document.items():
            if not isinstance(raw_pos_map, Mapping):
                continue
            lemma = str(raw_lemma)
            for raw_pos, raw_properties in raw_pos_map.items():
                if not isinstance(raw_properties, Mapping):
                    continue
                forms = tuple(sorted(str(item) for item in raw_properties.get("form", []) or []))
                senses: list[SenseRecord] = []
                for raw_sense in raw_properties.get("sense", []) or []:
                    if not isinstance(raw_sense, Mapping):
                        continue
                    sense_id = str(raw_sense.get("id", ""))
                    synset_id = str(raw_sense.get("synset", ""))
                    if not sense_id or not synset_id:
                        raise ValueError(f"incomplete sense in {path}: {raw_sense!r}")
                    subcat = raw_sense.get("subcat", ()) or ()
                    if isinstance(subcat, str):
                        subcategories = (subcat,)
                    else:
                        subcategories = tuple(sorted(str(item) for item in subcat))
                    senses.append(
                        SenseRecord(
                            sense_id=sense_id,
                            synset_id=synset_id,
                            relations=_relation_values(raw_sense, _SENSE_NON_RELATION_KEYS),
                            subcategories=subcategories,
                            adjective_position=(
                                None
                                if raw_sense.get("adjposition") is None
                                else str(raw_sense["adjposition"])
                            ),
                        )
                    )
                lexemes.append(
                    LexemeRecord(
                        lemma=lemma,
                        part_of_speech=str(raw_pos),
                        forms=forms,
                        senses=tuple(sorted(senses, key=lambda item: item.sense_id)),
                    )
                )

    synsets: list[SynsetRecord] = []
    for path in _iter_synset_files(root):
        document = _load_yaml(path)
        for raw_id, raw_properties in document.items():
            if not isinstance(raw_properties, Mapping):
                continue
            definitions_raw = raw_properties.get("definition", ()) or ()
            definitions = tuple(
                str(item.get("text", "")) if isinstance(item, Mapping) else str(item)
                for item in definitions_raw
            )
            synsets.append(
                SynsetRecord(
                    synset_id=str(raw_id),
                    part_of_speech=str(raw_properties.get("partOfSpeech", "")),
                    members=tuple(sorted(str(item) for item in raw_properties.get("members", ()) or ())),
                    definitions=definitions,
                    relations=_relation_values(raw_properties, _SYNSET_NON_RELATION_KEYS),
                )
            )

    snapshot = WordnetSnapshot(
        lexemes=tuple(sorted(lexemes, key=lambda item: (item.lemma, item.part_of_speech))),
        synsets=tuple(sorted(synsets, key=lambda item: item.synset_id)),
        source_tree_sha256=_source_tree_digest(all_yaml, root),
        source_file_count=len(all_yaml),
    )
    if len(snapshot.lemmas) != OEWN_EXPECTED_WORD_COUNT:
        raise ValueError(
            "OEWN 2025 word count mismatch: "
            f"expected {OEWN_EXPECTED_WORD_COUNT}, got {len(snapshot.lemmas)}"
        )
    if len(snapshot.synsets) != OEWN_EXPECTED_SYNSET_COUNT:
        raise ValueError(
            "OEWN 2025 synset count mismatch: "
            f"expected {OEWN_EXPECTED_SYNSET_COUNT}, got {len(snapshot.synsets)}"
        )
    return snapshot


__all__ = [
    "LexemeRecord",
    "OEWN_COMMIT",
    "OEWN_EXPECTED_RELATION_COUNT",
    "OEWN_EXPECTED_SYNSET_COUNT",
    "OEWN_EXPECTED_WORD_COUNT",
    "OEWN_LICENSE",
    "OEWN_RELEASE_DATE",
    "OEWN_REPOSITORY",
    "OEWN_TAG",
    "SenseRecord",
    "SynsetRecord",
    "WordnetSnapshot",
    "load_oewn_2025",
]
