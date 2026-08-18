# English lexical floor: EDCM evidence on UCNS representation

Status: `SURVIVED` only after the complete frozen run and independent replay
agree. This system represents lexical evidence; it does not prove a linguistic,
mathematical, geometric, empirical, or architectural claim.

The file and artifact name are retained because they identify a completed EDCM
OEWN evidence run. They do **not** make this EDCM construction the authority for
the stack's current UCNS lexical floor. The current gonol-native language
boundary is recorded separately in
[`GONOL_LANGUAGE_BOUNDARY.md`](GONOL_LANGUAGE_BOUNDARY.md).

## Work graph

- `The-Interdependency/skill-lib@6ef2e4c123225f9db20e5230e5894c9c86b42ee6`
  owns the build/evidence discipline used by this sealed run.
- `globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`
  is the licensed OEWN 2025 lexical evidence source.
- `The-Interdependency/ucns@d7c6f51304ed6c32d48badf63132bea6de8af497`
  owns the exact metadata-free ordered relational producer consumed by this
  sealed run.
- this EDCM run owns English source ingestion, affix inventory, reversible
  rendering candidates, decomposition evidence, identity bindings, freezing,
  and comparison.

For current architecture rather than reproduction of this run,
`The-Interdependency/ucns@d54c3b6b4d9867f7bc6b968e0424d702504b8497`
records the later lexical-floor closure boundary: Unicode character gonols are
the primitive inscription objects; fixed floor word gonols form the admitted
lexical floor; floor definitions may use only members of that floor; and the
resulting semantic objects are floor-definition gonols. That later declaration
does not rewrite this run or upgrade its evidence.

No relation transfers semantic authority, proof status, certification,
measurement validity, empirical validity, or canon standing. Artifact digests
are identities, not producer signatures.

## Reproducible run

Install EDCM with `lexical-floor`, then clone the exact UCNS producer checkout
used by this historical EDCM construction. Do **not** substitute the later UCNS
head when reproducing the sealed artifacts. The builder reads and freshly
compiles the verified committed producer bytes; the checkout does not need to
be installed into the environment:

```bash
python -m pip install -e '.[lexical-floor]'
git clone https://github.com/The-Interdependency/ucns.git /path/to/ucns-at-d7c6f513
git -C /path/to/ucns-at-d7c6f513 checkout --detach \
  d7c6f51304ed6c32d48badf63132bea6de8af497
```

The builder can acquire the exact OEWN checkout into a persistent cache:

```bash
python tools/build_oewn2025_embeddings.py \
  --source-repo /path/to/cache/oewn-2025 \
  --ucns-source-root /path/to/ucns-at-d7c6f513 \
  --output /path/to/oewn2025-lexical-floor \
  --acquire --resume
```

Acquisition checks the exact Git commit and release tag. Ingestion freezes the
license, source-tree digest, file and evidence counts. A valid completed branch
receipt may be reused with `--resume` only after every manifest-listed file,
branch receipt, external binding, intrinsic carrier, producer commit, and
producer-module digest is revalidated. Partial or altered state fails closed.

Single construction and comparison outputs remain `UNRESOLVED`. Only the
separate two-clean-run seal may record `SURVIVED` after byte identity is
observed.

The direct-atomic branch is constructed from whole-word, sense, synset, and
OEWN relation evidence without reading molecular output. The molecular branch
is independently constructed from the materialized surface set, versioned EDCM
affix inventory, reversible transformation rules, roots, explicit compounds,
and every admitted immediate decomposition. Neither branch derives from the
other. Both intrinsic carriers and their external identity bindings are frozen
before comparison.

Intrinsic `*.ucns.json` files contain only dense integer occurrence addresses,
ordered directed typed integer relations, schema identity, and false transfer
flags. English strings and provenance live in sibling `*.binding.json` files.

## Gonol interpretation boundary

The current stack language path is:

```text
Unicode character gonols
        ↓
fixed floor word gonols
        ↓
complete lexical floor F
        ↓
definitions expressed only with members of F
        ↓
floor-definition gonols
```

This EDCM OEWN run does not implement that complete semantic construction.
In particular, OEWN definition strings loaded by EDCM are **source prose and
provenance evidence**. Arbitrary definition text is not thereby a
floor-definition gonol.

For a future floor-definition gonol, the upstream closure condition is:

```text
support(definition_gonol(word, sense)) ⊆ F
```

A proposed definition that requires an out-of-floor word must fail as a floor
definition rather than silently expanding `F`. No tokenizer, token ID, subword
piece, or opaque external vector lookup may be inserted to bypass that closure.

The intended definition-gonol role is analogous to the semantic-representation
role of a conventional vector embedding. This run establishes no equivalence,
semantic quality, similarity behavior, benchmark advantage, or downstream
utility for that representation.

## Evidence interpretation

“Root”, “affix”, “direct-atomic”, and “molecular” name EDCM’s bounded OEWN and
inventory-relative evidence senses. They are not universal English
construction authority and are not substitutions for UCNS floor-gonol
identities. All matching affix alternatives and explicit marked compounds are
retained. Closed-compound analysis and pronunciation remain outside this run.

The comparison preserves agreement and disagreement between independently
frozen representations. It establishes neither equivalence nor superiority.
Repeated complete runs may claim determinism only when every manifest-listed
artifact digest and byte stream agrees.

## Usage guidance

Use this document and its pinned commits when reproducing or auditing the sealed
OEWN relational construction. Do not repin it to current UCNS and do not rewrite
its artifacts to use later terminology.

For new lexical-semantic construction, use the current UCNS lexical-floor and
definition-gonol producer contract instead. EDCM should become a consumer only
after exact source-bound definition-gonol receipts exist and an EDCM mapping is
separately declared and frozen.

## hmmm

The exact UCNS relation/composition law for composing ordered floor-word gonols
into a closed definition gonol remains unresolved upstream, as does the
source/custody procedure for a complete definition set expressible entirely
inside the fixed floor. EDCM has not selected the corresponding consumer
projection, metric, benchmark, or falsifier. Canonical English morphology,
upstream signatures, and phrase/sentence/discourse semantic constructions also
remain unresolved; none are manufactured by this sealed OEWN run.
