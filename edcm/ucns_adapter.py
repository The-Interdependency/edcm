"""Exact EDCM consumer for the UCNS word-gonol observation profile.

Usage guidance
--------------
Install the ``ucns-profile`` extra and pass ``ucns_turns`` as an ordered
sequence of exact ``(speaker_id, text)`` tuples. The adapter observes every
turn; it does not parse speaker boundaries from a flattened transcript.

The resulting ``ucns_profile_observation`` is exact corpus evidence. It is not
UCNS geometry, factorization evidence, theorem status, or an EDCM measurement
validity claim. The retired ordered-occurrence bridge input forms fail closed.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_adapter
#   module_name: ucns_adapter
#   module_kind: adapter
#   summary: fail-closed consumer for the exact EDCM-only UCNS word-gonol profile, preserving full-corpus speaker-turn observations without geometry or proof transfer
#   owner: Erin Spencer
#   public_surface: ActualUCNSAdapter, UCNSProfileObservationEvidence, UCNSIntegrationStatus, UCNSAdapterSelection, select_ucns_adapter, inspect_ucns_adapter
#   internal_surface: _canonical_bytes, _digest, _package_present, _token_record, _segment_record, _turn_record
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: exact source turns remain in caller-owned in-memory results and are not transmitted
#   admin_only: false
#   tests: tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_shared_stack_contract
#   rollout: optional exact-profile activation only when the pinned profile surface matches
#   rollback: suspend the optional adapter; base EDCM measurement remains operational
#   requires: ucns.edcm at eb264fba18bd051c46b4853c81c8fb91ec6d5811
#   since: 2026-07-25
#   unresolved: formal Mobius coordinates, higher-gonol composition, and projection policies remain outside this observation adapter
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: edcm_ucns_exact_profile_only
#   given: an importable UCNS package is considered for activation
#   then: every profile identity, option, public-alphabet invariant, and producer type matches the pinned EDCM word-gonol surface or the adapter remains suspended
#   class: safety
#   since: 2026-07-25
#
# id: edcm_ucns_full_turn_observation
#   given: ordered ucns_turns enter the active adapter
#   then: all turns are observed in order with exact Unicode, one unit of support per speaker turn, explicit SPACE boundaries, and retained out-of-alphabet evidence
#   class: evidence
#   since: 2026-07-25
#
# id: edcm_ucns_no_geometry_or_proof_transfer
#   given: exact profile observations are attached
#   then: geometry, factorization, theorem, certification, and measurement-validity attachment flags remain false
#   class: doctrine
#   since: 2026-07-25
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
from dataclasses import asdict, dataclass, replace
from types import ModuleType
from typing import Any, Mapping, Protocol, Sequence

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
SUPPORTED_PROFILE = ("ucns.profile.edcm-word-gonol", "0.1.0")
SUPPORTED_PROFILE_SCOPE = "edcm-only"
PINNED_UCNS_COMMIT = "eb264fba18bd051c46b4853c81c8fb91ec6d5811"
EXPECTED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
EXPECTED_PROFILE_OPTIONS = tuple(
    sorted(
        {
            "carrier_requirement": "mobius-origin-hidden-zero",
            "corpus_execution": "full-corpus",
            "gonol_initiation": "mobius-twist",
            "nesting_boundary": "superpositioned-space",
            "normalization": "none-preserve-source",
            "occurrence_operation": "ordered-concatenation",
            "out_of_alphabet": "retain-and-report",
            "profile_scope": "edcm-only",
            "smallest_gonol": "word",
            "support": "one-unit-per-speaker-turn",
            "token_alphabet": "public-gonol-157",
            "token_identity": "unicode-code-point",
        }.items()
    )
)
RESET_BOUNDARY_REASON = "exact EDCM UCNS word-gonol profile is unavailable or mismatched"
INSTALL_HINT = None
REJECTED_LEGACY_SCHEMAS = frozenset(
    {
        "ucns-canonical-json-v1",
        "ucns.bridge-record@1.0.0",
        "ucns.factorization-evidence@1.0.0",
        "ucns.bridge.edcm-metapat-ordered-occurrence",
    }
)
REJECTED_LEGACY_INPUTS = frozenset(
    {
        "ucns_object",
        "ucns_bridge_record",
        "ucns_bridge_record_json",
        "ucns_bridge_record_dict",
        "ucns_factorization_evidence",
        "ucns_factorization_evidence_json",
        "ucns_factorization_evidence_dict",
    }
)


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when UCNS fails the exact EDCM profile contract."""


class UnsupportedUCNSSchemaError(UCNSAdapterConstructionError):
    """Raised for retired or otherwise unsupported producer identities."""


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    package_present: bool
    producer_recognized: bool
    profile_supported: bool
    adapter_active: bool
    ucns_profile_observation_attached: bool = False
    ucns_object_attached: bool = False
    ucns_bridge_record_attached: bool = False
    ucns_scope_metadata_attached: bool = False
    ucns_factorization_evidence_attached: bool = False
    ucns_negative_certification_attached: bool = False
    ucns_theorem_status_attached: bool = False
    implementation_id: str = "edcm.ucns_adapter.word_gonol_profile"
    implementation_version: str | None = "0.1.0"
    source_repository: str = UCNS_SOURCE_REPOSITORY
    selection: str = "suspended"
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    @property
    def ucns_package_available(self) -> bool:
        return self.package_present

    @property
    def ucns_adapter_active(self) -> bool:
        return self.adapter_active

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ucns_package_available"] = self.package_present
        data["ucns_adapter_active"] = self.adapter_active
        return data


@dataclass(frozen=True)
class UCNSProfileObservationEvidence:
    profile_id: str
    profile_version: str
    profile_scope: str
    source_repository: str
    source_commit: str
    options: tuple[tuple[str, str], ...]
    normalization_policy: str
    support_policy: str
    corpus_execution: str
    smallest_gonol: str
    gonol_initiation: str
    token_alphabet_size: int
    token_alphabet_sha256: str
    turns: tuple[dict[str, Any], ...]
    observation_digest: str
    evidence_mode: str = "exact-observation"
    projection_status: str = "not-projected"
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class UCNSAdapter(Protocol):
    @property
    def status(self) -> UCNSIntegrationStatus: ...

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]: ...


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _token_record(token: Any) -> dict[str, Any]:
    return {
        "value": token.value,
        "code_point": token.code_point,
        "codepoint_offset": token.codepoint_offset,
        "alphabet_position": token.alphabet_position,
        "in_alphabet": token.in_alphabet,
    }


def _segment_record(module: ModuleType, segment: Any) -> dict[str, Any]:
    if isinstance(segment, module.EdcmWordGonol):
        return {
            "kind": "word-gonol",
            "word_index": segment.word_index,
            "raw_text": segment.raw_text,
            "source_start": segment.source_start,
            "source_end": segment.source_end,
            "initiation_event": segment.initiation_event,
            "tokens": tuple(_token_record(token) for token in segment.tokens),
        }
    if isinstance(segment, module.SuperpositionedSpaceBoundary):
        return {
            "kind": "superpositioned-space-boundary",
            "raw_text": segment.raw_text,
            "roles": tuple(segment.roles),
            "token": _token_record(segment.token),
        }
    raise TypeError("UCNS profile emitted an unknown segment type")


def _turn_record(module: ModuleType, observation: Any) -> dict[str, Any]:
    return {
        "speaker_id": observation.speaker_id,
        "turn_index": observation.turn_index,
        "raw_text": observation.raw_text,
        "source_id": observation.source_id,
        "unit_support": observation.unit_support,
        "segments": tuple(
            _segment_record(module, segment) for segment in observation.segments
        ),
        "word_count": len(observation.word_gonols),
        "nesting_boundary_count": len(observation.nesting_boundaries),
        "out_of_alphabet": tuple(
            _token_record(token) for token in observation.out_of_alphabet
        ),
        "has_complete_alphabet_coverage": (
            observation.has_complete_alphabet_coverage
        ),
    }


class SuspendedUCNSAdapter:
    def __init__(self, *, package_present: bool) -> None:
        self._status = suspended_ucns_status(package_present=package_present)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return self._status

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["ucns_integration"] = self.status.as_dict()
        state.pop("ucns_profile_observation", None)
        return state


class ActualUCNSAdapter:
    """Consumer of only the exact EDCM word-gonol observation surface."""

    def __init__(self, module: ModuleType) -> None:
        required = (
            "EDCM_PROFILE_ID",
            "EDCM_PROFILE_VERSION",
            "EDCM_PROFILE_SCOPE",
            "EDCM_PROFILE_OPTIONS",
            "EDCM_NORMALIZATION_POLICY",
            "EDCM_SUPPORT_POLICY",
            "EDCM_CORPUS_EXECUTION",
            "EDCM_SMALLEST_GONOL",
            "EDCM_GONOL_INITIATION",
            "PUBLIC_GONOL_157",
            "PUBLIC_GONOL_SHA256",
            "EdcmWordGonolProfile",
            "EdcmWordGonol",
            "SuperpositionedSpaceBoundary",
            "public_gonol_sha256",
        )
        missing = [name for name in required if not hasattr(module, name)]
        if missing:
            raise UCNSAdapterConstructionError(
                "UCNS exact EDCM profile surface missing: " + ", ".join(missing)
            )
        if (
            str(module.EDCM_PROFILE_ID),
            str(module.EDCM_PROFILE_VERSION),
        ) != SUPPORTED_PROFILE:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile identity mismatch")
        if str(module.EDCM_PROFILE_SCOPE) != SUPPORTED_PROFILE_SCOPE:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile scope mismatch")
        if tuple(module.EDCM_PROFILE_OPTIONS) != EXPECTED_PROFILE_OPTIONS:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile options mismatch")
        alphabet = tuple(module.PUBLIC_GONOL_157)
        if (
            len(alphabet) != 157
            or not all(isinstance(token, str) and len(token) == 1 for token in alphabet)
            or len(set(alphabet)) != 157
            or alphabet[0] != " "
            or "0" not in alphabet
        ):
            raise UnsupportedUCNSSchemaError("UCNS public gonol invariant mismatch")
        behavior = {
            "normalization": str(module.EDCM_NORMALIZATION_POLICY),
            "support": str(module.EDCM_SUPPORT_POLICY),
            "corpus_execution": str(module.EDCM_CORPUS_EXECUTION),
            "smallest_gonol": str(module.EDCM_SMALLEST_GONOL),
            "gonol_initiation": str(module.EDCM_GONOL_INITIATION),
        }
        expected_behavior = {
            "normalization": "none-preserve-source",
            "support": "one-unit-per-speaker-turn",
            "corpus_execution": "full-corpus",
            "smallest_gonol": "word",
            "gonol_initiation": "mobius-twist",
        }
        if behavior != expected_behavior:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile behavior mismatch")
        if (
            str(module.PUBLIC_GONOL_SHA256) != EXPECTED_PUBLIC_GONOL_SHA256
            or str(module.public_gonol_sha256()) != EXPECTED_PUBLIC_GONOL_SHA256
        ):
            raise UnsupportedUCNSSchemaError("UCNS public gonol digest mismatch")
        self._module = module
        try:
            self._profile = module.EdcmWordGonolProfile()
        except (TypeError, ValueError) as exc:
            raise UCNSAdapterConstructionError(
                "UCNS EDCM profile construction failed"
            ) from exc

    @property
    def status(self) -> UCNSIntegrationStatus:
        return UCNSIntegrationStatus(
            package_present=True,
            producer_recognized=True,
            profile_supported=True,
            adapter_active=True,
            selection="exact_edcm_word_gonol_profile",
        )

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        legacy = sorted(REJECTED_LEGACY_INPUTS.intersection(state))
        if legacy:
            raise UnsupportedUCNSSchemaError(
                "retired UCNS bridge/object/factorization inputs are rejected: "
                + ", ".join(legacy)
            )

        raw_turns = state.get("ucns_turns")
        if raw_turns is None:
            state["ucns_integration"] = self.status.as_dict()
            state.pop("ucns_profile_observation", None)
            return state
        if isinstance(raw_turns, (str, bytes)) or not isinstance(
            raw_turns, Sequence
        ):
            raise TypeError("ucns_turns must be an ordered sequence of tuples")

        turns: list[tuple[str, str]] = []
        for turn in raw_turns:
            if not isinstance(turn, tuple) or len(turn) != 2:
                raise TypeError("each ucns_turns item must be (speaker_id, text)")
            speaker_id, text = turn
            if not isinstance(speaker_id, str) or not speaker_id:
                raise TypeError("speaker_id must be a non-empty string")
            if not isinstance(text, str):
                raise TypeError("turn text must be a string")
            turns.append((speaker_id, text))

        source_ref = state.get("source_ref")
        source_id = str(source_ref) if source_ref is not None else None
        observed = tuple(
            self._profile.observe_corpus(tuple(turns), source_id=source_id)
        )
        turn_records = tuple(
            _turn_record(self._module, observation) for observation in observed
        )
        evidence_fields = {
            "profile_id": self._module.EDCM_PROFILE_ID,
            "profile_version": self._module.EDCM_PROFILE_VERSION,
            "profile_scope": self._module.EDCM_PROFILE_SCOPE,
            "source_repository": UCNS_SOURCE_REPOSITORY,
            "source_commit": PINNED_UCNS_COMMIT,
            "options": EXPECTED_PROFILE_OPTIONS,
            "normalization_policy": self._module.EDCM_NORMALIZATION_POLICY,
            "support_policy": self._module.EDCM_SUPPORT_POLICY,
            "corpus_execution": self._module.EDCM_CORPUS_EXECUTION,
            "smallest_gonol": self._module.EDCM_SMALLEST_GONOL,
            "gonol_initiation": self._module.EDCM_GONOL_INITIATION,
            "token_alphabet_size": len(self._module.PUBLIC_GONOL_157),
            "token_alphabet_sha256": self._module.PUBLIC_GONOL_SHA256,
            "turns": turn_records,
        }
        evidence = UCNSProfileObservationEvidence(
            **evidence_fields,
            observation_digest=_digest(evidence_fields),
        )
        status = replace(
            self.status,
            ucns_profile_observation_attached=True,
            ucns_scope_metadata_attached=True,
        )
        state["ucns_profile_observation"] = evidence.as_dict()
        state["ucns_integration"] = status.as_dict()
        state.pop("ucns_geometry", None)
        state.pop("ucns_factorization_evidence", None)
        return state


@dataclass(frozen=True)
class UCNSAdapterSelection:
    adapter: UCNSAdapter | None
    status: UCNSIntegrationStatus


def _package_present() -> bool:
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return "ucns" in __import__("sys").modules


def suspended_ucns_status(
    *,
    package_present: bool | None = None,
    error: str | None = None,
) -> UCNSIntegrationStatus:
    present = _package_present() if package_present is None else package_present
    return UCNSIntegrationStatus(
        package_present=present,
        producer_recognized=False,
        profile_supported=False,
        adapter_active=False,
        selection="suspended",
        unresolved_constraints=(RESET_BOUNDARY_REASON,),
        errors=((error or RESET_BOUNDARY_REASON),),
    )


def missing_ucns_status() -> UCNSIntegrationStatus:
    return suspended_ucns_status(package_present=False)


def select_ucns_adapter() -> UCNSAdapterSelection:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        status = suspended_ucns_status(package_present=False)
        return UCNSAdapterSelection(adapter=None, status=status)
    try:
        adapter = ActualUCNSAdapter(module)
    except UCNSAdapterConstructionError as exc:
        status = suspended_ucns_status(package_present=True, error=str(exc))
        return UCNSAdapterSelection(adapter=None, status=status)
    return UCNSAdapterSelection(adapter=adapter, status=adapter.status)


def inspect_ucns_adapter() -> UCNSIntegrationStatus:
    return select_ucns_adapter().status


__all__ = [
    "ActualUCNSAdapter",
    "EXPECTED_PROFILE_OPTIONS",
    "EXPECTED_PUBLIC_GONOL_SHA256",
    "INSTALL_HINT",
    "PINNED_UCNS_COMMIT",
    "REJECTED_LEGACY_INPUTS",
    "REJECTED_LEGACY_SCHEMAS",
    "RESET_BOUNDARY_REASON",
    "SUPPORTED_PROFILE",
    "SUPPORTED_PROFILE_SCOPE",
    "SuspendedUCNSAdapter",
    "UCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSAdapterSelection",
    "UCNSIntegrationStatus",
    "UCNSProfileObservationEvidence",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "missing_ucns_status",
    "select_ucns_adapter",
    "suspended_ucns_status",
]
