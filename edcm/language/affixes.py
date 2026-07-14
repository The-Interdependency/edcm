"""Complete affix inventory for the OEWN 2025 embedding run.

"Complete" means every canonical affix and every declared allomorph in EDCM's
versioned ``bones_affixes_v1.json`` is materialized. The inventory is a frozen
run boundary, not a claim that English can never acquire another affix.

Applicability is universal: no record contains or enforces a root-selection
predicate. Conventionality is evidence attached after composition.
"""

# === MODULE_BUILD ===
# id: edcm_language_affixes
#   module_name: affixes
#   module_kind: engine
#   summary: expands every canonical EDCM affix and allomorph into a deterministic universally applicable inventory for the OEWN 2025 run
#   owner: Erin Spencer
#   public_surface: AffixRecord, load_affix_inventory, affix_inventory_record
#   internal_surface: _canon_path, _slug
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_full_run
#   rollout: default_enabled
#   rollback: restore the prior inventory version and regenerate every dependent artifact
#   requires: edcm measurement canon bones_affixes_v1.json
#   since: 2026-07-13
#   unresolved: future run versions may add newly documented English affixes without invalidating this freeze
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Any


@dataclass(frozen=True, slots=True)
class AffixRecord:
    """One canonical affix realization.

    Distinct grammatical operations sharing the same spelling remain distinct
    records, for example plural ``-s`` and third-person singular ``-s``.
    """

    affix_id: str
    canonical: str
    surface: str
    kind: str
    section: str
    primary: str
    families: tuple[str, ...]
    notes: str
    variant_of: str | None
    universally_applicable: bool = True

    @property
    def bare(self) -> str:
        if self.kind == "prefix":
            return self.surface.removesuffix("-")
        if self.kind == "suffix":
            return self.surface.removeprefix("-")
        return self.surface


_SECTION_ORDER = (
    "inflectional",
    "derivational_prefixes",
    "derivational_suffixes",
    "contractions",
)


def _canon_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "measurement"
        / "canon"
        / "data"
        / "bones_affixes_v1.json"
    )


def _slug(value: str) -> str:
    value = value.replace("'", "apostrophe").replace("-", "dash")
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_").lower()
    return value or "empty"


def load_affix_inventory(path: str | Path | None = None) -> tuple[AffixRecord, ...]:
    """Return every declared affix operation and allomorph in stable order."""

    source = Path(path) if path is not None else _canon_path()
    document = json.loads(source.read_text(encoding="utf-8"))
    records: list[AffixRecord] = []
    for section in _SECTION_ORDER:
        entries = document[section]["affixes"]
        for index, entry in enumerate(entries):
            canonical = str(entry["affix"])
            operation_id = (
                f"{section}:{index:03d}:{entry['type']}:"
                f"{_slug(canonical)}:{entry['primary']}"
            )
            base = AffixRecord(
                affix_id=operation_id,
                canonical=canonical,
                surface=canonical,
                kind=str(entry["type"]),
                section=section,
                primary=str(entry["primary"]),
                families=tuple(str(item) for item in entry.get("families", [entry["primary"]])),
                notes=str(entry.get("notes", "")),
                variant_of=None,
            )
            records.append(base)
            for variant_index, variant in enumerate(entry.get("variants", ())):
                records.append(
                    AffixRecord(
                        affix_id=f"{operation_id}:variant:{variant_index:02d}:{_slug(str(variant))}",
                        canonical=canonical,
                        surface=str(variant),
                        kind=str(entry["type"]),
                        section=section,
                        primary=str(entry["primary"]),
                        families=tuple(
                            str(item) for item in entry.get("families", [entry["primary"]])
                        ),
                        notes=str(entry.get("notes", "")),
                        variant_of=operation_id,
                    )
                )
    return tuple(records)


def affix_inventory_record(records: tuple[AffixRecord, ...] | None = None) -> dict[str, Any]:
    """Return the metadata-bearing affix artifact payload."""

    values = records if records is not None else load_affix_inventory()
    return {
        "schema": "edcm.english-affix-inventory",
        "version": "1.0.0",
        "universal_application": True,
        "selection_restrictions": False,
        "source": "edcm/measurement/canon/data/bones_affixes_v1.json",
        "count": len(values),
        "affixes": [asdict(record) for record in values],
    }


__all__ = ["AffixRecord", "affix_inventory_record", "load_affix_inventory"]
