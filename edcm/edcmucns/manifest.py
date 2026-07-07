# === MODULE_BUILD ===
# id: edcmucns_manifest
#   module_name: manifest
#   module_kind: schema
#   summary: PolicyManifest — the measurement-identity manifest for edcmucns v0.3.1; stable-serializable, hashable; hash changes create epoch breaks
#   owner: Erin Spencer
#   public_surface: PolicyManifest, DEFAULT_FAMILY_PRIME_GAUGE, RESIDUE_RULE_VERSION
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_identity_v031, tests.test_edcmucns_epochs_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-07-06
#   unresolved: policy version strings are architecture placeholders; the policies they name (polarity dictionary, contact predicate, training updates) remain frontier
# === END MODULE_BUILD ===

"""Policy manifest for edcmucns v0.3.1.

The manifest is part of measurement identity (design canon v0.3.1):
``M_EDCM = readout(G_ucns, Π_provenance, payloads, field_state,
policy_manifest)``. It must be stable-serializable and hashable; a manifest
hash change is a chain epoch break (see :mod:`edcm.edcmucns.epochs`).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# Family → prime gauge pinned by the v0.3.1 canon.
DEFAULT_FAMILY_PRIME_GAUGE: dict[str, int] = {"P": 3, "K": 5, "Q": 7, "T": 13, "S": 29}

# The v0.3.1 non-origin residue rule name. The old modulo rule
# (theta = 2*pi*(m mod p)/p) is forbidden: it lets the p-th bone land on the
# origin.
RESIDUE_RULE_VERSION = "non_origin_residue_v031"


@dataclass(frozen=True, slots=True)
class PolicyManifest:
    """Measurement-identity manifest. All fields are readout-bearing.

    Required fields per the v0.3.1 handoff. Version strings identify the
    governing policy documents; the manifest does not embed the policies
    themselves.
    """

    family_prime_gauge: tuple[tuple[str, int], ...] = tuple(
        sorted(DEFAULT_FAMILY_PRIME_GAUGE.items())
    )
    residue_rule_version: str = RESIDUE_RULE_VERSION
    polarity_dictionary_version: str = "v031"
    bone_emission_policy_version: str = "v031"
    payload_governance_version: str = "v031"
    contact_predicate_version: str = "v031-frontier-unimplemented"
    lens_readout_policy_version: str = "v031"
    training_update_policy_version: str = "v031"

    def __post_init__(self) -> None:
        if self.residue_rule_version != RESIDUE_RULE_VERSION:
            raise ValueError(
                "v0.3.1 manifests must pin residue_rule_version="
                f"{RESIDUE_RULE_VERSION!r}; got {self.residue_rule_version!r}"
            )
        for family, prime in self.family_prime_gauge:
            if prime < 2:
                raise ValueError(f"family {family!r} gauge must be >= 2, got {prime}")

    @property
    def gauge(self) -> dict[str, int]:
        return dict(self.family_prime_gauge)

    def prime_for(self, family: str) -> int:
        try:
            return self.gauge[family]
        except KeyError:
            raise ValueError(f"family {family!r} not in manifest prime gauge") from None

    def canonical_json(self) -> str:
        payload = {
            "family_prime_gauge": self.gauge,
            "residue_rule_version": self.residue_rule_version,
            "polarity_dictionary_version": self.polarity_dictionary_version,
            "bone_emission_policy_version": self.bone_emission_policy_version,
            "payload_governance_version": self.payload_governance_version,
            "contact_predicate_version": self.contact_predicate_version,
            "lens_readout_policy_version": self.lens_readout_policy_version,
            "training_update_policy_version": self.training_update_policy_version,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    def manifest_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
