# Interconnectivity and the shared work graph

Date: 2026-07-15

## Operating rule

```text
repository boundary != agent boundary
repository boundary == authority and provenance boundary
```

One repository / one AI is not an adequate operating model for The Interdependency stack. EDCM work commonly depends on several independently governed surfaces at once:

- METAPAT supplies semantic authority;
- UCNS supplies mathematical representation and its own evidence status;
- EDCM supplies measurement, projection, and result contracts;
- skill-lib supplies reusable build and evidence discipline;
- external corpora supply bounded source evidence.

An agent may coordinate work across that complete graph. It may not collapse the graph by copying another repository's authority into EDCM, treating dependency availability as evidence, or transferring theorem, semantic, or measurement status between domains.

## Stack-manifest contract

Cross-repository runs emit `the-interdependency.stack-manifest` version `1.0.0`.

The manifest records:

- every participating repository or evidence source;
- the exact commit consumed from each;
- the authority held by each participant;
- the participant's relation to the run;
- explicit authority, proof-status, and measurement-status non-transfer boundaries;
- the semantic mapping mode;
- unresolved `hmmm` constraints;
- a deterministic SHA-256 identity over the work graph.

The manifest is written before artifact sealing so its bytes are included in the generated artifact inventory.

## Coordination without centralization

The work graph coordinates identity and execution. It does not create a new central authority.

```text
METAPAT meaning       remains METAPAT meaning.
UCNS proof evidence   remains UCNS proof evidence.
EDCM measured output  remains EDCM measured output.
skill-lib doctrine    remains skill-lib doctrine.
source evidence       remains source evidence.
```

A consuming repository may retain and cite these identities. It may not inherit their claim status merely by naming or importing them.

## Agent behavior

Before changing an interconnected surface, an agent must:

1. identify all participating repositories and evidence sources;
2. resolve their exact commits rather than moving branch names;
3. state which authority each participant owns;
4. preserve unresolved boundaries as `hmmm`;
5. validate the complete graph, not only the repository currently open;
6. produce one shared evidence record that later agents can consume without repeating or guessing the work.

This allows one agent to follow the actual problem across repositories while allowing several agents to cooperate through the same deterministic record.

## Current OEWN application

The Open English WordNet 2025 embedding run binds:

- the EDCM artifact-producing commit;
- the exact OEWN 2025 source commit;
- the pinned skill-lib commit;
- the UCNS producer commit pinned by EDCM;
- the METAPAT producer commit pinned by EDCM.

Its stack manifest accompanies source attribution, corpus summaries, metadata-bearing inventories, intrinsic gonol lists, and direct/generated comparison records.

## hmmm

Content identity is not yet cryptographic producer authentication. Signed producer records or authenticated transport remain unresolved.

The long-term organization-wide location for live shared work graphs remains unresolved. The artifact-local manifest is the first executable coordination surface, not the final user interface.
