name: edcm
description: |
  Energy–Dissonance Circuit Model research and measurement repository. Preserve the frozen maintained baseline as a candidate, run the exact UCNS–EDCM experiment graph, and never transfer proof, empirical validity, or canon status across repository boundaries.

# === LLMS ===
# id: edcm_agent_overview
#   content: EDCM now has a frozen maintained baseline and an experiment-first UCNS–EDCM research surface. The baseline is candidate edcm-measurement-v1, not automatic joint canon. Joint canon may be selected only through reproducible development and holdout experiments with exact EDCM/UCNS identities, declared structural and comparison policies, preserved falsifiers, information-loss records, and a separate decision packet. Preserve NA != 0 and all proof/measurement non-transfer boundaries.
#
# id: edcm_agent_usage
#   content: Read CANON.md, README.md, docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md, CLAUDE.md, .agents/skills/the-interdependency/SKILL.md, and .agents/skills/meta-module-build/SKILL.md before editing. For joint experiments install the exact UCNS commit declared by edcm.ucns_edcm_experiments, run tests/test_ucns_edcm_experiments.py, run the experiment twice, require byte-identical reports, and retain supported, falsified, and errored hypotheses without appointing a winner.
# === END LLMS ===

# EDCM agent entrypoint

## Read first

1. `CANON.md`
2. `README.md`
3. `docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md`
4. `CLAUDE.md`
5. `.agents/skills/the-interdependency/SKILL.md`
6. `.agents/skills/msdmd/SKILL.md`
7. `.agents/skills/meta-module-build/SKILL.md`
8. `.agents/skills/test-build/SKILL.md`
9. `.agents/skills/canon/SKILL.md`
10. `.agents/skills/interdependent-work-graph/SKILL.md` for cross-repository work
11. `docs/integrity-gates.md`
12. `docs/RETAINED_STRUCTURE.md` in the pinned UCNS checkout when working on joint structure
13. the source module's `MODULE_BUILD` block and its named tests

## Authority boundaries

```text
EDCM baseline implementation: The-Interdependency/edcm:edcm/measurement
UCNS research instruments:    The-Interdependency/ucns at the experiment-pinned commit
semantic authority:           The-Interdependency/metapat when explicitly attached
organization skills:          The-Interdependency/skill-lib
experiment evidence:          exact report, corpus, candidate, and workflow identities
```

Repository boundaries are authority and provenance boundaries, not isolated-agent boundaries.

## Current status

- `edcm/measurement/` is the frozen maintained baseline candidate.
- `edcm.ucns_edcm_experiments` is the first joint experiment runner.
- UCNS structural policies, product-character candidates, and faithful-breadth candidates remain noncanonical.
- EDCM axes, thresholds, marker lists, and circuit parameters remain candidates unless an explicit canon decision says otherwise.
- A passing hypothesis is experiment-supported evidence, not canon.
- A failed hypothesis remains evidence and must not be removed to make the report look successful.

## Required joint experiment validation

```bash
python -m pip install -e .[dev,ucns-experiments]
python tools/check_metadata_contracts.py
python -m pytest -q tests/test_ucns_edcm_experiments.py
python -m edcm.ucns_edcm_experiments --ucns-source-root /path/to/ucns-checkout --output artifacts/ucns-edcm-report.json
python -m edcm.ucns_edcm_experiments --ucns-source-root /path/to/ucns-checkout --output artifacts/ucns-edcm-report-repeat.json
diff -u artifacts/ucns-edcm-report.json artifacts/ucns-edcm-report-repeat.json
```

The dedicated workflow checks out the exact UCNS commit and uploads the report artifact.

## Required baseline validation

```bash
python -m pip install -e .[dev]
python -m edcm.integrity
python -m pytest -q
python tools/check_metadata_contracts.py
python -m build
python -m twine check dist/*
```

## Non-negotiable boundaries

- `NA != 0`.
- represented evidence != candidate-measured evidence != experiment-supported evidence != canonically measured evidence.
- UCNS proof or theorem status does not validate EDCM readouts.
- EDCM empirical fit does not prove UCNS mathematics.
- METAPAT labels are authority constraints, not calculated EDCM values.
- package availability alone attaches no evidence.
- no structural policy, support assignment, comparison policy, EDCM axis, `M`, or `B` becomes canonical by registration, majority, convenience, or development-fixture success.
- exact turn order, multiplicity, sidedness, source bytes, candidate identity, and information loss must remain recoverable.
- transcript-derived claims may not be expanded into diagnosis, intention, morality, consciousness, or external truth.
- new EDCM-native modules require accurate `MODULE_BUILD` metadata, usage guidance, and real test references.

## hmmm

External holdout custody, independent replication, human outcome-label authority, signed producer records, and the procedure for the first UCNS–EDCM canon decision remain unresolved.
