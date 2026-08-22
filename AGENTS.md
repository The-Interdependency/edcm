name: edcm
description: |
  Energy–Dissonance Circuit Model research, text-gonol construction, and measurement repository. Preserve the frozen maintained baseline as a candidate, keep METAPAT affixiation semantics / UCNS geometry / EDCM text construction distinct, run the exact UCNS–EDCM experiment graph, and never transfer proof, empirical validity, or canon status across repository boundaries.

# === LLMS ===
# id: edcm_agent_overview
#   content: EDCM has a frozen maintained measurement baseline, an experiment-first UCNS–EDCM research surface, and the active text-domain gonol construction boundary. METAPAT owns affixiation semantics; UCNS owns gonol/Möbius/Public Gonol geometry and geometrically established operations; EDCM owns text-domain admission and linguistic/semantic gonol construction, including the rule that every admitted character is a gonol. Construction does not activate measurement. The baseline is candidate edcm-measurement-v1, not automatic joint canon. Preserve NA != 0 and all semantic/geometry/construction/measurement non-transfer boundaries.
#
# id: edcm_agent_usage
#   content: Read CANON.md, docs/GONOL_LANGUAGE_BOUNDARY.md, .agents/skills/gonol-build/SKILL.md, README.md, docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md, CLAUDE.md, and the applicable organization skills before editing. For text-gonol work start in EDCM, consume current METAPAT affixiation invariants and current UCNS geometry, keep unresolved geometric operations hmmm, and independently replay claimed completed constructions. For joint measurements freeze the EDCM projection and falsifier separately.
# === END LLMS ===

# EDCM agent entrypoint

## Read first

1. `CANON.md`
2. `docs/GONOL_LANGUAGE_BOUNDARY.md`
3. `.agents/skills/gonol-build/SKILL.md` for gonol, character, word, definition, recursive-relation, or affixiation work
4. `README.md`
5. `docs/UCNS_EDCM_EXPERIMENT_PROGRAM.md`
6. `CLAUDE.md`
7. `.agents/skills/the-interdependency/SKILL.md`
8. `.agents/skills/msdmd/SKILL.md`
9. `.agents/skills/meta-module-build/SKILL.md`
10. `.agents/skills/test-build/SKILL.md`
11. `.agents/skills/canon/SKILL.md`
12. `.agents/skills/interdependent-work-graph/SKILL.md` for cross-repository work
13. `docs/integrity-gates.md`
14. the exact historical UCNS source named by a historical experiment when replaying it
15. the source module's `MODULE_BUILD` block and its named tests

## Authority boundaries

```text
METAPAT affixiation semantics: The-Interdependency/metapat at the current governing commit
UCNS gonol geometry:          The-Interdependency/ucns at the current governing or experiment-pinned commit
EDCM text construction:       The-Interdependency/edcm current canon/profile
EDCM baseline measurement:    The-Interdependency/edcm:edcm/measurement
organization skills:          The-Interdependency/skill-lib@fb3b53a7629f7f03ecf255167d52c13abef1a979
experiment evidence:          exact report, corpus, candidate, and workflow identities
```

Repository boundaries are authority and provenance boundaries, not isolated-agent boundaries.

For active EDCM text construction:

```text
every admitted character is a gonol
```

EDCM owns the character-admission profile and linguistic/semantic construction. UCNS owns the geometry used to realize admitted gonols. METAPAT owns the meaning of affixiation. Do not move either semantic authority into UCNS merely because UCNS supplies the carrier.

## Current status

- `edcm/measurement/` is the frozen maintained baseline candidate.
- `edcm.ucns_edcm_experiments` is the first joint experiment runner.
- EDCM owns current text-domain gonol admission and construction; measurement remains separately frozen and evaluated.
- `edcm.character_word`, `edcm.definition_gonol`, and `edcm.recursive_gonol` are the implemented candidates for `characters -> words -> definitions -> recursive gonol relations`. None is selected canon.
- UCNS structural policies, product-character candidates, faithful-breadth candidates, and unresolved Möbius coupling laws remain noncanonical unless current UCNS authority says otherwise.
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

Historical runners use the exact UCNS commit they declare; do not silently repin historical evidence to current UCNS.

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
- every admitted character is a gonol for active EDCM text construction.
- METAPAT defines affixiation; EDCM applies it; UCNS realizes its geometry where constructed.
- represented evidence != constructed representation != candidate-measured evidence != experiment-supported evidence != canonically measured evidence.
- UCNS proof or theorem status does not validate EDCM readouts.
- EDCM empirical fit does not prove UCNS mathematics.
- METAPAT labels are authority constraints, not calculated EDCM values.
- package availability alone attaches no evidence.
- unresolved UCNS geometric operation remains `hmmm`; do not infer it from Unicode names, dictionary definitions, glyph shape, adjacency, or conventional grammar.
- no structural policy, support assignment, comparison policy, EDCM axis, `M`, or `B` becomes canonical by registration, majority, convenience, or development-fixture success.
- exact turn order, multiplicity, sidedness, source bytes, candidate identity, and information loss must remain recoverable.
- transcript-derived claims may not be expanded into diagnosis, intention, morality, consciousness, or external truth.
- new EDCM-native modules require accurate `MODULE_BUILD` metadata, usage guidance, and real test references.

## Usage guidance

For new text-gonol construction, begin in EDCM. Resolve the exact EDCM source/admission profile, import METAPAT affixiation invariants without redefining them, consume current UCNS geometry, construct `characters -> words` with `edcm.character_word`, definition gonols with `edcm.definition_gonol`, and recursive relations with `edcm.recursive_gonol`. Replay independently before claiming completion. Freeze any EDCM measurement only after construction and keep its evidence status separate.

For historical experiments, reproduce the exact historical producer epoch and names. Historical UCNS-owned lexical artifacts remain evidence; they do not restore current language authority to UCNS.

## hmmm

The exact character-admission unit remains profile-specific where not selected. The source-supported complete English morphology law, the exact UCNS Möbius-carrier affixiation/coupling law, direct distant-scale coupling geometry, EDCM measurement projection for recursive text gonols, external holdout custody, independent replication, human outcome-label authority, signed producer records, and the procedure for the first UCNS–EDCM canon decision remain unresolved.
