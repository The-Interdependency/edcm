# EDCM canon — experiment-first UCNS–EDCM boundary

**Status:** pre-canon research program.  
**Authority:** Erin Spencer.  
**Joint surface:** `ucns-edcm`, determined by reproducible experiment rather than unilateral declaration.

## Primary doctrine

EDCM measures response under declared constraint. UCNS supplies candidate structural representations, policies, and measuring instruments for those responses.

Neither repository determines the joint canon alone:

- UCNS structure or proof status does not validate an EDCM readout;
- EDCM empirical fit does not prove a UCNS theorem or make a UCNS candidate canonical;
- the present `edcm.measurement` package is a frozen **baseline candidate**, not the final joint canon;
- a candidate becomes `ucns-edcm` canon only through an explicit evidence-bearing decision packet after development and holdout experiments.

## The loop

The joint construction is intentionally reciprocal:

1. EDCM proposes observable distinctions and falsifiable readout hypotheses.
2. UCNS proposes ways to retain, pair, compare, and measure those distinctions.
3. Experiments test whether a UCNS choice preserves EDCM-relevant differences and whether an EDCM readout survives structural perturbations.
4. Failed candidates remain provenance-bearing evidence.
5. Supported candidates remain candidates until an explicit canon decision.

This reciprocal loop is the intended meaning of **UCNS–EDCM canon**.

## Evidence states

These states may not be collapsed:

1. **Represented evidence** — source material or structure is retained.
2. **Candidate-measured evidence** — a named versioned evaluator produced a readout under declared policies.
3. **Experiment-supported evidence** — the candidate passed declared development and holdout relations.
4. **Canonically measured evidence** — a separate authority decision selected the candidate and recorded alternatives, losses, and rollback.

The repository currently permits states 1–3. State 4 does not yet exist for the joint surface.

## First experiment dimensions

The initial program pressures four load-bearing distinctions:

- **order:** identical turns in different sequence;
- **multiplicity:** one occurrence versus repeated occurrence;
- **constraint pressure:** low-pressure versus high-pressure prompts;
- **resolution timing:** resolution after refusal versus refusal after apparent resolution.

These dimensions are selected because sequence-, set-, and multiset-based UCNS policies make different predictions about whether EDCM readouts should remain invariant.

## Baseline candidate

The maintained `edcm.measurement` implementation remains frozen as:

```text
candidate: edcm-measurement-v1
source: The-Interdependency/edcm:edcm/measurement
standing: historical maintained baseline, not joint canon
```

Its marker canon, parser, eleven-component round vector, and circuit recurrence remain available for comparison. Existing integrity gates preserve its identity; they do not confer empirical validity.

## Experiment rules

Every joint experiment must record:

- exact EDCM and UCNS commits;
- corpus and partition identities;
- source transcripts without normalization loss;
- candidate code references and versions;
- event-to-cell support policy;
- structural policy and comparison policy;
- expected relation and falsifier;
- observed outputs, errors, and disagreements;
- whether evidence is development, holdout, or external;
- no canonical winner unless separately authorized.

Hypothesis failure is a valid experiment result and must not be converted into a build failure merely to preserve a preferred model.

## Non-transfer firewall

The following remain false unless separately established:

```text
ucns_proof_status_implies_edcm_validity = false
edcm_fit_implies_ucns_proof = false
candidate_registration_implies_canon = false
passing_development_fixtures_implies_canon = false
majority_candidate_agreement_implies_truth = false
NA_equals_zero = false
```

## Current implementation boundary

This phase may implement:

- immutable experiment cases and expected relations;
- deterministic EDCM baseline and contrastive candidate readouts;
- explicit event-to-UCNS encoding candidates;
- UCNS equivalence, product-character, and breadth candidate evaluation;
- reproducible reports and policy-preservation findings;
- CI execution against an exact UCNS commit.

This phase may not promote:

- canonical EDCM axes or thresholds;
- canonical event support `mu`;
- canonical structural equivalence;
- canonical product character `M`;
- canonical faithful breadth `B`;
- diagnosis, intention, morality, consciousness, or external truth claims;
- a complete production `UCNSObject` or EDCM deployment contract.

## Usage guidance

Run the joint program only in an environment containing the exact UCNS experiment commit declared by the runner:

```text
python -m edcm.ucns_edcm_experiments --output ucns-edcm-report.json
```

The report is research evidence. It is not a canon file and must not be renamed or imported as one.

## hmmm

External holdout custody, human outcome labels, independent replication, and the authority procedure for the first joint canon selection remain open.
