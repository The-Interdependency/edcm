# EDCM stack repair — implementation status

Updated: 2026-07-12

This ledger tracks evidence against `REQUIRED_CHANGES.md` and `COMPLETED_LOOKS_LIKE.md`. A checked item means implemented on a merged or active repair branch with named tests or CI evidence; it does not mean the entire repair is complete.

## Completed or active

- [x] Authoritative package metadata, version, build system, typed marker, frozen canon package data, and development dependencies — merged in PR #15.
- [x] Python 3.11–3.13 base tests, source/wheel build, `twine check`, clean-wheel install, and installed public-API smoke gate — merged in PR #15.
- [x] EDCM-owned UCNS adapter over actual public surfaces, typed absence, fail-closed schema/object handling, and stable-hash preservation — merged in PR #17.
- [x] Installed `edcmbone` cannot override canonical `edcm.measurement`; authority and consolidation provenance are machine-readable — merged in PR #17.
- [x] Canonical METAPAT producer schema and actual-UCNS adapter established in `The-Interdependency/metapat` — merged in METAPAT PR #3.
- [x] EDCM-owned METAPAT consumer validates actual envelope objects, canonical JSON, and canonical mappings through producer constructors — merged in PR #18.
- [x] METAPAT canon identity, exact source statements/references, constraints, permitted interpretations, unresolved `hmmm`, and provenance digest survive the EDCM path — merged in PR #18.
- [x] Final result contract separates source evidence, METAPAT constraints, UCNS geometry, EDCM policy identity, implementation provenance, readouts/`NA`, status evidence, and unresolved constraints — merged in PR #18 and extended in active PR #20.
- [x] Canon or EDCM manifest rotation produces a new epoch identity; transcript measurement remains deterministic — merged in PR #18.
- [x] Base, UCNS-only, METAPAT-only, full UCNS/METAPAT/EDCM, build, metadata, and clean-wheel CI gates pass — merged in PR #18.
- [x] Exact frozen-canon byte manifest, complete file-set gate, measurement-authority policy check, and orthogonality no-fork check run from source and installed wheel — merged in PR #19.
- [x] Canonical versioned UCNS bridge and factorization-evidence producer records — merged in `The-Interdependency/ucns` PR #108.
- [x] EDCM consumes actual UCNS bridge and factorization records as objects, canonical JSON, or canonical mappings through producer constructors — active PR #20.
- [x] Live UCNS objects and serialized bridge records share one `ucns.bridge_record()` identity path — active PR #20.
- [x] Factorization evidence is stable-hash-bound to geometry; mismatched, tampered, coerced, unknown, or unsupported records fail closed — active PR #20.
- [x] Object, bridge, scope, factorization, negative-certification, and theorem-status attachment are independent; package availability alone attaches nothing — active PR #20.
- [x] Certified, uncertified, factor-found, and unit-domain UCNS evidence remain distinguishable and never promote EDCM measurement validity — active PR #20.
- [x] Result schema `edcm.shared-stack-result/1.1.0` preserves canonical UCNS factorization evidence and binds it into result identity — active PR #20.

## Not yet complete

- [ ] Reconcile remaining MODULE_BUILD, DOCS, CAPABILITIES, BOUNDARIES, CONTRACTS, DEPENDENCIES, OWNERS, and skill-lib declarations.
- [ ] Install repo-local skill-lib and add real drift/msdmd gates; EDCM currently has no `.agents/skills/` tree or callable local runner.

## Preserved frontier

Contact convergence, DA geometry correlation, cadence admission from text, and semantic-label-to-operating-state inference remain non-operational. No placeholder values or language-model judgments have been added.

## hmmm

Version 1 UCNS evidence digests establish canonical content identity but not cryptographic producer signatures. Signed producer or transport authentication remains unresolved. Repo-local skill-lib checks remain unavailable until the actual skill installation and runner are added.
