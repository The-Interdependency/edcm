"""EDCM package bootstrap.

Provides a single place to assemble all four EDCM layers while
optionally integrating with external `ucns` and `edcmbone` packages.
"""

from .layers import EDCMLayers, build_default_layers

__all__ = ["EDCMLayers", "build_default_layers"]
