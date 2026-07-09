# === MODULE_BUILD ===
# id: edcmucns_validation
#   module_name: validation
#   module_kind: engine
#   summary: witness_geometry_consistent validator + polarity gauge audit — mismatches emit Bridge diagnostics, never silent alternate readings
#   owner: Erin Spencer
#   public_surface: witness_geometry_consistent, validate_window, gauge_audit
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_edcmucns_identity_v031, tests.test_edcmucns_encoder_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_types,edcmucns_manifest,edcmucns_geometry,edcmucns_provenance
#   since: 2026-07-06
#   unresolved: none
# === END MODULE_BUILD ===

"""Witness/geometry consistency validator for edcmucns v0.3.1.

``witness_geometry_consistent(G_ucns, Π_provenance, policy_manifest)`` checks
that the geometry and its testimony tell the same story under the
manifest-pinned gauge. Every mismatch is a :class:`BridgeDiagnostic` — it
must not silently become an alternate reading. Witness provenance never
overrides inconsistent geometry.
"""

from __future__ import annotations

from fractions import Fraction

from .geometry import L_op, bone_anchors, non_origin_residue
from .manifest import PolicyManifest
from .provenance import ProvenanceWitness, canonicalize
from .types import Anchor, BridgeDiagnostic, Window


def witness_geometry_consistent(
    anchors: tuple[Anchor, ...],
    witnesses: tuple[ProvenanceWitness, ...],
    policy_manifest: PolicyManifest,
    *,
    payload_ids: tuple[str, ...] = (),
) -> list[BridgeDiagnostic]:
    """Return Bridge diagnostics; an empty list means consistent."""

    diags: list[BridgeDiagnostic] = []
    bones = tuple(a for a in anchors if a.role == "bone")

    for a in anchors:
        if a.role == "origin":
            if a.theta != 0 or a.face != 0:
                diags.append(BridgeDiagnostic(
                    kind="origin_datum_violation",
                    detail="origin anchors must sit at theta=0 with face=0",
                    expected="theta=0, face=0",
                    observed=f"theta={a.theta}, face={a.face}",
                ))
        elif a.theta == 0:
            diags.append(BridgeDiagnostic(
                kind="phase_zero_without_datum_role",
                detail="theta=0 is reserved for explicit datum roles",
                expected="role=origin at theta=0",
                observed=f"role={a.role} at theta=0",
            ))

    if not bones:
        diags.append(BridgeDiagnostic(
            kind="present_geometry_without_bones",
            detail="a no-bone turn must be AbsentOperatorGeometry, not an "
                   "empty Present window",
            expected="AbsentOperatorGeometry",
            observed="Present window with zero bone anchors",
        ))

    if len(bones) != len(witnesses):
        diags.append(BridgeDiagnostic(
            kind="witness_bone_pairing",
            detail="bone anchors and witnesses must pair 1:1 in order",
            expected=f"{len(bones)} witnesses",
            observed=f"{len(witnesses)} witnesses",
        ))

    gauge = policy_manifest.gauge
    for anchor, witness in zip(bones, witnesses):
        if witness.role != "bone":
            diags.append(BridgeDiagnostic(
                kind="witness_role_mismatch",
                detail="a witness paired with a bone anchor must carry role='bone'; "
                       "role is readout-bearing testimony",
                expected="bone",
                observed=repr(witness.role),
            ))
        family = witness.family
        if family is None or family not in gauge:
            diags.append(BridgeDiagnostic(
                kind="family_gauge_mismatch",
                detail="witness family is not in the manifest-pinned prime gauge",
                expected=f"one of {sorted(gauge)}",
                observed=repr(family),
            ))
            continue
        prime = gauge[family]
        if anchor.family != family or anchor.lattice_n != prime:
            diags.append(BridgeDiagnostic(
                kind="family_gauge_mismatch",
                detail="anchor lattice disagrees with manifest family->prime gauge",
                expected=f"family={family}, lattice_n={prime}",
                observed=f"family={anchor.family}, lattice_n={anchor.lattice_n}",
            ))
            continue
        if witness.ordinal_m_f is None or witness.ordinal_m_f < 1:
            diags.append(BridgeDiagnostic(
                kind="residue_rule_mismatch",
                detail="bone witnesses carry 1-based ordinals",
                expected="ordinal_m_f >= 1",
                observed=repr(witness.ordinal_m_f),
            ))
            continue
        expected_residue = non_origin_residue(witness.ordinal_m_f, prime)
        expected_theta = Fraction(expected_residue, prime)
        if (
            witness.residue_r_f != expected_residue
            or anchor.residue != expected_residue
            or anchor.theta != expected_theta
        ):
            diags.append(BridgeDiagnostic(
                kind="residue_rule_mismatch",
                detail="witness/geometry disagree with the v0.3.1 non-origin "
                       "residue rule",
                expected=f"r={expected_residue}, theta={expected_theta}",
                observed=(
                    f"witness r={witness.residue_r_f}, anchor r={anchor.residue}, "
                    f"theta={anchor.theta}"
                ),
            ))
        for label, value in (("turn_id", witness.turn_id),
                             ("speaker_or_source", witness.speaker_or_source)):
            if value != canonicalize(value):
                diags.append(BridgeDiagnostic(
                    kind="canonicalization_unstable",
                    detail=f"witness {label} is not in canonical form",
                    expected=canonicalize(value),
                    observed=value,
                ))
        if witness.payload_attachment is not None \
                and witness.payload_attachment not in payload_ids:
            diags.append(BridgeDiagnostic(
                kind="payload_attachment_missing",
                detail="witness payload_attachment target does not exist",
                expected=f"one of {sorted(payload_ids)}",
                observed=witness.payload_attachment,
            ))

    return diags


def validate_window(window: Window, policy_manifest: PolicyManifest) -> list[BridgeDiagnostic]:
    """Window-level convenience wrapper around witness_geometry_consistent.

    Also asserts the structural invariant that origin anchors are excluded
    from operator mass.
    """

    diags = witness_geometry_consistent(
        window.anchors,
        window.witnesses,
        policy_manifest,
        payload_ids=tuple(p.payload_id for p in window.payloads),
    )
    # The window was sealed under a manifest; validating it against a different
    # manifest (a rotation that keeps the family gauge but changes another
    # policy version) must not silently report a clean reading.
    if window.manifest_hash != policy_manifest.manifest_hash():
        diags.append(BridgeDiagnostic(
            kind="manifest_epoch_mismatch",
            detail="window manifest hash differs from the manifest it is "
                   "validated against; this is a manifest-rotation boundary",
            expected=window.manifest_hash,
            observed=policy_manifest.manifest_hash(),
        ))
    if L_op(window) != len(bone_anchors(window)):
        diags.append(BridgeDiagnostic(
            kind="operator_mass_contamination",
            detail="operator mass must count family-signature bone anchors only",
            expected=str(len(bone_anchors(window))),
            observed=str(L_op(window)),
        ))
    return diags


def gauge_audit(a: Window, b: Window) -> list[BridgeDiagnostic]:
    """Polarity gauge audit, scoped to bone faces only.

    A constant flip across every paired bone face is a gauge mismatch (same
    measurement in a flipped polarity gauge); a non-constant face difference
    is measurement divergence. Origin and cadence anchors are out of scope.
    """

    faces_a = [x.face for x in bone_anchors(a)]
    faces_b = [x.face for x in bone_anchors(b)]
    if len(faces_a) != len(faces_b):
        return [BridgeDiagnostic(
            kind="measurement_divergence",
            detail="bone-face sequences have different lengths",
            expected=str(len(faces_a)),
            observed=str(len(faces_b)),
        )]
    diffs = [fa != fb for fa, fb in zip(faces_a, faces_b)]
    if not diffs or not any(diffs):
        return []
    if all(diffs):
        return [BridgeDiagnostic(
            kind="gauge_mismatch",
            detail="constant face flip across all bone faces (polarity gauge "
                   "disagreement, not measurement divergence)",
            expected=str(faces_a),
            observed=str(faces_b),
        )]
    return [BridgeDiagnostic(
        kind="measurement_divergence",
        detail="non-constant bone-face difference",
        expected=str(faces_a),
        observed=str(faces_b),
    )]
