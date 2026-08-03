# EDCM response-tension-release experiment

## Frozen next-experiment packet v0.1.6

| Field | Frozen value |
|---|---|
| Date frozen | `2026-08-03` |
| Design status | **FROZEN** |
| Execution status | **BLOCKED pending signed custody, allocation-audit, and human-label manifests** |
| Schema | `edcm.response-tension-release-experiment/0.1.6` |
| Candidate | `edcm.response-tension-release/0.1.0` |
| Canon selection | `null` |
| Supersedes | Immutable v0.1.5 packet SHA-256 `95d24a3866fddddd97736df33c3b03f08ea4351b55f18dd2ba6a133839b9e8f6` |
| Current-packet index | `docs/experiments/README.md` |

This complete v0.1.6 packet freezes the same single new experiment design and
supersedes v0.1.5 to close six review-raised pre-data degrees of freedom:
source-event identity, duplicate-input representative selection,
booking-domain assignment, allocation-seed verification, score-affecting
runtime identity, and exact development-variance arithmetic. It also closes
the necessary decision-arithmetic, authority-ledger, and custody propagation
exposed while resolving them, plus the successor-facing callable-state and
represented-evidence path boundary exposed by later PR #49 review. It does not
modify any immutable earlier packet,
authorize execution, alter EDCM equations, reopen prior evidence, activate
production, or select a canonical measurement. No earlier packet was executed.
No candidate input, human label, partition membership, event-specific source
row, per-event score, or sealed outcome was viewed between packet versions;
only tracked source schema and code, pull-request metadata, public
documentation, and committed aggregate check evidence were inspected.

This v0.1.6 packet is immutable. Named people, keys, encrypted-bundle digests,
and final runner/container identities must be supplied in separately signed
execution and completion manifests that bind this packet's file digest without
overriding the frozen sections 4.1.1–4.1.3 runtime. Changing any rule in
this packet requires a new packet version and a fresh sealed test.

## 1. Controlling predecessor boundary

The predecessor is [EDCM PR #49](https://github.com/The-Interdependency/edcm/pull/49),
`experiment: seal externally labelled MultiWOZ booking holdout`.

| Identity | Frozen value |
|---|---|
| PR base | `main@28632bd7ca5dc9397793bd66b73f0970dc51e650` |
| PR head after binding-surface repair, with residual review limits below | `ee9dea48b75151353bb56493cfa251fb921eb90d` |
| PR head tree | `101d05a96ebece1f715939980fcfb28635dbac31` |
| Actions synthetic merge | `26486b287a32dedc0348ca16a161445737375c18` |
| Sealed EDCM producer | `c292430771b4dc76734522b580caa2be18ca04f9` |
| Sealed EDCM tree | `04beb8d9c6f01f2ec00bb06e55f77bea21e9b14a` |
| UCNS producer | `a98c9e6c69804a8a08d0786b1d8b450bb2c49a97` |
| MultiWOZ 2.1 archive SHA-256 | `d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e` |
| Sealed report digest | `a726434a533395e7e3bd7d72ba3e9ce68f58c5b62f3b6b10d2b0556b09e85e61` |
| Report file SHA-256 | `4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3` |
| Receipt file SHA-256 | `ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5` |

The predecessor's controlling empirical result is:

- sensitivity `0.469811320754717`, 95% Wilson interval
  `[0.42769111208421506, 0.51236599762268]`; the preregistered sensitivity
  hypothesis was falsified;
- balanced accuracy `0.5211652023620913`, 95% dialogue-cluster interval
  `[0.4656057510819316, 0.5739376739379676]`; the interval spans chance;
- Platt slope `0.019040813646053385`; the old terminal-progress score added
  little movement beyond class prevalence;
- low ten-bin expected calibration error did not repair weak discrimination.

The old candidate, `edcm.maintained-terminal-progress/0.1.0`, used only terminal
progress before the labelled response. Its 661 test events, membership,
per-event labels, per-event scores, errors, and fitted choices are forbidden
inputs to this experiment. The old aggregate result above is a boundary, not
training data.

## 2. Successful-check audit

All three GitHub Actions workflows associated with the PR head completed
successfully, comprising twelve successful jobs:

| Workflow | Verified surface | Material limit |
|---|---|---|
| [UCNS–EDCM joint experiments](https://github.com/The-Interdependency/edcm/actions/runs/30793734390) | Python 3.11/3.12 historical experiment tests and byte-identical v0.1–v0.4 reruns | Historical joint reports; not a raw-corpus rerun of the new holdout |
| [Skill and metadata compliance](https://github.com/The-Interdependency/edcm/actions/runs/30793734489) | Seven pinned skill-lib consumers clean; canonical metadata regeneration matched | Contract and drift evidence only |
| [CI](https://github.com/The-Interdependency/edcm/actions/runs/30793734408) | 254 tests passed with 20 producer-dependent skips on Python 3.11–3.13; integrity, authority boundaries, packaging, Twine, and clean-wheel smoke passed | Raw MultiWOZ bytes and event labels were absent; the sealed evaluation was not independently regenerated |

The checks establish that the synthetic merge is buildable and that committed
hashes, leakage guards, aggregate schemas, status boundaries, and deterministic
machinery are internally consistent. They do not establish hidden external
custody, implementer blindness, independent human outcome validity, raw-corpus
ground truth, useful discrimination, generalization, production readiness, or
measurement validity. Green checks therefore preserve rather than supersede
the falsified sensitivity result and chance-spanning interval.

The repaired PR head fails closed when the loaded EDCM runtime does not match
the recorded checkout, loads one authenticated in-memory canon for all events,
and re-verifies the runtime after canon load and after scoring. It authenticates
the complete current `metrics.compute` call surface, the `RoundMetrics` class
methods, slots, and member descriptors, every compute-to-stats,
compute-to-risk, and risk-to-stats import identity, and the source-export names
and module-global dictionaries. Foreign, same-origin, alias, coordinated-export,
class-method, and slot-descriptor substitutions fail closed. It leaves a
single-run byte-repeat finding
`not-evaluated`; rejects colliding report, receipt, and atomic-temporary paths;
and rejects any such artifact path that aliases the admitted source archive.
Python 3.13's compiler-owned `__firstlineno__` and `__static_attributes__`
metadata are accepted only with their exact non-behavioral types; behavioral
class keys and slot descriptors remain closed.
Those repairs govern future predecessor schema v0.1.1 output. They do not
change the sealed v0.1.0 report or receipt bytes, their metrics, or the
controlling negative interpretation.

Three later review findings remain unresolved on PR #49 despite those green
checks: the future holdout runner does not authenticate its own local scoring/
calibration/evaluation helpers, its mutable output and atomic-temporary paths
can alias two represented-evidence inputs, and an existing callable's
`__code__` can be mutated in place while preserving the metadata and object
identity checked by `ee9dea4`. They do not alter the historical sealed bytes,
but they block treating the future PR #49 runner or its verification routine as
a complete runtime authority. This successor neither resolves those code
threads nor inherits trust from the green status. Section 4.1.1 freezes a
strict superset, completed by sections 4.1.2–4.1.3, for the new external runner:
its own complete callable surface,
callable-code digests, and all represented-evidence/input path identities must
fail closed before any source row is processed.

The historical v0.1.0 producer serialized its repeat finding as `supported`
before a second complete output existed; that producer status was premature.
Two complete commands were later compared externally and their report and
receipt files were byte-identical. This distinction and both historical file
hashes remain visible rather than being rewritten.

## 3. New question

> When the target system response itself is measured, does its one-turn effect
> on maintained EDCM stored tension distinguish independently human-adjudicated
> resolution from non-resolution of one explicit booking request on a fresh,
> externally held test partition?

This is a bounded response-measurement experiment. It is not a forecast of an
unseen response and not a claim about universal dialogue success, satisfaction,
truth, intention, diagnosis, morality, consciousness, or competence.

## 4. Exactly one new candidate

### 4.1 Candidate identity

`edcm.response-tension-release/0.1.0`

The candidate is genuinely distinct from the predecessor:

- the predecessor scored terminal novelty and relative entropy gain before the
  response;
- this candidate includes the target response and measures its immediate
  directional effect on stored tension;
- it adds no learned feature weights, sign search, ensemble, ablation family,
  or alternative candidate;
- it is never executed on the predecessor's test events.

### 4.1.1 Frozen score-affecting runtime

The maintained measurement referent is no longer deferred. The candidate must
load its parser, canon, metric, stats, and risk implementation from the exact
read-only PR #49 snapshot below. Git object IDs are full SHA-1 values over exact
tracked bytes.

| Runtime object | Frozen identity |
|---|---|
| Repository commit / tree | `ee9dea48b75151353bb56493cfa251fb921eb90d` / `101d05a96ebece1f715939980fcfb28635dbac31` |
| `edcm/` tree | `a215ccaf087961bb56a6fb8c5c22966cbd821e43` |
| `edcm/measurement/` controlling tree | `95c53d601bbc610c12e137d16e5a30957c956e46` |
| parser tree / `turns_rounds.py` blob | `8f8f72e626b09f0f2c757c601eb76257acad3b47` / `d6d472f1f9dcd6c6650b5ab8cf008658a0ef9bc0` |
| canon tree / `loader.py` blob | `281ddaa0a2cd74d4c0ea36d48fce05fce3bcd482` / `4fd6d80c18e23e364a36495ba4eb312b98841e36` |
| metrics tree / `compute.py` blob | `9b28e06c553bbf63367a7a1d7b08ee39213ef216` / `eca2e53c51522e43e4d5e63a066ea9b3044a1ba1` |
| `stats.py` / `risk.py` blobs | `e195c129d6f8b40feaed859b17787e3f3433b7c7` / `1018614c9b959f5f5cd5f9962b18e5fc8b7878c0` |
| canon data blobs: affixes / punctuation / words / markers | `68811fc62ffe61022c9db2d325c80b900d501282` / `5cc294c70ebbd7325f07ad67982a9353d0017754` / `422cd3d0aa31ab0b2aac6dcbb982bbe4853e6a19` / `f937fab506c2201159ec90024ea18c898a331066` |
| [Base image, platform manifest](https://hub.docker.com/layers/library/python/3.12.13-bookworm/images/sha256-058149828b8d4a90425f5ae6d255ee1fcfe73bf7d749635d824f4e033460d83c) | `docker.io/library/python:3.12.13-bookworm@sha256:058149828b8d4a90425f5ae6d255ee1fcfe73bf7d749635d824f4e033460d83c`, `linux/amd64` only |
| Interpreter / Unicode database | CPython `3.12.13`, `sys.implementation.cache_tag = cpython-312`, `unicodedata.unidata_version = 15.0.0` |
| Process environment | `LC_ALL=C.UTF-8`, `LANG=C.UTF-8`, `TZ=UTC`, `PYTHONHASHSEED=0`, `PYTHONNOUSERSITE=1`, `PYTHONSAFEPATH=1`; no other environment key whose ASCII-uppercase name begins `PYTHON`; network disabled; no trace/profile hook |

The runtime topology has exactly two code roots. `/opt/edcm-base` is a complete
read-only checkout at the frozen PR #49 commit/tree and is the sole import root
that may provide a top-level `edcm` package. `/opt/experiment` contains exactly
`response_tension_release_runner.py`,
`response_tension_release_allocator.py`, and the independently implemented
`response_tension_release_verifier.py`, with no top-level `edcm` package,
`.pth`, compiled extension, bytecode, or other executable file. The runner
entrypoint is an exact `execve` of `/usr/local/bin/python3.12` with argv
`["/usr/local/bin/python3.12", "-P", "-s", "-S", "-c", runtime_bootstrap]` and no
stdin. `runtime_bootstrap` is the UTF-8 encoding, with LF line endings and a
final LF, of the following text; no semantically equivalent spelling is
allowed:

```python
import sys
sys.path[:0] = ["/opt/experiment", "/opt/edcm-base"]
import response_tension_release_allocator as allocator
import response_tension_release_verifier as verifier
import response_tension_release_runner as runner
runner.main()
```

The independent manifest builder uses the identical first five lines, byte for byte,
and the sole different final line
`verifier.emit_runtime_manifest()`. The allocation-audit process instead uses
this exact UTF-8 bootstrap, again with LF endings and a final LF:

```python
import sys
sys.path[:0] = ["/opt/experiment", "/opt/edcm-base"]
import response_tension_release_verifier as verifier
verifier.emit_allocation_audit_receipt()
```

These are the only three permitted bootstrap strings. Runtime and manifest
build modes load all three external modules under exactly the
module names shown in the import statements in both processes; none is ever
loaded as `__main__`. The runtime runner's module top level may only define
authenticated objects. `runner.main()` must authenticate the signed manifest
before opening a source, label, allocation, or score artifact. A non-Python
custody supervisor authenticates the container, interpreter executable, both
read-only code-root trees, exact argv/bootstrap digest, mounts, and environment
before `execve`; the scored process cannot self-approve its pre-import code.
`-P` prevents unsafe path prepending, `-s` disables the user site, and `-S`
prevents global `site` and executable `.pth` startup while still allowing the
frozen `PYTHONHASHSEED=0` environment variable to take effect. The image contains no
`sitecustomize.py` or `usercustomize.py`, `site` may not later be imported,
`sys.gettrace()` and `sys.getprofile()` must be `None`, and
the monitoring checks below must pass.
Scoring and evidence rendering use one process and one thread with no mutable
plugin, callback, nonstandard import hook, or instrumentation interface. No
installed wheel, editable install, namespace package, zip import, or other
`sys.path` entry may provide `edcm`.

Allocation-audit mode must have both
`response_tension_release_allocator` and `response_tension_release_runner`
absent from `sys.modules` before and after receipt construction; verifier module
source contains no import or dynamic load of either. Its custody supervisor
authenticates its distinct read-only primary-artifact mounts and stdout-only
output topology. Runtime-manifest build mode has no source/label/seed mounts;
allocation-audit mode has no runtime-signing key/HSM handle. The role/mount/FD
mode token and exact bootstrap digest are bound into the corresponding signed
envelope.

The full `edcm/measurement` tree remains the controlling dependency and the
listed blobs are audit anchors. The successor imports no `edcm.corpora` module
and no PR #49 holdout-local archive, Wilson, percentile, digest, report,
receipt, or atomic-write helper. Those small rules are implemented and
authenticated only in `/opt/experiment` from the exact packet formulas and
Python standard library. The only retained references into `/opt/edcm-base`
are the exact `Round`, `parse_transcript`, `CanonLoader`, and `compute_round`
exports and their transitive source-defined call graph in exactly these five
modules:

```text
edcm.measurement.parser.turns_rounds
edcm.measurement.canon.loader
edcm.measurement.metrics.compute
edcm.measurement.metrics.stats
edcm.measurement.metrics.risk
```

After the four exports are captured, no other base binding may be retained and
no later `edcm` import is permitted. The recursively reachable base-module set
starts at those four objects and follows to a fixed point every global binding
named by each function/code object's recursive `co_names`, every function
default/keyword-default/annotation, and every referenced class namespace/
method/attribute; standard-library references terminate traversal. It must
equal those five names; an extra or missing base name fails before source
access. The complete base tree is authenticated before import, so exact package
initialization may load other frozen modules, but none may remain reachable
from the runner or the four retained exports. Experiment code may not modify,
copy-edit, shadow, wheel-install over, monkeypatch, dynamically rebind, or
substitute a loaded object or resource. The final experiment-root commit,
dependency lock, and container digest freeze before any source row or label is
released.

### 4.1.2 Independently signed runtime-state manifest

The runtime manifest is not generated or signed by the execution process. In a
separate hermetic, network-disabled build verification using the exact frozen
container, code roots, environment, entrypoint flags, and no source data, the
named independent allocation verifier acts as runtime-manifest builder, while
a distinct non-Python custody supervisor controls the runtime-attestation
signing service. The scheme, supervisor legal identity, HSM/key-handle identity,
public key, and fingerprint freeze in the pre-data role manifest. The verifier authenticates both code-root trees and the container,
imports all three external modules and the four base exports to completion,
derives the manifest below, and writes exactly its canonical bytes to file
descriptor 1 with no prefix/suffix; stdin is `/dev/null`, stderr is diagnostic
only, and it has no other writable descriptor. The supervisor runs that exact
builder twice in fresh processes, requires byte identity, and only then asks
the custody HSM to sign the frozen payload below. No private key bytes, HSM
device, socket, token, credential, handle, signing environment variable, or
writable signer mount is present in either Python builder or scored runtime.
The supervisor records and signs those absence/topology assertions. Execution may
only verify the resulting read-only manifest and detached envelope; it may not
create, replace, or self-baseline either artifact.

The authenticated source-module inventory is the five exact base modules above
plus the three exact `/opt/experiment` Python files, ordered by module name's
strict UTF-8 bytes. Standard-library and builtin behavior is not silently
trusted or counted as an additional source module: its exact live dependency
surface is recorded separately below. Within each source module, sort the exact
namespace-key set by strict UTF-8 bytes, excluding only `__loader__`,
`__spec__`, and `__cached__`. The `__builtins__` key is excluded from recursive
content encoding only after requiring that it is the exact object
`builtins.__dict__`; the key and that identity relation are recorded. Enumerate
every module-defined Python function and class, and every function underlying a
class function, `staticmethod`, `classmethod`, or property. Class namespace
keys, slots, member/getset descriptors, and all other class attributes are
included.

Every enumerated **source** Python function must have `__closure__ is None`,
`fn.__globals__ is vars(sys.modules[fn.__module__])`, and
`fn.__builtins__ is builtins.__dict__`. Its record includes the stable defining
module relation, the stable builtins relation, module/name/qualname, a
domain-separated SHA-256 of `marshal.dumps(fn.__code__, 4)`, and canonically
encoded `__defaults__`, `__kwdefaults__`, `__annotations__`, and `__dict__`.
Each class record additionally binds `type(cls)`, the ordered `cls.__bases__`,
and the ordered full `cls.__mro__` as stable references. A different globals
dictionary, builtins dictionary, metaclass, base, or MRO fails even if all
names, code bytes, defaults, and class namespace values match.

The exact live builtin/standard-library **call surface** is computed to a fixed
point; container or file hashes are not treated as a substitute for checking
its in-memory entry bindings. Let the callable-code surface begin with every
enumerated source function code object and every nested `types.CodeType` found
recursively in its `co_consts`. It adds only a pure-Python stdlib function that
is the target of a recorded global, import, call, constructor,
constructed-callable, receiver, or protocol
resolution below; merely appearing elsewhere in a reached class/module
namespace does not schedule its body. For each code object in that surface,
`dis.get_instructions(code, adaptive=False, show_caches=False)` is the only
instruction decoder. Every `LOAD_GLOBAL`, `LOAD_NAME`,
`LOAD_FROM_DICT_OR_GLOBALS`, `LOAD_FROM_DICT_OR_DEREF`, `LOAD_BUILD_CLASS`, or
`LOAD_ASSERTION_ERROR` has one global-resolution row. Resolve `LOAD_GLOBAL`
first in the defining module dictionary and then
`builtins.__dict__`. `LOAD_NAME` instead records CPython's exact
locals-mapping, globals, then builtins priority and a finite target allowlist;
absence from every applicable source fails. Dict-or-global/deref rows record
the proven locals-mapping/cell/global source order and a finite exact target
allowlist. `LOAD_BUILD_CLASS` and `LOAD_ASSERTION_ERROR` bind the exact
`builtins.__build_class__` and `builtins.AssertionError` objects. Record opcode,
owner/source, name, and encoded target; a dynamic source outside its signed
allowlist fails.

Every `IMPORT_NAME` or `IMPORT_FROM` in the callable-code surface also has one
signed `import_resolution` row. Packet-local stack dataflow must prove the exact
integer level and tuple-of-strings fromlist loaded for `IMPORT_NAME`; the row
records code path/offset, opcode, requested name, level, fromlist, exact
returned module reference, origin/file digest, and the authenticated
`builtins.__import__` binding. An `IMPORT_FROM` row additionally records its
source module reference, requested key, and exact returned binding. Sort and
preload every resolved stdlib module by requested-name UTF-8 bytes in both clean
builds and runtime before the first manifest snapshot; subsequent local import
opcodes must return those same `sys.modules` objects. `IMPORT_STAR`, a relative
level other than the signed integer, dynamic `importlib`/`__import__` use outside
the frozen bootstraps, a custom finder/loader, an unrecorded import, or any later
`edcm` import fails. Imported modules/bindings join the receiver-specific call
surface; for example, if reached, `Counter.most_common` binds its exact `heapq`
module and `nlargest` target rather than leaving them implicit.

Every `MAKE_FUNCTION` in the callable-code surface has exactly one signed
`ephemeral_function_resolution` row. Stack dataflow must bind the exact nested
stable code path, opcode flags, defaults tuple, keyword-default mapping,
annotations, closure-cell construction provenance, defining module
globals, and `builtins.__dict__`. Its stable construction token is
`ephemeral:<enclosing-stable-code-path>:<instruction-offset-decimal>`. A live
function produced by that instruction is admitted by construction provenance,
not cross-process `is`: it must have the recorded code object, exact metadata,
globals/builtins relations, defaults/annotations, and ordered closure recipe, and may
follow only its signed lifecycle path; it may not enter module/class state or replace a named callable. This is the only
permitted anonymous source/stdlib function mechanism and covers generator
expressions and JSON's nested encoder closures.

An ephemeral closure recipe never contains or hashes a source-derived live
value. For each zero-based free-variable cell it records the exact
`co_freevars` name and a producer proven by bytecode dataflow: either
`{"kind":"local","index":local_index,"name":local_name}` or
`{"kind":"enclosing-cell","index":cell_index,"name":cell_name}`. It also
records a finite value contract: an exact authenticated class/type reference;
or a recursively specified core container contract over `str`, `bytes`, `int`,
`float`, `tuple`, `list`, `dict`, `set`, or `frozenset`. At each
`MAKE_FUNCTION`, packet-local static stack/dataflow analysis of the
authenticated bytecode must prove that CPython will place the recorded producer
into the recorded cell and that the subsequent call consumes that exact
constructed function. The recipe records one or more exact instruction paths
with lifecycle token `immediate-call`, `returned-to-signed-caller`, or
`retained-by-generator-until-exhaustion`; JSON's `_make_iterencode` closure uses
the latter two. Each returned target/caller/generator code path is already in
the callable-code inventory. An unrecorded merge, return, store, or escape fails
contract lint. Two
pre-data synthetic probes with dummy values of each signed type/container
contract must reproduce the function metadata, cell sameness/distinctness, and
producer identity under the pinned interpreter. Event-time tracing,
monitoring, cell inspection, or serialization is forbidden. Runtime assurance
comes from re-authenticating the exact bytecode, closure recipe, interpreter,
and no-hook state before and after scoring, not from observing source-derived
closures. Event-local contents are never compared with clean-build contents or
written to the manifest.

An exact class/type target of an ordinary `CALL` may mint one anonymous
callable result only through a signed `constructed_callable_resolution` row.
No other factory, call opcode, or target kind may mint one. Its stable token is
`constructed-callable:<producer-stable-code-path>:<producer-CALL-offset-decimal>`;
the producer key must identify the existing `call_resolution` row whose target
allowlist has exactly that one class/type. The row repeats the exact constructor
record already bound there, records the exact concrete result-type reference,
and binds the first raw `__call__` function-or-descriptor binding and owner found in that result
type's signed MRO plus its authenticated source/stdlib/builtin/frozen/extension
provider origin and digest. A Python
`__call__` body joins the callable-code surface.

The construction row records every positional and keyword argument in actual
call order. Each `argument_recipe` has its positional index or keyword name,
the exact producer code/offset path proven by packet-local stack dataflow, and
exactly one of: a recursively encoded constant; a named,
receiver-bound, ephemeral-function, or earlier constructed-callable target; or
a source-safe `value_contract` defined below. Constant or callable recipes are
required whenever static dataflow can prove them; a value contract is permitted
only for a live value whose contents are not safe to freeze. The producer path
and authenticated bytecode must prove its call-argument position and every
branch; an unknown producer or unrecorded merge fails.

Its nonempty ordered `lifecycle_paths` use only `immediate-call`,
`stored-local-then-call`, `returned-to-signed-caller`,
`passed-as-signed-call-argument`, or `retained-until-signed-caller-return` and
give every stable code/offset traversed from construction to each use. Every
use must be on exactly one listed path. Module/class/container storage,
serialization, source- or label-derived identity, an unlisted merge or escape,
or survival beyond the final listed use fails contract lint. A later call may
admit the token only when dataflow proves the callable is the same stack/local
value minted at the producer; that call schedules the recorded raw `__call__`
binding. Two clean builds and startup run a source-free synthetic probe for
each construction recipe with constants or dummy values satisfying the signed
recipes and require the exact result type, raw binding, owner, provider, and
callability. No constructed live object or event-time argument value is placed
in the manifest or compared across processes. This rule covers the C
`_json.Encoder` object stored by `JSONEncoder.iterencode`; its markers,
default/encoder, indent, separators, sorting, skipping, and non-finite-number
arguments are all bound by their individual recipes before its later call.

A value contract is exactly one of
`{"kind":"exact-type","type":encoded_type_reference}`;
`{"kind":"sequence","type":encoded_core_container_type_reference,
"item":value_contract}` for list/tuple/set/frozenset;
`{"kind":"mapping","type":encoded_dict_type_reference,
"key":value_contract,"value":value_contract}`; or
`{"kind":"one-of","options":[value_contract,...]}`. One-of options sort by
canonical bytes and are nonempty/unique. Contracts check exact concrete types
recursively but contain no value, length, order, digest, or event identifier.

Every `CALL`, `CALL_FUNCTION_EX`, `CALL_INTRINSIC_1`, or `CALL_INTRINSIC_2` in
the callable-code surface has exactly one signed `call_resolution` row. For
ordinary `CALL`/`CALL_FUNCTION_EX`, the same packet-local stack dataflow must
prove the callable producer and target arguments. `CALL` records a nonnull
positional count, `KW_NAMES` as `[]` or the exact active tuple, and null flags;
`CALL_FUNCTION_EX` records null positional/KW fields and its nonnull flags.
Both record a nonempty exact finite target allowlist whose members are named encoded
references, signed ephemeral-construction tokens, exact receiver-bound or
owner-bound-builtin callable tokens, or signed
constructed-callable tokens pointing to the one producing call row. A merged/parameter callable is permitted
only when every branch is narrowed to that signed allowlist and the live target
is `is`-identical to one member; otherwise it or an extra row fails. This admits
the signed `json` encoder/decoder branch targets without admitting an arbitrary
callable. A Python function target adds its body to the callable-code surface. A
class/type target also records and schedules the exact metaclass `__call__`,
MRO-resolved `__new__`, and MRO-resolved `__init__` targets actually invoked; a
callable-instance target records its signed instance and schedules its exact
class-MRO `__call__`. A CPython intrinsic row records the integer intrinsic ID
and pinned-interpreter semantic token. Thus `random.Random(20260803)` binds the
`type.__call__`, `_random.Random.__new__`, `Random.__init__`, and downstream
`Random.seed` path rather than authenticating the class name alone. An intrinsic
row has no callable producer: its allowlist and constructor list are empty and
positional/KW/flags fields are null, while it records the exact nonzero integer
intrinsic ID and the pinned CPython semantic token (for example,
`3:INTRINSIC_STOPITERATION_ERROR`). If that intrinsic performs data-model
dispatch (for example `5:INTRINSIC_UNARY_POSITIVE`), the row also contains the
same exact operand-type/ordered-target/result-type protocol record below and
schedules every Python target; otherwise that field is null. Any other mixture
fails.

Implicit data-model dispatch is not treated as interpreter magic. Every
instruction in this exact pinned-3.12 set has one signed
`protocol_resolution` row:

```text
UNARY_NEGATIVE UNARY_NOT UNARY_INVERT
BINARY_OP BINARY_SLICE BINARY_SUBSCR STORE_SLICE STORE_SUBSCR
DELETE_SUBSCR COMPARE_OP CONTAINS_OP
GET_ITER FOR_ITER GET_YIELD_FROM_ITER SEND UNPACK_SEQUENCE UNPACK_EX
POP_JUMP_IF_FALSE POP_JUMP_IF_TRUE
STORE_ATTR DELETE_ATTR FORMAT_VALUE
BUILD_SET BUILD_MAP BUILD_CONST_KEY_MAP SET_ADD SET_UPDATE MAP_ADD
LIST_EXTEND DICT_UPDATE DICT_MERGE
BEFORE_WITH WITH_EXCEPT_START BEFORE_ASYNC_WITH
GET_AITER GET_ANEXT GET_AWAITABLE END_ASYNC_FOR
GET_LEN MATCH_MAPPING MATCH_SEQUENCE MATCH_KEYS MATCH_CLASS
CHECK_EXC_MATCH CHECK_EG_MATCH RAISE_VARARGS
```

For each row, packet-local stack dataflow records the exact opcode/oparg and
semantic token, a finite exact concrete-type allowlist for each operand, the
ordered CPython dispatch targets (including descriptor binding,
`NotImplemented`, reflected-operation, truth, iterator/next, and context-
manager fallbacks), and a finite result-type allowlist. Each target is a named
reference, receiver-bound target, or pinned C/interpreter descriptor/provider
record. Every pure-Python target body joins the callable-code surface. Unknown
or merged operand types not narrowed to the signed allowlists fail; core/C
targets still bind their exact type, descriptor, provider, and interpreter
digest. Thus `Fraction` arithmetic/comparison schedules the exact
`Fraction` dunders and their `fractions.operator` globals, while
`_DATA_DIR / filename` schedules the exact pathlib division path.

Every decoded instruction, including nested code, also has one
`opcode_classification` row whose category is exactly one of `global`,
`import`, `make-function`, `call`, `receiver`, `protocol`, or
`interpreter-only`. The dynamic opcodes listed above and all load/import/call/
receiver/make-function opcodes may not be classified interpreter-only. Any
`INSTRUMENTED_*`, `RESERVED`, `INTERPRETER_EXIT`, unknown opcode, missing row,
extra row, or category/resolution mismatch fails. The remaining pinned opcodes
may be interpreter-only only after the verifier's frozen classification table
confirms they cannot invoke a Python-visible global, callable, descriptor, or
data-model protocol under CPython 3.12.13; the table's canonical bytes and
SHA-256 are part of the signed manifest.

There is no module-by-all-names or class-by-all-names cross product. Every
`LOAD_ATTR`, `LOAD_METHOD`, `LOAD_SUPER_ATTR`, `LOAD_SUPER_METHOD`,
`LOAD_ZERO_SUPER_ATTR`, or `LOAD_ZERO_SUPER_METHOD` in the callable-code surface has exactly one signed
`receiver_resolution` row keyed by stable code path and instruction offset.
For a `static-binding` row, the verifier's packet-local bytecode dataflow must
prove that the receiver is the stated `LOAD_GLOBAL`/prior static-attribute
chain with no unknown stack producer or control-flow merge. Static lookup
imports no `inspect`: for a module, the requested name exists only when it is a
key of `vars(module)`; for a class/type, scan its signed `__mro__` in order and
take the first matching `vars(base)` key. Any of the four super-opcode rows records the
exact authenticated `__class__` closure cell, receiver type, starting class,
ordered MRO, first owner strictly after that class, raw descriptor, and resolved
target under pinned CPython 3.12 semantics; every relation must agree. Apply only the row's one requested
attribute to that one proven receiver and record the raw target. For an
`immutable-core-type`, `type-probe`, or `super-binding` row, record only the named descriptor on
that exact type. Any instruction whose receiver cannot be proved under one of
the four row kinds fails contract lint; an extra row also fails. The manifest
may report the sorted union `attribute_names` for audit, but that union never
drives lookup or reachability.

Seed the object surface with resolved globals, receiver-specific targets, and
every non-source module, class/type, builtin, descriptor, or named stdlib
instance directly bound in a source module/class record. A reached pure-Python
stdlib function receives the full code/default/annotation/dict/globals/builtins
record plus its canonical occurrence path/digest. Only when that function is a global/receiver target does it add its
nested code and global/receiver resolutions to the callable-code surface.
Unlike source functions, a reached pure-Python stdlib function may have a closure. Record
`fn.__closure__` in order as `{"type":"closure","cells":[...]}`. Each cell is
`{"type":"empty-cell"}` when reading `cell.cell_contents` raises `ValueError`,
or `{"type":"cell","value":encoded_value}` otherwise. Closure-cell binding
paths are `<stdlib-function-reference-name>:closure:<zero-based-index>`; include
every cell object, including singletons, in the manifest identity partition so
shared cells and distinct equal-valued cells cannot be exchanged. This admits
the pinned `collections.Counter` method closures while binding their exact
`Counter` class references. A reached stdlib class
receives the full metaclass/bases/MRO/namespace/function record. A named stdlib
instance receives the exact instance record below, and its class is added.
Repeat opcode classification, global/import/call/protocol and
constructed-callable resolution, receiver-specific lookup, callable-code
addition, and object recording until
the inventories do not change. This bounded rule never
crawls an inspector's implementation, every namespace member's body, or an
unrelated module alias.

Every one of those six receiver opcodes in the callable-code surface, including all
eight authenticated source modules, must have one
signed `receiver_resolution` row keyed by stable code path and instruction
offset. The row is exactly one of: a recorded static module/type binding; one
of the immutable core types `str`, `bytes`, `int`, `float`, `tuple`, `list`,
`dict`, `set`, or `frozenset`; a `receiver_type_probe` ID; or the exact
`super-binding` record above. A probe record
contains the stable callable reference, recursively encoded constant positional
and keyword arguments, the expected exact result-type reference, and the sorted
attribute names permitted on that result. Probes run in both clean builds and
at startup before source access and must return the same exact type. The five
unmodified base modules use only data-independent synthetic probe calls, and
their exact factory bindings are attested immediately before and after scoring.
Reached stdlib code is not modified; its exact provider/binding and each result
type are signed. External code must immediately pass each opaque stdlib result through the packet-local
`require_exact_type(value, probe_id)` and invoke only a descriptor listed for
that type; contract lint rejects an opaque result used by raw attribute access.
This rule covers, for example, `_hashlib.HASH` returned by
`hashlib.sha256(b"")`, even though that type is not a `hashlib` module export.
A data-dependent result type outside its signed probe allowlist fails before
its attribute is read. Runtime lookup of an unrecorded global, static binding,
receiver type, or attribute is forbidden.

The concrete type/class of every specially encoded `re.Pattern` and
`pathlib.PurePath` value is also added to the surface and receives the same
type/metaclass/base/MRO/descriptor record. Receiver rows therefore cover
maintained parser match objects, compiled patterns, and path operations as well
as experiment-owned hash/archive/file objects.

Core immutable CPython types reached only as the concrete type of an input
scalar/container are bound by their `stdlib-type` record, metaclass, bases,
MRO, and pinned interpreter binary; the verifier must also require that
`setattr(recorded_type, recorded_attribute, sentinel)` raises `TypeError` and
that the original descriptor identity and encoded value remain unchanged. A Python or extension function reached in the surface
has an exact record. A Python function uses the record above. Except for the
nonrecursive owner-bound-builtin target encoded inline below, an extension or
builtin callable record contains its stable name, concrete type reference,
canonical occurrence path/digest,
encoded `__module__`, `__name__`, `__qualname__`, `__self__`, and
`__text_signature__`, plus a domain-separated SHA-256 of its UTF-8 `__doc__`
(or encoded `None`) and the SHA-256 of its providing extension file; a built-in
or frozen provider instead records the authenticated interpreter executable
SHA-256 and literal origin `built-in` or `frozen`.

A descriptor record always contains its stable name, concrete type reference,
owner class/type reference, and exact owner namespace key, **plus its
behavior-bearing payload**. A `staticmethod` or `classmethod` record contains
the exact encoded `__func__` reference. A property record contains exact
encoded `fget`, `fset`, and `fdel` references-or-`None` and encoded `__doc__`.
A member, getset, method, or wrapper descriptor records encoded live
`__objclass__`, `__name__`, `__qualname__`, `__doc__`, and
`__text_signature__` when each attribute exists, with explicit encoded `None`
when it does not, plus its built-in/frozen/extension provider digest. Any other
Python descriptor instance must have a named stdlib-instance record with its
complete `__dict__`, readable member/getset slots, class record, and identity
relations. A wrapper reconstructed with a different underlying function or a
property getter/setter/deleter permutation therefore fails even when owner,
namespace keys, function inventory, and descriptor types match.

A standard-library module record contains its stable name,
exact `__name__`, literal origin, and providing-file SHA-256, or the interpreter
digest for a built-in/frozen origin.

A named standard-library instance is admitted only when reached at a recorded
module/class/instance binding path. Its stable name uses the lexicographically
first canonical occurrence path, and its record contains that path, concrete
class/type reference, provider origin/digest, recursively encoded `__dict__`
(or encoded `None`), and every readable member/getset slot found in its signed
class MRO, ordered by owner reference then key. Slot values are read by the
recorded descriptor's `__get__`; an exception fails. Its nested mutable
content and identity aliases use the same order-preserving encoding and
equivalence rules. Callable stdlib instances are allowed only through this
record, so `json._default_decoder` and its `_json.Scanner` are encodable while
an anonymous source-owned callable remains forbidden.

The only behavior-neutral mutable stdlib caches normalized between phases are
the pinned CPython 3.12 `re._cache` and `re._cache2` dictionaries. Immediately
before each manifest snapshot, require both bindings to be exact built-in
`dict` objects, invoke the authenticated descriptor directly as
`dict.clear(re._cache)` and `dict.clear(re._cache2)` in that order, and require
both exact objects to be empty while `_MAXCACHE == 512` and `_MAXCACHE2 == 256`;
record those identities and values. Do not call or reach `re.purge()` or
`re._compile_template`, because `purge()` also mutates a separate template LRU
cache. No score/report/receipt object may retain a cache entry. This reset
occurs before development, validation, and sealed scoring and after each phase,
so a phase always starts clean; any other stdlib mutable-state drift fails. No
other cache may be excluded or reset.

Unsupported origins, dynamic module `__getattr__`, a static-lookup exception,
or a value that cannot be encoded by these rules fails before source access.
Thus substitutions such as
`stats.math.log2`, `re.compile`, `random.Random.randrange`, `json.loads`,
`os.replace`, or a referenced builtin cannot retain a valid manifest.

At both clean signing builds and every execution attestation,
`sys.gettrace()` and `sys.getprofile()` must be `None`. For each tool ID
`0,1,2,3,4,5`, require `sys.monitoring.get_tool(i) is None`,
`sys.monitoring.get_events(i) == 0`, and
`sys.monitoring.get_local_events(i, code) == 0` for every code object in the
fixed-point inventory. The supported event map must equal exactly
`PY_START=1, PY_RESUME=2, PY_RETURN=4, PY_YIELD=8, CALL=16, LINE=32,
INSTRUCTION=64, JUMP=128, BRANCH=256, STOP_ITERATION=512, RAISE=1024,
EXCEPTION_HANDLED=2048, PY_UNWIND=4096, PY_THROW=8192, RERAISE=16384,
C_RETURN=32768, C_RAISE=65536, NO_EVENTS=0`. In ascending positive event
value order, call `sys.monitoring.register_callback(i, event, None)` and require
its returned prior callback to be `None`; a non-`None` return is unregistered
by that call but still fails the run. Recheck event masks afterward. Stale
callbacks and inactive local/global monitoring therefore cannot pass merely
because a tool ID was freed.

Every remaining recorded module, class, or admitted-instance state value is encoded recursively with an exact
type tag: `None`; Boolean; unbounded integer as signed decimal; any binary64 as
its exact big-endian IEEE-754 bytes; Unicode string; bytes as lowercase hex; ordered tuple/list;
dictionary as encoded key/value pairs sorted by the canonical bytes of the
encoded key **and** a second encoded-key list preserving actual insertion
order; set/frozenset sorted by encoded element bytes; `re.Pattern` as
pattern string plus integer flags; `pathlib.PurePath` as concrete qualified
type plus POSIX string; or a stable named reference to an authenticated module,
class, function, builtin, descriptor, standard-library module/function/type,
or recorded standard-library instance. Mutable
containers are allowed only through this content encoding and are recomputed
at every attestation. Cycles may traverse named references only. Arbitrary
source-owned callable instances, decorated wrappers not identical to an
enumerated named function, `functools.partial`, unsupported values, duplicate
stable names, or unenumerated references fail the build before source access.
Each module `state` record covers every non-excluded module namespace key,
including function/class/import bindings as named references. Each class
`state` record covers every class namespace key, including method/property/
descriptor bindings as named references; its `functions` list separately binds
the code-bearing functions underlying those descriptors. Thus namespace keys
are neither silently omitted nor represented only by identity.

The recursive JSON encoding is exact. `None` is `{"type":"none"}`; Boolean,
integer, float, string, and bytes are respectively
`{"type":"bool","value":<JSON Boolean>}`,
`{"type":"int","value":"<signed decimal>"}`,
`{"type":"float","bits":"<16 lowercase hex from struct.pack('>d', value)>"}`,
`{"type":"str","value":"<string>"}`, and
`{"type":"bytes","value":"<lowercase hex>"}`. Tuple, list, set, and
frozenset use `{"type":"<type>","items":[...]}`; tuple/list preserve order,
while set/frozenset items sort by each item's canonical JSON bytes. A mapping is
`{"type":"dict","entries":[{"key":...,"value":...},...],
"insertion_keys":[...encoded keys in actual iteration order...]}`. `entries`
sort by key-encoding bytes; `insertion_keys` contains every encoded key exactly
once and preserves the mapping's iteration order. The two key multisets must be
identical. This second list is mandatory because canon methods consume
dictionary order. Pattern, path, and named reference records are
`{"type":"re-pattern","pattern":<encoded str-or-bytes>,"flags":"<unsigned decimal>"}`,
`{"type":"path","class":"<module.qualname>","value":"<POSIX string>"}`,
and `{"type":"ref","kind":"<module|class|function|builtin|descriptor|stdlib-module|stdlib-function|stdlib-type|stdlib-instance>","name":"<stable name>"}`.
An ephemeral callable target is exactly
`{"type":"ephemeral-function","token":"<signed construction token>"}` and is
legal only in a call allowlist or an ephemeral-function recipe; it is never a
named reference or identity-partition member.
A constructed callable target is exactly
`{"type":"constructed-callable","token":"<signed construction token>"}` and
is legal only in a later call allowlist or construction-argument recipe; it is
never a named reference, general state value, or identity-partition member.
A method produced by a receiver row is
`{"type":"receiver-bound-callable","code":stable_code_path,
"offset":instruction_offset_decimal}`. Stack dataflow must trace the call target
to that exact signed receiver-opcode result and its
signed descriptor/self/type relations; the token cannot name another row.
An already-bound Python method is
`{"type":"bound-python-method","function":encoded_function_reference,
"self":encoded_value}` and must satisfy `value.__func__`/`value.__self__`
identity. A builtin callable stored directly in a signed module or class/type
namespace, with live `__module__ is None` and `__self__ is owner`, is
`{"type":"owner-bound-builtin-callable","owner":encoded_module_or_type_reference,
"namespace_key":namespace_key,"module_token":"none",
"callable_type":encoded_type_reference,"name":encoded_string,
"qualname":encoded_string,"text_signature":encoded_string_or_none,
"doc_sha256":doc_sha256,"provider_origin":literal_origin,
"provider_sha256":provider_sha256}`. The verifier requires
`vars(owner)[namespace_key] is value`, binds every recorded live metadata field,
and resolves the provider under the extension/builtin/frozen rules above; it
does not recurse through a descriptor or assign a standalone reference name.
This exact token is legal only as an encoded callable target in a call
allowlist, constructor slot, protocol row, or construction-argument recipe,
or as the exact class/module-state or attribute-binding value whose recorded
owner and namespace key equal the token's own `owner` and `namespace_key`.
That matching state value is the complete inline object record; it creates no
separate `objects` row or standalone reference. The token is forbidden in
every unrelated state position. Every occurrence of the same owner/key token
must resolve to that one live object by `is`; its stable owner namespace-binding
path participates in the identity partition and binds its constructor/call-
surface aliases even though the target has no standalone reference name.
It covers the class-bound module-None `_json.Encoder.__new__` and
`_random.Random.__new__` entries.

Any other already-bound builtin method whose live `__module__` is `None` is
`{"type":"descriptor-bound-builtin-method","descriptor":encoded_descriptor_reference,
"self":encoded_value}`; the descriptor is the exact raw owner-type namespace
entry at `value.__name__` and must reproduce the same concrete callable type,
`__name__`, `__qualname__`, and `__self__` when bound. It is not assigned a
collision-prone standalone reference name.
Duplicate canonical keys/items, noncanonical decimals/hex, and an unknown key
in any tagged object fail.

The manifest object has exactly these top-level keys and shapes; all lists use
the ordering rules above and every SHA-256 is lowercase 64-hex:

```python
{
  "schema": "edcm.response-tension-release-runtime-state/1",
  "packet_sha256": packet_sha256,
  "edcm_base": {
    "commit_sha1": edcm_base_commit_sha1,
    "repository_tree_sha1": edcm_base_repository_tree_sha1,
    "edcm_tree_sha1": edcm_tree_sha1,
    "measurement_tree_sha1": measurement_tree_sha1,
  },
  "experiment_root": {
    "tree_sha1": experiment_root_tree_sha1,
    "files": [
      {"module": module_name, "path": absolute_posix_path,
       "sha256": file_sha256},
      ...
    ],
  },
  "container_sha256": container_sha256,
  "bootstrap": {
    "import_prefix_sha256": import_prefix_sha256,
    "runtime_sha256": runtime_bootstrap_sha256,
    "builder_sha256": builder_bootstrap_sha256,
    "allocation_audit_sha256": allocation_audit_bootstrap_sha256,
  },
  "runtime": {
    "implementation": "CPython",
    "version": "3.12.13",
    "cache_tag": "cpython-312",
    "unicode_version": "15.0.0",
    "marshal_version": "4",
  },
  "modules": [
    {
      "name": module_name,
      "path": absolute_posix_path,
      "file_sha256": file_sha256,
      "namespace_keys": [key, ...],
      "functions": [
        {
          "name": stable_function_name,
          "code_sha256": code_sha256,
          "globals_module": source_module_name,
          "builtins": "stdlib-module:builtins",
          "closure": {"type": "none"},
          "defaults": encoded_value,
          "kwdefaults": encoded_value,
          "annotations": encoded_value,
          "function_dict": encoded_value,
        },
        ...
      ],
      "classes": [
        {
          "name": stable_class_name,
          "metaclass": encoded_reference,
          "bases": [encoded_reference, ...],
          "mro": [encoded_reference, ...],
          "namespace_keys": [key, ...],
          "functions": [stable_function_name, ...],
          "state": [{"name": key, "value": encoded_value}, ...],
        },
        ...
      ],
      "state": [{"name": key, "value": encoded_value}, ...],
    },
    ...
  ],
  "runtime_surfaces": {
    "opcode_classification_table": opcode_classification_table,
    "opcode_classification_table_sha256": opcode_classification_table_sha256,
    "opcode_classifications": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": opcode_name, "oparg": signed_decimal_string_or_null,
       "category": "global" | "import" | "make-function" | "call" |
                   "receiver" | "protocol" | "interpreter-only"}, ...
    ],
    "code_objects": [
      {"name": stable_code_path, "code_sha256": code_sha256}, ...
    ],
    "global_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": global_load_opcode, "name": global_name,
       "sources": [encoded_module_mapping_or_cell_reference, ...],
       "targets": [encoded_value, ...]}, ...
    ],
    "import_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": "IMPORT_NAME" | "IMPORT_FROM", "name": import_name,
       "level": signed_decimal_string, "fromlist": [name, ...],
       "source": encoded_module_reference_or_null,
       "result": encoded_reference, "importer": encoded_builtin_reference,
       "origin": literal_origin, "file_sha256": file_sha256_or_null}, ...
    ],
    "ephemeral_function_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "token": ephemeral_construction_token,
       "nested_code": nested_stable_code_path,
       "flags": unsigned_decimal_string,
       "defaults": encoded_value, "kwdefaults": encoded_value,
       "annotations": encoded_value,
       "lifecycle_paths": [
         {"token": "immediate-call" | "returned-to-signed-caller" |
                   "retained-by-generator-until-exhaustion",
          "instruction_path": [stable_code_path_and_offset, ...]}, ...
       ],
       "closure_provenance": [
         {"freevar_index": unsigned_decimal_string,
          "freevar_name": name,
          "producer": {"kind": "local" | "enclosing-cell",
                       "index": unsigned_decimal_string, "name": name},
          "value_contract": exact_type_or_recursive_core_container_contract,
          "cell_equivalence_class": unsigned_decimal_string}, ...
       ],
       "globals_module": defining_module_name,
       "builtins": "stdlib-module:builtins"}, ...
    ],
    "constructed_callable_resolutions": [
      {"token": constructed_callable_token,
       "producer_code": stable_code_path,
       "producer_offset": instruction_offset_decimal,
       "constructor": {"callable": encoded_callable_target,
                       "metaclass_call": encoded_callable_target,
                       "new": encoded_callable_target,
                       "init": encoded_callable_target},
       "result_type": encoded_type_reference,
       "result_contract": {"kind": "exact-type",
                           "type": encoded_type_reference},
       "call_descriptor": {"owner": encoded_type_reference,
                           "raw_binding": encoded_function_or_descriptor_reference,
                           "provider_origin": literal_origin,
                           "provider_sha256": provider_sha256},
       "argument_recipes": [
         {"argument_index": unsigned_decimal_string,
          "position": unsigned_decimal_string_or_null,
          "keyword": name_or_null,
          "producer_path": [stable_code_path_and_offset, ...],
          "recipe": {"kind": "constant", "value": encoded_value} |
                    {"kind": "callable",
                     "target": encoded_callable_target} |
                    {"kind": "value-contract",
                     "contract": exact_type_or_recursive_core_container_contract}}, ...
       ],
       "lifecycle_paths": [
         {"token": "immediate-call" | "stored-local-then-call" |
                   "returned-to-signed-caller" |
                   "passed-as-signed-call-argument" |
                   "retained-until-signed-caller-return",
          "instruction_path": [stable_code_path_and_offset, ...]}, ...
       ],
       "probe": {"source_free": True,
                 "result_type_match": True,
                 "call_binding_match": True,
                 "callable": True}}, ...
    ],
    "call_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": call_opcode, "callable_allowlist": [encoded_callable_target, ...],
       "positional_count": unsigned_decimal_string_or_null,
       "kw_names": [name, ...] | None, "flags": unsigned_decimal_string_or_null,
       "constructors": [{"callable": encoded_callable_target,
                         "metaclass_call": encoded_callable_target,
                         "new": encoded_callable_target,
                         "init": encoded_callable_target}, ...],
       "intrinsic_id": unsigned_decimal_string_or_null,
       "intrinsic_semantic_token": ascii_token_or_null,
       "intrinsic_protocol": exact_protocol_record_or_null}, ...
    ],
    "protocol_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": opcode_name, "oparg": signed_decimal_string_or_null,
       "semantic_token": semantic_token,
       "operand_type_allowlists": [[encoded_type_reference, ...], ...],
       "targets": [{"slot": slot_name,
                    "owner": encoded_type_reference,
                    "callable": encoded_callable_target,
                    "condition": dispatch_condition_token}, ...],
       "result_type_allowlist": [encoded_type_reference, ...]}, ...
    ],
    "attribute_names": [attribute_name, ...],
    "attribute_bindings": [
      {"owner": encoded_reference, "name": attribute_name,
       "value": encoded_value}, ...
    ],
    "receiver_resolutions": [
      {"code": stable_code_path, "offset": instruction_offset_decimal,
       "opcode": "LOAD_ATTR" | "LOAD_METHOD" | "LOAD_SUPER_ATTR" |
                 "LOAD_SUPER_METHOD" | "LOAD_ZERO_SUPER_ATTR" |
                 "LOAD_ZERO_SUPER_METHOD",
       "kind": "static-binding" | "immutable-core-type" | "type-probe" | "super-binding",
       "target": encoded_reference_or_probe_id,
       "attribute": attribute_name,
       "super": {"class_cell": encoded_cell_binding,
                 "receiver_type": encoded_reference,
                 "starting_class": encoded_reference,
                 "mro": [encoded_reference, ...],
                 "owner": encoded_reference,
                 "raw_descriptor": encoded_value} | None}, ...
    ],
    "receiver_type_probes": [
      {"id": probe_id, "callable": encoded_reference,
       "args": encoded_tuple, "kwargs": encoded_dict,
       "result_type": encoded_reference,
       "attributes": [attribute_name, ...]}, ...
    ],
    "objects": [
      {"name": stable_reference_name, "kind": reference_kind,
       "origin": literal_origin, "file_sha256": file_sha256_or_null,
       "record": exact_kind_specific_record}, ...
    ],
  },
  "canon_instance": {
    "class": encoded_canonloader_reference,
    "resources": [
      {"path": relative_posix_path, "git_blob_sha1": blob_sha1,
       "sha256": resource_sha256}, ...
    ],
    "expected_state_sha256": canon_expected_state_sha256,
  },
  "identity_equivalence_classes": [[stable_binding_name, ...], ...],
}
```

Module records sort by module name; external file records by module name;
function/class records and state records by stable name; namespace-key lists by
key; identity-class members by binding name; and identity classes by their
canonical JSON bytes. `container_sha256` is the lowercase 64-hex payload digest
without a `sha256:` prefix. Function code uses exactly
`sha256(b"edcm.response-tension-release:function-code:v1\x00" +
marshal.dumps(fn.__code__, 4)).hexdigest()`.
The import-prefix, runtime-bootstrap, builder-bootstrap, and allocation-audit-bootstrap fields are ordinary
SHA-256 hex digests of the exact UTF-8 source strings frozen above. A stable
code path is `<stable-function-reference-name>/code` for a function's root
code and appends `/const:<zero-based-co_consts-index>` for each nested code
object. A code object reachable at two paths is recorded at both paths and must
be `is`-identical in the signed identity partition. Instruction offsets are
unsigned canonical decimal strings. Runtime-surface global-resolution records
and opcode-classification, import-, ephemeral-function-, constructed-callable-,
call-, protocol-, and receiver-resolution records sort by code path then
integer offset; each applicable instruction has exactly one row and duplicate
`(code, offset)` keys within a list fail. Attribute bindings sort by owner
reference canonical bytes then attribute-name UTF-8 bytes. Global source/target
lists preserve exact lookup/branch priority and contain no duplicate. Probes sort by strict UTF-8 probe
ID and their attribute lists by strict UTF-8 bytes; surface objects sort by
stable reference name. Each nonintrinsic call allowlist and every constructor
list sorts by encoded callable-target canonical bytes and contains no
duplicate; intrinsic lists are empty. Constructed-callable rows sort by
producer code and integer offset. Their argument indexes are exactly
`0..len(argument_recipes)-1` in list order; exactly one of `position` or
`keyword` is nonnull, positions are strictly increasing before unique keyword
names, and exactly one recipe variant is present. Lifecycle paths preserve use
order and may not duplicate an instruction path. Protocol operand/result allowlists sort
by encoded type-reference canonical bytes with no duplicate, while targets
preserve exact dispatch order. A probe ID is a nonempty ASCII token matching
`[a-z0-9][a-z0-9._-]*`; duplicates fail.

The classification table object is exactly
`{"schema":"edcm.response-tension-release-opcode-classification/1",
"python":"3.12.13","rows":[{"opcode":opcode_name,
"number":unsigned_decimal_string,"category":category,
"requires_resolution":json_boolean},...]}`. It contains every entry of the
pinned interpreter's `dis.opmap` exactly once, sorted by integer opcode number
then opcode-name UTF-8 bytes. Its digest is
`sha256(b"edcm.response-tension-release:opcode-classification:v1\x00" +
canonical_json_bytes(table)).hexdigest()`. The two builders and runtime must
reproduce identical table bytes and digest.
Reference target names use exactly this ASCII-prefix grammar:

```text
module:<authenticated-source-module-name>
function:<authenticated-source-module-name>:<qualname>
class:<authenticated-source-module-name>:<qualname>
builtin:<live-__module__>:<live-__qualname__>:<64hex-occurrence-path-sha256>
descriptor:<owner-module>:<owner-qualname>:<owner-namespace-key>
stdlib-module:<live-module-name>
stdlib-function:<live-module-name>:<live-qualname>:<64hex-occurrence-path-sha256>
stdlib-type:<live-__module__>:<live-__qualname__>
stdlib-instance:<owner-module-name>:<64hex-occurrence-path-sha256>
```

Every component is nonempty and contains no colon. The name uses the object's
defining live metadata, never an import alias. An authenticated source object
uses `module`, `function`, or `class`, never a stdlib kind. A descriptor owner
and namespace key must be unique in the signed owner inventory. Each reference
name resolves to exactly one signed target record; each record must resolve
back to the same live object by `is`. Two non-identical targets with the same
name, one target admitted under two target names, an alias-only name, or an
unresolved reference fails. Stable module and class **binding path** names,
which are distinct from reference target names, are
`module:<module>:<key>` and `class:<module>:<qualname>:<key>`. Colons inside any
component are forbidden; all names and keys are preserved Unicode strings and
sort by strict UTF-8 bytes.

A named builtin, stdlib-function, or stdlib-instance occurrence path is a canonical JSON list beginning with
either `{"step":"module-binding","module":module_name,"name":binding_name}`
or `{"step":"class-binding","module":module_name,"qualname":owner_qualname,
"name":binding_name}`. It continues, as needed, with
`{"step":"instance-attribute","name":attribute_name}`,
`{"step":"descriptor-function","slot":"__func__"|"fget"|"fset"|"fdel"}`,
`{"step":"list","index":"<unsigned decimal>"}`,
`{"step":"dict-value","key":encoded_key}`, or
`{"step":"bound-self"}`. Thus a generated class function, descriptor payload,
custom class descriptor, or module-bound
method's `__self__` has a legal path without a numeric identity. A candidate
path is finite and simple: while traversing the signed recorded binding graph,
no live object identity may occur twice. Of all such paths to the same object,
choose the one with lexicographically least canonical JSON bytes. The final name component
is `sha256(canonical_json_bytes(chosen_path)).hexdigest()` and the full chosen
path is present in the builtin/function/instance record. This gives generated Fraction
forward/reverse wrappers and nested instances cross-process names without an
object address. Aliases of one object choose one least path; distinct objects
bound under different keys necessarily retain different path digests even when
their live module and qualname are equal. Contract fixtures must show that the
distinct generated `Fraction` forward and reverse wrappers sharing identical
live module and qualname receive distinct path digests, while two aliases of
one function collapse to the same least simple path and target name.

Named binding identity is never a process-local numeric ID. For every recorded
binding or stable code path whose value is a module, function, class,
descriptor, owner-bound builtin callable, list, dictionary,
set, closure cell, `types.CodeType`, or another permitted mutable container, group paths that are
`is`-identical into sorted stable-name equivalence classes, including singleton
classes. Immutable scalar, tuple/frozenset, pattern, and path values are
content-bound but excluded from identity partitioning so interpreter interning
cannot change evidence bytes. The identity partition must cover every eligible
named binding exactly once and execution verifies both sameness within and
distinctness across all classes. The
manifest also binds exact module/class/function inventories, namespace keys,
file paths and SHA-256 values, code-state digests, recursively encoded state,
CPython/cache-tag/Unicode identities, both code-root identities, and container
digest in one section 6.1 canonical-JSON object with schema
`edcm.response-tension-release-runtime-state/1`. The manifest contains no
self-digest. Define externally:

```python
runtime_state_manifest_sha256 = sha256(
    b"edcm.response-tension-release:runtime-state:v1\x00"
    + runtime_state_manifest_bytes
).hexdigest()
runtime_state_manifest_file_sha256 = sha256(
    runtime_state_manifest_bytes
).hexdigest()
```

After the two builder outputs match, the supervisor freezes this exact
section-6.1 canonical-JSON claims object (no omitted or extra key):

```python
{
  "schema": "edcm.response-tension-release-runtime-signature-claims/1",
  "supervisor_legal_identity": supervisor_legal_identity,
  "hsm_service_legal_identity": hsm_service_legal_identity,
  "hsm_key_handle_identity": hsm_key_handle_identity,
  "public_key_fingerprint": public_key_fingerprint,
  "signature_scheme": signature_scheme,
  "builder_bootstrap_sha256": builder_bootstrap_sha256,
  "runtime_bootstrap_sha256": runtime_bootstrap_sha256,
  "builder_stdout_sha256": [runtime_state_manifest_file_sha256,
                             runtime_state_manifest_file_sha256],
  "two_build_byte_identical": True,
  "builder_fd_mount_environment_claims": builder_topology_claims,
  "runtime_fd_mount_environment_claims": runtime_topology_claims,
  "builder_private_key_or_hsm_access_absent": True,
  "runtime_private_key_or_hsm_access_absent": True,
  "timestamp_rfc3339_utc": timestamp_rfc3339_utc,
}
```

Each topology claim has exactly
`{"schema":"edcm.response-tension-release-process-topology/1",
"mode":mode_token,"fds":[{"number":unsigned_decimal_string,
"kind":fd_kind,"access":"read"|"write","target":target_identity},...],
"mounts":[{"path":absolute_posix_path,"st_dev":unsigned_decimal_string,
"read_only":json_boolean,"source":source_identity},...],
"environment_keys":[key,...],"private_key_material_absent":true,
"hsm_device_socket_token_handle_absent":true,"verdict":"pass"}`.
FD rows sort numerically, mounts and environment keys by strict UTF-8 bytes;
`target_identity` and `source_identity` are nonempty role-manifest tokens.
Define
`runtime_signature_claims_sha256 = sha256(
b"edcm.response-tension-release:runtime-signature-claims:v1\x00" +
runtime_signature_claims_bytes).hexdigest()`. The custody HSM signs exactly:

```python
b"edcm.response-tension-release:runtime-state-signature:v1\x00" \
+ bytes.fromhex(packet_sha256) \
+ bytes.fromhex(edcm_base_commit_sha1) \
+ bytes.fromhex(experiment_root_tree_sha1) \
+ bytes.fromhex(container_sha256) \
+ bytes.fromhex(runtime_state_manifest_sha256) \
+ bytes.fromhex(runtime_signature_claims_sha256)
```

The detached envelope contains exactly the signature fields above, the complete
claims object/claims digest, and the signature. Altering a topology, identity,
key, verdict, or timestamp therefore invalidates it.
The custody supervisor authenticates the pre-import objects and exact bootstrap
before process launch. The execution process then imports by the shared prefix
and recomputes the full manifest before source access. This detects in-place
function code/default/annotation mutation, alternate function globals or
builtins, local-helper or stdlib substitution, metaclass/base/MRO drift,
named-identity drift, active instrumentation, and mutable global/class changes
such as parser pattern-list append or reorder.

The canon instance has an independently derived signed expectation, not a
post-load self-baseline. The verifier first authenticates these exact resource
bytes, ordered by relative path:

| Resource beneath `edcm/measurement/canon/data/` | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `bones_affixes_v1.json` | `68811fc62ffe61022c9db2d325c80b900d501282` | `430a6b4b1fe1c74de1020e66f7105b1e81d3776569fdea7a14a6b95afa23e06d` |
| `bones_punct_v1.json` | `5cc294c70ebbd7325f07ad67982a9353d0017754` | `4ff465aa4fe0d1218d27e17df899d575f8bc855aca455407a33d9bebdd3cedda` |
| `bones_words_v1.json` | `422cd3d0aa31ab0b2aac6dcbb982bbe4853e6a19` | `b2287b3b2d35f1d8bafcda64c36365d354eba8b41a3562b9c23d4bafbb2013fe` |
| `markers_v1.json` | `f937fab506c2201159ec90024ea18c898a331066` | `f891788644bc100777d36233680d10a0199925fd726696aab5e4e964bea4c0cc` |

Without calling or inspecting a `CanonLoader` instance, the independent
verifier decodes each exact byte string with strict UTF-8 and `json.loads` and
assigns the four decoded values to `_affixes_data`, `_punct_data`,
`_words_data`, and `_markers_data`. It then constructs `_word_index` as
`{entry["word"].lower(): entry for entry in _words_data["words"]}`,
`_multiword_index` as
`{entry["joined"].lower(): entry for entry in
_words_data.get("multiword_joins", [])}`, and `_punct_index` as
`{entry["mark"]: entry for entry in _punct_data["punctuation"]}`. It constructs
`_affix_index` from an empty dictionary by iterating, in order,
`("inflectional", "derivational_prefixes", "derivational_suffixes")`, then
each `_affixes_data[section]["affixes"]` in list order, assigning
`entry["affix"].lower()` to that same `entry` object. These are the only eight
instance attributes.

The expected canon-state object is exactly:

```python
{
  "schema": "edcm.response-tension-release-canon-state/1",
  "class": {
    "type": "ref", "kind": "class",
    "name": "class:edcm.measurement.canon.loader:CanonLoader",
  },
  "resources": [resource_record, ...],
  "attributes": [
    {"name": attribute_name, "value": encoded_value}, ...
  ],
  "identity_equivalence_classes": [[canon_occurrence_path, ...], ...],
}
```

Resource and attribute records sort by strict UTF-8 path/name bytes. Attribute
values use the recursive order-preserving encoder above. A canon occurrence
path is a JSON list beginning
`{"step":"attribute","name":attribute_name}` and continuing through nested
containers with either `{"step":"list","index":"<unsigned decimal>"}` or
`{"step":"dict-value","key":encoded_key}`. Traverse every list and every
dictionary value; unsupported containers or a cycle fail. For every mutable
list or dictionary occurrence, group paths resolving to `is`-identical objects,
including singleton groups. Members and groups sort by canonical JSON bytes,
and the partition covers every mutable occurrence exactly once. This binds the
source-data/index alias graph as well as contents and insertion order.

Define the signed expected digest exactly as:

```python
canon_expected_state_sha256 = sha256(
    b"edcm.response-tension-release:canon-state:v1\x00"
    + canonical_json_bytes(expected_canon_state)
).hexdigest()
```

Both clean manifest-builder runs derive that expected object without constructing
`CanonLoader`, require byte identity, and place its digest in the signed runtime
manifest. They then call `CanonLoader()` exactly once, encode the resulting
instance with the same schema, and require the digest to match. Execution also
constructs exactly one instance after manifest import, requires its exact class
and eight-key dictionary, and compares its digest with the signed expectation
before source access and at every attestation. The runner retains that one
object for its lifetime and passes it explicitly as `canon=canon` to the sole
`parse_transcript` call and every `compute_round` call. `canon=None`, another
constructor call, copying, deserializing, replacement, or mutation is
incomplete nonconformance.

### 4.1.3 Protected evidence and output writes

All code and input/evidence artifacts are mounted read-only. Mutable outputs
are direct leaf files beneath a separate, initially empty `/custody/output`
mount owned by the custodian, mode `0700`, with no other writer; its `st_dev`
must differ from every protected input mount. The runner opens that directory
once with `O_DIRECTORY|O_NOFOLLOW`, records `fstat`, and rejects absolute names,
`..`, separators, symlinks, pre-existing leaves, duplicate final names, and
duplicate exact deterministic temporary names. It creates each temporary leaf
dirfd-relative with `O_CREAT|O_EXCL|O_NOFOLLOW` and mode `0600`, verifies it by
`fstat`, writes and `fsync`s it, and publishes with dirfd-relative `os.replace`.
It then `fsync`s the directory descriptor. The directory identity/mode/link
count, empty-or-expected leaf inventory, and
every protected input identity are rechecked immediately before and after each
replace. Any mismatch or concurrent-writer evidence stops incomplete.

The protected set includes every code root, packet, lock, source archive,
exclusion/label/ledger/manifest/threshold artifact, and these four exact files
beneath `/opt/edcm-base`:

- `experiments/corpora/results/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-full.json`, SHA-256 `e228b9cb74c60ec4d6efb66f1d86c38069f613a875fa4c91f2973b46d20436f6`;
- `experiments/corpora/receipts/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-complete.json`, SHA-256 `8d20f99f3f788e09e9edad40f7d28a2b97de9d634868652bd058e50d504fe9c9`;
- `experiments/corpora/results/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0.json`, SHA-256 `4c7254cc2a2244eaf0e30e182153f803c9e2706774e9a743f7c22899bdcd64a3`;
- `experiments/corpora/receipts/2026-08-02-multiwoz-2.1-booking-outcome-holdout-v0.1.0-complete.json`, SHA-256 `ea2db8bf06785b54ab67dfa01a236bbec2e1d8ec79a5f9808c949363cff4ffe5`.

At startup, after canon load, after development scoring, after validation
scoring, and before and after each sealed custody run, the runner rereads the
signed manifest/envelope and verifies the exact base commit/tree, full
measurement tree and listed blobs, code-root/file identities, sole-provider/
reachable-module rule, interpreter/Unicode/environment/monitoring state,
canonical runtime-state manifest, canon instance, and stabilized path/mount/
dirfd state. Any mismatch is incomplete nonconformance, not an upgrade or
retry. The PR #49 verifier may be run only as a negative conformance fixture;
it is never authoritative for this successor.

### 4.2 Input and structural policy

Candidate input contains source turns from the dialogue start through the
target system response under exactly one frozen, loss-recorded presentation
transform. The exact source dialogue value at `data.json[dialogue_id]` must be
a JSON mapping whose exact `log` value is a JSON array. For every integer index
`i` from `0` through `response_log_index` inclusive, `log[i]` must be a JSON
mapping with an exact `text` key whose value is a JSON string. Define
`source_turn = log[i]["text"]` byte-for-byte as decoded by the authenticated
archive JSON loader; every strict UTF-8 encoding must succeed. Extra turn keys
are ignored. The corpus convention is even `i = USER`, odd `i = SYSTEM`; it
does not rely on a native speaker field, and the odd target index is the target
system response. A missing/non-mapping dialogue, missing/non-list `log`, absent
prefix index, non-mapping turn, missing/non-string `text`, strict-UTF-8 failure,
or parity/target mismatch stops the whole experiment incomplete as
`source-turn-schema-mismatch`; it is never an exclusion or fallback.

For each exact `source_turn`, compute these values in order under the frozen
Python interpreter:

```python
newline_normalized = source_turn.replace("\r", " ").replace("\n", " ")
left_trimmed = newline_normalized.lstrip()
candidate_turn = left_trimmed.rstrip()
cr_count = source_turn.count("\r")
lf_count = source_turn.count("\n")
leading_removed = len(newline_normalized) - len(left_trimmed)
trailing_removed = len(left_trimmed) - len(candidate_turn)
```

The no-argument `lstrip` and `rstrip` calls use that interpreter's Unicode
whitespace semantics, and the counts are Unicode code points. No Unicode
normalization, internal whitespace collapse, case change, or other text
transform is permitted. A `candidate_turn` that is empty makes the event
structurally invalid and excludes it before the eligible inventory freezes or
any outcome label is created.

Prefix alternating `candidate_turn` values with exactly `USER: ` and `SYSTEM: `,
starting with `USER: `, join them with one LF, and add no trailing LF. Call
maintained `parse_transcript` exactly once on that complete framed string with
`round_strategy="cycle"` and the frozen run's one authenticated `CanonLoader`.
The parser must return exactly the source turn count, alternating `USER` /
`SYSTEM` speakers, and `Turn.text` values equal to the frozen `candidate_turn`
values. A nonempty transform/framing/parser mismatch stops the whole experiment
incomplete as `parser-reconciliation-mismatch`, whether detected before or
after inventory freeze; it is never a rowwise exclusion. Speaker prefixes are
framing and must not remain in `Turn.text` or its tokens. Ignore the parser's
cycle-grouped `rounds` for this candidate.

The following are candidate non-inputs:

- human outcome labels, rater notes, and rubric decisions;
- source dialogue-act labels and payloads;
- goals, turn metadata, ontology, and domain databases;
- the next user turn and every later turn;
- partition identity, test membership, and custody secrets.

For each parsed turn at zero-based position `i`, construct exactly
`Round(index=i, turns=[parsed.turns[i]])`. Apply the existing `compute_round`
equations unchanged to those one-turn rounds with `alpha = 0.85` and
`delta_max = 0.30`. This turnwise policy belongs only to this candidate; it does
not alter the maintained cycle-grouped baseline.

Process the constructed rounds chronologically with initial stored tension
`kappa_0 = 0` and initial previous entropy `0`. Each one-turn round becomes the
next call's `prev_round`; stored tension and previous entropy advance exactly
once per turn. Parsing turns separately, passing a one-line prefixed transcript
to the parser, using parser-produced cycle rounds, retaining prefixes as tokens,
or calling a different round strategy is forbidden.

### 4.3 Frozen score

Let `kappa_pre` be stored tension immediately after the user turn directly
preceding the target response. Let `kappa_post` be stored tension after one
additional circuit step on the target system response.

```text
release = kappa_pre - kappa_post
score   = (1 + release) / 2
```

Because both tension states must lie in `[0,1]`, `release` must lie in
`[-1,1]` and `score` in `[0,1]`. Higher score means greater response-induced
tension release. Missing turns, empty parsing, non-finite values, state values
outside their declared ranges, a missing event output, an extra or unexpected
event-output row, a duplicate event-output row, or an out-of-range score are
administrative or integrity nonconformance: they fail closed with an incomplete
status and are not scientific falsification. Equal numeric score values on
distinct admitted events are permitted and are not duplicates. No post-hoc
sign inversion is permitted.

There is no fitted development model. Validation selects one operating
threshold from `{0, 1, each distinct observed validation score, each midpoint
between adjacent distinct observed scores}` by maximum balanced accuracy.
Convert every binary64 score to `Fraction(*score.as_integer_ratio())`; `0` and
`1` are exact rationals, and each midpoint is the exact rational mean of its
two adjacent score fractions. A row predicts `resolved = 1` if and only if its
exact score fraction is greater than or equal to the exact selected threshold;
otherwise it predicts `resolved = 0`. This comparator governs every candidate
threshold, the selected validation confusion matrix, and the sealed test,
including scores exactly equal to the threshold. Rank balanced accuracy using
exact count-derived rational values. Ties resolve first by exact rational
distance from `1/2`, then by the lower exact rational threshold. The signed
threshold configuration records the reduced nonnegative numerator and positive
denominator; no binary64 rounding of a midpoint or threshold is permitted.
This is the only allowed data-dependent choice.

After selection, serialize exactly this configuration with the section 6.1
canonical-JSON rule; quoted count and rational fields are unsigned decimal
strings without leading zeros, and all fractions are reduced:

```python
{
  "schema": "edcm.response-tension-release-threshold/1",
  "packet_sha256": packet_sha256,
  "candidate_id": "edcm.response-tension-release/0.1.0",
  "validation_manifest_sha256": validation_manifest_sha256,
  "validation_score_inventory_sha256": validation_score_inventory_sha256,
  "candidate_threshold_count": str(candidate_threshold_count),
  "threshold_numerator": str(threshold.numerator),
  "threshold_denominator": str(threshold.denominator),
  "balanced_accuracy_numerator": str(validation_ba.numerator),
  "balanced_accuracy_denominator": str(validation_ba.denominator),
  "true_positive": str(TP),
  "false_negative": str(FN),
  "true_negative": str(TN),
  "false_positive": str(FP),
  "comparator": "Fraction(*score.as_integer_ratio())>=threshold",
  "selection": "max-ba;min-abs-threshold-minus-1/2;min-threshold"
}
```

Define

```python
threshold_configuration_sha256 = sha256(
    b"edcm.response-tension-release:threshold:v1\x00"
    + threshold_configuration_bytes
).hexdigest()
```

The named candidate implementer signs this exact payload with its frozen
role-manifest key:

```python
b"edcm.response-tension-release:threshold-signature:v1\x00" \
+ bytes.fromhex(packet_sha256) \
+ bytes.fromhex(threshold_configuration_sha256)
```

The custodian verifies that signature, digest, validation manifest,
score-inventory digest, exact gate verdict, and policy before any test access.

### 4.4 Score-inventory commitment

Every development, validation, and test score inventory uses one frozen digest
rule. Sort admitted rows by their lowercase 64-hex event digest; duplicate
event digests fail closed. For each row, encode
`event_digest + TAB + float.hex(score) + LF` as ASCII, where `score` is the
final finite IEEE-754 binary64 candidate score. Concatenate the rows without a
header and record the SHA-256. The digest may leave custody; the sealed test
rows, event digests, and scores may not.

### 4.5 Whitespace-loss commitment

The custodian commits every admitted presentation-transform loss without
publishing source text or row identities. Order events by lowercase 64-hex
event digest and turns by zero-based source index. For every turn, encode

```text
event_digest + TAB + decimal(turn_index) + TAB +
sha256(source_turn.encode("utf-8", errors="strict")).hexdigest() + TAB +
sha256(candidate_turn.encode("utf-8", errors="strict")).hexdigest() + TAB +
decimal(cr_count) + TAB + decimal(lf_count) + TAB +
decimal(leading_removed) + TAB + decimal(trailing_removed) + LF
```

as ASCII. Duplicate event digests, missing turn indexes, or non-contiguous
indexes fail closed. Hex digests are lowercase. Every decimal field is
unsigned base-10 ASCII without leading zeros, with zero encoded exactly as
`0`.

The global pre-label transform-loss ledger contains those rows for every
post-domain eligible event, ordered as above and concatenated without a header.
It freezes with the eligible inventory before the allocation-seed commitment:

```python
global_transform_loss_ledger_sha256 = sha256(
    b"edcm.response-tension-release:transform-loss:v1\x00"
    + global_transform_loss_ledger_bytes
).hexdigest()
```

After allocation, each partition ledger is the exact row projection for the
events in that signed partition manifest, with unchanged row bytes and the same
order. Using the section 6.4 partition token, define

```python
partition_transform_loss_ledger_sha256 = sha256(
    b"edcm.response-tension-release:partition-transform-loss:v1\x00"
    + partition_token.encode("ascii")
    + b"\x00"
    + partition_transform_loss_ledger_bytes
).hexdigest()
```

The global and each partition provenance record ledger digest, row/event
counts, turns affected by CR, LF, leading trim, and trailing trim, plus total
CR/LF replacements and leading/trailing code points removed. Partition counts
must equal exact projections from the global artifact and partition manifest;
the independent verifier recomputes them. Digests and aggregate counts may
leave custody; ledger rows, raw padding, event digests, per-turn digests, and
source text joined to hidden membership may not.

## 5. Human outcome-label authority

The source dialogue action locates a candidate event but has no outcome-label
authority. Authority belongs to an independent human panel operating under a
signed, frozen manual.

For one active explicit booking request:

- `resolved = 1` when the target response correctly completes and confirms the
  requested action, or correctly establishes that it cannot be completed and
  supplies the minimum usable next choice required to continue;
- `resolved = 0` when the response falsely claims completion, omits an active
  constraint, refuses or offloads without a valid necessity, contradicts the
  authoritative record, or otherwise leaves the request unresolved;
- `not-adjudicable` when there are multiple inseparable active requests,
  insufficient authoritative evidence, malformed source structure, or
  irreducible ambiguity. These events are excluded and counted before
  allocation.

Raters may inspect the full context through the response, the source goal,
relevant turn metadata and database state, and the immediately following user
turn when available. These label-only materials never enter the candidate.

The label-manual author, training-example author, label authority, both raters,
and the adjudicator must be independent of the candidate author, every
candidate designer or implementer, the external custodian, and the independent
allocation verifier. Before the manual or examples are created, a signed role
manifest freezes those exclusions and permanently bars those people from
candidate design, implementation, custody, or allocation verification for this
experiment. They must not compute, inspect, receive, or order any source row by
a candidate score. Training examples must be digest-excluded from the source
frame before eligibility is frozen. Every source-derived training example
excludes its whole dialogue. Put its exact `dialogue_id` in a sealed list,
reject duplicates, sort strings by their strict UTF-8 bytes, and serialize the
list with the section 6.1 canonical-JSON rule. Synthetic examples add no list
entry. The empty list is exactly `[]`. Define

```python
training_example_exclusion_manifest_sha256 = sha256(
    b"edcm.response-tension-release:training-example-exclusions:v1\x00"
    + training_example_exclusion_manifest_bytes
).hexdigest()
```

The training-example author and label authority sign that digest and exact
canonical-list identity before source inventory construction. The sealed list
is available only to the custodian and independent verifier; its digest and
count may leave custody.

Two raters label every event independently while blinded to candidate scores
and partition membership. If either rater assigns `not-adjudicable`, the event
is excluded and counted; the adjudicator may not promote it into the experiment.
The third adjudicator resolves only disagreements where both original ratings
are binary.

The allocation-controlling label artifacts have exact schemas. Tokens are
ASCII `resolved`, `unresolved`, and `not-adjudicable`. In ascending binary
event-digest order, the pre-adjudication ledger contains exactly one row for
every post-domain eligible event:

```text
event_digest + TAB + rater_1_token + TAB + rater_2_token + LF
```

The post-adjudication allocation projection also contains exactly one row for
every such event:

```text
event_digest + TAB + final_token + LF
```

Their domain-separated digests are

```python
pre_adjudication_label_ledger_sha256 = sha256(
    b"edcm.response-tension-release:pre-adjudication-labels:v1\x00"
    + pre_adjudication_label_ledger_bytes
).hexdigest()
post_adjudication_label_projection_sha256 = sha256(
    b"edcm.response-tension-release:post-adjudication-labels:v1\x00"
    + post_adjudication_label_projection_bytes
).hexdigest()
```

Each rater signs the exact pre-ledger signature payload, and the adjudicator
and named human label authority each sign the exact post-projection payload:

```python
b"edcm.response-tension-release:label-signature:v1\x00" \
+ bytes.fromhex(packet_sha256) \
+ bytes.fromhex(eligible_inventory_sha256) \
+ bytes.fromhex(label_artifact_sha256)
```

Each signer uses the key and signature scheme frozen in the role manifest.
Signatures, keys, and role identities are separate envelope fields, never
bytes inside the ledger or projection. Every eligible event must occur exactly
once in both artifacts. If either pre-ledger token is `not-adjudicable`, the
post token must be `not-adjudicable`; otherwise a binary agreement carries
through and a binary disagreement must equal the third adjudicator's decision.
Every `not-adjudicable` event is excluded before allocation. Every allocated
manifest event must have the same `resolved` or `unresolved` token in the
signed projection. Missing, extra, duplicated, reordered, or unreconciled rows
stop incomplete. Rich rater notes and the adjudicator's working ledger remain
separately sealed and cannot override this projection.

Before adjudication, two separate reliability gates must both pass. On the
complete paired three-category ledger, raw agreement must be at least `0.80`
and unweighted Cohen's kappa at least `0.70`. On the complete subset where both
raters assigned `resolved` or `unresolved`, binary raw agreement must also be at
least `0.80` and binary unweighted Cohen's kappa at least `0.70`. The binary
subset, its counts, and both statistics freeze before any binary disagreement
is adjudicated; an empty subset or undefined kappa fails. These calculations
occur before exclusion or allocation. Failure stops the experiment; the manual
may not be repaired after viewing agreement or candidate results. The signed
post-adjudication allocation projection is controlling. Candidate code has no
authority to change it.

All agreement and kappa arithmetic is exact from integer contingency counts.
For each gate, `p_o = diagonal_count / n`,
`p_e = sum(row_total[i] * column_total[i]) / n**2`, and
`kappa = (p_o - p_e) / (1 - p_e)` as reduced rationals; `1 - p_e = 0` is
undefined and fails. Compare raw agreement to exactly `4/5` and kappa to
exactly `7/10`, never to rounded binary64 values. The signed gate evidence
records each contingency count and every reduced numerator/denominator.

That gate evidence is one section 6.1 canonical-JSON object with schema
`edcm.response-tension-release-reliability-gate/1`, `packet_sha256`,
`eligible_inventory_sha256`, and
`pre_adjudication_label_ledger_sha256`; category order
`["resolved","unresolved","not-adjudicable"]`; the full `3x3` contingency
matrix with rater 1 as rows and rater 2 as columns; binary category order
`["resolved","unresolved"]`; the complete-subset `2x2` matrix; both population
counts; exact raw-agreement and kappa values; exact `4/5` and `7/10` minima;
separate raw-agreement/kappa verdict Booleans for both populations; and one
`all_pass` Boolean. Counts serialize as unsigned decimal strings. Every
rational serializes as
`{"numerator":"<reduced signed decimal>","denominator":"<positive decimal>"}`;
matrix cells are unsigned decimal strings. Define

```python
reliability_gate_sha256 = sha256(
    b"edcm.response-tension-release:reliability-gate:v1\x00"
    + reliability_gate_bytes
).hexdigest()
```

After both raters sign the immutable pre-adjudication ledger, the named label
authority signs this gate digest with its role-manifest key. Only a signed
`all_pass = true` object authorizes adjudication. The verifier independently
recomputes the object and signatures from the primary pre-ledger.

## 6. Source frame and partitions

The initial source frame is the exact MultiWOZ 2.1 archive identified above.
Every dialogue in the Cambridge `testListFile.json` used by PR #49 is excluded
entirely. The exclusion-list member SHA-256 is
`56fff5bf8c7b0a64fba8672241a7bdd947c3a58986bf06f46d37f33288f73ce0` and
its exact archive member path is `MULTIWOZ2.1/testListFile.json`.

### 6.1 Source event and event-digest construction

The admitted archive members are fixed as follows:

| Member | SHA-256 |
|---|---|
| `MULTIWOZ2.1/data.json` | `cb88bd0070bf11b04974cee54c84ad16cfee723c86b096bea04d2cebad098d58` |
| `MULTIWOZ2.1/dialogue_acts.json` | `54d02ef40aed0e00e5aa84b62ccf7f23df901d07f54c2376d5e8130909c2546f` |

The exact top-level `data.json` key is `dialogue_id`, preserving case, Unicode,
and a literal `.json` suffix. For source-act lookup only, remove that suffix
when it is exact. Use the full key when present and otherwise the
suffix-removed key. If both exist and their canonical JSON bytes differ, stop
incomplete; if they are identical, use the full key. A missing source-act
dialogue mapping excludes the whole dialogue as
`missing-source-act-dialogue`; a non-mapping value excludes it as
`nonmapping-source-act-dialogue`.

Within each remaining source-train or source-validation dialogue, validate the
source-act dialogue mapping and every source-turn key and value before
candidate selection. Every source-turn key must be a JSON string matching
ASCII `^[1-9][0-9]*$`; parse it in base ten as `k`, require the original string
to equal `str(k)`, and reject any two keys that map to the same integer. A key
violation excludes the whole dialogue as `noncanonical-source-turn-key`; a
non-mapping turn value excludes it as `nonmapping-source-turn-value`. Among
the remaining canonical source-turn mappings, let a Booking candidate be any
mapping containing at least one of the exact keys `Booking-Book` and
`Booking-NoBook`. No candidate excludes the dialogue as
`no-booking-locator`. Otherwise sort candidates by numeric `k` and select the
lowest exactly once. The selected mapping must contain exactly one of the two
generic keys; neither or both excludes the whole dialogue as
`invalid-booking-locator`. Derive `response_log_index = 2*k - 1` and apply the
exact section 4.2 source-dialogue/log/turn/text extraction. Any missing,
out-of-range, malformed, non-string, non-UTF-8, or parity/target mismatch is the
experiment-wide `source-turn-schema-mismatch` stop, not a dialogue exclusion.
There is no scan for a later replacement after the lowest candidate is
selected. The generic Booking key locates an event only; it has no human
outcome-label authority and is excluded from the event digest.

Apply those six typed whole-dialogue exclusions in the order stated above
and record only the first applicable reason. No event digest is constructed
for them. They belong to the source-schema exclusion summary below. A mismatch
between a derived locator and the frozen source bytes is instead an
experiment-wide integrity stop.

Before transform, domain assignment, any human label, seed generation, or
score, construct exactly this JSON object:

```python
{
  "archive_sha256": "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e",
  "data_member": "MULTIWOZ2.1/data.json",
  "data_member_sha256": "cb88bd0070bf11b04974cee54c84ad16cfee723c86b096bea04d2cebad098d58",
  "dialogue_acts_member": "MULTIWOZ2.1/dialogue_acts.json",
  "dialogue_acts_member_sha256": "54d02ef40aed0e00e5aa84b62ccf7f23df901d07f54c2376d5e8130909c2546f",
  "dialogue_id": dialogue_id,
  "response_log_index": 2*k - 1,
  "schema": "edcm.response-tension-release-event/1",
  "source_turn_id": k
}
```

The two index fields serialize as JSON integers, not strings. Canonical bytes
are strict UTF-8 encoding of
`json.dumps(object, ensure_ascii=False, allow_nan=False, sort_keys=True,
separators=(",", ":"))`, with no BOM or trailing LF. Then:

```python
event_digest = sha256(
    b"edcm.response-tension-release:event:v1\x00" + canonical_bytes
).hexdigest()
```

The digest is lowercase 64-hex and is the sole event identity used by every
loss, deduplication, domain, score, bootstrap, allocation, and partition
artifact. Outcome, generic Booking key, booking domain, candidate input,
candidate score, packet digest, seed, and partition are forbidden digest
fields. A digest or locator mismatch against the frozen source bytes, or a
duplicate event digest, stops incomplete before labels. After the lowest
candidate is selected, an empty post-transform turn is the one typed transform
exclusion; any other transform/framing/parser mismatch is the experiment-wide
stop above. Deduplication, domain, and label exclusions then apply exactly as
specified, and no later Booking response from that dialogue may replace it.

### 6.2 Transform, deterministic deduplication, and loss record

Every source turn through the target response must remain nonempty under the
section 4.2 transform and pass its framing/parser reconciliation. An empty turn
is excluded as `empty-after-normalization`; any nonempty transform/framing/
parser mismatch stops the entire experiment incomplete as
`parser-reconciliation-mismatch`, with no rowwise exclusion or fallback. After
old-test and training-example
exclusions, lowest-event selection, transformation, and structural/parser
validation—but before domain assignment, labels, seed, or scoring—encode the
complete framed candidate input as strict UTF-8 and compute:

```python
framed_input_digest = sha256(
    b"edcm.response-tension-release:framed-input:v1\x00" + framed_bytes
).hexdigest()
```

Group on exact `framed_bytes`, not merely the digest. Unequal byte strings with
one digest stop incomplete as `framed-input-digest-collision`. The sole group
representative is the event having minimum `bytes.fromhex(event_digest)`;
source iteration, domain, labels, goals, metadata, scores, and partition state
cannot participate. Every other member is excluded as
`duplicate-framed-input-nonrepresentative`. A discarded member can never
replace its representative if that representative is later excluded,
not-adjudicable, or unavailable; the inventory must fill from other unique
groups or stop incomplete.

The custodian freezes one sealed deduplication ledger covering every
pre-deduplication event, including singletons. Each ASCII row is:

```text
framed_input_digest + TAB + representative_event_digest + TAB +
member_event_digest + TAB + ("representative" or "discarded") + LF
```

Rows sort by `(bytes.fromhex(framed_input_digest),
bytes.fromhex(member_event_digest))`. There is no header. Exactly one
representative exists per group and status equals whether member and
representative digests match. The ledger digest is
`sha256(b"edcm.response-tension-release:dedup-ledger:v1\x00" +
concatenated_rows).hexdigest()`. Duplicate rows or identities fail closed.
Provenance must reconcile `pre_dedup_count = retained_count + discarded_count`,
ledger rows to `pre_dedup_count`, and duplicate exclusions to
`discarded_count`. Raw rows remain sealed; only the ledger digest and aggregate
counts may leave custody.

### 6.3 Frozen booking-domain assignment and inventories

The ordered booking-domain taxonomy is exactly `hotel < restaurant < train`,
the three booking domains used by the source's
[official preprocessing](https://github.com/budzianowski/multiwoz/blob/master/create_delex_data.py).
For a retained representative, the sole domain authority is the set of exact
act-key prefixes in that same selected `dialogue_acts.json` source-turn
mapping: `Hotel-` maps to `hotel`, `Restaurant-` to `restaurant`, and `Train-`
to `train`. Repeated acts in one domain count once. Ignore `Booking-*`,
`general-*`, and every other prefix and do not inspect act payloads, dialogue
goals, `data.json` metadata, databases, text, or neighboring turns. Exactly one
recognized domain assigns the event. None excludes it as
`booking-domain-absent`; more than one excludes it as
`booking-domain-ambiguous`. Non-mapping source turns were already excluded at
the whole-dialogue source-schema stage; encountering one here is an inventory/
source mismatch and stops incomplete. There is no precedence, fallback,
pooling, or reclassification.
Domain is locator/stratification metadata only and never candidate input or
human outcome authority.

If the earliest selected event is excluded by this domain rule, no later
Booking response from that dialogue may replace it.

For every post-domain eligible event, encode
`event_digest + TAB + domain + LF` as ASCII and sort by event digest. The direct
SHA-256 of concatenated rows is `eligible_inventory_sha256`; this same artifact
and digest are also the domain-assignment ledger. For every valid-locator event
excluded before human labeling, encode
`event_digest + TAB + exact_reason_code + LF`, sort by event digest and reason,
and SHA-256 the direct concatenation as `exclusion_inventory_sha256`. There is
no header, every row ends LF, and SHA-256 of no rows is SHA-256 of empty bytes.
The only source-schema summary keys, in their precedence order, are the exact
ASCII strings `missing-source-act-dialogue`,
`nonmapping-source-act-dialogue`, `noncanonical-source-turn-key`,
`nonmapping-source-turn-value`, `no-booking-locator`,
and `invalid-booking-locator`. Include only keys whose counts are positive JSON
integers; zero and negative values, unknown
keys, and alternate spellings fail closed. With no such exclusions the object
is exactly `{}`. Serialize it by the section 6.1 canonical-JSON rule and define

```python
source_schema_exclusion_summary_sha256 = sha256(
    b"edcm.response-tension-release:source-schema-exclusions:v1\x00"
    + source_schema_exclusion_summary_bytes
).hexdigest()
```

All identities are unique. The eligible, exclusion, source-schema,
training-example-exclusion, and deduplication digests and their counts freeze
before the allocation seed commitment and before any human label.

### 6.4 Seed commitment, exact allocation, and independent audit

The custodian draws exactly one 32-octet CSPRNG seed. With every named field a
lowercase 64-hex SHA-256 decoded to 32 bytes, the pre-label commitment is:

```python
sha256(
    b"edcm.response-tension-release:allocation-seed:v1\x00"
    + bytes.fromhex(packet_sha256)
    + bytes.fromhex(allocation_code_sha256)
    + bytes.fromhex(allocation_verifier_code_sha256)
    + bytes.fromhex(eligible_inventory_sha256)
    + bytes.fromhex(exclusion_inventory_sha256)
    + bytes.fromhex(source_schema_exclusion_summary_sha256)
    + bytes.fromhex(training_example_exclusion_manifest_sha256)
    + bytes.fromhex(dedup_ledger_sha256)
    + bytes.fromhex(global_transform_loss_ledger_sha256)
    + seed
).hexdigest()
```

The signed pre-label release records that formula/version, commitment, bound
digests, and counts, but never seed or membership. After adjudication, define
available count `A[y,d]` for outcome `y` and domain `d`. For each outcome and
each partition independently in fixed order development `N=150`, validation
`N=100`, test `N=200`, let `T = sum_d A[y,d]`, `num = N*A[y,d]`,
`base = num // T`, and `remainder = num % T`. Give the
`N - sum_d base` residual seats to descending remainder, ties in domain order
`hotel < restaurant < train`. Use integers only. Compute all quotas before
assignment; if `T=0` or cumulative demand for any outcome-domain exceeds its
available count, stop incomplete without redistribution.

For each event, compute exactly:

```python
tag = hmac.new(
    seed,
    b"edcm.response-tension-release:allocation:v1\x00"
    + bytes.fromhex(event_digest),
    hashlib.sha256,
).digest()
```

Within each outcome-domain, order by `(tag, bytes.fromhex(event_digest))` and
take consecutive quota slices in development, validation, test order; unused
remainder is unallocated. The only outcome tokens are ASCII `resolved` for
`y=1` and `unresolved` for `y=0`; the only partition tokens are ASCII
`development`, `validation`, and `test`. Hidden manifest rows are
`event_digest + TAB + outcome_token + TAB + domain + TAB + tag.hex() + LF`,
ordered within each partition by outcome `resolved < unresolved`, then the
fixed domain order, then `(tag,event_digest)`. For each partition, concatenate
those ASCII rows without a header and define

```python
partition_manifest_sha256 = sha256(
    b"edcm.response-tension-release:partition-manifest:v1\x00"
    + partition_token.encode("ascii")
    + b"\x00"
    + partition_manifest_bytes
).hexdigest()
```

The custodian signs each partition token, schema/version, row count, and exact
manifest digest before development release. Empty, extra, duplicate,
misordered, or token-invalid rows fail closed. There is no seed trial, retry,
replacement, adaptive quota, or manifest substitution.

A named independent allocation verifier must be legally and operationally
separate from the custodian, repository writers, candidate team, manual and
training authors, label authority, raters, and adjudicator; it records identity,
conflict attestation, the associated supervisor/HSM allocation-audit public-key
fingerprint without verifier access to its private key or handle,
confidentiality terms, and no-retention terms. After adjudication and allocation but before any development release,
the verifier receives one-time read-only access inside a custodian-controlled,
network-disabled enclave to the raw seed; the authenticated source archive and
exact admitted members; the Cambridge old-test exclusion artifact at
`MULTIWOZ2.1/testListFile.json`; the signed
training-example exclusion manifest; frozen source, transform, deduplication,
domain, and exclusion ledgers; the signed pre-adjudication ledger and signed
post-adjudication allocation projection; quota inputs; independently frozen
verifier executable; and hidden manifests. Every primary artifact is mounted
read-only with its packet-bound path, byte digest, and signature where
applicable. The verifier executable may not import, invoke, copy, or treat the
allocator or any allocator-derived ledger as authoritative. Starting from the
authenticated primary archive, exclusion artifacts, label artifacts, and raw
seed, it independently derives and compares every event and framed-input
digest, representative, exclusion, domain, retained outcome-domain stratum,
commitment opening, HMAC tag, integer quota, allocation, collision check,
ordered manifest byte string, and domain-separated manifest digest. It also
verifies every label-artifact and manifest signature and the one-to-one label/
eligible/manifest reconciliation.

The verifier then emits canonical public zero-disclosure audit-receipt bytes containing all
bound identities and digests, including the archive and admitted-member
digests, old-test exclusion path/digest, training-example exclusion manifest,
both signed label-artifact digests, every primary-ledger/code digest, and every
partition-manifest schema/token/digest. It also contains the timestamp,
verifier legal identity/code digest, custody-supervisor identity, allocation-
audit HSM public-key fingerprint, access-log digest, no-retention attestation,
and booleans
`seed_opening_verified = true` and `allocation_recomputed = true`. It contains
no seed, source row, label, event ID, score, or membership. Raw seed remains at
rest only with the custodian; the verifier's temporary enclave access is the
sole exception to exclusive handling. Define:

```python
allocation_audit_receipt_sha256 = sha256(
    b"edcm.response-tension-release:allocation-audit-receipt:v1\x00"
    + allocation_audit_receipt_bytes
).hexdigest()
allocation_audit_receipt_file_sha256 = sha256(
    allocation_audit_receipt_bytes
).hexdigest()

allocation_audit_signature_claims = {
    "schema": "edcm.response-tension-release-allocation-audit-signature-claims/1",
    "supervisor_legal_identity": supervisor_legal_identity,
    "hsm_service_legal_identity": hsm_service_legal_identity,
    "hsm_key_handle_identity": allocation_audit_hsm_key_handle_identity,
    "public_key_fingerprint": allocation_audit_public_key_fingerprint,
    "signature_scheme": allocation_audit_signature_scheme,
    "verifier_legal_identity": verifier_legal_identity,
    "verifier_file_sha256": verifier_file_sha256,
    "captured_stdout_sha256": allocation_audit_receipt_file_sha256,
    "process_topology": allocation_audit_process_topology,
    "allocator_and_runner_modules_absent": True,
    "verifier_private_key_or_hsm_access_absent": True,
    "timestamp_rfc3339_utc": timestamp_rfc3339_utc,
}

allocation_audit_signature_claims_sha256 = sha256(
    b"edcm.response-tension-release:allocation-audit-signature-claims:v1\x00"
    + canonical_json_bytes(allocation_audit_signature_claims)
).hexdigest()

allocation_audit_signature_payload = (
    b"edcm.response-tension-release:allocation-audit-signature:v1\x00"
    + bytes.fromhex(packet_sha256)
    + bytes.fromhex(verifier_file_sha256)
    + bytes.fromhex(allocation_audit_bootstrap_sha256)
    + bytes.fromhex(allocation_audit_receipt_sha256)
    + bytes.fromhex(allocation_audit_signature_claims_sha256)
)
```

The supervisor compares the ordinary captured-stdout SHA-256 and independently
derives the domain-separated receipt digest from those same bytes,
then asks the allocation-audit HSM handle to sign exactly that payload. The
detached envelope contains exactly the five digest inputs, complete canonical
claims object/claims digest, and signature; the verifier process has no signing
handle. `allocation_audit_process_topology` uses the exact topology schema and
ordering above. Missing or invalid audit receipt,
commitment mismatch, alternate seed, ledger/code/quota/manifest mismatch,
verifier conflict, disclosure, retention, or access breach stops incomplete
before development. No repair or reseed is permitted under this packet.

| Partition | Positive | Negative | Total | Permitted use |
|---|---:|---:|---:|---|
| Development | 150 | 150 | 300 | Extractor conformance and frozen go/no-go only; no formula or direction change |
| Validation | 100 | 100 | 200 | Select the single threshold and freeze its digest |
| External sealed test | 200 | 200 | 400 | Exactly one aggregate evaluation after all freezes |

If the exact inventories cannot be filled without changing eligibility or
reusing a dialogue, execution stops incomplete. Because allocation is
class-balanced, this experiment makes no prevalence, probability-calibration,
Brier-score, or expected-calibration-error claim.

## 7. Freeze and execution order

1. Freeze and digest this packet.
2. Name and sign the manual author, training-example author, label authority,
   raters, adjudicator, candidate author/implementer, external custodian, and
   independent allocation-verifier, custody-supervisor/runtime-attestation-
   signer, and HSM-service role manifests, separately scoped public keys/
   handles, and every exclusion above.
3. Before any real source row is processed, freeze the candidate runner,
   inventory, allocation, and independently implemented verifier executables;
   sections 4.1.1–4.1.3 two-root runtime attestations; dependency lock; derived
   network-disabled container; independently reproduced twice and externally
   signed runtime-state manifest/envelope; protected/mutable/atomic-temporary
   path and exclusive-output-mount manifest/preflight; synthetic-only
   conformance results; and every implementation commit/tree/blob/file digest.
4. Author and freeze the manual, digest-excluded training examples, and signed
   training-example exclusion manifest while score-blind. Candidate,
   inventory, allocation, and verifier bytes remain frozen.
5. Only now construct and freeze event locators, transform/loss evidence, the
   complete deduplication ledger, deterministic representatives, domain
   assignments, eligible and exclusion inventories, source-schema summary,
   and every count. Generate the one 32-octet seed and publish its signed
   commitment over all section 6.4 identities before any label exists.
6. Both raters label every eligible event, freeze and separately sign the exact
   pre-adjudication ledger, and make no further change. Compute and sign the
   exact reliability-gate object from that ledger; both gates must pass before
   the adjudicator sees a binary disagreement. Only then exclude every row
   with either `not-adjudicable` rating, adjudicate the remaining binary
   disagreements without candidate scores or partition identities, and have
   the adjudicator and label authority sign the frozen post-adjudication
   allocation projection.
7. Only after those signatures, allocate exactly once; commit the encrypted
   bundle, access log, ordered hidden partition manifests, and exact
   per-partition projections of the global transform-loss ledger. The
   independent verifier verifies every label/gate/manifest signature and
   digest, recomputes every retained outcome-domain stratum, commitment
   opening, quota, HMAC assignment, manifest, and transform-loss projection,
   and emits the canonical zero-disclosure receipt; the custody supervisor
   validates stdout and obtains its detached HSM signature before publication.
   All occur before
   any development release.
8. Release development rows and labels; run only the frozen development gate.
9. Release validation rows and labels; select the single threshold, construct
   and sign the exact section 4.3 threshold configuration, and freeze its
   domain-separated digest. Candidate code and container remain byte-identical.
10. Deliver that network-disabled immutable container, signed threshold
    configuration, and audit-receipt identity to the custodian. The custodian
    evaluates the sealed test twice internally, confirms both byte-identical
    aggregate bytes and ordered test score-inventory digests, then releases one
    signed aggregate report and completion receipt binding the allocation-audit
    receipt. Underlying per-event scores remain sealed.

There are no interim test looks, per-event disclosures, adaptive accrual,
sample extension, relabelling, threshold retry, feature addition, sign change,
or second candidate.

## 8. Preregistered hypotheses and decision rule

### Development gate

Before the scientific development gate, every admitted row must pass the
frozen source, framing, parser, state-range, and score-range conformance checks
and yield exactly one finite score in `[0,1]`. Admitted, produced, unique-event,
finite, and in-range counts must be equal. No row may be dropped, imputed,
clipped, or retried. A missing event output, extra or unexpected event-output
row, duplicate event-output row, non-finite or out-of-range score, or
structurally nonconforming row is an incomplete execution with reason
`invalid-development-score-output`, not evidence against the candidate; no
development gate verdict or AUC is computed. Conditional on complete
conformance, order the `n = 300` final IEEE-754 binary64 scores by event digest
and convert each exact value with `Fraction(*score.as_integer_ratio())`. With
exact rational `S = sum(x_i)` and `Q = sum(x_i*x_i)`, the controlling population
variance is

```text
V = (n*Q - S*S) / (n*n)
```

using rational arithmetic only. Reduce it to a coprime numerator and positive
denominator; zero is exactly `0/1`. Serialize this object under the packet's
canonical JSON rule:

```python
{
  "schema": "edcm.exact-binary64-population-variance/1",
  "n": "300",
  "numerator": "<unsigned decimal>",
  "denominator": "<positive unsigned decimal>",
  "gate": "numerator>0",
  "verdict": variance_numerator > 0
}
```

The expression for `verdict` serializes as a JSON Boolean. The quoted numeric
fields are canonical decimal strings without leading zeros. The
variance gate passes if and only if the exact numerator is positive. Sample
variance, epsilon, rounded decimal/binary64 variance,
`statistics.variance`, `statistics.pvariance`, or floating-point
`E[x^2] - E[x]^2` cannot decide it.

The exact variance must be non-zero and development area under the
receiver-operating-characteristic curve at least `0.55` in the declared
direction. Development AUC is the exact Mann–Whitney probability over every
positive-negative pair: a strictly greater positive score contributes `1`, an
equal score contributes `0.5`, and a lower score contributes `0`, divided by
the number of pairs. Compute it as the reduced exact rational
`(2*wins + ties) / (2*positive_count*negative_count)` and compare it to exactly
`11/20`; no binary64 or rounded decimal decides the gate. Exact zero variance
or sub-threshold AUC is a preserved development falsification and stops the
experiment before validation.

Every signed completion, `stopped-before-test`, or incomplete manifest must
contain a development compartment. Once development starts, it records
admitted, produced, unique-event, finite, and in-range counts plus the
source/framing/parser/state/score integrity verdict. A conforming run also
records the ordered score-inventory digest, variance schema, `n`, exact reduced
numerator/denominator, comparator and verdict, AUC method/value, declared
direction, gate thresholds, and gate verdict even when that verdict
stops the experiment. An invalid run records the offending-condition code,
`not-produced` for a score-inventory digest that cannot be formed from complete
canonical finite rows, and `not-evaluated` for variance, AUC, and the scientific
gate; it receives an incomplete status. If execution stops before development,
the same fields are present with typed `not-run` values and the prior stop
reason.

### Validation gate

Before threshold selection, every admitted validation row must pass the same
frozen source, framing, parser, state-range, and score-range conformance checks
and yield exactly one finite score in `[0,1]`; the five integrity counts must be
equal, with no row dropping, imputation, clipping, or retry. Any violation is
an incomplete execution with reason `invalid-validation-score-output`; it
records the admitted, produced, unique-event, finite, and in-range counts and
offending-condition code, types an unformable inventory digest as
`not-produced`, and leaves threshold selection and the scientific gate
`not-evaluated`. Conditional on complete conformance, balanced accuracy at
every candidate threshold is the exact rational
`((TP / P) + (TN / N)) / 2` from integer counts. At the selected threshold it
must be at least exactly `11/20`; exact sensitivity `TP/P` and specificity
`TN/N` must each be at least `1/2`. All selection, tie-breaking, and gate
comparisons use reduced rationals. The signed evidence records confusion counts
and reduced numerators/denominators. Failure of a conforming metric gate is a
preserved validation falsification and stops the experiment before test.

### Sealed-test hypotheses

Before any sealed-test metric, the custodian applies the same source, framing,
parser, state-range, row-count, event-identity, uniqueness, finiteness, and
score-range checks. Admitted, produced, unique-event, finite, and in-range
counts must be equal, with no dropping, imputation, clipping, coercion,
rescoring, or retry. Any mismatch is an invalid test execution under section 10;
the score-inventory digest is `not-produced` when complete canonical finite rows
cannot be formed, and every confusion count, point estimate, interval, AUC, and
scientific verdict is `not-evaluated`. Equal numeric score values on distinct
admitted test events remain permitted.

All three empirical hypotheses are co-primary and must pass:

1. **Discrimination:** the lower bound of the two-sided 95% balanced-accuracy
   interval is strictly greater than `0.50`.
2. **Sensitivity repair:** the lower bound of the two-sided 95% Wilson
   sensitivity interval is strictly greater than `0.50`.
3. **Specificity guardrail:** the lower bound of the two-sided 95% Wilson
   specificity interval is strictly greater than `0.50`.

The packet-local Wilson helper uses IEEE-754 binary64 operations in exactly the
shown Python evaluation order under the pinned interpreter/libm, with integer
`successes`, positive integer `total`, and no alternate continuity correction:

```python
z = 1.959963984540054
estimate = successes / total
denominator = 1.0 + z * z / total
centre = (estimate + z * z / (2.0 * total)) / denominator
half_width = (
    z
    * math.sqrt(
        estimate * (1.0 - estimate) / total
        + z * z / (4.0 * total * total)
    )
    / denominator
)
low = max(0.0, centre - half_width)
high = min(1.0, centre + half_width)
```

The method token is `wilson-score`, confidence is binary64 `0.95`, and support
is the exact integer `total`. Only `low` decides the two Wilson hypotheses.

Balanced accuracy uses a deterministic 10,000-replicate, outcome-stratified
dialogue bootstrap with seed `20260803`. Because eligibility admits at most one
event per dialogue, each test event is its dialogue cluster. Within each
outcome, the 200 clusters are ordered by event digest. One
`random.Random(20260803)` instance runs exactly 10,000 replicates; in each
replicate it draws 200 positive indices and then 200 negative indices with
replacement using `randrange(200)`. In replicate `j`, let integer `TP_j` be
the number of resampled positive scores at or above the frozen threshold and
integer `TN_j` the number of resampled negative scores below it. Store only
the exact integer `b_j = TP_j + TN_j`; the replicate balanced accuracy is the
exact rational `b_j / 400`, never binary64.

Sort the 10,000 integers into zero-based `b[0] <= ... <= b[9999]`. The linear
percentile rule uses exact `q_low = 1/40`, `q_high = 39/40`, and
`h = 9999*q`. Consequently the interval endpoints are exactly:

```python
ba_low_unreduced_num = b[249] + 39 * b[250]
ba_high_unreduced_num = 39 * b[9749] + b[9750]
ba_unreduced_den = 16000
```

Bind the complete sorted count inventory without releasing it row-wise:

```python
ba_bootstrap_counts_sha256 = sha256(
    b"edcm.response-tension-release:ba-bootstrap-counts:v1\x00"
    + b"".join(value.to_bytes(2, "big", signed=False) for value in b)
).hexdigest()
```

The concatenated count payload is exactly 20,000 bytes; each `value` must be an integer in
`0..400`, encoded in sorted order at fixed width two with no count prefix or
separator. Record the literal schema token
`edcm.response-tension-release-ba-bootstrap-counts/1`, digest, `replicates = 10000`,
`width_bytes = 2`, and `order = ascending-balanced-correct-count`.

Serialize each endpoint as the numerator and positive denominator reduced by
their integer greatest common divisor, while also recording the three
unreduced integers above. The discrimination gate is evaluated without a
float: `ba_low_unreduced_num > 8000`. Equality is failure. Any optional decimal
display is secondary and is computed only after the verdict as pinned-binary64
`reduced_numerator / reduced_denominator`; it cannot enter a comparison.
The observed test balanced-accuracy point estimate is likewise the exact
rational `(TP + TN) / 400`, reduced for serialization. No alternative seed,
draw order, stratification, percentile rule, arithmetic type, interpolation
order, rounding, or invalid-replicate filtering is permitted.
Confusion counts, point estimates, all intervals, validation results, and the
threshold must be reported whether the hypotheses pass or fail. Threshold-free
area under the receiver-operating-characteristic curve is secondary and cannot
rescue a co-primary failure.

If the balanced-accuracy interval touches or spans chance, sensitivity fails,
or specificity fails, the candidate is not experiment-supported. The result
is preserved as falsified or weak evidence. Scientific failure must serialize
successfully and must not be converted into a build failure.

## 9. External test custody

The custodian must be a named person or organization with:

- no write role in the EDCM repository;
- no role in candidate design, implementation, human labelling, or
  adjudication, and no role as the independent allocation verifier;
- a recorded legal identity, conflict disclosure, public-key fingerprint, and
  signed acceptance of this packet;
- exclusive at-rest control, after the signed allocation-projection handoff and
  allocation, of the joined test-membership-to-final-label mapping, sealed test
  manifest, per-event test scores, secret allocation seed, and encrypted
  source bundle, subject only to the verifier's one-time logged enclave access
  under section 6.4; the human panel may retain its signed blinded full ledger
  but never receives the seed or any partition manifest and therefore cannot
  identify the test subset;
- an append-only access log whose digest is included in the receipt.

The human panel creates the full blinded ledger and signed allocation
projection but never receives the
allocation seed or any partition manifest. After the signed ledger handoff,
the custodian alone executes the mapping; the independent verifier only
recomputes it in the enclave and cannot write or substitute a manifest. No
development material leaves custody until its signed zero-disclosure audit
receipt validates. The candidate implementer receives development and
validation material only. The custodian receives the immutable container by
digest, runs it without
network access, and releases no output until the two internal renders are
byte-identical. Only output from the sealed-test compartment consisting of
aggregate counts, metrics, intervals, identities, digests, status boundaries,
and an `hmmm` field may leave custody. This restriction does not revoke the
authorized, logged development and validation releases in steps 8 and 9. The
signed ordered test score-inventory digest leaves custody as provenance; its
underlying ordered scores do not.
The per-partition whitespace-loss ledger digests, deduplication-ledger digest,
allocation-audit receipt, and aggregate loss/deduplication counts may also
leave custody; their ledger rows, raw padding, event digests, and hidden
membership do not. The completion receipt binds the allocation-audit receipt
digest.

An operational retry is allowed only when the identical container and inputs
failed for a documented infrastructure reason before any metric was released.
The custodian must sign the incident and zero-disclosure statement. A changed
container, configuration, threshold, label, test manifest, or sample is a new
experiment version, not a retry.

## 10. Stopping and failure conditions

### Administrative or integrity stop before test — incomplete

- custodian, allocation verifier, label-authority, consent, licence, source, or
  runtime identity is missing;
- a role conflict, manual-author score exposure, verifier conflict/retention,
  or undisclosed source/test access exists;
- any real source row is processed before the runner, inventory, allocator,
  independent verifier, runtime/container, and synthetic conformance artifacts
  have frozen;
- PR #49 test membership or any predecessor test event enters the frame;
- the signed training-example exclusion manifest is absent, late, replaced,
  malformed, or does not exclude every source-derived example dialogue;
- a dialogue or exact-input digest crosses partitions;
- the agreement thresholds fail;
- either signed pre-adjudication ledger or post-adjudication allocation
  projection is absent, late, replaced, invalid, or inconsistent with the
  independently recomputed eligible identities, final labels, exclusions, or
  retained outcome-domain strata;
- adjudication begins before both rater signatures and a valid signed exact
  reliability-gate object with `all_pass = true` freeze;
- an event locator, canonical event digest, framed-input group, representative,
  deduplication/domain/exclusion ledger, source-schema summary, global or
  per-partition transform-loss ledger, inventory, quota, manifest, digest,
  signature, schema, projection, or provenance field fails to reconcile;
- a discarded duplicate is promoted after its representative is excluded;
- the pre-label seed commitment or independent audit receipt is absent, late,
  replaced, inconsistent, invalid, or fails to verify the one committed seed
  and actual hidden manifests;
- raw sealed-test source, per-event test label, per-event test score, event
  locator joined to hidden membership, or test membership is disclosed to an
  unauthorized role or written to Git/the aggregate report; public source
  bytes and authorized logged development/validation release are not a leak;
- frozen candidate/runtime identity, imported binding, interpreter/Unicode,
  base-image platform, or synthetic conformance fails before development
  release or drifts at a required re-verification point;
- the independently reproduced and signed runtime-state manifest/envelope is
  incomplete, late, mutable, self-generated by execution, non-byte-identical
  across its two clean builds, or inconsistent; any module inventory,
  code/default/annotation/globals/builtins state, recursive module/class mutable
  state, metaclass/base/MRO relation, namespace key, slot/descriptor,
  standard-library call-surface binding, receiver-type probe, cache-normalization
  verdict, stable reference resolution or
  identity equivalence, independently derived canon expectation/instance,
  trace/profile/global-or-local-monitoring event/callback state, shared import
  protocol, process/thread rule, or imported helper drifts;
- any mutable output or exact atomic-temporary path aliases another output or
  a protected code/input/ledger/manifest/threshold/represented-evidence path
  by canonical name, symlink, hard link, or existing inode; or the exclusive
  output mount, device separation, stabilized dirfd, permissions, link count,
  leaf inventory, no-concurrent-writer rule, or before/after checks drift;
- the exact source-dialogue/log/turn/text extraction or strict-UTF-8/parity
  contract fails as `source-turn-schema-mismatch`;
- a nonempty presentation-transform/framing/parser reconciliation fails at any
  point, or an event admitted to the eligible inventory contains an empty
  post-transform turn;
- development or validation row count, event identity, uniqueness, finiteness,
  or range fails to reconcile, including a missing event output, extra or
  unexpected event-output row, duplicate event-output row, non-finite score, or
  out-of-range score;
- a conforming development inventory uses any variance arithmetic or
  serialization other than the exact rational population rule in section 8;
- a reliability, AUC, threshold-ranking, validation-gate, or threshold-
  comparison decision uses rounded decimal or binary64 arithmetic instead of
  its frozen exact rational rule;
- the canonical threshold configuration, its signature, validation bindings,
  policy, digest, or custodian verification is absent or inconsistent before
  test access;
- an invalid row is dropped, imputed, clipped, coerced, rescored, or used in a
  scientific metric; repairing code or a container after such a failure
  requires a new experiment version and is not an operational retry;
- formula, direction, round policy, label manual, eligibility, partition size,
  threshold policy, metric, uncertainty method, dependency, or candidate code
  changes after its applicable freeze;
- test membership, labels, or aggregate results are disclosed before the
  authorized release.

### Preregistered gate stop — stopped-before-test

A completed, fully conforming development or validation gate that fails its
frozen scientific criterion is a valid negative stop, not an invalid
execution. It emits a signed `stopped-before-test` receipt containing the
controlling gate provenance and falsification reason; no sealed-test verdict
exists. Zero development-score variance, sub-threshold development AUC, or a
conforming validation metric below its threshold are gate failures under this
rule. Source, parser, state, or score nonconformance remains incomplete under
the preceding rule.

### Test scientific failure

A completed custody run that fails any co-primary hypothesis is a valid
scientific falsification. It receives a complete receipt with
`candidate_measurement_status = candidate-measured-evidence` and
`experiment_supported = false`.

### Invalid test execution

Byte mismatch between the two internal runs or their ordered test
score-inventory digests; custody breach, digest drift, or partition collision;
source-transform, parser, state, row-count, event-identity, uniqueness,
finiteness, or range nonconformance; a missing event output, extra or unexpected
event-output row, duplicate event-output row, non-finite or out-of-range sealed
test score; forbidden output; or an unauthorized retry invalidates the
execution. It receives an incomplete receipt, typed `not-produced` and
`not-evaluated` fields as applicable, and no empirical verdict.

## 11. Required provenance fields

The signed execution and completion manifests must record at least:

| Compartment | Required fields |
|---|---|
| Packet | schema, version, design status, file SHA-256, freeze timestamp, superseded-packet SHA-256, no-data-between-versions attestation, predecessor identities |
| Candidate | candidate ID, exact newline/edge-trim and framing rules, source/post-transform turn-digest and global/per-partition transform-loss ledger rules, digests and aggregate CR/LF/edge-loss counts, parser reconciliation verdict, single parser call and arguments, one-turn construction, formula, direction, `alpha`, `delta_max`, runner commit/tree/blob identities |
| Runtime | frozen PR #49 commit/tree, full `edcm` and controlling measurement trees, exact read-only `/opt/edcm-base` identity, exact three-file `/opt/experiment` commit/tree/file inventory and absence of a top-level `edcm`, exact shared import prefix and runtime/manifest-builder/allocation-audit bootstrap strings/digests/mode tokens, supervisor pre-exec and FD/mount/key-handle-absence verdicts, exact five-module reachable base set and no `edcm.corpora` import, parser/canon/metrics/stats/risk/resource blobs and loaded-file SHA-256 values, base-image platform manifest, interpreter executable digest, exact CPython/cache-tag/Unicode identities, locale/timezone/hash-seed/safe-path/no-user-site/`-S`/network policies, no trace/profile/global-or-local-monitoring event/callback, one-process/one-thread rule, lockfile, skill-lib, canonical runtime-state manifest/schema/digest and detached supervisor/HSM signer envelope, independent two-build byte-identity verdict, function/code/default/annotation/globals/builtins state, class metaclass/bases/MRO/descriptor payloads, recursive order-preserving mutable module/class state, exact receiver-specific builtin/stdlib call surface, receiver-type probes, `re` cache-normalization verdict, and reference-name resolution, stable named identity/code/closure equivalence classes, import origins, sole-provider, independently derived canon expected-state digest/actual-state verdict, and repeated-attestation verdicts |
| Source | owner, DOI/source URL, licence, consent/privacy decision, archive and exact data/dialogue-act member paths and digests, exact `MULTIWOZ2.1/testListFile.json` old-test exclusion path/digest, language, domain, collection period |
| Eligibility | locator and event-digest schemas/canonical-byte rule, exact source-dialogue/log/turn/text extraction and strict-UTF-8/parity verdict, source-schema reason precedence/counts/domain-separated summary digest, signed training-example exclusion manifest schema/digest/count, framed-input digest schema and collision verdict, deduplication schema/digest/row count, representative rule/no-promotion assertion, pre/retained/discarded and duplicate-group counts, complete duplicate exclusion count, post-dedup inventory, fixed domain taxonomy/source rule, absent/ambiguous/malformed counts, eligible/domain-ledger and exclusion-ledger digests/counts, global and per-partition transform-loss schemas/digests/counts/projection verdicts, `empty-after-normalization` exclusions, parser-reconciliation stop count |
| Labels | manual/training-example author and authority role IDs, manual and digest-excluded training-example identities, candidate-score-blinding assertions, allocation-verifier exclusions, conflicts, exact pre-ledger and post-projection schemas/tokens/order/digests/signatures, one-to-one reconciliation, complete `3x3` and binary `2x2` contingency counts, exact rational agreement/kappa values and minima, signed reliability-gate object/digest/verdict, exclusion counts, adjudicator identity |
| Partitions | allocation and independently implemented verifier code digests, commitment formula/version, signed pre-label seed commitment and every bound eligible/exclusion/source-summary/training-example/dedup/global-transform-loss digest/timestamp, exact strata counts, integer quota inputs/outputs/remainders/tie order, HMAC domain/message rule, exact outcome/partition tokens, ordered encrypted manifest schemas/domain-separated digests/counts/signatures, label-projection reconciliation, collision audit, verifier receipt digest and verdicts |
| Custody | custodian, independent verifier, custody-supervisor/runtime-signer, and HSM-service legal identities; conflict disclosures, separately scoped key-handle identities/public fingerprints, acceptance signatures, private-key/HSM-handle absence from builder/runtime, exact FD/mount/environment topology attestations, confidentiality/no-retention terms, signed ledger handoff, verifier read-only access to authenticated primary archive/members, old-test and training-example exclusions, both signed label artifacts, raw seed, and hidden manifests, allocator/verifier separation verdict, encrypted bundle digest, enclave and append-only access-log digests, exact mutable/final/atomic-temporary names and protected input/represented-evidence paths/digests, separate-output-mount `st_dev`/mode/ownership/no-writer assertions, stabilized directory-fd and before/after `fstat`/inventory verdicts, zero-disclosure audit receipt/signature, label/gate/manifest signature verification, outcome-domain and transform-loss projection recomputation, seed-opening, and allocation-recomputation booleans |
| Development | admitted, produced, unique-event, finite, in-range, missing-output, unexpected-output, duplicate-event-output, NaN, positive/negative-infinity, below-zero, and above-one counts plus integrity verdict; ordered score-inventory digest; exact binary64 population-variance schema, `n`, reduced numerator/denominator, event order, comparator and verdict; exact rational Mann–Whitney AUC numerator/denominator, direction, exact `11/20` minimum and verdict when conforming; typed `not-produced` digest and `not-evaluated` scientific fields with an incomplete reason when nonconforming, or typed `not-run` fields and prior stop reason; required in every completion, `stopped-before-test`, or incomplete manifest |
| Validation | admitted, produced, unique-event, finite, in-range, missing-output, unexpected-output, duplicate-event-output, NaN, positive/negative-infinity, below-zero, and above-one counts plus integrity verdict; score-inventory digest; exact-rational threshold candidate count/ranking/tie policy; reduced selected-threshold, sensitivity, specificity, and balanced-accuracy numerators/denominators; confusion counts; exact gate minima/verdicts; canonical threshold-configuration bytes/domain-separated digest/signature when conforming; typed `not-produced`, `not-evaluated`, or `not-run` fields with the controlling reason otherwise |
| Test | admitted, produced, unique-event, finite, in-range, missing-output, unexpected-output, duplicate-event-output, NaN, positive/negative-infinity, below-zero, and above-one counts plus source/framing/parser/state/score/runtime integrity verdict; before/after runtime attestations; verified threshold-configuration digest/signature and exact rational comparator; ordered score-inventory digest, confusion counts, Wilson method/order, bootstrap seed/draw order, sorted integer `b_j` digest, exact point balanced-accuracy fraction, unreduced/reduced percentile endpoint integers, exact `> 1/2` comparator, co-primary verdicts, and aggregate-byte/score-inventory-repeat verdicts when conforming; typed `not-produced` and `not-evaluated` fields plus incomplete reason when nonconforming; run nonce/timestamps and exact container/config digest in every reached test compartment |
| Evidence | allocation-audit receipt digest and detached supervisor/HSM signature, canonical report digest, report file SHA-256, receipt payload digest, receipt file SHA-256, runtime-signer/HSM and custodian signatures |
| Boundaries | canon selection, activation states, typed absences, every theorem/proof/certification/semantic/measurement/empirical transfer flag |

The deterministic aggregate report excludes run nonce, timestamps, access-log
content, signatures, and other render-varying custody fields; those belong only
in the signed receipt and completion manifest. The receipt binds the aggregate
report's digest and file SHA-256. Because a file cannot contain its own digest,
the receipt file SHA-256 is recorded in a separately signed completion envelope
or append-only custody registry after the receipt bytes freeze.

Every status serializes every compartment. A compartment that was not reached
contains typed `not-run` values and the controlling prior stop reason rather
than disappearing from the evidence chain.

Raw source text, dialogue identifiers, event locators, per-event labels,
per-event scores, rater identities beyond role-safe provenance, secret seed,
and test membership must remain outside Git and outside the aggregate report.

## 12. Smallest implementation plan

No implementation occurs under this packet-drafting task. A later authorized
implementation is limited to:

1. one external `/opt/experiment/response_tension_release_runner.py` module,
   never added beneath or imported as part of `/opt/edcm-base`, containing the
   packet-local source/archive, transform/dedup/domain, exact Wilson/percentile/
   variance, digest/report/receipt/atomic-write, scoring, and repeated runtime/
   callable-state/path helpers; it uses only the Python standard library and
   the four authenticated maintained measurement exports, and never imports
   `edcm.corpora` or the PR #49 holdout runner;
2. one `/opt/experiment/response_tension_release_allocator.py` implementing the
   exact commitment/HMAC/integer-quota/manifest rules, plus one separately
   frozen `/opt/experiment/response_tension_release_verifier.py` that
   derives them from authenticated primary artifacts without importing or
   invoking the allocator and emits canonical runtime-manifest and
   zero-disclosure allocation-audit bytes but has no private key or signing
   handle; the non-Python custody supervisor requires the two clean manifest
   builds to match and asks the HSM to sign the runtime envelope and audit
   receipt under separately scoped handles, but signs no candidate result or
   scientific verdict; neither Python module
   accepts a tuning or reseed option;
3. one contract-test file covering the existing four synthetic tension
   transitions and presentation/parser/whitespace-loss rules, plus: canonical
   event bytes and downstream identity equality; non-ASCII and literal `.json`
   preservation; exact dialogue/log/turn/text extraction; missing/non-list log,
   non-mapping turn, non-string text, UTF-8/parity, integer-versus-string,
   leading-zero, wrong-index, missing-field, extra-field, BOM/LF, and
   duplicate-locator rejection; deterministic
   minimum-digest representatives under reversed input order; complete
   singleton/duplicate loss mapping, exact-byte grouping, digest-collision
   failure, and no later promotion; allowed/repeated/absent/ambiguous/wrong-case
   booking-domain acts and proof that goals, metadata, payloads, text, and
   neighbors cannot affect the domain; integer largest-remainder ties,
   insufficient strata, HMAC order, one-bit commitment changes, alternate seed,
   manifest tamper, missing/forged supervisor/HSM audit signature, verifier
   process exposed to a signing handle, access/no-retention
   binding, label-ledger/projection/reliability-gate reconciliation, global-to-
   partition transform-loss projection, source-summary and manifest digest
   framing, and zero-disclosure scanning; parser exception/nonempty mismatch as
   incomplete versus empty-turn exclusion; exact variance fixtures `0/1`,
   `1/4`, `2/9`, permutation invariance, and
   `1/20769187434139310514121985316880384` for adjacent binary64 values around
   `0.1`; every frozen runtime blob, installed/shadow import, callable/class
   rebind, holdout-equivalent local-helper substitution, in-place `__code__`/
   default/annotation/globals/builtins mutation, parser pattern-list
   append/reorder, `math.log2`/`re`/`json`/`random.Random`/`os.replace`
   substitution, pure-Python stdlib-function and named stdlib-instance
   substitution, opaque `_hashlib.HASH` receiver-type mismatch, missing or
   extra receiver-resolution row, missing/altered `IMPORT_NAME`/`IMPORT_FROM`
   row or importer binding (including the `Counter`/`heapq` fixture), exact
   `LOAD_SUPER_ATTR` resolution for `Counter` and `Random`, class/callable-
   instance constructor scheduling for `random.Random(20260803)`, exact
   nonrecursive owner-bound-builtin targets for `_random.Random.__new__` and
   `_json.Encoder.__new__`, including each exact `__new__` key/value in the
   complete corresponding class state as well as the constructor row, exact finite
   merged-call allowlists for the JSON encoder/decoder, empty-callable/nonzero-
   ID rows for `INTRINSIC_STOPITERATION_ERROR`, exact `MAKE_FUNCTION` recipes
   for maintained generator expressions and JSON nested closures, including
   `novelty.set_a` and `RoundMetrics.__repr__.self` producer identity/type
   contracts with no captured event value in manifest bytes; exhaustive opcode
   classification and implicit-protocol fixtures that detect a replaced
   `fractions.operator.lt`, bind reflected `Fraction` arithmetic, and bind
   `pathlib` division for `_DATA_DIR / filename`; distinct canonical binding-
   path identities for Fraction's same-qualname generated forward/reverse
   operator wrappers while true aliases collapse; proof that unrelated module aliases such as
   entropy-seeded `random._inst` are not reached by a name cross product,
   altered or unshared `Counter` closure cell,
   direct `re._cache`/`re._cache2` clearing and proof that
   `re._compile_template` is untouched, prohibited other-cache mutation,
   metaclass/base/MRO change, swapped property getter/setter/deleter or
   staticmethod/classmethod payload, dictionary insertion-order drift,
   namespace-key/reference-name/identity-equivalence drift, independently
   derived canon content/index/alias/order mismatch, pre-import/self-baseline
   attempts, exact allocation-audit bootstrap with allocator/runner absent from
   `sys.modules`, builder/runtime private-key/HSM-handle absence, stdout/FD/mount
   topology mismatch, trace/profile and active or stale global/local `sys.monitoring`
   events/callbacks, interpreter/Unicode/platform mismatch, proof that the
   exact `-P -s -S` launch honors `PYTHONHASHSEED=0`, and two-build/runtime
   attestation; output/
   receipt/completion and exact atomic-temporary aliases against one another,
   the source/ledger/manifest inputs, and all four represented-evidence files;
   exact adjacent-binary64 midpoint selection, equality at
   `score >= selected_threshold`, exact `4/5`, `7/10`, `11/20`, and `1/2`
   boundary cases; bootstrap sorted-count fixtures exercising indices
   `249/250/9749/9750`, exact denominator `16000`, reduction, and equality at
   numerator `8000`; threshold-configuration digest/signature tamper, both
   reliability gates, complete compartment provenance, invalid outputs as
   incomplete, valid zero variance/scientific gate failures as
   `stopped-before-test`, aggregate-only output, and two-run determinism;
4. one two-root entrypoint derived from the exact pinned `linux/amd64` base
   image, with read-only `/opt/edcm-base`, separately frozen `/opt/experiment`,
   the three exact supervised `python3.12 -P -s -S -c` runtime,
   manifest-builder, and allocation-audit bootstrap modes, a
   separately signed two-build runtime-state manifest, one
   process/thread, no trace/profile/monitoring hook, network disabled, and the
   frozen environment; plus a separate empty custodian-exclusive output mount,
   stabilized dirfd-relative no-follow writes, custody fixtures for the
   independent enclave audit, and one sealed test run;
5. after a valid run only, one immutable aggregate report, audit-bound receipt,
   and the minimum documentation/generated-metadata updates required by the
   repository gates.

The maintained metric equations, PR #49 report and receipt, historical
experiments, source archive, and old test partition are unchanged. A regression
must prove the predecessor report and receipt remain byte-identical.

## 13. Non-transfer boundary

Regardless of outcome:

```text
canon_selection = null
formal_ucns_geometry = NA
formal_higher_gonol_composition = NA
edcm_production_activation = inactive
metapat_production_activation = inactive
theorem_status_transfer = false
proof_status_transfer = false
certification_status_transfer = false
semantic_authority_transfer = false
measurement_validity_claim = false
measurement_status_transfer = false
empirical_status_transfer = false
```

Even complete support establishes only one bounded candidate measurement on
one English booking corpus under one human manual and one custody event.

## 14. Current execution boundary

No external custodian, independent allocation verifier, signing key, human
panel, conflict disclosures, or signed execution manifest is presently
instantiated. Execution is therefore blocked without weakening the frozen
design. The new event, deduplication, domain, seed-audit, runtime, exact
decision-arithmetic, label-authority, transform-loss, and variance freezes
close protocol degrees of freedom only. They do not rehabilitate PR
#49's falsified sensitivity hypothesis, move its balanced-accuracy interval
away from chance, or supply evidence for this unexecuted candidate. MultiWOZ
source bytes are public; external custody can hide test membership, human
labels, and per-event outputs,
not make the public corpus itself secret. Participant independence is not
recoverable from the released corpus, so one-event-per-dialogue is the strongest
available clustering boundary. Cross-domain, multilingual, prospective, and
real-world action validity remain unresolved. A green machine can preserve a
negative result perfectly; it cannot promote it by good manners. Maintained
parsing discards turn-edge Unicode whitespace; this packet records that loss
exactly but cannot establish that the discarded padding was semantically
irrelevant. PR #49 also retains three unresolved code-review findings on its
future runner; this packet propagates their successor-facing failure boundaries
but does not repair or resolve that code.
