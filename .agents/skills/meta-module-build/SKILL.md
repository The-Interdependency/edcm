---
name: meta-module-build
description: Metadata-first scaffolding for new modules. Use this when creating a new module, route, service, adapter, schema, worker, engine, UI panel, migration, or experiment. Also use when a user says "start a module", "scaffold this", "add a service", "create an adapter", "add a worker", "build a route", or "make this self-documenting". This skill requires a MODULE_BUILD block before implementation and marks unknown fields as hmmm instead of guessing.
---

# meta-module-build

Create modules from metadata first.

The metadata declaration is part of the implementation. It should exist before the first working line of module logic.

## Required principle

Before implementing a new module, declare:

- what the module is;
- what it exposes;
- what it depends on;
- what boundaries it crosses;
- how it is tested;
- who owns it;
- how it rolls out;
- how it rolls back;
- what remains unresolved.

Unknown values must be written as:

```text
hmmm
```

Do not guess.

## Default workflow

1. create the target file;
2. add a `MODULE_BUILD` block;
3. fill known fields;
4. mark unknown fields as `hmmm`;
5. add related metadata blocks when needed;
6. implement module logic below the metadata;
7. run the relevant tests;
8. run metadata collection;
9. update root collection artifacts if the repository tracks them;
10. report unresolved `hmmm` items.

## MODULE_BUILD block

Python:

```python
# === MODULE_BUILD ===
# id: example_module
#   module_name: example
#   module_kind: service
#   summary: hmmm
#   owner: hmmm
#   public_surface: hmmm
#   internal_surface: hmmm
#   auth_boundary: hmmm
#   storage_boundary: hmmm
#   network_boundary: hmmm
#   user_data_boundary: hmmm
#   admin_only: hmmm
#   tests: hmmm
#   rollout: hmmm
#   rollback: hmmm
#   requires: hmmm
#   since: hmmm
#   unresolved: hmmm
# === END MODULE_BUILD ===
```

TypeScript:

```ts
// === MODULE_BUILD ===
// id: example_module
//   module_name: example
//   module_kind: service
//   summary: hmmm
//   owner: hmmm
//   public_surface: hmmm
//   internal_surface: hmmm
//   auth_boundary: hmmm
//   storage_boundary: hmmm
//   network_boundary: hmmm
//   user_data_boundary: hmmm
//   admin_only: hmmm
//   tests: hmmm
//   rollout: hmmm
//   rollback: hmmm
//   requires: hmmm
//   since: hmmm
//   unresolved: hmmm
// === END MODULE_BUILD ===
```

## Field guidance

### `id`

Stable metadata identifier.

Use lower snake case.

### `module_name`

The file, package, route, worker, panel, or service name.

### `module_kind`

Examples:

- `service`
- `adapter`
- `schema`
- `worker`
- `route`
- `engine`
- `ui`
- `migration`
- `experiment`
- `test_helper`

### `summary`

One sentence describing the module's purpose.

### `owner`

Person, team, service, or `hmmm`.

### `public_surface`

Public functions, classes, routes, events, exports, or commands.

### `internal_surface`

Private helpers, implementation-only types, local state, or `none`.

### `auth_boundary`

Authentication and authorization behavior.

Examples:

- `none`
- `session_required`
- `api_key`
- `service_token`
- `hmmm`

### `storage_boundary`

Databases, files, caches, object stores, queues, or `none`.

### `network_boundary`

External services, internal APIs, sockets, queues, or `none`.

### `user_data_boundary`

What user data the module reads, writes, transforms, retains, or exports.

### `admin_only`

`true`, `false`, or `hmmm`.

### `tests`

Test files, contract IDs, commands, or `hmmm`.

### `rollout`

Examples:

- `default_enabled`
- `feature_flag:<name>`
- `manual_only`
- `migration_gated`
- `hmmm`

### `rollback`

Shortest correct rollback path.

### `requires`

Internal modules, external packages, services, schemas, or `none`.

### `since`

Date, version, release, commit, or `hmmm`.

### `unresolved`

Explicit unresolved items.

Use `none` only when truly closed.

## Related metadata blocks

Add only when relevant.

### Documentation

```text
DOCS
```

### Capabilities

```text
CAPABILITIES
```

### Dependencies

```text
DEPENDENCIES
```

### Ownership

```text
OWNERS
```

### Risk boundaries

```text
BOUNDARIES
```

### Contracts

```text
CONTRACTS
```

### Ratios

```text
ratios:<id>
```

### Living manifest

```text
manifest
```

## Agent rules

### Rule 1

Do not create implementation-only files without metadata when this skill applies.

### Rule 2

Do not invent owners, permissions, rollout plans, rollback plans, or dependencies.

Use `hmmm`.

### Rule 3

Keep metadata and code in the same change.

### Rule 4

When metadata changes, inspect whether tests, docs, generated manifests, and root collection points also need updates.

### Rule 5

When creating a new module, the first artifact should be the metadata block, not the code body.

### Rule 6

Tests and helper files should also declare metadata when they represent stable repo behavior, not disposable scratch work.

## Validation checklist

Before marking work complete:

- [ ] module has a stable `MODULE_BUILD` id;
- [ ] known fields are filled;
- [ ] unknown fields are `hmmm`;
- [ ] public surface matches code;
- [ ] dependencies match imports;
- [ ] auth/storage/network/user-data boundaries are explicit;
- [ ] tests are named;
- [ ] rollout and rollback are explicit;
- [ ] unresolved items are preserved;
- [ ] metadata collection was run;
- [ ] generated root artifacts were updated if required.

## Minimal example

```python
# === MODULE_BUILD ===
# id: file_export_service
#   module_name: file_export
#   module_kind: service
#   summary: Exports a validated report to a local file.
#   owner: hmmm
#   public_surface: export_report
#   internal_surface: _validate_path, _serialize_report
#   auth_boundary: none
#   storage_boundary: local_filesystem
#   network_boundary: none
#   user_data_boundary: writes caller-provided report content to caller-selected path
#   admin_only: false
#   tests: tests/test_file_export.py
#   rollout: default_enabled
#   rollback: remove module and its exports
#   requires: pathlib, json
#   since: 2026-06-03
#   unresolved: owner assignment
# === END MODULE_BUILD ===
```

Then implement below it.

## hmmm

- whether all repositories should require `MODULE_BUILD` blocks for new test helpers;
- whether rollout and rollback fields should become mandatory validation errors;
- whether collector output should fail CI when `hmmm` count increases;
- whether generated `llms.txt` files should include unresolved metadata summaries.
