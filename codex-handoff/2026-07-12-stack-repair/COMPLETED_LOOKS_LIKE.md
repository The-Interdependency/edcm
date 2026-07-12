# EDCM stack repair — completed looks like

The EDCM repair is complete only when every applicable statement below is true and evidenced by package artifacts, code, tests, provenance records, current documentation, or CI results.

## Package and release surface

- **Completed looks like:** EDCM has one authoritative `pyproject.toml`, package version, license declaration, Python support policy, package discovery configuration, and development dependencies.
- **Completed looks like:** `edcm.__version__` matches built package metadata.
- **Completed looks like:** source distribution and wheel build successfully, pass `twine check`, install in a clean environment, and expose the documented public API.
- **Completed looks like:** GitHub Actions runs the supported Python matrix and clean-wheel smoke tests.
- **Completed looks like:** README and agent instructions no longer say there is no packaging or CI.

## UCNS integration

- **Completed looks like:** EDCM owns the adapter protocol it needs and does not expect UCNS to expose `SemanticsLayer`.
- **Completed looks like:** the live adapter consumes actual `ucns.UCNSObject` instances or the official UCNS bridge record.
- **Completed looks like:** missing UCNS, adapter failure, unsupported schema, and malformed geometry are distinguishable states.
- **Completed looks like:** optional integration code catches only expected missing-dependency errors; unexpected errors are visible.
- **Completed looks like:** every pipeline result identifies the selected UCNS adapter, version, source, and fallback status.
- **Completed looks like:** a successful import or object construction does not imply a theorem, domain, or measurement-validity claim.

## Measurement source of truth

- **Completed looks like:** exactly one repository/surface is declared canonical for the maintained EDCM measurement implementation and canon data.
- **Completed looks like:** if EDCM is canonical after consolidation, an installed edcmbone package cannot silently override it.
- **Completed looks like:** if edcmbone remains temporarily authoritative, synchronization is deterministic, pinned, and enforced by CI drift checks.
- **Completed looks like:** no manually maintained duplicate orthogonality or measurement implementation can drift without a failing check.
- **Completed looks like:** consolidation provenance, source commit, local deltas, and compatibility policy are machine-readable.

## METAPAT semantic boundary

- **Completed looks like:** EDCM consumes a versioned immutable METAPAT semantic module envelope.
- **Completed looks like:** METAPAT canon digest, source references, module kind, constraints, provenance, and unresolved `hmmm` fields survive the pipeline.
- **Completed looks like:** METAPAT semantic labels remain separate from EDCM metric values.
- **Completed looks like:** changing METAPAT canon identity is visible as a provenance or epoch change rather than silently rewriting historical output.
- **Completed looks like:** EDCM never claims that its measurements validate METAPAT root ontology.

## Provenance-bearing layer selection

- **Completed looks like:** semantics, measurement, composition, and delivery layers each report implementation id, version, source, role, and canonical/fallback/unavailable state.
- **Completed looks like:** no layer silently falls back after an unexpected adapter exception.
- **Completed looks like:** transcript-only mode and full UCNS-backed mode, if both supported, are explicitly different modes.
- **Completed looks like:** absent adapter, no-bone turn, empty field, and missing context remain typed absence or `NA`, never zero.

## Dependency and status reporting

- **Completed looks like:** reports distinguish UCNS package availability, adapter activation, object attachment, scope-metadata attachment, negative-certification attachment, and theorem-status attachment.
- **Completed looks like:** package import alone sets only package availability.
- **Completed looks like:** malformed or absent metadata cannot be reported as attached evidence.
- **Completed looks like:** any attached UCNS negative certification includes the actual evidence-bearing envelope and declared domain.
- **Completed looks like:** theorem status, when attached, is provenance only and never promotes EDCM empirical validity.

## EDCM object identity

- **Completed looks like:** `ConstraintField`, `FieldMotion`, windows, operator turns, axes, and readouts are documented as EDCM objects constructed using UCNS geometry.
- **Completed looks like:** no EDCM-local type is presented as a replacement implementation of `UCNSObject`.
- **Completed looks like:** UCNS stable hash, METAPAT canon digest, EDCM policy manifest hash, and EDCM measurement identity are recorded as distinct fields.
- **Completed looks like:** geometry equivalence and measurement equivalence remain separate tests.

## Empirical frontier

- **Completed looks like:** contact convergence, DA geometry correlation, cadence admission from text, and comparable empirical frontier gates remain explicit non-implementations until their falsifiers and tests exist.
- **Completed looks like:** no placeholder number, heuristic, language-model judgment, or default value impersonates a frontier result.
- **Completed looks like:** ordered windows use `SeqAppend` where order is testimony and are never replaced by averaging.
- **Completed looks like:** no EDCM output claims diagnosis, intent, consciousness, or external empirical truth beyond its declared measurement contract.

## Shared stack contract

- **Completed looks like:** the shared fixture accepts a METAPAT semantic envelope and an actual UCNS object.
- **Completed looks like:** UCNS equality and stable hash survive the EDCM integration path.
- **Completed looks like:** METAPAT canon identity and EDCM manifest identity remain distinct and both are visible.
- **Completed looks like:** valid readouts are produced without proof-status transfer.
- **Completed looks like:** `NA != 0` is preserved in every empty or absent case.
- **Completed looks like:** malformed bridge, schema, provenance, or status records fail closed.
- **Completed looks like:** canon or manifest rotation creates a new epoch identity.
- **Completed looks like:** transcript measurement remains deterministic and reproducible.

## Verification and compliance

- **Completed looks like:** base tests, integration tests, full-stack fixtures, build checks, `twine check`, wheel installation, and public API smoke tests pass in CI.
- **Completed looks like:** optional sibling integrations skip explicitly when unavailable and never pass through silent imitation.
- **Completed looks like:** frozen canon integrity and source-of-truth drift checks pass.
- **Completed looks like:** every changed native module has accurate msdmd metadata and real test references.
- **Completed looks like:** repo-local skill-lib drift checks report clean.

## Final boundary

- **Completed looks like:** one EDCM result record lets a reviewer determine separately:

  1. which source evidence was measured;
  2. which METAPAT semantic constraints applied;
  3. which actual UCNS geometry was used;
  4. which EDCM policy manifest governed the readout;
  5. which implementation and fallback mode ran;
  6. which values are measurements, which are `NA`, and which are unresolved;
  7. whether any UCNS status evidence was attached without confusing it for EDCM validity.

## hmmm

Completion does not require eliminating transcript-only operation. Completion requires that transcript-only operation cannot be mistaken for the full METAPAT-constrained, UCNS-backed EDCM path.