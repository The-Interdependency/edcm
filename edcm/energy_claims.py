"""Stdlib-only energy-theory falsifiability audit layer.

This module audits claim structure and falsifiability readiness. It does not
validate physics, import Lean proof status, or transfer UCNS-A theorem status
into EDCM outputs. UCNS package availability is reported separately from
object, scope, certification, and theorem-evidence attachment.
"""

# === MODULE_BUILD ===
# id: edcm_energy_claims
#   module_name: energy_claims
#   module_kind: engine
#   summary: stdlib-only energy-theory falsifiability audit with explicit UCNS package/adapter/evidence status and no physics validation or proof-status transfer
#   owner: Erin Spencer
#   public_surface: EnergyClaim, AuditFlag, EnergyAuditReport, extract_energy_claim_candidates, audit_energy_claim, audit_energy_text, CAPABILITY_STATEMENT
#   internal_surface: _contains_any, _split_spans, _candidate, _first_unit, _claimed_quantity, _extract_after_markers, _flag, _summarize
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: audits arbitrary claim text supplied by the caller
#   admin_only: false
#   tests: tests.test_energy_claims, tests.test_ucns_dependency
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcm_ucns_dependency
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .ucns_dependency import ucns_dependency_report

CAPABILITY_STATEMENT = (
    "This report audits energy-theory claim structure and falsifiability readiness. "
    "It does not validate external physics, import UCNS-A proof status, or decide "
    "empirical truth."
)
UCNS_PACKAGE_ONLY = (
    "UCNS package and adapter are available, but this text audit attached no UCNS "
    "object, scope metadata, negative certification, or theorem-status evidence."
)
UCNS_SCOPE_MISSING = "UCNS package unavailable; no UCNS object or scope evidence attached."


@dataclass(frozen=True)
class EnergyClaim:
    claim_id: str
    raw_text: str
    source_ref: Optional[str]
    claimed_quantity: Optional[str]
    units: Optional[str]
    source: Optional[str]
    sink: Optional[str]
    transfer_path: Optional[str]
    coupling: Optional[str]
    storage_variable: Optional[str]
    dissipation_rule: Optional[str]
    boundary_condition: Optional[str]
    predicted_delta: Optional[str]
    falsifier: Optional[str]
    empirical_target: Optional[str]
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class AuditFlag:
    claim_id: str
    code: str
    severity: str
    message: str
    raw_text: str


@dataclass(frozen=True)
class EnergyAuditReport:
    claims: Tuple[EnergyClaim, ...]
    flags: Tuple[AuditFlag, ...]
    summary: Dict[str, int]
    capability_statement: str = CAPABILITY_STATEMENT
    ucns_dependency: Dict[str, Any] = field(default_factory=dict)
    ucns_scope_note: str = UCNS_SCOPE_MISSING


ENERGY_WORDS = {
    "energy", "pressure", "force", "mass", "frequency", "wave", "strain",
    "damping", "resonance", "intensity", "coherence", "phase", "coupling",
    "modulation", "dissipation", "transfer", "gradient", "entropy",
    "negentropy", "work", "power",
}
BOUNDARY_WORDS = {
    "ceiling", "limit", "clamp", "stable", "unstable", "runaway", "drift",
    "threshold", "closure", "conserved", "conservation", "exact", "locked", "fixed",
}
FALSIFIABILITY_WORDS = {
    "falsifiable", "prediction", "predicts", "testable", "observable", "confirm",
    "falsify", "kill the theory", "measurement", "measured", "within error",
}
SYMBOL_PATTERNS = ["P", "N_n", "ω", "D_f", "φ_I", "κ", "R", "L_eff", "theta", "psi", "∇", "ψ"]
UNITS = ["rad/s", "MeV", "GeV", "eV", "Mpc", "Gpc", "years", "kg", "Pa", "Hz", "J", "N", "W", "m", "s"]
QUANTITY_WORDS = ["pressure", "frequency", "mass", "intensity", "dimension", "phase", "coupling", "radius", "strain", "power", "force", "energy"]
EMPIRICAL_TARGETS = ["CMB", "Euclid", "DESI", "LIGO", "PDG", "lithium", "galaxy clustering", "X-ray echo", "multipole", "abundance", "strain", "rotation curves"]

_NUMERIC_RE = re.compile(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?(?:\s*[×x*]\s*10(?:\^[-+]?\d+|[⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+))?|[-+]?\d+\.\d+")
_SENTENCE_RE = re.compile(r"[^.!?;\n]+(?:[.!?;]|$)", re.UNICODE)


def _contains_any(text: str, terms: List[str] | set[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def _split_spans(text: str) -> List[str]:
    return [m.group(0).strip() for m in _SENTENCE_RE.finditer(text) if m.group(0).strip()]


def _candidate(span: str) -> bool:
    return _contains_any(span, ENERGY_WORDS) or _contains_any(span, BOUNDARY_WORDS) or _contains_any(span, FALSIFIABILITY_WORDS) or any(sym in span for sym in SYMBOL_PATTERNS)


def _first_unit(span: str) -> Optional[str]:
    for unit in UNITS:
        if re.search(rf"(?<![A-Za-z]){re.escape(unit)}(?![A-Za-z])", span):
            return unit
    if "dimensionless" in span.lower() or "declared dimension" in span.lower():
        return "dimensionless"
    return None


def _claimed_quantity(span: str) -> Optional[str]:
    for word in QUANTITY_WORDS:
        match = re.search(rf"\b{word}\b\s*(?:([A-Za-z_][A-Za-z0-9_]*|[A-Z]|[ωφκψ∇](?:_[A-Za-z])?))?", span, re.I)
        if match:
            sym = match.group(1)
            return f"{word} {sym}".strip() if sym else word
    for sym in SYMBOL_PATTERNS:
        if sym in span:
            return sym
    return None


def _extract_after_markers(span: str, markers: List[str]) -> Optional[str]:
    lower = span.lower()
    for marker in markers:
        idx = lower.find(marker)
        if idx >= 0:
            return span[idx: idx + 80].strip(" ,.;")
    return None


def extract_energy_claim_candidates(text: str, source_ref: Optional[str] = None) -> List[EnergyClaim]:
    """Extract sentence-like energy-claim candidates using deterministic heuristics."""

    claims: List[EnergyClaim] = []
    for index, span in enumerate((s for s in _split_spans(text) if _candidate(s)), start=1):
        lower = span.lower()
        source = _extract_after_markers(span, ["source", "from ", "reservoir", "emits", "releases"])
        sink = _extract_after_markers(span, ["sink", " to ", " into ", "absorbs"])
        transfer_path = _extract_after_markers(span, ["through", "across", "via", "transfer", "flow"])
        coupling = _extract_after_markers(span, ["coupling", "κ", "phi", "φ", "phase", "modulates", "drives", "locks", "interacts"])
        storage_variable = _extract_after_markers(span, ["stored", "tension", "strain", "pressure", "intensity", "potential", "reservoir", "field", "mode", "standing wave"])
        dissipation_rule = _extract_after_markers(span, ["damps", "damping", "dissipates", "decay", "lifetime", "returns to", "loss", "noise"])
        boundary_condition = _extract_after_markers(span, ["hard ceiling", "ceiling", "limit", "threshold", "clamp", "closure", "must not exceed", "bounded", "cap"])
        predicted_delta = _extract_after_markers(span, ["predicts", "prediction", "excess", "delta", "shift", "change"])
        falsifier = _extract_after_markers(span, ["falsify", "falsifiable", "kill the theory", "testable"])
        empirical_target = next((target for target in EMPIRICAL_TARGETS if target.lower() in lower), None)
        claims.append(EnergyClaim(
            claim_id=f"ECL-{index:04d}", raw_text=span, source_ref=source_ref,
            claimed_quantity=_claimed_quantity(span), units=_first_unit(span),
            source=source, sink=sink, transfer_path=transfer_path, coupling=coupling,
            storage_variable=storage_variable, dissipation_rule=dissipation_rule,
            boundary_condition=boundary_condition, predicted_delta=predicted_delta,
            falsifier=falsifier, empirical_target=empirical_target, notes=(),
        ))
    return claims


def _flag(claim: EnergyClaim, code: str, severity: str, message: str) -> AuditFlag:
    return AuditFlag(claim.claim_id, code, severity, message, claim.raw_text)


def audit_energy_claim(claim: EnergyClaim) -> List[AuditFlag]:
    """Audit one extracted claim for falsifiability-readiness flags."""

    flags: List[AuditFlag] = []
    text = claim.raw_text
    lower = text.lower()
    if not claim.claimed_quantity:
        flags.append(_flag(claim, "E001_NO_QUANTITY", "warning", "Candidate uses energy language but no measurable quantity is identified."))
    if _NUMERIC_RE.search(text) and not claim.units and "dimension" not in lower:
        flags.append(_flag(claim, "E002_NUMERIC_WITHOUT_UNIT", "failure", "Numeric claim appears without a unit or declared dimension."))
    if (_contains_any(text, {"transfer", "flow", "modulates", "coupling", "dissipates", "emits", "absorbs"}) or claim.transfer_path) and not (claim.source or claim.sink):
        flags.append(_flag(claim, "E003_NO_SOURCE_OR_SINK", "warning", "Flow / transfer / modulation claim lacks source or sink."))
    if claim.coupling and not (claim.transfer_path or claim.source or claim.sink or claim.predicted_delta):
        flags.append(_flag(claim, "E004_COUPLING_WITHOUT_EXCHANGE_RULE", "failure", "Coupling is asserted without saying what is exchanged or how it changes the target."))
    if claim.storage_variable and not claim.dissipation_rule and _contains_any(text, {"stored", "tension", "pressure", "intensity", "reservoir"}):
        flags.append(_flag(claim, "E005_STORAGE_WITHOUT_RELEASE_OR_DISSIPATION", "warning", "Stored tension / pressure / intensity appears without release, decay, or damping rule."))
    if claim.boundary_condition and not _contains_any(text, {"derive", "derived", "because", "test", "measured", "observable", "falsify"}):
        flags.append(_flag(claim, "E006_BOUNDARY_WITHOUT_DERIVATION", "warning", "Boundary, ceiling, cap, or clamp is asserted without derivation or test."))
    if _contains_any(text, {"clamp", "ceiling", "cap"}) and _contains_any(text, {"derived", "exact", "follows from", "therefore"}):
        flags.append(_flag(claim, "E007_CLAMP_PRESENTED_AS_DERIVED", "failure", "Text presents an imposed clamp as if it follows from the equation."))
    if (_contains_any(text, ENERGY_WORDS | BOUNDARY_WORDS) and not (claim.falsifier or claim.empirical_target)):
        flags.append(_flag(claim, "E008_FALSIFIER_ABSENT", "warning", "Major theory claim lacks a concrete falsifier or empirical target."))
    if _contains_any(text, {"exactly", "exact", "zero free parameter", "zero free parameters", "complete", "reproduces every"}) and not _contains_any(text, {"data", "dataset", "measurement path", "measured by"}):
        flags.append(_flag(claim, "E009_EXACTNESS_OVERCLAIM", "warning", "Exact / zero-free-parameter / complete / reproduces every claim appears without data path."))
    if ("=" in text or "≈" in text) and _NUMERIC_RE.search(text) and not claim.units and any(sym in text for sym in SYMBOL_PATTERNS):
        flags.append(_flag(claim, "E010_DIMENSIONAL_RISK", "failure", "Equation-like span appears to combine unlike terms or includes symbols with undefined dimensions."))
    if claim.empirical_target:
        flags.append(_flag(claim, "E011_EMPIRICAL_TARGET_PRESENT", "info", "Claim names an empirical target and is at least potentially checkable later."))
    return flags


def _summarize(flags: List[AuditFlag]) -> Dict[str, int]:
    summary: Dict[str, int] = {"claims": 0, "flags": len(flags)}
    for flag in flags:
        summary[flag.severity] = summary.get(flag.severity, 0) + 1
        summary[flag.code] = summary.get(flag.code, 0) + 1
    return summary


def audit_energy_text(text: str, source_ref: Optional[str] = None) -> EnergyAuditReport:
    """Extract and audit energy claims; report UCNS states without attachment inflation."""

    claims = extract_energy_claim_candidates(text, source_ref)
    flags: List[AuditFlag] = []
    for claim in claims:
        flags.extend(audit_energy_claim(claim))
    summary = _summarize(flags)
    summary["claims"] = len(claims)
    dependency = ucns_dependency_report()
    note = UCNS_PACKAGE_ONLY if dependency["ucns_adapter_active"] else UCNS_SCOPE_MISSING
    return EnergyAuditReport(
        tuple(claims),
        tuple(flags),
        summary,
        CAPABILITY_STATEMENT,
        dependency,
        note,
    )
