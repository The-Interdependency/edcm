# Fail-closed METAPAT authorization lint for UCNS payload forks

## Authority split

A UCNS payload records recursive structure. It does not, by itself, say that its children are simultaneous constitutive parts of one semantic parent.

The integration boundary is:

```text
METAPAT  authorizes constitutive meaning
UCNS     owns exact recursive payload geometry and stable hashes
EDCM     verifies the producer authorization against the encoded topology
```

No UCNS theorem status or METAPAT ontology status transfers into EDCM measurement validity.

## Build one topology binding

Install EDCM's full stack and obtain an actual METAPAT authorization:

```bash
python -m pip install -e ".[dev,full-stack]"
```

```python
import edcm
import metapat

parent = metapat.root_spine_module_envelope()
authorization = metapat.authorize_constitutive_fork(
    parent,
    child_module_ids=("metapat.child.alpha", "metapat.child.beta"),
    source_statement_refs=(parent.source_statement_refs[0],),
)

binding = edcm.build_fork_topology_binding(
    root_ucns_object,
    authorization,
    fork_path=(),
)
```

`fork_path` is a tuple of UCNS cell indices. An empty path selects the root object. Each later index descends through that cell's non-unit payload.

The binding records:

```text
root UCNS stable hash
selected fork-object stable hash
exact fork path
METAPAT parent module id
ordered semantic child module ids
ordered payload-bearing cell indices
ordered actual child UCNS stable hashes
METAPAT authorization digest
METAPAT canon digest
Phi policy version
relation kind = constitutive-simultaneous
unresolved constraints
status-transfer firewalls
binding digest
```

The linter does not infer child module ids from hashes. The integration encoder supplies the semantic order, and the binding makes that choice reviewable and tamper-evident.

## Validate one fork

```python
edcm.lint_fork_topology(
    root_ucns_object,
    envelope=parent,
    authorization=authorization,
    binding=binding,
)
```

Validation calls METAPAT's own producer validator, then recomputes the exact UCNS root hash, selected fork hash, payload indices, and ordered child hashes.

## Require complete recursive coverage

A valid fixture must declare every recursive object that has two or more non-unit payload children:

```python
declaration = edcm.AuthorizedUCNSFork(
    envelope=parent,
    authorization=authorization,
    binding=binding,
)

report = edcm.lint_all_payload_forks(
    root_ucns_object,
    declarations=(declaration,),
)
```

The complete lint fails closed for:

- a missing declaration;
- duplicate declarations for one path;
- a declaration for a path that is not an actual fork;
- child-order, cell-index, or stable-hash drift;
- parent, canon, policy-version, or authorization-digest drift;
- malformed, unknown, coerced, or tampered binding fields;
- a cyclic or non-UCNS payload graph;
- direct absence of a required full-stack package.

A single non-unit payload is not silently promoted into a fork. It remains ordinary recursive geometry and acquires no constitutive meaning from this linter.

## Negative relations

Temporal succession, adjacency, provenance, alternatives, fiq connectivity, arbitrary graph association, and external symmetry action remain external relation surfaces. The binding schema has no external-edge field, and unknown fields fail closed. The only accepted relation kind comes from the METAPAT producer and is exactly:

```text
constitutive-simultaneous
```

## Serialization

`UCNSForkTopologyBinding.to_json()` emits canonical JSON. `from_json()` and `from_dict()` reject unknown, missing, wrongly typed, reordered, or digest-inconsistent fields.

The resulting `UCNSForkLintReport` is evidence that the supplied fixture passed the declared integration contract at one exact root hash. It is not a proof of METAPAT canon truth, UCNS theorem status, EDCM metric validity, intent, consciousness, or external factual correctness.

## hmmm

The first production fixture remains to be chosen. Until its parent semantics, ordered child modules, actual UCNS object, and all recursive fork declarations are supplied together, the honest result is not “approximately authorized”; it is no accepted fixture.
