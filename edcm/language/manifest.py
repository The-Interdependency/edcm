"""Pinned scope and provenance for the retired English gonol experiment."""

# === MODULE_BUILD ===
# id: edcm_language_manifest
#   module_name: manifest
#   module_kind: policy
#   summary: pins OEWN input provenance while recording that public-gonol authority belongs to UCNS and legacy placement is retired
#   owner: Erin Spencer
#   public_surface: EnglishEmbeddingManifest, embedding_manifest, SOURCE_DICTIONARY, PUBLIC_GLYPH_FLOOR_SOURCE
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: fail_closed_pending_canonical_bridge
#   rollback: restore active placement only after an Erin-ratified UCNS public-gonol bridge exists
#   requires: none
#   since: 2026-07-16
#   unresolved: public-gonol to EDCM language-object bridge remains hmmm
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import dataclass

SOURCE_DICTIONARY = "Open English WordNet 2025"
PUBLIC_GLYPH_FLOOR_SOURCE = (
    "The-Interdependency/ucns@"
    "c7849498bb5b14b87dbb4cffb6522fbc82639373:"
    "ucns/public_gonol.py#PUBLIC_GONOL_157"
)
PUBLIC_GLYPH_FLOOR_SHA256 = "20d6ed51fdff5505ed9696c38d6dcc82f982eba166d9b712bee68c4521b751ac"


@dataclass(frozen=True)
class EnglishEmbeddingManifest:
    """Boundary record for the superseded OEWN gonol-placement experiment."""

    source_dictionary: str = SOURCE_DICTIONARY
    source_dictionary_is_exclusive: bool = True
    public_glyph_floor_source: str = PUBLIC_GLYPH_FLOOR_SOURCE
    public_glyph_floor_sha256: str = PUBLIC_GLYPH_FLOOR_SHA256
    public_glyph_floor_vertices: int = 157
    canonical_public_gonol_required: bool = True
    edcm_owns_public_gonol: bool = False
    legacy_hash_placement_retired: bool = True
    universal_composition: bool = False
    affix_selection_restrictions: bool = False
    direct_atomic_assignment_is_independent: bool = False
    molecular_results_generate_atomic_views: bool = False
    generated_atomic_materialization: str = "retired-pending-canonical-ucns-bridge"
    shared_superposition_count: int = 0
    scale_changes_operation: bool = False


def embedding_manifest() -> EnglishEmbeddingManifest:
    """Return the fail-closed manifest for the retired placement experiment."""

    return EnglishEmbeddingManifest()


__all__ = [
    "EnglishEmbeddingManifest",
    "PUBLIC_GLYPH_FLOOR_SHA256",
    "PUBLIC_GLYPH_FLOOR_SOURCE",
    "SOURCE_DICTIONARY",
    "embedding_manifest",
]
