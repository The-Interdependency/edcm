"""Frozen-canon and measurement-authority integrity gates.

Usage guidance
--------------
Run from any installed EDCM environment:

    python -m edcm.integrity

The gate verifies exact Git blob identities for every frozen ``*_v1.json`` canon
file, the complete set of frozen files, the machine-readable measurement
authority policy, and the no-fork orthogonality alias. Any byte change requires
a new canon version and migration record rather than updating these identities
silently.
"""

# === MODULE_BUILD ===
# id: edcm_integrity
#   module_name: integrity
#   module_kind: guardrail
#   summary: non-tautological frozen-canon byte manifest and measurement source-of-truth drift gate with installed-package CLI
#   owner: Erin Spencer
#   public_surface: FROZEN_CANON_GIT_BLOBS, EXPECTED_MEASUREMENT_AUTHORITY, IntegrityFinding, IntegrityReport, git_blob_sha1, verify_frozen_canon, verify_measurement_authority, verify_orthogonality_alias, run_integrity_gate, main
#   internal_surface: _canon_root
#   auth_boundary: none
#   storage_boundary: reads packaged canon resources only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_integrity
#   rollout: default_enabled
#   rollback: remove integrity module and CI invocation only after replacing with an equivalent or stronger gate
#   requires: edcm_measurement, edcm_ucns_objects
#   since: 2026-07-12
#   unresolved: future canon versions require an explicit versioned manifest and migration record
# === END MODULE_BUILD ===

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

FROZEN_CANON_GIT_BLOBS = {
    "bones_affixes_v1.json": "68811fc62ffe61022c9db2d325c80b900d501282",
    "bones_punct_v1.json": "5cc294c70ebbd7325f07ad67982a9353d0017754",
    "bones_words_v1.json": "422cd3d0aa31ab0b2aac6dcbb982bbe4853e6a19",
    "markers_v1.json": "f937fab506c2201159ec90024ea18c898a331066",
}

EXPECTED_MEASUREMENT_AUTHORITY = {
    "canonical": True,
    "source_of_truth": "The-Interdependency/edcm:edcm/measurement",
    "implementation_version": "0.1.0",
    "compatibility_policy": "edcmbone-provenance-only-v1",
    "consolidation_source_repository": "https://github.com/The-Interdependency/edcmbone",
    "consolidation_source_path": "backend_old/src/edcmbone/",
    "consolidation_source_commit": "05eee6d15c7ad0a7dcf62220a3a0a8618f481a81",
    "runtime_override_by_edcmbone": False,
    "ucns_theorem_status_transfer": False,
}


@dataclass(frozen=True, slots=True)
class IntegrityFinding:
    check: str
    passed: bool
    expected: Any
    observed: Any
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    passed: bool
    findings: tuple[IntegrityFinding, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "findings": [finding.as_dict() for finding in self.findings],
        }


def git_blob_sha1(data: bytes) -> str:
    """Return Git's content-addressed blob identity for exact bytes."""

    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def _canon_root():
    return files("edcm.measurement.canon").joinpath("data")


def verify_frozen_canon(resource_root=None) -> tuple[IntegrityFinding, ...]:
    """Verify both the complete frozen file set and every exact byte identity."""

    root = resource_root or _canon_root()
    observed_names = frozenset(
        entry.name for entry in root.iterdir() if entry.name.endswith("_v1.json")
    )
    expected_names = frozenset(FROZEN_CANON_GIT_BLOBS)
    findings: list[IntegrityFinding] = [
        IntegrityFinding(
            check="frozen_canon_file_set",
            passed=observed_names == expected_names,
            expected=sorted(expected_names),
            observed=sorted(observed_names),
            detail="frozen v1 canon files must be neither added nor removed without a versioned migration",
        )
    ]
    for name, expected in sorted(FROZEN_CANON_GIT_BLOBS.items()):
        path = root.joinpath(name)
        try:
            observed = git_blob_sha1(path.read_bytes())
        except FileNotFoundError:
            observed = None
        findings.append(
            IntegrityFinding(
                check=f"frozen_canon_blob:{name}",
                passed=observed == expected,
                expected=expected,
                observed=observed,
                detail="exact packaged bytes must match the pinned Git blob identity",
            )
        )
    return tuple(findings)


def verify_measurement_authority(
    authority: Mapping[str, Any] | None = None,
) -> IntegrityFinding:
    """Verify the complete source-of-truth and compatibility policy record."""

    if authority is None:
        from .measurement import MEASUREMENT_AUTHORITY

        authority = MEASUREMENT_AUTHORITY
    observed = dict(authority)
    return IntegrityFinding(
        check="measurement_authority",
        passed=observed == EXPECTED_MEASUREMENT_AUTHORITY,
        expected=EXPECTED_MEASUREMENT_AUTHORITY,
        observed=observed,
        detail="EDCM must remain canonical and installed edcmbone must remain provenance-only",
    )


def verify_orthogonality_alias() -> IntegrityFinding:
    """Verify measurement re-exports EDCM objects rather than a drifting copy."""

    from . import ucns_objects
    from .measurement.metrics import AxisState, ConstraintField, FieldMotion

    observed = {
        "AxisState": AxisState is ucns_objects.AxisState,
        "ConstraintField": ConstraintField is ucns_objects.ConstraintField,
        "FieldMotion": FieldMotion is ucns_objects.FieldMotion,
    }
    return IntegrityFinding(
        check="orthogonality_no_fork",
        passed=all(observed.values()),
        expected={name: True for name in observed},
        observed=observed,
        detail="measurement orthogonality must re-export one canonical EDCM object surface",
    )


def run_integrity_gate(resource_root=None) -> IntegrityReport:
    findings = (
        *verify_frozen_canon(resource_root),
        verify_measurement_authority(),
        verify_orthogonality_alias(),
    )
    return IntegrityReport(
        passed=all(finding.passed for finding in findings),
        findings=tuple(findings),
    )


def main() -> int:
    report = run_integrity_gate()
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "EXPECTED_MEASUREMENT_AUTHORITY",
    "FROZEN_CANON_GIT_BLOBS",
    "IntegrityFinding",
    "IntegrityReport",
    "git_blob_sha1",
    "main",
    "run_integrity_gate",
    "verify_frozen_canon",
    "verify_measurement_authority",
    "verify_orthogonality_alias",
]
