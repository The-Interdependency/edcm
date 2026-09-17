name: edcm
description: |
  Energy–Dissonance Circuit Model measurement and evaluation. Preserve exact source,
  typed absence, candidate status, historical evidence and cross-repository authority.

# === LLMS ===
# id: project_overview
#   content: EDCM owns measurement/evaluation only. Package 0.2.0 supplies candidate edcm-measurement-v2, result schema 2.0.0 and codec 2. Frozen v1 canon data and historical reports retain their exact identities. UCNS owns gonol objects, constructors and geometry; Stack owns active language construction; METAPAT owns its semantic contracts. No proof or empirical status transfers.
#
# id: usage_rules
#   content: Read CANON.md, CLAUDE.md, docs/GONOL_LANGUAGE_BOUNDARY.md and docs/migrations/0.2.0-audit-repair.md. Submit raw inputs to build_default_layers().run(); output-only and retired inputs fail closed. For active language construction start in the owning Stack workspace using UCNS constructors. Historical replay uses exact original EDCM and producer commits. Preserve NA != 0 and unresolved hmmm.
#
# id: architecture_summary
#   content: The public pipeline validates raw inputs, selects independent METAPAT and UCNS adapters, measures transcripts with edcm.measurement, and assembles a complete hashed result. Optional absence is typed. UCNS geometry and factorization remain NA. Current language construction belongs to Stack/UCNS; retained EDCM construction modules serve historical replay.
#
# id: key_definitions
#   NA: Required evidence, context, geometry, or authority is unavailable; never numeric zero
#   hmmm: An unresolved constraint carried forward rather than guessed
# === END LLMS ===

# EDCM agent entrypoint

## Read first

1. `CANON.md`, `README.md`, and `CLAUDE.md`.
2. `docs/migrations/0.2.0-audit-repair.md` and `docs/integrity-gates.md`.
3. `docs/GONOL_LANGUAGE_BOUNDARY.md` for construction/evaluation routing.
4. Current canonical skill-lib entrypoint and applicable skills; vendored copies
   are consumers, pinned at `dd5027d99516831c0dcb83a176a67140d3819b66`.
5. The owning module's declarations and named tests before changes.
6. `docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md` and exact historical producer sources
   when replaying historical experiments.

## Authority

| Owner | Responsibility |
|---|---|
| METAPAT | Its semantic contracts and affixiation meaning |
| UCNS | Gonol objects, constructors, and geometry |
| Stack | Active language-gonol construction research and source/admission profiles |
| EDCM | Measurement/evaluation only |
| skill-lib | Organization build and evidence discipline |

For new construction use [Stack English](https://github.com/The-Interdependency/stack/tree/250a0afb7077b036a6c537411d004fa095c8b24a/research/english-gonol)
or [Stack Python](https://github.com/The-Interdependency/stack/tree/250a0afb7077b036a6c537411d004fa095c8b24a/research/python-gonol).
Resolve current owning commits before new work. EDCM’s retained `edcm.gonol` and `edcm.language`
modules are historical replay surfaces, not active construction authority.

## Non-negotiable boundaries

- `NA != 0`.
- Preserve source text, order, multiplicity, provenance and declared information loss.
- Public pipeline inputs cannot supply derived readouts, provenance or attachments.
- Missing geometry stays `NA`; an unresolved UCNS operation stays `hmmm`.
- Construction reproducibility does not establish measurement validity.
- UCNS or METAPAT proof/status does not validate EDCM readouts; EDCM fit does
  not prove their mathematics or semantics.
- Candidate registration, fixture success or majority agreement does not select canon.
- Transcript measurements do not establish diagnosis, intention, morality,
  consciousness or external truth.
- Frozen `*_v1.json` files change only by versioned canon migration. The 0.2
  implementation migration does not alter their byte identities.
- Historical reports remain immutable. Replay requires their exact original
  EDCM and upstream source commits; current v2 output is new evidence.
- New modules and changed native modules declare real tests, boundaries and usage.

## Validation and usage guidance

```bash
python -m pip install -e '.[dev]'
python -m edcm.integrity
python -m pytest -q
python tools/check_metadata_contracts.py
python -m build
python -m twine check dist/*
```

Use a separate environment with `.[dev,full-stack]` for the exact optional
producer gates. Historical joint experiment epochs use `.[dev,ucns-experiments]`
and the exact source checkout named by their runner; never silently repin them.

For measurement:

```python
from edcm import build_default_layers
result = build_default_layers().run({"transcript": "A: State the condition.\nB: Recorded."})
assert result["edcm_result"]["schema_version"] == "2.0.0"
```

## hmmm

General construct validity, independent outcome labels and holdout custody,
external replication, lawful projections over completed Stack constructions,
and signed producer authentication remain unresolved. See `docs/UPGRADE_AVENUES.md`.
