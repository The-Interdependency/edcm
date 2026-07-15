name: edcm
description: |
  Maintained Energy–Dissonance Circuit Model package. Load repo-local skills before editing, preserve source/semantic/geometry/policy/readout identity separation, and operate across the exact shared work graph rather than treating one repository as one AI boundary.

# === LLMS ===
# id: edcm_agent_overview
#   content: EDCM is the canonical maintained measurement package. It consumes canonical METAPAT semantic envelopes and canonical UCNS geometry/status evidence without transferring proof status into empirical validity. Use typed absence where evidence is unavailable, preserve NA != 0, compose ordered windows with SeqAppend, and run package, integrity, metadata, skill-drift, msdmd, and cross-repository identity gates before completion.
#
# id: edcm_agent_usage
#   content: Read CLAUDE.md, README.md, codex-handoff/2026-07-12-stack-repair/IMPLEMENTATION_STATUS.md, .agents/skills/the-interdependency/SKILL.md, .agents/skills/meta-module-build/SKILL.md, and docs/interconnectivity.md. Resolve work against the exact EDCM, METAPAT, UCNS, skill-lib, and evidence-source identities used by the task. Run python -m edcm.integrity, python -m pytest -q, python tools/check_metadata_contracts.py, and the canonical skill-lib drift/msdmd workflow.
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
9. `docs/interconnectivity.md`

## Canonical source boundaries

```text
measurement implementation: The-Interdependency/edcm:edcm/measurement
semantic authority:        The-Interdependency/metapat
UCNS algebra/evidence:     The-Interdependency/ucns
organization skills:       The-Interdependency/skill-lib
dictionary evidence:       globalwordnet/english-wordnet at the declared run commit
```

Repo-local skill copies are consumers, never authorities.

## Interconnected operating model

```text
repository boundary != agent boundary
repository boundary == authority and provenance boundary
```

An EDCM task may depend on several repositories at once. Before implementation, resolve the exact commit for every participating authority and evidence source. Preserve those identities in a shared stack manifest or equivalent task record. One agent may coordinate the complete graph; no agent may silently flatten the graph into one repository's assumptions.

The current stack-manifest contract is `the-interdependency.stack-manifest` version `1.0.0`. It records participating repositories, their exact commits, their authority roles, their work relations, a deterministic work-graph digest, and explicit non-transfer boundaries.

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
- Cross-repository coordination transfers neither authority, proof status, nor measurement validity.
- Agents must preserve exact participating-repository identities rather than assuming each repository is an isolated AI workspace.

## hmmm

UCNS evidence records currently provide canonical content identity but not cryptographic producer signatures. Signed producer or transport authentication remains unresolved.

Interconnectivity means one repository / one AI is not an adequate operating model. The shared work graph is implemented as an identity and coordination layer while authority remains distributed.
