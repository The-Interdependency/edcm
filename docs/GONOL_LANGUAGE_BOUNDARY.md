# EDCM gonol language boundary

**Status:** active EDCM text-construction and measurement boundary.  
**Authority split:** METAPAT owns affixiation semantics; UCNS owns gonol/Möbius/Public Gonol geometry; EDCM owns text-domain admission and linguistic/semantic gonol construction and measurement.  
**Corrected:** 2026-08-21 after UCNS geometry-only canon and skill-lib `gonol-build` authority repair.

## Governing authorities

The current stack separates meaning, geometry, text construction, and measurement:

```text
METAPAT
    affixiation semantics and relational integration invariants
        ↓
UCNS
    gonol geometry, native Möbius/Public Gonol carrier,
    geometrically established operations
        ↓
EDCM
    text-domain admission and linguistic/semantic gonol construction
        ↓
EDCM measurement
    separately declared observations, projections, metrics, and falsifiers
```

Authority does not transfer automatically between these layers.

- METAPAT semantic authority does not prove UCNS geometry.
- UCNS geometry does not choose EDCM text sources, morphology, definitions, or semantic relations.
- EDCM construction does not validate EDCM measurement.
- EDCM measurement does not validate METAPAT or UCNS.

## Character rule

For active EDCM text construction:

```text
every admitted character is a gonol
```

This is an EDCM text-domain rule.

EDCM owns the declared source/profile that determines what is admitted as a character. A profile may select Unicode code points, graphemes, the exact Public Gonol glyph inventory, or another explicitly defined character unit. If that admission unit is not yet selected for a construction, it remains `hmmm`; UCNS does not silently decide it merely because UCNS supplies the geometry.

Every admitted occurrence remains separately addressable. Repeated characters may share gonol identity where the governing construction says they are the same gonol, while occurrence order, multiplicity, source location, and provenance remain preserved.

## Active text construction

Current EDCM text construction uses declared scale option sets rather than a mandatory adjacent-scale ladder. Every admitted character is a gonol, but EDCM must not encode `character -> word -> definition -> recursive` as the only lawful construction path.

Once closed, a gonol is atomic at any scale. Closed gonols may participate directly at any admissible scale without reopening, while identity, order, multiplicity, source positions, relation identity, and provenance remain recoverable.

`edcm.gonol` is the implemented candidate constructor for closing one gonol through a declared scale option set. Its current option sets include character, word, definition, and recursive relation scales. None is selected canon. UCNS coupling geometry remains `hmmm`, and absent `ucns.public_gonol` does not prevent candidate construction.

Relationships that constitute a gonol enter the construction. They are not merely external semantic edges. Sidecars may index, cache, project, or record provenance; they do not replace intrinsic relational content.

## Affixiation

Affixiation is not defined by EDCM and is not defined by UCNS.

METAPAT defines affixiation as a declared relation among already-bounded participants that preserves their individual addressability, identities, and provenance while the relation may integrate as a higher-scale object-whole. An affixiated whole may participate recursively without erasing its constituents.

UCNS owns any exact geometric realization of that operation. The native Möbius/Public Gonol carrier is the current geometric authority. Where the precise coupling operation has not yet been constructed, it remains `hmmm`; EDCM must not fill the gap with an invented carrier, topology, scale increment, arity rule, containment rule, or coupling law.

EDCM applies affixiation to text-domain gonols. Linguistic prefixes and suffixes are one instance of affixiation; they do not define affixiation.

The complete English root, stem, affix, irregular-transformation, and family law remains unresolved unless source-backed EDCM evidence establishes it. EDCM must not invent decomposition to complete a pipeline.

## Public Gonol function positions

UCNS owns the geometry of the exact 157-position Public Gonol carrier and any function operation that geometry actually establishes.

EDCM may use a Public Gonol position in text construction, but it may not derive the position's operation from Unicode names, dictionary definitions, conventional punctuation grammar, glyph shape, or adjacency. An unresolved operation remains `hmmm`.

When an operation is geometrically authorized, an EDCM construction must preserve the exact function identity, occurrence address, ordered participants, source/profile identity, carrier/construction identity, result identity, and provenance needed for replay.

## No hidden token or vector layer

EDCM must not insert conventional NLP token IDs, subword IDs, opaque embedding vectors, or whole-string hashes as substitutes for gonol identity.

Source prose, dictionary material, corpora, labels, and annotations may remain evidence and provenance. Their inclusion does not by itself make them gonol semantics. A text-domain relationship becomes authoritative only through an EDCM construction whose source, admission, relation, closure, and replay boundaries are explicit.

## Historical evidence

EDCM contains sealed historical UCNS/OEWN, lexical-floor, word-gonol, token-named, morphology, and other experiments. Preserve them exactly for reproducibility.

Historical names and producer boundaries remain historical evidence. They do not restore the former rule that UCNS owns lexical construction and they do not override current UCNS geometry-only canon or this EDCM text-domain boundary.

When reproducing a sealed experiment, use its exact historical commits and artifacts. When beginning new text construction, use the current authority split above.

## EDCM measurement boundary

Construction and measurement remain separate.

EDCM may declare a measurement projection over constructed gonols only when the projection, information loss, metric, aggregation, baseline, partitioning, stopping rules, and falsifiers are explicitly frozen as required by the governing experiment.

A reproducible text-gonol construction establishes only that construction. It does not establish semantic quality, compression advantage, reconstruction quality, embedding equivalence, cognition, consciousness, or measurement validity.

## Evidence and replay requirements

A completed text-gonol construction must bind the material identities that determine it, including as applicable:

1. current METAPAT affixiation authority;
2. current UCNS geometric authority;
3. exact EDCM construction code/profile;
4. exact source artifacts and admission rules;
5. participant identity, occurrence, order, multiplicity, relation identity, scale, and provenance;
6. closure and atomic-participation boundaries;
7. unresolved state and information loss;
8. a deterministic construction receipt; and
9. independent complete reconstruction or replay when completion is claimed.

Preflight real resource requirements before a complete run. Once a healthy admitted run begins, let it reach its natural terminal condition unless a genuine external resource/safety boundary or preregistered load-bearing stopping rule fires.

## Usage guidance

Copy-pasteable unified candidate:

```python
from edcm.gonol import construct_gonol, replay_gonol

word = construct_gonol(scale="word", source="cut", source_id="example:cut")
definition = construct_gonol(
    scale="definition",
    relation="example:definition-evidence",
    source="to divide with a sharp edge",
    participants=(word.gonol,),
    source_id="example:cut#1",
)
recursive = construct_gonol(
    scale="recursive",
    relation="example:mentions",
    participants=(word.gonol, definition.gonol),
    source_id="example:relation#1",
)
assert recursive.receipt_digest == replay_gonol(
    scale="recursive",
    relation="example:mentions",
    participants=(word.gonol, definition.gonol),
    source_id="example:relation#1",
).receipt_digest
```

If `ucns.public_gonol` is normally importable and its digest matches the pinned Public Gonol identity, `edcm.gonol` observes source-unit positions. If it is absent, construction records geometry as `hmmm` and still closes the candidate. It does not mutate `sys.path`.

For new text-gonol work:

1. start in EDCM;
2. resolve the exact EDCM source/admission profile;
3. import current METAPAT affixiation invariants rather than redefining them;
4. consume current UCNS geometry rather than moving text semantics into UCNS;
5. close gonols through declared scale option sets under explicit EDCM receipts; use `edcm.gonol`;
6. keep unresolved UCNS geometric operations as `hmmm`;
7. replay the complete declared construction before claiming completion; and
8. freeze any later EDCM measurement separately.

For UCNS geometry work, work in UCNS. For changes to the meaning of affixiation, work in METAPAT.

## hmmm

- the exact EDCM character-admission unit for any source/profile that has not yet selected one;
- the source-supported complete English morphology law;
- the exact UCNS Möbius-carrier affixiation/coupling law exposed by implementation;
- which scale option sets and recursive relations, if any, are later selected, and the exact UCNS geometry for those relations;
- executable direct coupling across distant recursive scales;
- the EDCM projection, information-loss accounting, metric, benchmark, and falsifier for recursive text-gonol evaluation.
