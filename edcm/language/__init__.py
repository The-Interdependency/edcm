"""EDCM English lexical evidence over a UCNS-owned relational carrier."""

# === MODULE_BUILD ===
# id: edcm_language_package
#   module_name: language
#   module_kind: engine
#   summary: exposes exact OEWN evidence, reversible lexical candidates, and independent EDCM-to-UCNS relational branch construction without EDCM-owned geometry
#   owner: Erin Spencer
#   public_surface: source, affix, rendering, morphology, model, manifest, and relational-bridge names listed in __all__
#   internal_surface: none
#   auth_boundary: exact OEWN and UCNS producer commits
#   storage_boundary: caller-selected lexical artifact directory
#   network_boundary: none
#   user_data_boundary: public licensed lexical evidence only
#   admin_only: false
#   tests: tests.test_language_full_run, tests.test_language_relational_bridge
#   rollout: explicit lexical-floor construction; no measurement or higher-language activation
#   rollback: remove relational bridge while retaining EDCM evidence modules
#   requires: edcm_language_manifest, edcm_language_model, edcm_language_oewn_source, edcm_language_affixes, edcm_language_rendering, edcm_language_morphology, edcm_language_relational_bridge
#   since: 2026-08-16
#   unresolved: UCNS geometry and higher-gonol composition remain absent; lexical decomposition remains dictionary-and-inventory bounded evidence
# === END MODULE_BUILD ===

from .affixes import AffixRecord, affix_inventory_record, load_affix_inventory
from .manifest import EnglishEmbeddingManifest, SOURCE_DICTIONARY, embedding_manifest
from .model import Attestation, CompositionNode, LexicalEvidence, Soundness
from .morphology import Decomposition, MorphologyGraph, build_morphology_graph
from .relational_bridge import (
    DirectAtomicFreeze, LexicalBridgeError, MolecularFreeze,
    UCNS_RELATIONAL_COMMIT, build_direct_atomic, build_molecular,
    canonical_json_bytes, compare_frozen_branches, freeze_branch,
)
from .rendering import (
    TransformationRule, compound_candidates, inverse_affix_candidates,
    normalize_lemma, render_affix_candidates, transformation_inventory,
)
from .source import (
    LexemeRecord, OEWN_COMMIT, OEWN_LICENSE, OEWN_REPOSITORY, OEWN_TAG,
    SenseRecord, SynsetRecord, WordnetSnapshot, load_oewn_2025,
)

__all__ = [
    "AffixRecord", "Attestation", "CompositionNode", "Decomposition",
    "DirectAtomicFreeze", "EnglishEmbeddingManifest", "LexemeRecord",
    "LexicalBridgeError", "LexicalEvidence", "MolecularFreeze",
    "MorphologyGraph", "OEWN_COMMIT", "OEWN_LICENSE", "OEWN_REPOSITORY",
    "OEWN_TAG", "SOURCE_DICTIONARY", "SenseRecord", "Soundness",
    "SynsetRecord", "TransformationRule", "UCNS_RELATIONAL_COMMIT",
    "WordnetSnapshot", "affix_inventory_record", "build_direct_atomic",
    "build_molecular", "build_morphology_graph", "canonical_json_bytes",
    "compare_frozen_branches", "compound_candidates", "embedding_manifest",
    "freeze_branch", "inverse_affix_candidates", "load_affix_inventory",
    "load_oewn_2025", "normalize_lemma", "render_affix_candidates",
    "transformation_inventory",
]
