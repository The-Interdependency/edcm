"""EDCM-owned English atomic and molecular embedding foundation."""

# === MODULE_BUILD ===
# id: edcm_language_package
#   module_name: language
#   module_kind: engine
#   summary: exposes the Open English WordNet-bounded dual atomic/molecular embedding manifest, public 157-glyph floor, universal composer, explicit grouping records, and metadata-free gonol artifacts
#   owner: Erin Spencer
#   public_surface: EnglishEmbeddingManifest, embedding_manifest, PUBLIC_GLYPH_FLOOR_157, CompositionNode, Attestation, Soundness, LexicalEvidence, AtomicForkRelation, AtomicForkResult, GonolRegistry, compose_gonols, materialize, compare_atomic_fork, intrinsic_gonol_record, metadata_free_jsonl, write_metadata_free_gonol_list
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: default_enabled
#   rollback: remove package before any published artifact depends on this surface
#   requires: edcm_language_manifest, edcm_language_glyph_floor, edcm_language_model, edcm_language_composition, edcm_language_artifacts
#   since: 2026-07-13
#   unresolved: complete affix, root, rendering, and independent whole-word assignment datasets are not yet materialized
# === END MODULE_BUILD ===

from .artifacts import (
    intrinsic_gonol_record,
    metadata_free_jsonl,
    write_metadata_free_gonol_list,
)
from .composition import (
    GonolRegistry,
    MissingGonolError,
    compare_atomic_fork,
    compose_gonols,
    materialize,
)
from .glyph_floor import (
    PUBLIC_GLYPH_FLOOR_157,
    build_public_glyph_floor_157,
    glyph_floor_sha256,
    validate_public_glyph_floor,
)
from .manifest import (
    EnglishEmbeddingManifest,
    PUBLIC_GLYPH_FLOOR_SHA256,
    PUBLIC_GLYPH_FLOOR_SOURCE,
    SOURCE_DICTIONARY,
    embedding_manifest,
)
from .model import (
    AtomicForkRelation,
    AtomicForkResult,
    Attestation,
    CompositionNode,
    LexicalEvidence,
    Soundness,
)

__all__ = [
    "AtomicForkRelation",
    "AtomicForkResult",
    "Attestation",
    "CompositionNode",
    "EnglishEmbeddingManifest",
    "GonolRegistry",
    "LexicalEvidence",
    "MissingGonolError",
    "PUBLIC_GLYPH_FLOOR_157",
    "PUBLIC_GLYPH_FLOOR_SHA256",
    "PUBLIC_GLYPH_FLOOR_SOURCE",
    "SOURCE_DICTIONARY",
    "Soundness",
    "build_public_glyph_floor_157",
    "compare_atomic_fork",
    "compose_gonols",
    "embedding_manifest",
    "glyph_floor_sha256",
    "intrinsic_gonol_record",
    "materialize",
    "metadata_free_jsonl",
    "validate_public_glyph_floor",
    "write_metadata_free_gonol_list",
]
