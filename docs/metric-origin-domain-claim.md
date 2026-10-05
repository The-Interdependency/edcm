# Domain claim — EDCM metric origin

```yaml
surface_form: metric origin
term_id: edcm.measurement.metric-origin
claiming_domain: EDCM measurement
claimed_sense: the source-owned semantic description against which a metric instrument may be constructed; it defines what the instrument is about, not evidence that the measured phenomenon occurred
scope: EDCM semantic-instrument construction and provenance
claim_type: native
authority_source: hmmm — originating operator decision is conversational and lacks an immutable public source identity; this repository change records prospective adoption only
status: provisional
included_uses:
  - metric name and defining words
  - separately recorded declared and implemented measurement rules
  - source provenance for downstream language construction
excluded_uses:
  - observed transcript evidence
  - automatic truth or diagnosis
  - UCNS geometric proof
  - METAPAT semantic transfer
neighboring_terms:
  - metric value
  - marker
  - UCNS origin
  - semantic trajectory
known_collisions:
  - UCNS geometric origin remains separate
  - legacy single-letter O and L carriers are noncanonical identities
effective_version: metric-origin-v0.1
supersedes: metric-origin-v0
resolved_identity_split:
  - O_scope != O_confidence
  - L_load != L_loss != L_resistance
legacy_carrier_targets:
  O: edcm.behavioral.O_scope
  L: edcm.behavioral.L_loss
unresolved:
  - authority provenance for the originating operator declaration
  - lawful observed-construct to semantic-origin projection/distance
```

The circularity firewall is binding:

```text
metric-origin words -> define instrument
observed system      -> supplies evidence
EDCM comparison      -> produces readout
```

Declared metric semantics and implemented proxies are separate fields. A proxy
may measure only part of its semantic origin. The origin words may never be
counted as evidence that their own metric occurred.
