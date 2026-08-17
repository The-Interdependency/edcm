# English lexical floor: EDCM evidence on UCNS representation

Status: `SURVIVED` only after the complete frozen run and independent replay
agree. This system represents lexical evidence; it does not prove a linguistic,
mathematical, geometric, empirical, or architectural claim.

## Work graph

- `The-Interdependency/skill-lib@6ef2e4c123225f9db20e5230e5894c9c86b42ee6`
  owns build, evidence, claim, and cross-repository work discipline.
- `globalwordnet/english-wordnet@dc343f2683279ecbb13fab4e2fd778d7b162d287`
  is the licensed OEWN 2025 lexical evidence source.
- `The-Interdependency/ucns@d7c6f51304ed6c32d48badf63132bea6de8af497`
  owns the metadata-free ordered relational representation.
- this EDCM commit owns English source ingestion, affix inventory, reversible
  rendering candidates, decomposition evidence, identity bindings, freezing,
  and comparison.

No relation transfers semantic authority, proof status, certification,
measurement validity, empirical validity, or canon standing. Artifact digests
are identities, not producer signatures.

## Reproducible run

Install EDCM with `lexical-floor`, then clone the exact UCNS producer checkout.
The builder reads and freshly compiles the verified committed producer bytes;
the checkout does not need to be installed into the environment:

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

## Evidence interpretation

“Root”, “affix”, “direct-atomic”, and “molecular” name EDCM’s bounded OEWN and
inventory-relative evidence senses. They are not universal English
construction authority. All matching affix alternatives and explicit marked
compounds are retained. Closed-compound analysis and pronunciation remain
outside this floor.

The comparison preserves agreement and disagreement between independently
frozen representations. It establishes neither equivalence nor superiority.
Repeated complete runs may claim determinism only when every manifest-listed
artifact digest and byte stream agrees.

hmmm: UCNS geometric assignment, higher-gonol composition, canonical English
morphology, upstream signatures, and phrase/sentence/discourse semantics remain
unresolved and are not manufactured by this lexical floor.
