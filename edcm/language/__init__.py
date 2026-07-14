"""EDCM-owned English atomic and molecular embedding implementation."""

# === MODULE_BUILD ===
# id: edcm_language_package
#   module_name: language
#   module_kind: engine
#   summary: exposes the pinned OEWN 2025 source, complete run affixes, universal rendering and morphology, independent atomic/molecular placement laws, public 157-glyph floor, and metadata-free gonol artifacts
#   owner: Erin Spencer
#   public_surface: EnglishEmbeddingManifest, embedding_manifest, PUBLIC_GLYPH_FLOOR_157, CompositionNode, Attestation, Soundness, LexicalEvidence, AtomicForkRelation, AtomicForkResult, GonolRegistry, compose_gonols, materialize, compare_atomic_fork, intrinsic_gonol_record, metadata_free_jsonl, write_metadata_free_gonol_list, AffixRecord, load_affix_inventory, TransformationRule, transformation_inventory, render_affix_candidates, inverse_affix_candidates, compound_candidates, normalize_lemma, Decomposition, MorphologyGraph, build_morphology_graph, OEWN_REPOSITORY, OEWN_TAG, OEWN_COMMIT, OEWN_LICENSE, LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot, load_oewn_2025, assign_affix_gonol, assign_root_gonol, assign_direct_atomic_gonol, superpose_gonols, compare_gonols, gonol_sha256
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: read_write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings, tests.test_language_full_run
#   rollout: default_enabled
#   rollback: remove generated artifacts and restore the prior language package plus its metadata collection
#   requires: edcm_language_manifest, edcm_language_glyph_floor, edcm_language_model, edcm_language_composition, edcm_language_artifacts, edcm_language_oewn_source, edcm_language_affixes, edcm_language_rendering, edcm_language_morphology, edcm_language_placement
#   since: 2026-07-13
#   unresolved: pronunciation rendering and empirical interpretation of fork distances remain subsequent research layers
# === END MODULE_BUILD ===

from .affixes import AffixRecord, affix_inventory_record, load_affix_inventory
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
from .morphology import Decomposition, MorphologyGraph, build_morphology_graph
from .placement import (
    assign_affix_gonol,
    assign_direct_atomic_gonol,
    assign_root_gonol,
    compare_gonols,
    gonol_sha256,
    superpose_gonols,
)
from .rendering import (
    TransformationRule,
    compound_candidates,
    inverse_affix_candidates,
    normalize_lemma,
    render_affix_candidates,
    transformation_inventory,
)
from .source import (
    LexemeRecord,
    OEWN_COMMIT,
    OEWN_LICENSE,
    OEWN_REPOSITORY,
    OEWN_TAG,
    SenseRecord,
    SynsetRecord,
    WordnetSnapshot,
    load_oewn_2025,
)

__all__ = [
    "AffixRecord",
    "AtomicForkRelation",
    "AtomicForkResult",
    "Attestation",
    "CompositionNode",
    "Decomposition",
    "EnglishEmbeddingManifest",
    "GonolRegistry",
    "LexemeRecord",
    "LexicalEvidence",
    "MissingGonolError",
    "MorphologyGraph",
    "OEWN_COMMIT",
    "OEWN_LICENSE",
    "OEWN_REPOSITORY",
    "OEWN_TAG",
    "PUBLIC_GLYPH_FLOOR_157",
    "PUBLIC_GLYPH_FLOOR_SHA256",
    "PUBLIC_GLYPH_FLOOR_SOURCE",
    "SOURCE_DICTIONARY",
    "SenseRecord",
    "Soundness",
    "SynsetRecord",
    "TransformationRule",
    "WordnetSnapshot",
    "affix_inventory_record",
    "assign_affix_gonol",
    "assign_direct_atomic_gonol",
    "assign_root_gonol",
    "build_morphology_graph",
    "build_public_glyph_floor_157",
    "compare_atomic_fork",
    "compare_gonols",
    "compound_candidates",
    "compose_gonols",
    "embedding_manifest",
    "glyph_floor_sha256",
    "gonol_sha256",
    "intrinsic_gonol_record",
    "inverse_affix_candidates",
    "load_affix_inventory",
    "load_oewn_2025",
    "materialize",
    "metadata_free_jsonl",
    "normalize_lemma",
    "render_affix_candidates",
    "superpose_gonols",
    "transformation_inventory",
    "validate_public_glyph_floor",
    "write_metadata_free_gonol_list",
]
