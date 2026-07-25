"""UCNS dependency diagnostics for the exact EDCM word-gonol profile.

Usage guidance
--------------
Use :func:`ucns_dependency_report` for non-throwing diagnostics and
:func:`require_ucns` only where the exact optional profile is mandatory.
Package presence alone never counts as profile recognition.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_dependency
#   module_name: ucns_dependency
#   module_kind: adapter
#   summary: diagnostics and fail-closed loading for the optional exact EDCM UCNS word-gonol profile
#   owner: Erin Spencer
#   public_surface: INSTALL_HINT, require_ucns, ucns_available, ucns_dependency_report
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_ucns_dependency
#   rollout: optional dependency diagnostic
#   rollback: report typed dependency absence while base EDCM remains operational
#   requires: edcm_ucns_adapter
#   since: 2026-07-25
#   unresolved: installed package provenance is enforced by the exact optional-dependency pin and profile invariants rather than a signed runtime attestation
# === END MODULE_BUILD ===
from __future__ import annotations

import importlib
import importlib.util
from types import ModuleType
from typing import Any

from .ucns_adapter import (
    INSTALL_HINT,
    RESET_BOUNDARY_REASON,
    UCNSAdapterConstructionError,
    inspect_ucns_adapter,
    select_ucns_adapter,
)


def require_ucns() -> ModuleType:
    """Return only an exact recognized UCNS producer; otherwise fail closed."""
    selection = select_ucns_adapter()
    if selection.adapter is None:
        reason = selection.status.errors[0] if selection.status.errors else RESET_BOUNDARY_REASON
        raise RuntimeError(reason)
    module = importlib.import_module("ucns")
    return module


def ucns_available() -> bool:
    """Report package presence only; this never implies producer recognition."""
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return False


def ucns_dependency_report() -> dict[str, Any]:
    status = inspect_ucns_adapter()
    report = status.as_dict()
    if status.adapter_active:
        dependency = "available"
    elif status.package_present:
        dependency = "failed"
    else:
        dependency = "missing"
    report.update(
        available=status.package_present,
        dependency=dependency,
        install_hint=INSTALL_HINT,
        reset_boundary_reason=RESET_BOUNDARY_REASON,
    )
    return report


__all__ = ["INSTALL_HINT", "require_ucns", "ucns_available", "ucns_dependency_report"]
