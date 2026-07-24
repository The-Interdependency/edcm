"""UCNS package-presence diagnostics with activation suspended."""
from __future__ import annotations

import importlib.util
from typing import Any, NoReturn

from .ucns_adapter import INSTALL_HINT, RESET_BOUNDARY_REASON, inspect_ucns_adapter


def require_ucns() -> NoReturn:
    """Fail closed until an exact reviewed post-reset producer profile is pinned."""
    raise RuntimeError(RESET_BOUNDARY_REASON)


def ucns_available() -> bool:
    """Report package presence only; this never implies producer recognition."""
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return False


def ucns_dependency_report() -> dict[str, Any]:
    status = inspect_ucns_adapter()
    report = status.as_dict()
    report.update(
        available=status.package_present,
        dependency="suspended",
        install_hint=None,
        reset_boundary_reason=RESET_BOUNDARY_REASON,
    )
    return report


__all__ = ["INSTALL_HINT", "require_ucns", "ucns_available", "ucns_dependency_report"]
