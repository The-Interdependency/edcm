"""Inactive exact-identity protocol for the first bounded post-reset UCNS profile."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class BoundedUCNSProfileIdentity:
    producer_epoch: str
    profile_id: str
    profile_version: str
    bridge_schema_id: str
    bridge_schema_version: str
    source_commit: str
    package_identity: str
    option_set: tuple[tuple[str, str], ...]
    stable_object_identity: str
    theorem_transfer: bool = False
    measurement_validity: bool = False
    metapat_validity: bool = False

    def __post_init__(self) -> None:
        required = (
            self.producer_epoch,
            self.profile_id,
            self.profile_version,
            self.bridge_schema_id,
            self.bridge_schema_version,
            self.source_commit,
            self.package_identity,
            self.stable_object_identity,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("exact non-empty UCNS identity fields are required")
        if not self.option_set:
            raise ValueError("complete profile option_set is required")
        if self.theorem_transfer or self.measurement_validity or self.metapat_validity:
            raise ValueError("proof and validity transfer flags must remain false")


@dataclass(frozen=True)
class TranscriptOccurrenceCell:
    occurrence_id: str
    source_index: int
    source_event_id: str
    stable_cell_identity: str
    active_state: str
    support_policy: str | None

    def __post_init__(self) -> None:
        if self.source_index < 0:
            raise ValueError("source_index must preserve exact non-negative order")
        if not all((self.occurrence_id, self.source_event_id, self.stable_cell_identity, self.active_state)):
            raise ValueError("occurrence identity and retained event state are required")


def validate_exact_profile(actual: Mapping[str, Any], expected: BoundedUCNSProfileIdentity) -> None:
    required = {
        "producer_epoch": expected.producer_epoch,
        "profile_id": expected.profile_id,
        "profile_version": expected.profile_version,
        "bridge_schema_id": expected.bridge_schema_id,
        "bridge_schema_version": expected.bridge_schema_version,
        "source_commit": expected.source_commit,
        "package_identity": expected.package_identity,
        "option_set": list(expected.option_set),
        "stable_object_identity": expected.stable_object_identity,
        "theorem_transfer": False,
        "measurement_validity": False,
        "metapat_validity": False,
    }
    for key, value in required.items():
        if actual.get(key) != value:
            raise ValueError(f"UCNS bounded profile mismatch for {key}; fail closed")


def graph_edges_enter_scalar_w(*, candidate_policy: str | None) -> bool:
    """Edges never enter scalar W without an explicitly named candidate policy."""
    return candidate_policy is not None and bool(candidate_policy.strip())
