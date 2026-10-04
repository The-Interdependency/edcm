# Domain claim — EDCM metric origin

```yaml
surface_form: metric origin
term_id: edcm.measurement.metric-origin
claiming_domain: EDCM measurement
claimed_sense: the source-owned semantic description against which a metric instrument may be constructed; it defines what the instrument is about, not evidence that the measured phenomenon occurred
scope: EDCM semantic-instrument construction and provenance
claim_type: native
authority_source: operator declaration, 2026-10-03
status: provisional
included_uses:
  - metric name and defining words
  - formula or rule description
  - source provenance for downstream language construction
excluded_uses:
  - observed transcript evidence
  - automatic truth or diagnosis
  - UCNS geometric proof
  - METAPAT semantic transfer
neighboring_terms:
  - metric value
  - marker
  - origin
  - semantic trajectory
known_collisions:
  - UCNS geometric origin remains separate
effective_version: metric-origin-v0
supersedes: none
unresolved:
  - O naming conflict: Overextension versus Overconfidence
  - L naming conflict: Load versus Coherence Loss
```

The circularity firewall is binding:

```text
metric-origin words -> define instrument
observed system      -> supplies evidence
EDCM comparison      -> produces readout
```

The origin words may never be counted as evidence that their own metric occurred.
