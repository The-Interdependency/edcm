# English lexical floor: EDCM evidence on UCNS representation

Status: `SURVIVED` only after the complete frozen run and independent replay agree. This system represents lexical evidence; it does not prove a linguistic, mathematical, geometric, empirical, or architectural claim.

## Historical-name notice

The file and artifact name are retained because they identify a completed EDCM OEWN evidence run. The stack-level **lexical-floor** premise is now DEPRECATED. This historical name does not define current UCNS lexical architecture and must not be read forward as a fixed-list semantic closure requirement.

Current lexical construction is recorded separately in [`GONOL_LANGUAGE_BOUNDARY.md`](GONOL_LANGUAGE_BOUNDARY.md): UCNS now targets a source-bound dictionary corpus, with a Scrabble dictionary authorized as the replacement source class once exact edition/source custody is pinned.

## Work graph

- `The-Interdependency/skill-lib@6ef2e4c123225f9db20e5230e5894c9c86b42ee6` owns the build/evidence discipline used by this sealed run.
- `globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287` is the licensed OEWN 2025 lexical evidence source.
- `The-Interdependency/ucns@d7c6f51304ed6c32d48badf63132bea6de8af497` owns the exact metadata-free ordered relational producer consumed by this sealed run.
- this EDCM run owns English source ingestion, affix inventory, reversible rendering candidates, decomposition evidence, identity bindings, freezing, and comparison.

No relation transfers semantic authority, proof status, certification, measurement validity, empirical validity, or canon standing. Artifact digests are identities, not producer signatures.

## Reproducible run

Install EDCM with `lexical-floor`, then clone the exact UCNS producer checkout used by this historical EDCM construction. Do **not** substitute a later UCNS head when reproducing the sealed artifacts. The historical package-extra name is retained for replay only.

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

Acquisition checks the exact Git commit and release tag. Ingestion freezes the license, source-tree digest, file and evidence counts. A valid completed branch receipt may be reused with `--resume` only after every manifest-listed file, branch receipt, external binding, intrinsic carrier, producer commit, and producer-module digest is revalidated. Partial or altered state fails closed.

Single construction and comparison outputs remain `UNRESOLVED`. Only the separate two-clean-run seal may record `SURVIVED` after byte identity is observed.

The direct-atomic branch is constructed from whole-word, sense, synset, and OEWN relation evidence without reading molecular output. The molecular branch is independently constructed from the materialized surface set, versioned EDCM affix inventory, reversible transformation rules, roots, explicit compounds, and every admitted immediate decomposition. Neither branch derives from the other. Both intrinsic carriers and their external identity bindings are frozen before comparison.

Intrinsic `*.ucns.json` files contain only dense integer occurrence addresses, ordered directed typed integer relations, schema identity, and false transfer flags. English strings and provenance live in sibling `*.binding.json` files.

## Current gonol interpretation boundary

This sealed run does **not** define the current lexical basis.

The current upstream direction is:

```text
Unicode character gonols
        ↓
dictionary lexical entries / words
        ↓
word gonols
        ↓
source-bound dictionary definitions and senses
        ↓
ordered semantic relationships among word gonols
        ↓
definition gonols = first lexical deep-recursion layer
```

The former rule requiring definitions to close over a fixed NGSL word set is deprecated. OEWN definition strings loaded by this historical EDCM run remain source prose and provenance evidence; they are not automatically promoted into the replacement UCNS dictionary-definition-gonol representation.

The current definition-gonol role remains analogous to the semantic-representation role of conventional vector embeddings. This historical run establishes no equivalence, semantic quality, similarity behavior, benchmark advantage, or downstream utility for that representation.

## Evidence interpretation

“Root”, “affix”, “direct-atomic”, and “molecular” name EDCM’s bounded OEWN and inventory-relative evidence senses. They are not universal English construction authority and are not substitutions for current UCNS dictionary-derived word/definition-gonol identities. All matching affix alternatives and explicit marked compounds are retained. Closed-compound analysis and pronunciation remain outside this run.

The comparison preserves agreement and disagreement between independently frozen representations. It establishes neither equivalence nor superiority. Repeated complete runs may claim determinism only when every manifest-listed artifact digest and byte stream agrees.

## Usage guidance

Use this document and its pinned commits only when reproducing or auditing the sealed OEWN relational construction. Do not repin it to current UCNS and do not rewrite its historical artifacts or filenames.

For new lexical-semantic construction, follow current UCNS dictionary-corpus authority rather than this historical lexical-floor run. EDCM becomes a consumer only after UCNS pins the exact dictionary source and emits generalized source-bound definition-gonol receipts; any EDCM mapping must then be separately declared and frozen.

## hmmm

The exact Scrabble dictionary edition/source, machine-readable acquisition, immutable source identity, license/custody/redistribution boundary, and generalized UCNS dictionary-definition-gonol producer remain upstream unresolved. EDCM has not selected the corresponding consumer projection, metric, benchmark, or falsifier. Canonical English morphology, upstream signatures, and phrase/sentence/discourse semantic constructions also remain unresolved; none are manufactured by this sealed OEWN run.
