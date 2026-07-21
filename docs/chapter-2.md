# Chapter 2: Measurement Without Transfer

*Chapter 2 of the distributed Interdependency textbook. Chapter 0 lives in
`metapat/CHAPTER_ZERO.md`; Chapter 1 lives in `ucns/docs/chapter-1.md`. Each
chapter is bound by the license and status vocabulary of the repository that
carries it, and no theorem, proof, or empirical status crosses a chapter
boundary by citation.*

Chapter 1 closed with a promise: the floor was specified, the frame was true,
and the measuring instruments were still owed. This chapter is not the payment
of that debt. The instruments owed to the carrier — μ with its zero-test, M
witnessed distinct from W, an executable B — remain owed to the carrier, in the
carrier's own repository, under the carrier's own laws.

This chapter teaches something prior to any particular instrument: what it
costs to measure honestly at all. The Energy–Dissonance Circuit Model (EDCM) is
a measurement instrument for structure in transcripts — deterministic metrics
over what was actually said, in what order, by whom. Its subject matter is
narrow. Its discipline is not. Every rule in this chapter exists because the
easy alternative was tried somewhere, silently manufactured a result, and had
to be removed.

## 2.1 The Separation of Absences

Chapter 1 separated four zeros: Structural Null, the neutral product character,
algebraic zero, and the absent cell. Measurement inherits the same obligation
in its own jurisdiction, and states it as a single non-negotiable law:

```text
NA != 0
```

A metric that was not measured is not a metric that measured zero. Zero is a
readout — it asserts that the instrument ran and found nothing. `NA` is a typed
absence — it asserts that the instrument did not run, or could not run, or was
never given the evidence it requires. Conflating them converts ignorance into
data.

Absence itself has types. The producer package not being installed is one
absence. The package being installed but its import failing transitively is a
different event, and it stays a *visible failure*, never a quiet fallback. An
empty input, an absent adapter, a missing context, an absent bone inventory —
each remains typed absence or `NA`, each distinguishable from every other, and
none of them ever becomes `0` on the way to a report.

The rule generalizes: an instrument must be able to say "I was not here" in as
many distinct ways as there are distinct ways of not being here.

## 2.2 Authority and the Frozen Canon

Measurement requires a fixed point. If the definitions of the metrics can
drift while measurements accumulate, the accumulated record measures nothing —
each entry was taken with a different instrument wearing the same name.

EDCM therefore freezes its canon. The canonical measurement implementation
lives in one place (`edcm/measurement/`), declares itself machine-readably as
the authority, and pins its frozen canon data — versioned JSON whose exact
bytes are part of the instrument's identity. An integrity gate verifies, on
every run that matters, three things:

1. the exact set and content identity of every frozen canon file;
2. the complete authority and compatibility-policy record;
3. that every re-export is the canonical class and not a drifting copy.

Two corollaries carry the weight. First: an installed sibling package never
silently overrides the canonical implementation. Provenance is recorded;
authority is not transferred by import order. Second: a legitimate change to
canon is a *new version with a migration record*, never an edit to the pinned
identity. Updating a pinned digest to make a gate pass is not maintenance; it
is the destruction of the fixed point the gate exists to protect.

## 2.3 Compartments of Evidence

A measurement result is not one number. It is a record with compartments, and
the compartments do not leak into one another:

- **source evidence** — what was measured: reference, digest, size;
- **semantic constraints** — what an upstream semantic authority stated,
  preserved exactly: statements, references, permitted interpretations,
  unresolved `hmmm`, provenance digest;
- **geometry identity** — which upstream geometric object, under which
  producer schema, resolved to which stable identity;
- **attached status evidence** — certifications and theorem statuses that
  upstream producers actually issued;
- **policy manifest** — which measurement policy governed the run;
- **readouts** — what the instrument itself computed.

The compartment law: a semantic label never becomes a measured value merely by
being named. A statement of constraint from an upstream authority is carried
*as a statement*, with its provenance, into the result — it is never converted
into a metric. Conversely, a readout never promotes itself into a claim about
the semantics it was computed over.

Ordering is itself evidence. Ordered windows compose by explicit sequential
append; testimony-bearing order is never averaged, because an average of an
ordered record is a statement about a record that does not exist.

## 2.4 The Proof-Transfer Firewall

The strongest discipline in this chapter is a refusal. Every view EDCM holds
of upstream evidence carries three permanent flags:

```text
theorem_status_transfer = false
measurement_validity_claim = false
proof_status_transfers_to_measurement_validity = false
```

An upstream algebra may certify a result within its own defended domain. That
certification, attached to an EDCM result, remains exactly what it is:
attached evidence, content-addressed, provenance-bearing — and inert. It does
not make the measurement more valid. It does not promote a readout into a
theorem. Equality of upstream objects does not imply equivalence of
measurements taken over them. Naming a framework term transfers none of that
framework's status.

The firewall runs in both directions. EDCM's determinism is also not exported
upward: a deterministic transcript metric establishes no diagnosis, no intent,
no consciousness, no external truth, and no root ontology. The instrument
reads structure in text. Everything beyond that is somebody else's claim, made
in somebody else's jurisdiction, on somebody else's evidence.

## 2.5 Fail-Closed Consumption

EDCM owns consumer adapters, never producer schemas. The adapter consumes only
the surfaces a producer actually publishes — its envelope types, its schema
identifiers, its own constructors — and accepts input through mutually
exclusive keys, so a caller can never smuggle the same object in twice under
two descriptions.

Everything unexpected fails closed and fails visibly: unsupported schemas,
unknown fields, coerced records, wrong object types, invalid digests, evidence
whose identity does not bind to the geometry it claims to describe. Package
availability alone attaches nothing — the presence of a producer on the import
path is not evidence, any more than the presence of a thermometer in the room
is a temperature.

When a producer withdraws its public root — as happens, and has happened —
the consumer does not pin an archived version and pretend continuity.
Surface-name compatibility is not object-definition compatibility. The typed
absence machinery of §2.1 is exactly what makes withdrawal survivable: the
instrument keeps running, and every result honestly reports which evidence was
not there.

## 2.6 Identity and Epochs

Every supported result binds two identities.

**Epoch identity** binds what governs measurement: the canon versions, the
producer geometry, the policy manifest, the implementation selection. Rotating
canon or policy creates a *new epoch*; it never mutates the identity of
historical results. History is append-only because the alternative — history
that retroactively agrees with the present — is not history.

**Result identity** additionally binds what this particular run saw: the
source evidence, the readouts, the attachment states, the status evidence.
Attached evidence changes result identity without changing epoch identity,
because status evidence is attached, not readout-governing. The two identities
answer two different questions — *which instrument was this?* and *what did
this run of it observe?* — and keeping them distinct is what makes either
answer meaningful.

## 2.7 The Honest Frontier

Some capabilities are named, specified, and not yet operational: gates whose
falsifiers and tests do not exist yet. The discipline here is the bluntest in
the chapter: they raise `NotImplementedError`.

Not a constant. Not a heuristic. Not a language-model judgment standing in for
a measurement. Not a decorative number chosen to make a dashboard populate. A
frontier gate that returns a value before its falsifier exists has not been
implemented early — it has been faked, and every result downstream of it is
contaminated in a way no integrity gate can later detect. The unresolved is
marked `hmmm` and left visibly unresolved, because in this textbook an honest
gap is a load-bearing object and a guessed answer is a defect.

## 2.8 What Was Removed

Chapter 1 earned its geometry by subtraction, and so does this chapter. The
removed temptations are worth naming, because each reads as a convenience and
functions as a leak: the default value that turns absence into zero; the
import-order override that turns installation into authority; the silent
fallback that turns a broken producer into a quiet one; the label-to-value
shortcut that turns semantics into numbers; the borrowed theorem that turns a
neighbor's proof into one's own validity; the pinned-identity edit that turns
a failing gate into a passing one; the placeholder constant that turns a
frontier into a feature.

What remains after the removals is an instrument that can be trusted precisely
as far as it claims and no further — deterministic where it runs, typed where
it is absent, sealed against inheritance in both directions.

**hmmm — the discipline is closed but the frontier is not: contact
convergence, DA-geometry correlation, cadence admission from text, and
semantic-label-to-operating-state inference remain non-operational until their
named falsifiers and tests exist; cryptographically signed producer
authentication is still absent, so evidence digests establish content
identity, not who produced the content; and the upstream carrier's own
instruments — the ones Chapter 1 still owes — cannot be discharged from here,
because the whole point of this chapter is that nobody's debts transfer.**
