"""Bridge energy-audit falsifiability structure with edcmbone-style preservation checks.

The bridge is intentionally optional: EDCM can compare falsifiability-bearing
claims using its stdlib-only energy audit even when the sibling ``edcmbone``
package is absent.  If an importable edcmbone measurement surface is present,
its structural-density signal is reported as auxiliary metadata only.

No UCNS-A theorem/proof status, UCNS-G metric-geometry status, edcmbone metric,
or empirical physics validation is transferred by this module.
"""

# === MODULE_BUILD ===
# id: edcm_falsifiability_bridge
#   module_name: falsifiability_bridge
#   module_kind: engine
#   summary: audits whether falsifiability-bearing claims survive input->output using the stdlib energy audit; optional edcmbone structural-density as auxiliary metadata only
#   owner: Erin Spencer
#   public_surface: audit_falsifiability_preservation, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE
#   internal_surface: _has_falsifiability_bearing_claim, _texts, _edcmbone_structural_density
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: audits arbitrary input/output text supplied by the caller
#   admin_only: false
#   tests: tests.test_falsifiability_bridge
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcm_energy_claims
#   since: 2026-06-02
#   unresolved: optional edcmbone import is best-effort; structural_density is auxiliary metadata, not a proof-status signal
# === END MODULE_BUILD ===

from __future__ import annotations

from importlib import import_module, util
from typing import Any, Dict, Iterable, Optional, Tuple

from .energy_claims import EnergyAuditReport, audit_energy_text


EDCMBONE_FAILURE_TAXONOMY = {
    "F1": "Deletion: operative variable absent from response without notice.",
    "F2": "Mutation: variable present but meaning altered.",
    "F3": "Inversion: negation removed; claim reversed.",
    "F4": "Category collapse: specific class flattened to a vague descriptor.",
    "F5": "Persistence failure: variable absent across a session boundary.",
    "F6": "Decorative preservation: surface form remains while operative function is removed.",
}

BOUNDARY_NOTE = (
    "This bridge compares preservation of falsifiability-bearing claim structure. "
    "It does not validate external physics, import UCNS-A proof status, or decide empirical truth."
)


def _has_falsifiability_bearing_claim(report: EnergyAuditReport) -> Tuple[object, ...]:
    return tuple(
        claim
        for claim in report.claims
        if claim.falsifier or claim.empirical_target or claim.predicted_delta
    )


def _texts(claims: Iterable[object]) -> Tuple[str, ...]:
    return tuple(getattr(claim, "raw_text") for claim in claims)


def _edcmbone_structural_density(text: str) -> Optional[float]:
    """Return edcmbone structural density if an installed edcmbone exposes it.

    edcmbone has had more than one package surface.  This best-effort helper is
    deliberately narrow and silent on ImportError/AttributeError so the bridge
    never makes edcmbone a hard runtime dependency.
    """

    if util.find_spec("edcmbone") is None:
        return None
    module_names = ("edcmbone.canon", "edcmbone.parser", "edcmbone.metrics", "edcmbone.compress")
    if any(util.find_spec(name) is None for name in module_names):
        return None

    canon_module = import_module("edcmbone.canon")
    parser_module = import_module("edcmbone.parser")
    metrics_module = import_module("edcmbone.metrics")
    codec = import_module("edcmbone.compress")

    try:
        canon = canon_module.CanonLoader()
        parsed = parser_module.parse_transcript(f"Speaker: {text}", canon=canon)
        metrics = metrics_module.compute_transcript(parsed, canon=canon)
        stats = codec.compression_stats(text, codec.to_bytes(parsed, metrics), parsed)
        value = stats.get("structural_density")
        return float(value) if value is not None else None
    except Exception:
        # Auxiliary edcmbone scoring must not make the audit bridge fail.
        return None


def audit_falsifiability_preservation(input_text: str, output_text: str) -> Dict[str, Any]:
    """Compare whether falsifiability-bearing spans survive a text transform.

    The result uses EDCM's energy audit as the required substrate and adds
    edcmbone-inspired F-loss/deletion labels.  edcmbone density values are
    included only when an installed sibling package exposes the old metric API.
    """

    input_report = audit_energy_text(input_text, source_ref="input")
    output_report = audit_energy_text(output_text, source_ref="output")
    input_bearing = _has_falsifiability_bearing_claim(input_report)
    output_bearing = _has_falsifiability_bearing_claim(output_report)

    possible_loss = bool(input_bearing and len(output_bearing) < len(input_bearing))
    possible_decorative_preservation = bool(
        input_bearing
        and not output_bearing
        and len(output_text) >= len(input_text)
    )

    f_loss_codes = []
    if possible_loss:
        f_loss_codes.append("F1")
    if possible_decorative_preservation:
        f_loss_codes.append("F6")

    input_density = _edcmbone_structural_density(input_text)
    output_density = _edcmbone_structural_density(output_text)
    density_delta = (
        output_density - input_density
        if input_density is not None and output_density is not None
        else None
    )

    return {
        "input_falsifiable_count": len(input_bearing),
        "output_falsifiable_count": len(output_bearing),
        "possible_falsifiability_loss": possible_loss,
        "possible_decorative_preservation": possible_decorative_preservation,
        "edcmbone_failure_codes": tuple(f_loss_codes),
        "edcmbone_failure_taxonomy": EDCMBONE_FAILURE_TAXONOMY,
        "input_falsifiability_spans": _texts(input_bearing),
        "output_falsifiability_spans": _texts(output_bearing),
        "edcmbone_structural_density_input": input_density,
        "edcmbone_structural_density_output": output_density,
        "edcmbone_structural_density_delta": density_delta,
        "boundary_note": BOUNDARY_NOTE,
        "input_report": input_report,
        "output_report": output_report,
    }
