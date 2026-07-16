#!/usr/bin/env python3
"""Retired OEWN gonol builder.

The previous builder depended on a noncanonical EDCM-owned copy of the public
gonol and on hash/evidence-derived fractional placement. Those assumptions are
superseded. The canonical public gonol now belongs to UCNS, and no bridge from
that twist-bearing frame into EDCM's local language object has been ratified.

This command therefore fails before reading OEWN or writing artifacts. A future
builder must consume the UCNS public surface explicitly and document the exact
bridge approved by Erin.
"""

from __future__ import annotations

from edcm.language.placement import require_canonical_language_placement


def main() -> int:
    require_canonical_language_placement()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
