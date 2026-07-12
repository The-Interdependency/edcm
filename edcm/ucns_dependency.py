"""UCNS dependency and adapter-state reporting.

Usage guidance
--------------
Use :func:`ucns_dependency_report` when diagnostics need to distinguish package
availability from adapter activation and evidence attachment. Use
:func:`require_ucns` only when a caller explicitly requires the sibling
package. A successful import alone never means that geometry, scope metadata,
negative certification, or theorem status was attached to an EDCM result.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_dependency
#   module_name: ucns_dependency
#   module_kind: adapter
#   summary: Reports independent UCNS package, adapter, object, scope, certification, and theorem-evidence states without proof-status transfer.
#   owner: Erin Spencer
#   public_surface: require_ucns, ucns_available, ucns_dependency_report, INSTALL_HINT
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_ucns_dependency, tests.test_ucns_adapter
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: edcm_ucns_adapter
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any

from .ucns_adapter import INSTALL_HINT, inspect_ucns_adapter


def require_ucns() -> ModuleType:
    """Return ``ucns`` or raise a clear error only for direct package absence."""

    try:
        return importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        raise ModuleNotFoundError(INSTALL_HINT, name="ucns") from exc


def ucns_available() -> bool:
    """Return package import availability only; no attachment claim is implied."""

    try:
        require_ucns()
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        return False
    return True


def ucns_dependency_report() -> dict[str, Any]:
    """Return independent package/adapter/evidence state flags.

    ``available`` and ``dependency`` remain compatibility aliases for package
    availability. Callers must use the explicit fields for evidence claims.
    """

    status = inspect_ucns_adapter()
    report = status.as_dict()
    report.update(
        available=status.ucns_package_available,
        dependency=(
            "missing"
            if not status.ucns_package_available
            else "available"
            if status.ucns_adapter_active
            else "failed"
        ),
        install_hint=None if status.ucns_package_available else INSTALL_HINT,
    )
    return report


__all__ = ["INSTALL_HINT", "require_ucns", "ucns_available", "ucns_dependency_report"]
