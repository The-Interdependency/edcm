"""Runtime helper for the required sibling UCNS dependency.

EDCM uses the real ``ucns`` package for scope metadata and proof-boundary
vocabulary when it is installed.  This module intentionally does not recreate
UCNS semantics locally.
"""

from __future__ import annotations

import importlib
from types import ModuleType
from typing import Any, Dict

INSTALL_HINT = "Install the sibling ucns package with: python -m pip install -e ../ucns"


def require_ucns() -> ModuleType:
    """Return the imported ``ucns`` module or raise a clear setup error."""

    try:
        return importlib.import_module("ucns")
    except ImportError as exc:
        raise ImportError(INSTALL_HINT) from exc


def ucns_available() -> bool:
    """Return whether the runtime ``ucns`` package can be imported."""

    try:
        require_ucns()
    except ImportError:
        return False
    return True


def ucns_dependency_report() -> Dict[str, Any]:
    """Report UCNS import availability without requiring Lean or Mathlib."""

    try:
        module = require_ucns()
    except ImportError:
        return {
            "available": False,
            "dependency": "missing",
            "install_hint": INSTALL_HINT,
        }

    return {
        "available": True,
        "dependency": "available",
        "module": getattr(module, "__name__", "ucns"),
        "version": getattr(module, "__version__", None),
    }
