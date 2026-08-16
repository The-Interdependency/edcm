"""Pinned authority and provenance boundary for the English lexical floor."""

# === MODULE_BUILD ===
# id: edcm_language_manifest
#   module_name: manifest
#   module_kind: policy
#   summary: pins OEWN evidence and the exact UCNS relational producer while forbidding geometry and status transfer
#   owner: Erin Spencer
#   public_surface: EnglishEmbeddingManifest, embedding_manifest, SOURCE_DICTIONARY
#   internal_surface: none
#   auth_boundary: exact producer commits
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_relational_bridge
#   rollout: active lexical-floor bridge
#   rollback: restore fail-closed bridge state without restoring retired placement
#   requires: edcm_language_oewn_source, ucns_relational_carrier
#   since: 2026-08-16
#   unresolved: geometry, canonical English decomposition, measurement validity, and producer signatures
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: lexical_manifest_preserves_authority_firewall
#   given: the English lexical-floor manifest is inspected
#   then: EDCM owns English evidence, UCNS owns representation, and geometry, proof, measurement, empirical, and canon transfer remain false
#   class: doctrine
#   since: 2026-08-16
# === END CONTRACTS ===

from dataclasses import dataclass

from .relational_bridge import UCNS_RELATIONAL_COMMIT
from .source import OEWN_COMMIT, OEWN_REPOSITORY, OEWN_TAG

SOURCE_DICTIONARY = "Open English WordNet 2025"


@dataclass(frozen=True, slots=True)
class EnglishEmbeddingManifest:
    source_dictionary: str = SOURCE_DICTIONARY
    source_repository: str = OEWN_REPOSITORY
    source_tag: str = OEWN_TAG
    source_commit: str = OEWN_COMMIT
    ucns_repository: str = "The-Interdependency/ucns"
    ucns_commit: str = UCNS_RELATIONAL_COMMIT
    edcm_owns_english_evidence: bool = True
    ucns_owns_representation: bool = True
    intrinsic_metadata_free: bool = True
    direct_atomic_independent: bool = True
    molecular_independent: bool = True
    legacy_placement_present: bool = False
    geometry_attached: bool = False
    proof_status_transfer: bool = False
    measurement_status_transfer: bool = False
    empirical_status_transfer: bool = False
    canon_selection: None = None


def embedding_manifest() -> EnglishEmbeddingManifest:
    return EnglishEmbeddingManifest()


__all__ = ["EnglishEmbeddingManifest", "SOURCE_DICTIONARY", "embedding_manifest"]
