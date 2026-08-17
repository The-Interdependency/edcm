# Interdependent work graph — portfolio plan projection

This is the machine-reachable portfolio projection for the existing `interdependent-work-graph` skill.

## Contract

Each participating repository remains self-contained and authoritative for its own canon, implementation, evidence, status, and unresolved boundaries. It publishes exactly one repo-owned report at the conventional path:

```text
docs/work-graphs/repository-plan-report.json
```

The report validates against:

```text
interdependent-work-graph/repository-plan-report.schema.json
schema:   the-interdependency.repository-plan-report
version:  1.0.0
blob SHA: 9b347b2dff7692054b571602f30ee6d00c2e7265
```

The Git blob SHA pins the exact schema bytes independently of branch names or eventual PR merge strategy. The report's cited `source.commit` separately identifies the repository state being described. The commit which adds or refreshes a report is coordination metadata and does not silently become mathematical, semantic, empirical, measurement, runtime, or theorem evidence.

## Authority rule

```text
repo owns claim + evidence + status
skill-lib owns reporting contract + deterministic projection
portfolio plan owns no repo canon
```

Aggregation never transfers authority. It never upgrades candidate status, proof status, measurement validity, empirical validity, semantic validity, deployment authority, or permissions.

## Machine use

From a workspace containing checked-out repository reports:

```bash
python interdependent-work-graph/portfolio_plan.py \
  ../a0/docs/work-graphs/repository-plan-report.json \
  ../edcm/docs/work-graphs/repository-plan-report.json \
  ../metapat/docs/work-graphs/repository-plan-report.json \
  ../ucns/docs/work-graphs/repository-plan-report.json \
  ../zfae/docs/work-graphs/repository-plan-report.json \
  docs/work-graphs/repository-plan-report.json \
  --output portfolio-plan.json
```

The derived output shape is declared at:

```text
interdependent-work-graph/portfolio-plan.schema.json
schema:  the-interdependency.portfolio-plan
version: 1.0.0
```

The aggregator uses only the Python standard library. It validates the frozen contract identity, rejects duplicate repositories and authority transfer, sorts reports by repository identity, content-addresses every input report, and emits:

- source identities;
- repo authority and portfolio roles;
- delivered surfaces;
- cross-repository dependencies;
- active frontier;
- next actions;
- blocked work;
- `hmmm`;
- `portfolio_plan_sha256` over the deterministic projected body.

Local checkout paths are deliberately excluded from the projected body and its digest. Identical report content therefore produces identical portfolio identity regardless of where repositories are checked out.

## Staleness

A report is stale when the repository state of interest no longer matches `source.commit`. An aggregator may expose that mismatch if its execution environment can resolve repository HEAD, but it must not rewrite the report or infer what changed. Refreshing a report is a repo-owned operation.

## Missing reports

A portfolio view is complete only for reports actually supplied. A missing repository must not be synthesized from memory, neighboring repositories, package metadata, or a consumer's assumptions. If a known participant lacks a report, record that absence as `hmmm` in the calling workflow.

## Relationship to stack manifests

`repository-plan-report.json` answers:

> What part of the larger effort does this repository own, what has it delivered, and what remains live?

A stack manifest answers:

> Which exact participants and authority boundaries constitute this particular cross-repository work graph?

They are complementary. Neither replaces the other.

## hmmm

- Automatic discovery of organization repositories is deliberately not part of v1; an explicit input set avoids silently treating repository visibility as portfolio membership.
- Cryptographic producer authentication remains separate from content identity.
- A future service may fetch reports directly from GitHub or another registry, but the deterministic local projection remains the reference behavior.
