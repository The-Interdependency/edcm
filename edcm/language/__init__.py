"""EDCM English lexical evidence over a UCNS-owned relational carrier."""

# === MODULE_BUILD ===
# id: edcm_language_package
#   module_name: language
#   module_kind: engine
#   summary: exposes exact OEWN evidence, reversible lexical candidates, independent EDCM-to-UCNS floor construction, and the complete closed depth-one semantic/definition layer without EDCM-owned geometry
#   owner: Erin Spencer
#   public_surface: source, affix, rendering, morphology, model, manifest, and relational-bridge names listed in __all__
#   internal_surface: none
#   auth_boundary: exact OEWN and UCNS producer commits
#   storage_boundary: caller-selected lexical artifact directory
#   network_boundary: none
#   user_data_boundary: public licensed lexical evidence only
#   admin_only: false
#   tests: tests.test_language_full_run, tests.test_language_relational_bridge, tests.test_language_deep_recursion
#   rollout: explicit lexical-floor then depth-one construction; no measurement or phrase/discourse activation
#   rollback: remove relational bridge while retaining EDCM evidence modules
#   requires: edcm_language_manifest, edcm_language_model, edcm_language_oewn_source, edcm_language_affixes, edcm_language_rendering, edcm_language_morphology, edcm_language_relational_bridge, edcm_language_deep_recursion
#   since: 2026-08-16
#   unresolved: UCNS geometry, depth beyond one, and phrase/discourse composition remain absent; lexical evidence remains dictionary-and-inventory bounded
# === END MODULE_BUILD ===

from .affixes import AffixRecord, affix_inventory_record, load_affix_inventory
from .deep_recursion import (
    DEEP_RECURSION_LAYER, DeepRecursionError, DeepRecursionLayer,
    DefinitionAtom, build_deep_recursion_layer, definition_atoms,
    load_floor_surface_binding,
)
from .manifest import EnglishEmbeddingManifest, SOURCE_DICTIONARY, embedding_manifest
from .model import Attestation, CompositionNode, LexicalEvidence, Soundness
from .morphology import Decomposition, MorphologyGraph, build_morphology_graph
from .relational_bridge import (
    DirectAtomicFreeze, LexicalBridgeError, MolecularFreeze,
    UCNSProducerVerification, UCNS_RELATIONAL_COMMIT, build_direct_atomic, build_molecular,
    canonical_json_bytes, compare_frozen_branches, freeze_branch,
    freeze_relational_layer, validate_frozen_branch,
    validate_frozen_relational_layer, verify_ucns_producer,
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
    "DEEP_RECURSION_LAYER", "DeepRecursionError", "DeepRecursionLayer",
    "DefinitionAtom", "DirectAtomicFreeze", "EnglishEmbeddingManifest", "LexemeRecord",
    "LexicalBridgeError", "LexicalEvidence", "MolecularFreeze",
    "MorphologyGraph", "OEWN_COMMIT", "OEWN_LICENSE", "OEWN_REPOSITORY",
    "OEWN_TAG", "SOURCE_DICTIONARY", "SenseRecord", "Soundness",
    "SynsetRecord", "TransformationRule", "UCNS_RELATIONAL_COMMIT",
    "UCNSProducerVerification",
    "WordnetSnapshot", "affix_inventory_record", "build_deep_recursion_layer",
    "build_direct_atomic", "build_molecular", "build_morphology_graph", "canonical_json_bytes",
    "compare_frozen_branches", "compound_candidates", "embedding_manifest",
    "definition_atoms", "freeze_branch", "freeze_relational_layer",
    "inverse_affix_candidates", "load_affix_inventory", "load_floor_surface_binding",
    "load_oewn_2025", "normalize_lemma", "render_affix_candidates",
    "transformation_inventory", "validate_frozen_branch", "validate_frozen_relational_layer",
    "verify_ucns_producer",
]
