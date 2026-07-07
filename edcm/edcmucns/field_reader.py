# === MODULE_BUILD ===
# id: edcmucns_field_reader
#   module_name: field_reader
#   module_kind: engine
#   summary: field reader — build the ConstraintField/FieldMotion hash chain for a window's field_scope; NA-safe motion/state readouts; no empirical claim
#   owner: Erin Spencer
#   public_surface: FieldReading, read_field_chain, field_chain_hashes, attach_field_chain, field_readouts
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: constraint fields may summarize user-turn field state
#   admin_only: false
#   tests: tests.test_edcmucns_field_reader_v031
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcmucns_types,edcm.ucns_objects
#   since: 2026-07-07
#   unresolved: contact convergence over the chain stays the frontier gate in equivalence; this reader reports geometry/state only, no empirical operating-state claim
# === END MODULE_BUILD ===

"""Field reader for edcmucns v0.3.1.

Field state needs its own hash chain: ``field_scope`` in the readout registry
reads the ``ConstraintField`` / ``FieldMotion`` hash chain, and
:class:`edcm.edcmucns.Window` carries it as ``field_chain``. This module reads
an ordered sequence of :class:`edcm.ucns_objects.ConstraintField` states into
that chain — interleaving each field's ``field_hash`` with the
``prev -> curr`` transition hash of the :class:`FieldMotion` between
consecutive fields — and exposes the NA-safe F/E/O_scope motion readouts and
R/D/I/L_resistance state readouts the fields already produce.

Architecture only. The reader constructs and reports geometry and state; it
makes no empirical operating-state claim. Contact convergence over the chain
remains the frontier gate in :mod:`edcm.edcmucns.equivalence`; NA never
collapses to 0 (empty fields and absent motion stay NA).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..ucns_objects import ConstraintField, FieldMotion, MetricReadout
from .types import Window


@dataclass(frozen=True, slots=True)
class FieldReading:
    """The read result over an ordered ConstraintField sequence.

    ``chain`` is the chronological hash chain for ``field_scope``:
    ``[field_hash_0, motion_0->1, field_hash_1, motion_1->2, ...]``. A single
    field yields just its ``field_hash``; an empty sequence yields an empty
    chain.
    """

    fields: tuple[ConstraintField, ...]
    motions: tuple[FieldMotion, ...]
    chain: tuple[str, ...]

    @property
    def raised_field_count(self) -> int:
        """Total raised-field substrate across the read fields."""

        return sum(f.raised_field_count for f in self.fields)


def read_field_chain(
    fields: tuple[ConstraintField, ...] | list[ConstraintField],
    *,
    motion_reads: tuple[dict[str, tuple[float, ...]], ...] | None = None,
) -> FieldReading:
    """Read an ordered ConstraintField sequence into a FieldReading.

    ``motion_reads`` optionally supplies per-transition ``recurrence_reads`` /
    ``intensity_reads`` / ``scope_reads`` (one dict per consecutive pair,
    ``len(fields) - 1`` entries); absent reads leave the motion readouts at
    their present-but-empty ``0`` (or NA when neither field is present),
    exactly as :class:`FieldMotion` defines.
    """

    fields = tuple(fields)
    if motion_reads is not None and len(motion_reads) != max(0, len(fields) - 1):
        raise ValueError(
            "motion_reads must have exactly len(fields) - 1 entries "
            f"({max(0, len(fields) - 1)}); got {len(motion_reads)}"
        )

    motions: list[FieldMotion] = []
    chain: list[str] = []
    for i, cf in enumerate(fields):
        if i > 0:
            reads = motion_reads[i - 1] if motion_reads is not None else {}
            motion = FieldMotion.from_fields(
                fields[i - 1],
                cf,
                recurrence_reads=reads.get("recurrence_reads", ()),
                intensity_reads=reads.get("intensity_reads", ()),
                scope_reads=reads.get("scope_reads", ()),
            )
            motions.append(motion)
            chain.append(motion.parent_hash)
        chain.append(cf.field_hash)

    return FieldReading(fields=fields, motions=tuple(motions), chain=tuple(chain))


def field_chain_hashes(
    fields: tuple[ConstraintField, ...] | list[ConstraintField],
) -> tuple[str, ...]:
    """Convenience: just the field_scope hash chain for a field sequence."""

    return read_field_chain(fields).chain


def attach_field_chain(
    window: Window,
    fields: tuple[ConstraintField, ...] | list[ConstraintField],
    *,
    motion_reads: tuple[dict[str, tuple[float, ...]], ...] | None = None,
) -> Window:
    """Return a copy of ``window`` with its ``field_chain`` read from ``fields``.

    The window's ``raised_field_count`` is updated to the read total so
    ``lambda_field`` stays consistent with the attached field state.
    """

    reading = read_field_chain(fields, motion_reads=motion_reads)
    return Window(
        anchors=window.anchors,
        witnesses=window.witnesses,
        manifest_hash=window.manifest_hash,
        payloads=window.payloads,
        tok_count=window.tok_count,
        raised_field_count=reading.raised_field_count,
        field_chain=reading.chain,
    )


def field_readouts(reading: FieldReading) -> dict[str, list[MetricReadout]]:
    """Collect the NA-safe state and motion readouts for a reading.

    - ``state``: per-field R / D / I / L_resistance readouts (NA on empty
      fields);
    - ``motion``: per-transition F / E / O_scope readouts (NA when neither
      field of the pair is present).
    """

    state: list[MetricReadout] = []
    for cf in reading.fields:
        state.extend(cf.behavioral_readouts().values())
    motion: list[MetricReadout] = []
    for fm in reading.motions:
        motion.extend(fm.readouts().values())
    return {"state": state, "motion": motion}
