"""Pinned scope and provenance for the English atomic/molecular embedding run."""

# === MODULE_BUILD ===
# id: edcm_language_manifest
#   module_name: manifest
#   module_kind: policy
#   summary: pins the dictionary boundary, public 157-glyph floor provenance, and dual direct/generated English embedding doctrine
#   owner: Erin Spencer
#   public_surface: EnglishEmbeddingManifest, embedding_manifest, SOURCE_DICTIONARY, PUBLIC_GLYPH_FLOOR_SOURCE
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: default_enabled
#   rollback: remove language embedding package before any published artifact depends on this manifest
#   requires: none
#   since: 2026-07-13
#   unresolved: exact independent whole-word placement law over Open English WordNet relations and senses
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import dataclass

SOURCE_DICTIONARY = "Open English WordNet 2025"
PUBLIC_GLYPH_FLOOR_SOURCE = (
    "The-Interdependency/a0-betatest@"
    "3fe7fa035659c31c1e101e87c8d37302b073561b:"
    "backend/interdependent_lib/gonal/gonal.py#EXAMPLE_157"
)
PUBLIC_GLYPH_FLOOR_SHA256 = "20d6ed51fdff5505ed9696c38d6dcc82f982eba166d9b712bee68c4521b751ac"


@dataclass(frozen=True)
class EnglishEmbeddingManifest:
    """One bounded run of the English projection into UCNS."""

    source_dictionary: str = SOURCE_DICTIONARY
    source_dictionary_is_exclusive: bool = True
    public_glyph_floor_source: str = PUBLIC_GLYPH_FLOOR_SOURCE
    public_glyph_floor_sha256: str = PUBLIC_GLYPH_FLOOR_SHA256
    public_glyph_floor_vertices: int = 157
    universal_composition: bool = True
    affix_selection_restrictions: bool = False
    direct_atomic_assignment_is_independent: bool = True
    molecular_results_generate_atomic_views: bool = True
    generated_atomic_materialization: str = "lazy-or-cached-with-identical-canonical-identity"
    shared_superposition_count: int = 1
    scale_changes_operation: bool = False


def embedding_manifest() -> EnglishEmbeddingManifest:
    """Return the immutable doctrine for the selected embedding run."""

    return EnglishEmbeddingManifest()


__all__ = [
    "EnglishEmbeddingManifest",
    "PUBLIC_GLYPH_FLOOR_SHA256",
    "PUBLIC_GLYPH_FLOOR_SOURCE",
    "SOURCE_DICTIONARY",
    "embedding_manifest",
]
