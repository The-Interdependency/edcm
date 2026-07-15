"""Canonical UCNS audit objects for EDCM metric axes and observations.

This module converts existing scalar EDCM metrics into content-addressed UCNS
objects. It does not compute, score, normalize, or replace any metric formula.
The scalar value remains the EDCM readout; the UCNS object is an adjacent audit
and identity representation.

Usage guidance
--------------
Install the optional UCNS integration, then resolve either one observation or a
complete ``RoundMetrics`` vector::

    python -m pip install -e ".[ucns]"

    from edcm.ucns_metrics import resolve_metric_value, resolve_round_metrics

    resolved = resolve_metric_value(
        "behavioral:C",
        0.3,
        grain="round",
        source="RoundMetrics",
        context_id="round:7",
        formula_version="edcm.measurement.metrics.compute/1",
    )
    print(resolved.ucns_hash)
    print(resolved.record_list())

    vector = resolve_round_metrics(round_metrics)

``resolve_metric_vector`` and ``resolve_round_metrics`` never mutate their
inputs. ``round:P_progress`` and ``state:kappa`` intentionally have no UCNS-G
primitive axis assignment.

No UCNS-A theorem/proof status is transferred to EDCM, edcmbone, or UCNS-G by
this change.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_metrics
#   module_name: ucns_metrics
#   module_kind: adapter
#   summary: resolves scalar EDCM metric axes and observations into canonical UCNS audit objects without changing metric formulas
#   owner: Erin Spencer
#   public_surface: MetricDefinition, ResolvedMetricUCNS, UCNSMetricDependencyError, UCNSMetricResolutionError, METRIC_DEFINITIONS, SYMBOL_TO_METRIC_ID, resolve_metric_axis, resolve_metric_value, resolve_metric_vector, resolve_round_metrics, resolved_metric_objects_payload
#   internal_surface: _load_ucns, _canonical_metric_id, _metric_definition, _as_fraction, _clamp_fraction, _record_tuple, _encode_record, _resolved_from_record
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: metric context identifiers and scalar observations remain caller-supplied audit metadata
#   admin_only: false
#   tests: tests.test_ucns_metrics
#   rollout: optional_ucns_integration
#   rollback: remove module exports and resolved-metric call sites; scalar EDCM outputs remain unchanged
#   requires: edcm_ucns_adapter
#   since: 2026-07-15
#   unresolved: UCNS objects provide canonical content identity but not signed producer or transport authentication
# === END MODULE_BUILD ===

from __future__ import annotations

import importlib
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType, ModuleType
from typing import Any, Mapping, Sequence


METRIC_OBJECT_SCHEMA_ID = "edcm/metric_ucns_object_v1"
RESOLVED_METRICS_SCHEMA_ID = "edcm/resolved_metrics_ucns_v1"
EXPERIMENTAL_STATUS = "EXPERIMENTAL"
DEFAULT_MAX_DENOMINATOR = 1_000_000
DEFAULT_FORMULA_VERSION = "unknown"
ROUND_METRIC_FIELDS = ("C", "R", "F", "E", "D", "N", "I", "O", "L", "P", "kappa")


class UCNSMetricDependencyError(ModuleNotFoundError):
    """Raised when metric resolution is requested without the optional UCNS package."""


class UCNSMetricResolutionError(RuntimeError):
    """Raised when the available UCNS package cannot satisfy the metric contract."""


@dataclass(frozen=True)
class MetricDefinition:
    """Canonical EDCM metric-axis definition used by the UCNS resolver."""

    metric_id: str
    symbol: str
    name: str
    range_label: str
    ucns_g_axis: str | None
    kind: str


@dataclass(frozen=True)
class ResolvedMetricUCNS:
    """One EDCM metric axis or value observation resolved as a UCNS object."""

    metric_id: str
    symbol: str
    object_kind: str
    value_num: int | None
    value_den: int | None
    sign: int
    magnitude_num: int
    magnitude_den: int
    status: str
    ucns_object: Any
    ucns_hash: str
    record: tuple[tuple[str, Any], ...]

    def record_list(self) -> list[list[Any]]:
        """Return the canonical ordered list-of-pairs passed to UCNS encoding."""

        return [[name, value] for name, value in self.record]

    def to_payload(self) -> dict[str, Any]:
        """Return a JSON-compatible audit view without embedding the live object."""

        return {
            "hash": self.ucns_hash,
            "record": self.record_list(),
        }


_DEFINITIONS = {
    "behavioral:C": MetricDefinition(
        "behavioral:C", "C", "Constraint strain", "[0,1]", "C", "behavioral_metric"
    ),
    "behavioral:R": MetricDefinition(
        "behavioral:R", "R", "Refusal density", "[0,1]", "R", "behavioral_metric"
    ),
    "behavioral:D": MetricDefinition(
        "behavioral:D", "D", "Deflection", "[0,1]", "D", "behavioral_metric"
    ),
    "behavioral:N": MetricDefinition(
        "behavioral:N", "N", "Noise", "[0,1]", "N", "behavioral_metric"
    ),
    "behavioral:L": MetricDefinition(
        "behavioral:L",
        "L",
        "Coherence loss / resistance depending surface",
        "[0,1]",
        "L",
        "behavioral_metric",
    ),
    "behavioral:O": MetricDefinition(
        "behavioral:O",
        "O",
        "Overconfidence / signed axis depending surface",
        "[-1,1]",
        "O",
        "signed_behavioral_metric",
    ),
    "behavioral:F": MetricDefinition(
        "behavioral:F", "F", "Fixation", "[0,1]", "F", "behavioral_metric"
    ),
    "behavioral:E": MetricDefinition(
        "behavioral:E", "E", "Escalation", "[0,1]", "E", "behavioral_metric"
    ),
    "behavioral:I": MetricDefinition(
        "behavioral:I", "I", "Integration failure", "[0,1]", "I", "behavioral_metric"
    ),
    "round:P_progress": MetricDefinition(
        "round:P_progress",
        "P",
        "Progress",
        "[0,1]",
        None,
        "round_metric_non_ucns_g_primitive",
    ),
    "state:kappa": MetricDefinition(
        "state:kappa",
        "κ",
        "Stored tension",
        "[0,1]",
        None,
        "state_variable_non_ucns_g_primitive",
    ),
}
METRIC_DEFINITIONS: Mapping[str, MetricDefinition] = MappingProxyType(_DEFINITIONS)

_SYMBOLS = {
    "C": "behavioral:C",
    "R": "behavioral:R",
    "F": "behavioral:F",
    "E": "behavioral:E",
    "D": "behavioral:D",
    "N": "behavioral:N",
    "I": "behavioral:I",
    "O": "behavioral:O",
    "L": "behavioral:L",
    "P": "round:P_progress",
    "P_progress": "round:P_progress",
    "kappa": "state:kappa",
    "κ": "state:kappa",
}
SYMBOL_TO_METRIC_ID: Mapping[str, str] = MappingProxyType(_SYMBOLS)


__all__ = [
    "DEFAULT_FORMULA_VERSION",
    "EXPERIMENTAL_STATUS",
    "METRIC_DEFINITIONS",
    "METRIC_OBJECT_SCHEMA_ID",
    "MetricDefinition",
    "RESOLVED_METRICS_SCHEMA_ID",
    "ROUND_METRIC_FIELDS",
    "ResolvedMetricUCNS",
    "SYMBOL_TO_METRIC_ID",
    "UCNSMetricDependencyError",
    "UCNSMetricResolutionError",
    "resolve_metric_axis",
    "resolve_metric_value",
    "resolve_metric_vector",
    "resolve_round_metrics",
    "resolved_metric_objects_payload",
]


def _load_ucns() -> ModuleType:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        raise UCNSMetricDependencyError(
            "UCNS metric resolution requires the optional `ucns` package; "
            "install EDCM with `python -m pip install -e .[ucns]`.",
            name="ucns",
        ) from exc

    required = ("UCNSObject", "recursive_encode", "stable_hash")
    missing = tuple(name for name in required if not hasattr(module, name))
    if missing:
        raise UCNSMetricResolutionError(
            "Importable ucns package is missing required public surfaces: "
            + ", ".join(missing)
        )
    return module


def _canonical_metric_id(metric_id: str) -> str:
    if not isinstance(metric_id, str) or not metric_id.strip():
        raise ValueError("metric_id must be a non-empty string")
    value = metric_id.strip()
    if value in METRIC_DEFINITIONS:
        return value
    try:
        return SYMBOL_TO_METRIC_ID[value]
    except KeyError as exc:
        raise KeyError(f"unknown EDCM metric id or symbol: {metric_id!r}") from exc


def _metric_definition(metric_id: str) -> MetricDefinition:
    return METRIC_DEFINITIONS[_canonical_metric_id(metric_id)]


def _as_fraction(
    value: Fraction | float | int | str,
    *,
    max_denominator: int = DEFAULT_MAX_DENOMINATOR,
) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("metric values must not be booleans")
    if (
        not isinstance(max_denominator, int)
        or isinstance(max_denominator, bool)
        or max_denominator < 1
    ):
        raise ValueError("max_denominator must be a positive integer")
    try:
        if isinstance(value, Fraction):
            result = value
        elif isinstance(value, (int, float, str)):
            result = Fraction(str(value))
        else:
            raise TypeError(
                "metric values must be Fraction, int, float, or rational/decimal string"
            )
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"invalid finite metric value: {value!r}") from exc
    return result.limit_denominator(max_denominator)


def _clamp_fraction(value: Fraction, low: Fraction, high: Fraction) -> Fraction:
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))


def _record_tuple(record: Sequence[Sequence[Any]]) -> tuple[tuple[str, Any], ...]:
    converted: list[tuple[str, Any]] = []
    for item in record:
        if len(item) != 2 or not isinstance(item[0], str):
            raise ValueError("metric records must be ordered name/value pairs")
        converted.append((item[0], item[1]))
    return tuple(converted)


def _encode_record(record: Sequence[Sequence[Any]]) -> tuple[Any, str]:
    module = _load_ucns()
    record_list = [[item[0], item[1]] for item in record]
    try:
        obj = module.recursive_encode(record_list)
    except Exception as exc:
        raise UCNSMetricResolutionError("UCNS could not encode the metric record") from exc
    if not isinstance(obj, module.UCNSObject):
        raise UCNSMetricResolutionError(
            "ucns.recursive_encode returned the wrong object type"
        )
    try:
        digest = module.stable_hash(obj)
    except Exception as exc:
        raise UCNSMetricResolutionError("UCNS could not hash the metric object") from exc
    if not isinstance(digest, str) or not digest:
        raise UCNSMetricResolutionError("ucns.stable_hash returned an invalid digest")
    return obj, digest


def _resolved_from_record(
    definition: MetricDefinition,
    *,
    object_kind: str,
    value: Fraction | None,
    sign: int,
    magnitude: Fraction,
    record: Sequence[Sequence[Any]],
) -> ResolvedMetricUCNS:
    obj, digest = _encode_record(record)
    return ResolvedMetricUCNS(
        metric_id=definition.metric_id,
        symbol=definition.symbol,
        object_kind=object_kind,
        value_num=None if value is None else value.numerator,
        value_den=None if value is None else value.denominator,
        sign=sign,
        magnitude_num=magnitude.numerator,
        magnitude_den=magnitude.denominator,
        status=EXPERIMENTAL_STATUS,
        ucns_object=obj,
        ucns_hash=digest,
        record=_record_tuple(record),
    )


def resolve_metric_axis(metric_id: str) -> ResolvedMetricUCNS:
    """Resolve a metric-axis identity without attaching a scalar observation."""

    definition = _metric_definition(metric_id)
    record = [
        ["schema_id", METRIC_OBJECT_SCHEMA_ID],
        ["object_kind", "metric_axis"],
        ["metric_id", definition.metric_id],
        ["symbol", definition.symbol],
        ["name", definition.name],
        ["range", definition.range_label],
        ["ucns_g_axis", definition.ucns_g_axis or ""],
        ["kind", definition.kind],
        ["status", EXPERIMENTAL_STATUS],
        ["ucns_theorem_transfer", False],
    ]
    return _resolved_from_record(
        definition,
        object_kind="metric_axis",
        value=None,
        sign=0,
        magnitude=Fraction(0, 1),
        record=record,
    )


def resolve_metric_value(
    metric_id: str,
    value: Fraction | float | int | str,
    *,
    grain: str,
    source: str,
    context_id: str | None = None,
    formula_version: str = DEFAULT_FORMULA_VERSION,
) -> ResolvedMetricUCNS:
    """Resolve one scalar EDCM observation as a canonical UCNS audit object."""

    definition = _metric_definition(metric_id)
    if not isinstance(grain, str) or not grain.strip():
        raise ValueError("grain must be a non-empty string")
    if not isinstance(source, str) or not source.strip():
        raise ValueError("source must be a non-empty string")
    if context_id is not None and not isinstance(context_id, str):
        raise TypeError("context_id must be a string or None")
    if not isinstance(formula_version, str) or not formula_version.strip():
        raise ValueError("formula_version must be a non-empty string")

    raw_value = _as_fraction(value)
    if definition.metric_id == "behavioral:O":
        resolved_value = _clamp_fraction(
            raw_value, Fraction(-1, 1), Fraction(1, 1)
        )
        sign = -1 if resolved_value < 0 else 1 if resolved_value > 0 else 0
        magnitude = abs(resolved_value)
    else:
        resolved_value = _clamp_fraction(raw_value, Fraction(0, 1), Fraction(1, 1))
        sign = 0 if resolved_value == 0 else 1
        magnitude = resolved_value

    record = [
        ["schema_id", METRIC_OBJECT_SCHEMA_ID],
        ["object_kind", "metric_value"],
        ["metric_id", definition.metric_id],
        ["symbol", definition.symbol],
        ["name", definition.name],
        ["source", source.strip()],
        ["grain", grain.strip()],
        ["context_id", context_id or ""],
        ["formula_version", formula_version.strip()],
        ["value_num", resolved_value.numerator],
        ["value_den", resolved_value.denominator],
        ["sign", sign],
        ["magnitude_num", magnitude.numerator],
        ["magnitude_den", magnitude.denominator],
        ["range", definition.range_label],
        ["ucns_g_axis", definition.ucns_g_axis or ""],
        ["status", EXPERIMENTAL_STATUS],
        ["ucns_theorem_transfer", False],
    ]
    return _resolved_from_record(
        definition,
        object_kind="metric_value",
        value=resolved_value,
        sign=sign,
        magnitude=magnitude,
        record=record,
    )


def resolve_metric_vector(
    metrics: Mapping[str, Fraction | float | int | str],
    *,
    grain: str,
    source: str,
    context_id: str | None = None,
    formula_version: str = DEFAULT_FORMULA_VERSION,
) -> dict[str, ResolvedMetricUCNS]:
    """Resolve a mapping of metric ids or symbols without mutating scalar values."""

    if not isinstance(metrics, Mapping):
        raise TypeError("metrics must be a mapping")
    resolved: dict[str, ResolvedMetricUCNS] = {}
    for supplied_id, value in metrics.items():
        canonical_id = _canonical_metric_id(supplied_id)
        if canonical_id in resolved:
            raise ValueError(
                f"duplicate metric after namespace resolution: {canonical_id}"
            )
        resolved[canonical_id] = resolve_metric_value(
            canonical_id,
            value,
            grain=grain,
            source=source,
            context_id=context_id,
            formula_version=formula_version,
        )
    return resolved


def resolve_round_metrics(
    round_metrics: Any,
    *,
    grain: str = "round",
    source: str = "RoundMetrics",
    context_id: str | None = None,
    formula_version: str = "edcm.measurement.metrics.compute/1",
) -> dict[str, ResolvedMetricUCNS]:
    """Resolve the 11 scalar fields of a ``RoundMetrics``-shaped object or mapping."""

    if isinstance(round_metrics, Mapping):
        values = {name: round_metrics[name] for name in ROUND_METRIC_FIELDS}
        round_index = round_metrics.get("round_index")
    else:
        values = {name: getattr(round_metrics, name) for name in ROUND_METRIC_FIELDS}
        round_index = getattr(round_metrics, "round_index", None)
    if context_id is None and round_index is not None:
        context_id = f"round:{round_index}"
    return resolve_metric_vector(
        values,
        grain=grain,
        source=source,
        context_id=context_id,
        formula_version=formula_version,
    )


def resolved_metric_objects_payload(
    resolved: Mapping[str, ResolvedMetricUCNS],
) -> dict[str, Any]:
    """Serialize resolved objects beside scalar output under a non-scoring field."""

    if not isinstance(resolved, Mapping):
        raise TypeError("resolved must be a mapping")
    objects: dict[str, Any] = {}
    for metric_id, item in resolved.items():
        if not isinstance(item, ResolvedMetricUCNS):
            raise TypeError("resolved values must be ResolvedMetricUCNS instances")
        canonical_id = _canonical_metric_id(metric_id)
        if canonical_id != item.metric_id:
            raise ValueError("resolved mapping key does not match the object metric_id")
        objects[canonical_id] = item.to_payload()
    return {
        "schema_id": RESOLVED_METRICS_SCHEMA_ID,
        "status": EXPERIMENTAL_STATUS,
        "ucns_theorem_transfer": False,
        "objects": objects,
    }
