name: edcm
description: |
  Maintained Energy–Dissonance Circuit Model package. Load repo-local skills before editing, preserve source/semantic/geometry/policy/readout identity separation, and keep all empirical frontier gates non-operational until their falsifiers exist.

# === LLMS ===
# id: edcm_agent_overview
#   content: EDCM is the canonical maintained measurement package. It consumes canonical METAPAT semantic envelopes and canonical UCNS geometry/status evidence without transferring proof status into empirical validity. Use typed absence where evidence is unavailable, preserve NA != 0, compose ordered windows with SeqAppend, and run package, integrity, metadata, skill-drift, and msdmd gates before completion.
#
# id: edcm_agent_usage
#   content: Read CLAUDE.md, README.md, codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md, .agents/skills/the-interdependency/SKILL.md, and .agents/skills/meta-module-build/SKILL.md. Run python -m edcm.integrity, python -m pytest -q, python tools/check_metadata_contracts.py, and the canonical skill-lib drift/msdmd workflow.
# === END LLMS ===

# EDCM agent entrypoint

## Read first

1. `CLAUDE.md`
2. `README.md`
3. `codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md`
4. `.agents/skills/the-interdependency/SKILL.md`
5. `.agents/skills/meta-module-build/SKILL.md`
6. `docs/integrity-gates.md`
7. `docs/ucns-adapter.md`
8. `docs/shared-stack-result.md`

## Canonical source boundaries

```text
measurement implementation: The-Interdependency/edcm:edcm/measurement
semantic authority:        The-Interdependency/metapat
UCNS algebra/evidence:     The-Interdependency/ucns
organization skills:       The-Interdependency/skill-lib
```

Repo-local skill copies are consumers, never authorities.

## Required validation

```bash
python -m pip install -e .[dev]
python -m edcm.integrity
python -m pytest -q
python tools/check_metadata_contracts.py
python -m build
python -m twine check dist/*
```

Skill and msdmd validation use canonical `skill-lib@d0036c6c3a449f5a1213e3289dceb1c43263cb52` through `.github/workflows/skill-compliance.yml`.

## Non-negotiable boundaries

- `NA != 0`.
- METAPAT labels are not EDCM values.
- UCNS theorem/domain/certification evidence does not validate EDCM readouts.
- Package availability alone attaches no evidence.
- Ordered testimony-bearing windows use `SeqAppend`, never averaging.
- Contact convergence, DA geometry correlation, cadence admission from text, and semantic-label-to-operating-state inference remain explicit non-implementations.
- New EDCM-native modules begin with accurate `MODULE_BUILD` metadata and real test references.

## hmmm

UCNS evidence records currently provide canonical content identity but not cryptographic producer signatures. Signed producer or transport authentication remains unresolved.
