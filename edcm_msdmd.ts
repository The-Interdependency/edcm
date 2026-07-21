import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "edcm",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "__version__, build_default_layers, EDCMLayers, LayerProvenance, ConsolidatedMeasurementLayer, CompositeSemanticsLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, TranscriptOnlySemanticsLayer, UCNSSemanticsLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, ActualMetapatAdapter, MetapatIntegrationStatus, MetapatSemanticEvidence, select_metapat_adapter, inspect_metapat_adapter, ActualUCNSAdapter, UCNSIntegrationStatus, UCNSGeometryEvidence, UCNSFactorizationEvidenceRecord, select_ucns_adapter, inspect_ucns_adapter, AuthorizedUCNSFork, UCNSForkTopologyBinding, UCNSForkLintReport, ForkLintDependencyError, ForkTopologyError, build_fork_topology_binding, enumerate_payload_fork_paths, lint_fork_topology, lint_all_payload_forks, EDCMResultContract, build_result_contract, RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, IntegrityFinding, IntegrityReport, run_integrity_gate, verify_frozen_canon, verify_measurement_authority, verify_orthogonality_alias, audit_energy_text, audit_energy_claim, extract_energy_claim_candidates, audit_falsifiability_preservation, EnergyAuditReport, AuditFlag, EnergyClaim, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE, AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX, SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN, MetricDefinition, ResolvedMetricUCNS, UCNSMetricDependencyError, UCNSMetricResolutionError, METRIC_DEFINITIONS, SYMBOL_TO_METRIC_ID, resolve_metric_axis, resolve_metric_value, resolve_metric_vector, resolve_round_metrics, resolved_metric_objects_payload, measurement, language, edcmucns, CanonLoader, parse_transcript, ParsedTranscript, compute_transcript, RoundMetrics, project_transcript, AgentMetrics, fire_alerts",
        "requires": "edcm_layers, edcm_metapat_adapter, edcm_ucns_adapter, edcm_ucns_fork_lint, edcm_shared_stack, edcm_integrity, edcm_energy_claims, edcm_falsifiability_bridge, edcm_ucns_objects, edcm_ucns_metrics, edcmucns_package, edcm_language_package",
        "rollback": "remove new exports and restore prior package root only with a result-schema migration",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "EDCM package root \u2014 declares package identity and re-exports provenance-bearing shared-stack layers, canonical METAPAT consumer surfaces, actual-UCNS bridge, factorization-evidence and metric-object consumer surfaces, fail-closed METAPAT-to-UCNS fork topology lint, final result contracts, frozen-canon/authority integrity gates, energy audit, EDCM objects, edcmucns architecture, and canonical maintained measurement.",
        "tests": "tests.test_measurement, tests.test_ucns_adapter, tests.test_ucns_evidence_consumer, tests.test_metapat_adapter, tests.test_shared_stack_contract, tests.test_integrity, tests.test_ucns_objects, tests.test_ucns_fork_lint, tests.test_ucns_metrics, tests.test_energy_claims, tests.test_packaging",
        "unresolved": "UCNS evidence digests, fork topology bindings, and metric-object hashes provide content identity but not cryptographic producer authentication; the first accepted production fork fixture remains unselected",
        "user_data_boundary": "none"
      },
      "file": "edcm/__init__.py",
      "id": "edcm_package"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "edcmucns",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PolicyManifest, ProvenanceWitness, Anchor, Payload, Window, Present, AbsentOperatorGeometry, OperatorTurn, BridgeDiagnostic, BoneEvent, encode_turn, make_cadence_anchor, with_cadence, REGISTRY, resolve_scope, ReadoutScope, UnknownReadoutScopeError, ucns_carrier_equivalent, edcm_measurement_equivalent, witness_geometry_consistent, validate_window, gauge_audit, seq_append, interaction_product, flat_reduction, kappa_balance, kappa_audit, EpochBreakError, EpochChain, compare_across_epochs, operator_presence_readout",
        "requires": "edcm.ucns_objects",
        "rollback": "remove package and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "edcmucns v0.3.1 \u2014 EDCM on UCNS mathematics, provenance as the recurring theme; architecture-only implementation surface (identity layer), empirical claims remain frontier gates",
        "tests": "tests.test_edcmucns_identity_v031, tests.test_edcmucns_encoder_v031, tests.test_edcmucns_scopes_v031, tests.test_edcmucns_epochs_v031",
        "unresolved": "frontier gates (contact convergence, DA_geom, cadence admission from text, corpus parallel run, operating-state validity) are NotImplemented surfaces with named falsifiers; no empirical claim is made",
        "user_data_boundary": "transcript-shaped inputs (turn ids, speakers, surface forms, payload content)"
      },
      "file": "edcm/edcmucns/__init__.py",
      "id": "edcmucns_package"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "composer",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "seq_append, InteractionSignature, interaction_product, flat_reduction, kappa_balance, kappa_audit, EpochBreakError",
        "requires": "edcmucns_types",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "SeqAppend window composition (chronological append; lengths add; F concatenates; carrier = lcm), reserved interaction product, payload flat reduction, kappa ledger placeholders",
        "tests": "tests.test_edcmucns_scopes_v031, tests.test_edcmucns_epochs_v031",
        "unresolved": "kappa ledger is an architecture placeholder \u2014 open-payload tension only; the full stored-tension circuit remains upstream/frontier",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/composer.py",
      "id": "edcmucns_composer"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "encoder",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "BoneEvent, encode_turn, make_origin_anchor, make_cadence_anchor, with_cadence, admit_cadence_from_text",
        "requires": "edcmucns_manifest,edcmucns_types,edcmucns_provenance,edcmucns_geometry",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "v0.3.1 turn encoder \u2014 bone events to origin-anchored windows with provenance witnesses; no-bone turns emit AbsentOperatorGeometry; cadence admission from text is a reserved frontier gate",
        "tests": "tests.test_edcmucns_encoder_v031",
        "unresolved": "bone emission from raw text is out of scope here \u2014 callers supply BoneEvents; the bone_emission_policy_version pins which upstream emitter produced them",
        "user_data_boundary": "transcript-shaped inputs (turn ids, speakers, surface forms)"
      },
      "file": "edcm/edcmucns/encoder.py",
      "id": "edcmucns_encoder"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "epochs",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EpochBoundary, EpochSegment, EpochChain, window_identity_hash, compare_across_epochs, V031_ADOPTION_NOTE",
        "requires": "edcmucns_manifest,edcmucns_types,edcmucns_provenance,edcmucns_composer",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "Epoch chain for edcmucns v0.3.1 \u2014 manifest rotation seals the segment and opens a new epoch; cross-epoch comparisons are Bridge lensing events, not raw deltas",
        "tests": "tests.test_edcmucns_epochs_v031",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/epochs.py",
      "id": "edcmucns_epochs"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_operator_bundle_hash, _payload_signature, _cadence_signature",
        "module_kind": "engine",
        "module_name": "equivalence",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ucns_carrier_equivalent, edcm_measurement_equivalent, contact_convergence",
        "requires": "edcmucns_types,edcmucns_scopes,edcmucns_provenance,edcmucns_geometry",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "v0.3.1 equivalence tiers \u2014 ucns_carrier_equivalent (geometry only) and edcm_measurement_equivalent (geometry + in-scope witness + manifest); contact convergence is a frontier gate",
        "tests": "tests.test_edcmucns_identity_v031",
        "unresolved": "Theta+/F+ are compared as sorted multisets over host anchors (hmmm \u2014 ordering sensitivity lives in the witness bundle, which hashes chronologically); bridge_scope equivalence compares manifest identity only until the diagnostic vocabulary is frozen",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/equivalence.py",
      "id": "edcmucns_equivalence"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "field_reader",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "FieldReading, read_field_chain, field_chain_hashes, attach_field_chain, field_readouts",
        "requires": "edcmucns_types,edcm.ucns_objects",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-07",
        "storage_boundary": "none",
        "summary": "field reader \u2014 build the ConstraintField/FieldMotion hash chain for a window's field_scope; NA-safe motion/state readouts; no empirical claim",
        "tests": "tests.test_edcmucns_field_reader_v031",
        "unresolved": "contact convergence over the chain stays the frontier gate in equivalence; this reader reports geometry/state only, no empirical operating-state claim",
        "user_data_boundary": "constraint fields may summarize user-turn field state"
      },
      "file": "edcm/edcmucns/field_reader.py",
      "id": "edcmucns_field_reader"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_lcm_over",
        "module_kind": "engine",
        "module_name": "geometry",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "non_origin_residue, bone_theta, cadence_theta, L_geo, L_op, bone_anchors, cadence_anchors, origin_anchors, n_host_total, n_family, n_cadence, n_payload, active_families, operator_shares, lambda_field, da_geom_correlation",
        "requires": "edcmucns_types",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "v0.3.1 non-origin residue rule, anchor angles, mass helpers (L_geo/L_op), carriers (n_host_total/n_family/n_cadence/n_payload), operator shares, lambda_field",
        "tests": "tests.test_edcmucns_encoder_v031, tests.test_edcmucns_scopes_v031",
        "unresolved": "DA_geom correlation is frontier \u2014 placeholder raises NotImplementedError; cadence theta wrap at ordinal % n == 0 collides with the datum reservation and is left to the validator (hmmm)",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/geometry.py",
      "id": "edcmucns_geometry"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "manifest",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PolicyManifest, DEFAULT_FAMILY_PRIME_GAUGE, RESIDUE_RULE_VERSION",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "PolicyManifest \u2014 the measurement-identity manifest for edcmucns v0.3.1; stable-serializable, hashable; hash changes create epoch breaks",
        "tests": "tests.test_edcmucns_identity_v031, tests.test_edcmucns_epochs_v031",
        "unresolved": "policy version strings are architecture placeholders; the policies they name (polarity dictionary, contact predicate, training updates) remain frontier",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/manifest.py",
      "id": "edcmucns_manifest"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "provenance",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ProvenanceWitness, READOUT_BEARING_FIELDS, canonicalize, witness_hash, bundle_hash",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "ProvenanceWitness \u2014 anchor-level testimony for edcmucns v0.3.1; provenance is measurement material, not decorative metadata",
        "tests": "tests.test_edcmucns_identity_v031",
        "unresolved": "constraint_governance vocabulary is not yet enumerated; carried as an opaque readout-bearing string",
        "user_data_boundary": "transcripts may carry user speech in surface_form; hashes only summarize, they do not redact"
      },
      "file": "edcm/edcmucns/provenance.py",
      "id": "edcmucns_provenance"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "scopes",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ReadoutScope, REGISTRY, resolve_scope, UnknownReadoutScopeError",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "Closed readout_scope registry for edcmucns v0.3.1 \u2014 edcm_measurement_equivalent must not accept arbitrary strings",
        "tests": "tests.test_edcmucns_scopes_v031",
        "unresolved": "bridge_scope read set (witness/geometry diagnostics + manifest + epoch boundaries) is named but its diagnostic vocabulary is still growing with the validator",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/scopes.py",
      "id": "edcmucns_scopes"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "types",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ANCHOR_ROLES, Anchor, Payload, ContentLensEvent, Window, Present, AbsentOperatorGeometry, OperatorTurn, BridgeDiagnostic, operator_presence_readout",
        "requires": "edcmucns_provenance",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "Core edcmucns v0.3.1 value objects \u2014 Anchor (origin/bone/cadence), Payload, Window, OperatorTurn (Present | AbsentOperatorGeometry), BridgeDiagnostic",
        "tests": "tests.test_edcmucns_encoder_v031, tests.test_edcmucns_identity_v031",
        "unresolved": "cadence anchors are reserved in v0.3.1 (no admission from transcript text); composite cadence exists only for explicit caller-built fixtures",
        "user_data_boundary": "transcripts may carry user speech in payload content / lens events"
      },
      "file": "edcm/edcmucns/types.py",
      "id": "edcmucns_types"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "validation",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "witness_geometry_consistent, validate_window, gauge_audit",
        "requires": "edcmucns_types,edcmucns_manifest,edcmucns_geometry,edcmucns_provenance",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-07-06",
        "storage_boundary": "none",
        "summary": "witness_geometry_consistent validator + polarity gauge audit \u2014 mismatches emit Bridge diagnostics, never silent alternate readings",
        "tests": "tests.test_edcmucns_identity_v031, tests.test_edcmucns_encoder_v031",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/edcmucns/validation.py",
      "id": "edcmucns_validation"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_contains_any, _split_spans, _candidate, _first_unit, _claimed_quantity, _extract_after_markers, _flag, _summarize",
        "module_kind": "engine",
        "module_name": "energy_claims",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EnergyClaim, AuditFlag, EnergyAuditReport, extract_energy_claim_candidates, audit_energy_claim, audit_energy_text, CAPABILITY_STATEMENT",
        "requires": "edcm_ucns_dependency",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "stdlib-only energy-theory falsifiability audit with explicit UCNS package/adapter/evidence status and no physics validation or proof-status transfer",
        "tests": "tests.test_energy_claims, tests.test_ucns_dependency",
        "unresolved": "none",
        "user_data_boundary": "audits arbitrary claim text supplied by the caller"
      },
      "file": "edcm/energy_claims.py",
      "id": "edcm_energy_claims"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_has_falsifiability_bearing_claim, _texts, _edcmbone_structural_density",
        "module_kind": "engine",
        "module_name": "falsifiability_bridge",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "audit_falsifiability_preservation, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE",
        "requires": "edcm_energy_claims",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "audits whether falsifiability-bearing claims survive input->output using the stdlib energy audit; optional edcmbone structural-density as auxiliary metadata only",
        "tests": "tests.test_falsifiability_bridge",
        "unresolved": "optional edcmbone import is best-effort; structural_density is auxiliary metadata, not a proof-status signal",
        "user_data_boundary": "audits arbitrary input/output text supplied by the caller"
      },
      "file": "edcm/falsifiability_bridge.py",
      "id": "edcm_falsifiability_bridge"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canon_root",
        "module_kind": "guardrail",
        "module_name": "integrity",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "FROZEN_CANON_GIT_BLOBS, EXPECTED_MEASUREMENT_AUTHORITY, IntegrityFinding, IntegrityReport, git_blob_sha1, verify_frozen_canon, verify_measurement_authority, verify_orthogonality_alias, run_integrity_gate, main",
        "requires": "edcm_measurement, edcm_ucns_objects",
        "rollback": "remove integrity module and CI invocation only after replacing with an equivalent or stronger gate",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "reads packaged canon resources only",
        "summary": "non-tautological frozen-canon byte manifest and measurement source-of-truth drift gate with installed-package CLI",
        "tests": "tests.test_integrity",
        "unresolved": "future canon versions require an explicit versioned manifest and migration record",
        "user_data_boundary": "none"
      },
      "file": "edcm/integrity.py",
      "id": "edcm_integrity"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "language",
        "network_boundary": "optional_package_import",
        "owner": "Erin Spencer",
        "public_surface": "EnglishEmbeddingManifest, embedding_manifest, PUBLIC_GLYPH_FLOOR_157, UCNSPublicGonolDependencyError, UCNSPublicGonolContractError, NonCanonicalLanguagePlacementError, require_canonical_language_placement, CompositionNode, Attestation, Soundness, LexicalEvidence, AtomicForkRelation, AtomicForkResult, GonolRegistry, compose_gonols, materialize, compare_atomic_fork, intrinsic_gonol_record, metadata_free_jsonl, write_metadata_free_gonol_list, AffixRecord, load_affix_inventory, TransformationRule, transformation_inventory, render_affix_candidates, inverse_affix_candidates, compound_candidates, normalize_lemma, Decomposition, MorphologyGraph, build_morphology_graph, OEWN_REPOSITORY, OEWN_TAG, OEWN_COMMIT, OEWN_LICENSE, LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot, load_oewn_2025, assign_affix_gonol, assign_root_gonol, assign_direct_atomic_gonol, superpose_gonols, compare_gonols, gonol_sha256",
        "requires": "edcm_language_manifest, edcm_language_glyph_floor, edcm_language_model, edcm_language_composition, edcm_language_artifacts, edcm_language_oewn_source, edcm_language_affixes, edcm_language_rendering, edcm_language_morphology, edcm_language_placement",
        "rollback": "restore active placement only after an Erin-ratified UCNS public-gonol bridge exists",
        "rollout": "fail_closed_pending_canonical_bridge",
        "since": "2026-07-16",
        "storage_boundary": "read",
        "summary": "exposes OEWN source, morphology and rendering evidence while consuming UCNS public-gonol authority lazily and retiring noncanonical placement",
        "tests": "tests.test_language_embeddings, tests.test_language_full_run",
        "unresolved": "public-gonol to EDCM language-object bridge remains hmmm",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/__init__.py",
      "id": "edcm_language_package"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canon_path, _slug",
        "module_kind": "engine",
        "module_name": "affixes",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AffixRecord, load_affix_inventory, affix_inventory_record",
        "requires": "edcm measurement canon bones_affixes_v1.json",
        "rollback": "restore the prior inventory version and regenerate every dependent artifact",
        "rollout": "default_enabled",
        "since": "2026-07-13",
        "storage_boundary": "read",
        "summary": "expands every canonical EDCM affix and allomorph into a deterministic universally applicable inventory for the OEWN 2025 run",
        "tests": "tests.test_language_full_run",
        "unresolved": "future run versions may add newly documented English affixes without invalidating this freeze",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/affixes.py",
      "id": "edcm_language_affixes"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_anchor_record",
        "module_kind": "adapter",
        "module_name": "artifacts",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "intrinsic_gonol_record, metadata_free_jsonl, write_metadata_free_gonol_list",
        "requires": "edcmbone_ucns_v04",
        "rollback": "remove language embedding package before any published artifact depends on this serialization",
        "rollout": "default_enabled",
        "since": "2026-07-13",
        "storage_boundary": "write",
        "summary": "serializes ordered UCNS gonols as intrinsic-only canonical JSONL with no words, labels, evidence, source ids, or embedding classifications",
        "tests": "tests.test_language_embeddings",
        "unresolved": "producer signatures and authenticated transport remain outside intrinsic gonol serialization",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/artifacts.py",
      "id": "edcm_language_artifacts"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "composition",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "GonolRegistry, compose_gonols, materialize, compare_atomic_fork, MissingGonolError",
        "requires": "edcm_language_model, edcmbone_ucns_v04",
        "rollback": "remove language embedding package before any published artifact depends on this composer",
        "rollout": "default_enabled",
        "since": "2026-07-13",
        "storage_boundary": "none",
        "summary": "materializes explicit language composition trees through one UCNS product and compares independent direct atomic gonols with molecularly generated atomic views",
        "tests": "tests.test_language_embeddings",
        "unresolved": "the maintained local UCNS engine is associative while explicit language grouping remains preserved as independent provenance for comparison",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/composition.py",
      "id": "edcm_language_composition"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load_ucns_public_gonol, _PublicGonolProxy",
        "module_kind": "adapter",
        "module_name": "glyph_floor",
        "network_boundary": "package_import_only",
        "owner": "Erin Spencer",
        "public_surface": "PUBLIC_GLYPH_FLOOR_157, build_public_glyph_floor_157, validate_public_glyph_floor, glyph_floor_sha256, UCNSPublicGonolDependencyError, UCNSPublicGonolContractError",
        "requires": "edcm_language_manifest",
        "rollback": "restore only after reverting canonical ownership to the exact pinned UCNS source",
        "rollout": "compatibility_only",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "lazily consumes the UCNS-owned public gonol without retaining a competing EDCM arrangement authority",
        "tests": "tests.test_language_embeddings",
        "unresolved": "canonical public-gonol to EDCM language-object bridge remains hmmm",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/glyph_floor.py",
      "id": "edcm_language_glyph_floor"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "policy",
        "module_name": "manifest",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EnglishEmbeddingManifest, embedding_manifest, SOURCE_DICTIONARY, PUBLIC_GLYPH_FLOOR_SOURCE",
        "requires": "none",
        "rollback": "restore active placement only after an Erin-ratified UCNS public-gonol bridge exists",
        "rollout": "fail_closed_pending_canonical_bridge",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "pins OEWN input provenance while recording that public-gonol authority belongs to UCNS and legacy placement is retired",
        "tests": "tests.test_language_embeddings",
        "unresolved": "public-gonol to EDCM language-object bridge remains hmmm",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/manifest.py",
      "id": "edcm_language_manifest"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "model",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CompositionNode, Attestation, Soundness, LexicalEvidence, AtomicForkRelation, AtomicForkResult",
        "requires": "none",
        "rollback": "remove language embedding package before any published artifact depends on these schemas",
        "rollout": "default_enabled",
        "since": "2026-07-13",
        "storage_boundary": "none",
        "summary": "defines explicit composition trees, evidence states, and direct/generated atomic comparison records without placing linguistic metadata inside gonols",
        "tests": "tests.test_language_embeddings",
        "unresolved": "whether soundness will ultimately be indexed by context, technology, community, or all three",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/model.py",
      "id": "edcm_language_model"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_compound_parts, _alternative_key",
        "module_kind": "engine",
        "module_name": "morphology",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "Decomposition, MorphologyGraph, build_morphology_graph",
        "requires": "edcm_language_affixes, edcm_language_rendering, edcm_language_model",
        "rollback": "restore the prior graph builder and regenerate all molecular artifacts",
        "rollout": "builder_only",
        "since": "2026-07-13",
        "storage_boundary": "none",
        "summary": "derives the run root set and the complete affix/compound decomposition DAG for every OEWN surface while preserving all valid alternatives",
        "tests": "tests.test_language_full_run",
        "unresolved": "closed compounds without explicit dictionary separators remain whole roots unless an affix analysis reaches them",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/morphology.py",
      "id": "edcm_language_morphology"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_update_intrinsic_hash, _payload_depth, _theta_set",
        "module_kind": "adapter",
        "module_name": "placement",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "NonCanonicalLanguagePlacementError, require_canonical_language_placement, assign_affix_gonol, assign_root_gonol, assign_direct_atomic_gonol, superpose_gonols, compare_gonols, gonol_sha256",
        "requires": "edcm_language_manifest",
        "rollback": "restore placement only after an Erin-ratified UCNS public-gonol bridge and migration plan exist",
        "rollout": "fail_closed",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "retires noncanonical hash/evidence-derived language placement while retaining read-only compatibility inspection of existing objects",
        "tests": "tests.test_language_embeddings, tests.test_language_full_run",
        "unresolved": "public-gonol to EDCM language-object bridge remains hmmm",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/placement.py",
      "id": "edcm_language_placement"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_is_cvc, _ordered_unique",
        "module_kind": "engine",
        "module_name": "rendering",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "TransformationRule, transformation_inventory, render_affix_candidates, inverse_affix_candidates, compound_candidates, normalize_lemma",
        "requires": "edcm_language_affixes",
        "rollback": "restore the prior renderer version and regenerate all molecular artifacts",
        "rollout": "default_enabled",
        "since": "2026-07-13",
        "storage_boundary": "none",
        "summary": "codifies reversible English orthographic and compounding transformations without using them as composition gates",
        "tests": "tests.test_language_full_run",
        "unresolved": "pronunciation rendering remains outside this first complete written-English run",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/rendering.py",
      "id": "edcm_language_rendering"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load_yaml, _source_tree_digest, _relation_values",
        "module_kind": "adapter",
        "module_name": "source",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "OEWN_REPOSITORY, OEWN_TAG, OEWN_COMMIT, OEWN_LICENSE, LexemeRecord, SenseRecord, SynsetRecord, WordnetSnapshot, load_oewn_2025",
        "requires": "PyYAML only during artifact construction",
        "rollback": "remove loader and generated artifacts before publishing another source manifest",
        "rollout": "builder_only",
        "since": "2026-07-13",
        "storage_boundary": "read",
        "summary": "loads the exact Open English WordNet 2025 YAML release into deterministic lemma, sense, synset, and relation records and computes a source-tree digest",
        "tests": "tests.test_language_full_run",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/language/source.py",
      "id": "edcm_language_oewn_source"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_record_layer, _local_provenance",
        "module_kind": "engine",
        "module_name": "layers",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "LayerProvenance, MeasurementLayer, SemanticsLayer, CompositionLayer, DeliveryLayer, DefaultMeasurementLayer, DefaultSemanticsLayer, DefaultCompositionLayer, DefaultDeliveryLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, TranscriptOnlySemanticsLayer, UCNSSemanticsLayer, CompositeSemanticsLayer, ConsolidatedMeasurementLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, EDCMLayers, build_default_layers",
        "requires": "edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement, edcm_shared_stack",
        "rollback": "restore prior layer assembly and remove shared-stack result delivery",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Provenance-bearing EDCM stack with independently selected METAPAT semantic authority, actual UCNS geometry or typed absence, canonical local measurement, shared-stack composition, and final result-contract delivery.",
        "tests": "tests.test_measurement, tests.test_ucns_adapter, tests.test_metapat_adapter, tests.test_shared_stack_contract",
        "unresolved": "official negative-certification and theorem-status evidence envelopes remain unattached until validated schemas exist",
        "user_data_boundary": "threads caller payloads through deterministic package-local layers; transcript content is hashed in final result identity"
      },
      "file": "edcm/layers.py",
      "id": "edcm_layers"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load",
        "module_kind": "adapter",
        "module_name": "loader",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CanonLoader",
        "requires": "none",
        "rollback": "remove module; parser falls back to no embedded canon",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "read",
        "summary": "loads the v1 canon data files (bones/affixes/punct/markers) and exposes a lookup API",
        "tests": "hmmm",
        "unresolved": "dedicated canon-loader test module not located in tracked tests/",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/canon/loader.py",
      "id": "edcmbone_canon_loader"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_tok_to_dict,_dict_to_tok,_metrics_to_dict,_dict_to_metrics,_build_huffman_codes,_huffman_expected_bits",
        "module_kind": "engine",
        "module_name": "compress",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encode,decode,to_bytes,from_bytes,compression_stats",
        "requires": "edcmbone_parser_turns_rounds,edcmbone_metrics_compute",
        "rollback": "remove module; transcripts persist uncompressed",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "lossless EDCM-aware codec for ParsedTranscript + RoundMetrics (separate bone/flesh streams, zlib entropy coding)",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/compress.py",
      "id": "edcmbone_compress"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_compute_R,_compute_F,_compute_L,_compute_N,_compute_P,_compute_O,_compute_I,_compute_C,_compute_D,_compute_E,_build_phrase_patterns,_count_marker_hits",
        "module_kind": "engine",
        "module_name": "compute",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RoundMetrics,compute_round,compute_transcript,energy_step",
        "requires": "edcmbone_metrics_stats,edcmbone_metrics_risk,edcmbone_canon_loader",
        "rollback": "remove module; no behavioral metric vector produced",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "computes the EDCM metric vector M_t and dissonance energy for a parsed round/transcript",
        "tests": "tests.test_metrics_layer_designation",
        "unresolved": "per its own docstring this layer-A module canonically belongs upstream in the future edcm package",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/metrics/compute.py",
      "id": "edcmbone_metrics_compute"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "matrix",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "freeze, diff",
        "requires": "none",
        "rollback": "remove module; metric projection loses its frozen coefficient source",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "explicit freezable A matrix (Layer0->Layer1) and PROJECTION_MAP (Layer1->Layer3) as versioned, diffable dicts",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/metrics/matrix.py",
      "id": "edcmbone_metrics_matrix"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "projection",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AgentMetrics, project, project_transcript, gini_tbf, fire_alerts, crosswalk_risk",
        "requires": "edcmbone_metrics_matrix",
        "rollback": "remove module; agent-facing 6-metric view unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "projects the 11 Layer-1 Arc-Style metrics to the 6 agent-facing metrics (CM, DA, DRIFT, DVG, INT, TBF)",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/metrics/projection.py",
      "id": "edcmbone_metrics_projection"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "risk",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk",
        "requires": "none",
        "rollback": "remove module; risk composites unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "the EDCM risk proxies (fixation, broken-return, escalation, stagnation, loop), all clamped to [0,1]",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/metrics/risk.py",
      "id": "edcmbone_metrics_risk"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_count_vector",
        "module_kind": "engine",
        "module_name": "stats",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "tokenize, ngrams, ttr, repetition_ratio, shannon_entropy, rep_ngram_density, pattern_density, novelty, cosine_sim, jaccard, correction_fidelity, clamp, norm_per_100",
        "requires": "none",
        "rollback": "remove module; metric primitives unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "stdlib-only text statistics (TTR, entropy, novelty, cosine, n-gram density) feeding the EDCM metric vector",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/metrics/stats.py",
      "id": "edcmbone_metrics_stats"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_BoneClassifier, _split_turns, _group_into_rounds, _raw_tokens, _ordered_unique",
        "module_kind": "engine",
        "module_name": "turns_rounds",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "parse_transcript, BoneToken, FleshToken, Turn, Round, ParsedTranscript",
        "requires": "edcmbone_canon_loader",
        "rollback": "remove module; transcripts cannot be parsed into the EDCM structure",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "embedded rule-based transcript parser (canon-driven, no ML deps) producing bones/flesh tokens, turns, and rounds",
        "tests": "tests.test_apostrophe_normalization_and_tokenization",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/parser/turns_rounds.py",
      "id": "edcmbone_parser_turns_rounds"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_class_anchor, _wrap_with_class, _feature_payload, _build_dispatch_table",
        "module_kind": "adapter",
        "module_name": "closed_tokens",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encode, class_of, feature_payload_of",
        "requires": "edcmbone_ucns_v04",
        "rollback": "remove module; closed-token UCNS encoding unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "encodes English closed-class tokens, whitespace, punctuation, and small numerals to UCNS objects on a 16-gon host carrier",
        "tests": "tests.test_closed_tokens",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/ucns/closed_tokens.py",
      "id": "edcmbone_ucns_closed_tokens"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_lcm, _reduce_lcm",
        "module_kind": "engine",
        "module_name": "ucns_v04",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AnchorPayload, UCNSObject, unit_obj, is_unit_payload, multiply",
        "requires": "none",
        "rollback": "remove module; closed_tokens loses its UCNS object algebra",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "local UCNS engine using the turn-fraction angle convention on the doubled cover of the unit circle",
        "tests": "tests.test_ucns_objects",
        "unresolved": "this is edcmbone's local UCNS-A layer; per docs/ucns-boundary.md no UCNS-A theorem status transfers to EDCM/UCNS-G",
        "user_data_boundary": "none"
      },
      "file": "edcm/measurement/ucns/ucns_v04.py",
      "id": "edcmbone_ucns_v04"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_module_version, _failed_status, _coerce_envelope",
        "module_kind": "adapter",
        "module_name": "metapat_adapter",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "MetapatAdapter, ActualMetapatAdapter, MetapatAdapterSelection, MetapatIntegrationStatus, MetapatSemanticEvidence, MetapatAdapterConstructionError, UnsupportedMetapatSchemaError, select_metapat_adapter, inspect_metapat_adapter, missing_metapat_status",
        "requires": "optional metapat package",
        "rollback": "remove module and restore METAPAT-unavailable status in layer assembly",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "no persistence; canonical envelope data is copied into the result record",
        "summary": "EDCM-owned consumer for actual versioned immutable METAPAT semantic-authority envelopes; preserves canon identity, exact source references, constraints, permitted interpretations, hmmm, and provenance without creating metric values.",
        "tests": "tests.test_metapat_adapter, tests.test_shared_stack_contract",
        "unresolved": "official serialized UCNS bridge-record ingestion remains separate; payload-fork meaning requires explicit METAPAT authorization plus downstream topology lint",
        "user_data_boundary": "preserves caller-supplied METAPAT source statements and references exactly"
      },
      "file": "edcm/metapat_adapter.py",
      "id": "edcm_metapat_adapter"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canonical_bytes, _digest, _source_evidence, _typed_absence, _readouts, _collect_unresolved",
        "module_kind": "schema",
        "module_name": "shared_stack",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, EDCMResultContract, build_result_contract",
        "requires": "edcmucns_manifest, edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement",
        "rollback": "remove factorization-evidence compartment and restore prior result schema only with a versioned migration",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "no persistence; emits deterministic JSON-compatible records",
        "summary": "deterministic final EDCM result contract separating source evidence, METAPAT semantic authority, UCNS geometry, authoritative UCNS factorization evidence, EDCM policy identity, implementation provenance, readouts/NA, unresolved constraints, and attachment states.",
        "tests": "tests.test_shared_stack_contract, tests.test_ucns_evidence_consumer",
        "unresolved": "UCNS evidence digests provide content identity but not signed producer authentication",
        "user_data_boundary": "hashes caller transcript content and preserves caller source reference without external transmission"
      },
      "file": "edcm/shared_stack.py",
      "id": "edcm_shared_stack"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_module_version, _failed_status, _one_present, _geometry_from_record, _factorization_from_record",
        "module_kind": "adapter",
        "module_name": "ucns_adapter",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSAdapter, ActualUCNSAdapter, UCNSAdapterSelection, UCNSIntegrationStatus, UCNSGeometryEvidence, UCNSFactorizationEvidenceRecord, UCNSAdapterConstructionError, UnsupportedUCNSSchemaError, select_ucns_adapter, inspect_ucns_adapter, missing_ucns_status",
        "requires": "optional ucns package public surface including UCNSBridgeRecord and UCNSFactorizationEvidence",
        "rollback": "restore live-object-only adapter and mark serialized evidence unavailable",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "none",
        "summary": "EDCM-owned consumer over actual UCNS objects, canonical bridge records, and authoritative factorization evidence with stable-hash binding and no proof-status transfer.",
        "tests": "tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_ucns_evidence_consumer, tests.test_shared_stack_contract",
        "unresolved": "evidence digests are content identities, not cryptographic producer signatures",
        "user_data_boundary": "accepts caller-supplied UCNS objects or canonical producer records and returns deterministic evidence"
      },
      "file": "edcm/ucns_adapter.py",
      "id": "edcm_ucns_adapter"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "ucns_dependency",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "require_ucns, ucns_available, ucns_dependency_report, INSTALL_HINT",
        "requires": "edcm_ucns_adapter",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Reports independent UCNS package, adapter, object, scope, certification, and theorem-evidence states without proof-status transfer.",
        "tests": "tests.test_ucns_dependency, tests.test_ucns_adapter",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "edcm/ucns_dependency.py",
      "id": "edcm_ucns_dependency"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load_ucns, _verify_ucns_identity, _package_manifest, _split_turns, _turn_signals, _build_ucns_envelope, _structural_signatures, _flatten_structural_signatures, _evaluate_relation, _digest",
        "module_kind": "instrument",
        "module_name": "ucns_edcm_experiments",
        "network_boundary": "none; UCNS must already be installed from the pinned commit",
        "owner": "Erin Spencer",
        "public_surface": "ExperimentPartition, RelationOperator, ExperimentCase, ExpectedRelation, CandidateReadout, RelationVerdict, PolicyPreservationFinding, StructuralSignatureRecord, ExperimentReport, build_default_program, contrastive_readout, baseline_readout, run_default_experiments, main",
        "requires": "edcm_package, edcmbone_parser_turns_rounds, edcmbone_metrics_compute",
        "rollback": "remove module and workflow; frozen edcm.measurement baseline remains unchanged",
        "rollout": "explicit research runner; no default canon selection",
        "since": "2026-07-21",
        "storage_boundary": "writes only caller-selected report path",
        "summary": "runs fixed contrastive EDCM cases through the maintained EDCM baseline, a transparent candidate, explicit event-to-UCNS encodings, and noncanonical UCNS equivalence/M/B candidates",
        "tests": "tests/test_ucns_edcm_experiments.py",
        "unresolved": "external holdout custody, independent replication, and first joint canon decision authority",
        "user_data_boundary": "fixed synthetic transcripts only in the default program"
      },
      "file": "edcm/ucns_edcm_experiments.py",
      "id": "edcm_ucns_edcm_experiments"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "storage_boundary": "serialization-only",
        "summary": "EDCM verifies authority-to-geometry binding but does not invent METAPAT meaning, alter UCNS algebra, or transfer proof status into measurement validity",
        "user_data_boundary": "no transcript or measurement values"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_ucns_fork_lint_boundary"
    },
    {
      "block": "CAPABILITIES",
      "fields": {
        "boundaries": "auth:none, storage:serialization-only, network:none, user_data:semantic provenance only",
        "exposes": "edcm.lint_all_payload_forks",
        "inputs": "actual UCNSObject root and AuthorizedUCNSFork declarations",
        "outputs": "UCNSForkLintReport or typed failure",
        "summary": "validates every actual recursive UCNS payload fork against one exact METAPAT authorization and topology binding"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fail_closed_ucns_fork_lint"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "integration_contract",
        "given": "a METAPAT authorization is bound to an actual UCNS fork",
        "then": "root hash, fork path/hash, payload indices, ordered child ids/hashes, canon, policy, and authorization digest are exact"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_binding_exact_topology"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "schema_contract",
        "given": "a topology binding is serialized and reconstructed",
        "then": "every field survives exactly and malformed or tampered records fail closed"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_binding_roundtrip"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a recursive UCNS object is linted",
        "then": "every object with at least two payload children has exactly one valid declaration"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_complete_coverage"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "UCNS or METAPAT is directly absent or transitively broken",
        "then": "direct absence is typed and transitive import failure remains visible"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_dependency_visible"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "payload order, cell indices, object hashes, canon, policy, or producer authorization changes",
        "then": "lint fails closed"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_drift_rejected"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a declaration is missing, duplicated, or targets a non-fork path",
        "then": "lint fails closed"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_missing_extra_rejected"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "boundary_contract",
        "given": "geometry has fewer than two payload children or no declaration",
        "then": "no constitutive meaning is inferred; only actual forks require explicit authority"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_no_inference"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "boundary_contract",
        "given": "a valid binding and lint report",
        "then": "theorem_status_transfer and measurement_validity_claim remain false"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_fork_lint_no_status_transfer"
    },
    {
      "block": "DOCS",
      "fields": {
        "audience": "developer",
        "covers": "UCNSForkTopologyBinding, build_fork_topology_binding, lint_fork_topology, lint_all_payload_forks",
        "source": "docs/ucns-fork-lint.md",
        "status": "current",
        "summary": "documents exact topology binding, complete recursive coverage, negative fixtures, and authority boundaries"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_ucns_fork_lint_docs"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load_stack, _canonical_json, _text, _strings, _indices, _binding_payload, _binding_digest, _resolve_path, _payload_cells",
        "module_kind": "adapter",
        "module_name": "ucns_fork_lint",
        "network_boundary": "optional package import only; no network performed by runtime code",
        "owner": "Erin Spencer",
        "public_surface": "UCNSForkTopologyBinding, AuthorizedUCNSFork, UCNSForkLintReport, ForkLintDependencyError, ForkTopologyError, build_fork_topology_binding, lint_fork_topology, lint_all_payload_forks, enumerate_payload_fork_paths",
        "requires": "edcm_metapat_adapter, edcm_ucns_adapter",
        "rollback": "remove exports and consumer call sites; METAPAT authorization and UCNS geometry remain separate upstream authorities",
        "rollout": "optional_full_stack_integration",
        "since": "2026-07-15",
        "storage_boundary": "serialization-only",
        "summary": "binds METAPAT constitutive-fork authorizations to exact UCNS payload paths, indices, and stable hashes and fails closed over the complete recursive object",
        "tests": "tests.test_ucns_fork_lint",
        "unresolved": "no accepted production fixture exists until a caller supplies complete authorizations for every actual payload fork",
        "user_data_boundary": "semantic module ids and unresolved constraints remain producer provenance; transcript content and measurement values are not accepted"
      },
      "file": "edcm/ucns_fork_lint.py",
      "id": "edcm_ucns_fork_lint"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load_ucns, _canonical_metric_id, _metric_definition, _as_fraction, _clamp_fraction, _record_tuple, _encode_record, _resolved_from_record",
        "module_kind": "adapter",
        "module_name": "ucns_metrics",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "MetricDefinition, ResolvedMetricUCNS, UCNSMetricDependencyError, UCNSMetricResolutionError, METRIC_DEFINITIONS, SYMBOL_TO_METRIC_ID, resolve_metric_axis, resolve_metric_value, resolve_metric_vector, resolve_round_metrics, resolved_metric_objects_payload",
        "requires": "edcm_ucns_adapter",
        "rollback": "remove module exports and resolved-metric call sites; scalar EDCM outputs remain unchanged",
        "rollout": "optional_ucns_integration",
        "since": "2026-07-15",
        "storage_boundary": "none",
        "summary": "resolves scalar EDCM metric axes and observations into canonical UCNS audit objects without changing metric formulas",
        "tests": "tests.test_ucns_metrics",
        "unresolved": "UCNS objects provide canonical content identity but not signed producer or transport authentication",
        "user_data_boundary": "metric context identifiers and scalar observations remain caller-supplied audit metadata"
      },
      "file": "edcm/ucns_metrics.py",
      "id": "edcm_ucns_metrics"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_clamp_unit, _sign",
        "module_kind": "engine",
        "module_name": "ucns_objects",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, field_motion_fixture, canonical_axes",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "dependency-free mirror of edcmbone's UCNS metric construction layer (v0.2 signed-axis orthogonality)",
        "tests": "tests.test_ucns_objects",
        "unresolved": "mirror of edcmbone backend/src/edcmbone/metrics/orthogonality.py; keep in sync",
        "user_data_boundary": "none"
      },
      "file": "edcm/ucns_objects.py",
      "id": "edcm_ucns_objects"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contrastive_order_multiplicity_resolution",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments.py",
      "id": "check_contrastive_order_multiplicity_resolution"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_joint_runner_preserves_no_canon",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_ucns_edcm_experiments.py",
      "id": "check_joint_runner_preserves_no_canon"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_default_program_structure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments.py",
      "id": "check_ucns_edcm_program_structure"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_binding_captures_exact_payload_topology",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_binding_exact_topology"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_binding_exact"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_recursive_lint_accepts_every_declared_fork",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_complete_coverage"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_complete_coverage"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_direct_dependency_absence_is_typed",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_dependency_visible"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_dependency"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_payload_order_or_object_drift_fails_closed",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_drift_rejected"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_drift"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_missing_duplicate_and_extra_declarations_fail_closed",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_missing_extra_rejected"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_missing_extra"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_single_payload_is_not_silently_typed_as_a_fork",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_no_inference"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_no_inference"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_binding_roundtrip_is_strict_and_tamper_evident",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_binding_roundtrip"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_roundtrip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_valid_report_preserves_status_firewall",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_fork_lint_no_status_transfer"
      },
      "file": "tests/test_ucns_fork_lint.py",
      "id": "check_edcm_fork_status_firewall"
    }
  ],
  "edges": [
    {
      "from": "edcm_fail_closed_ucns_fork_lint",
      "kind": "exposes",
      "source_block": "CAPABILITIES",
      "source_id": "edcm_fail_closed_ucns_fork_lint",
      "to": "edcm.lint_all_payload_forks"
    },
    {
      "from": "edcm_fail_closed_ucns_fork_lint",
      "kind": "risk",
      "source_block": "CAPABILITIES",
      "source_id": "edcm_fail_closed_ucns_fork_lint",
      "to": "auth:none"
    },
    {
      "from": "edcm_fail_closed_ucns_fork_lint",
      "kind": "risk",
      "source_block": "CAPABILITIES",
      "source_id": "edcm_fail_closed_ucns_fork_lint",
      "to": "network:none"
    },
    {
      "from": "edcm_fail_closed_ucns_fork_lint",
      "kind": "risk",
      "source_block": "CAPABILITIES",
      "source_id": "edcm_fail_closed_ucns_fork_lint",
      "to": "storage:serialization-only"
    },
    {
      "from": "edcm_fail_closed_ucns_fork_lint",
      "kind": "risk",
      "source_block": "CAPABILITIES",
      "source_id": "edcm_fail_closed_ucns_fork_lint",
      "to": "user_data:semantic provenance only"
    },
    {
      "from": "check_contrastive_order_multiplicity_resolution",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contrastive_order_multiplicity_resolution",
      "to": "self::test_contrastive_order_multiplicity_resolution"
    },
    {
      "from": "check_contrastive_order_multiplicity_resolution",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contrastive_order_multiplicity_resolution",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "check_contrastive_order_multiplicity_resolution",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contrastive_order_multiplicity_resolution",
      "to": "python3"
    },
    {
      "from": "check_edcm_fork_binding_exact",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_binding_exact",
      "to": "self::test_binding_captures_exact_payload_topology"
    },
    {
      "from": "check_edcm_fork_binding_exact",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_binding_exact",
      "to": "edcm_fork_binding_exact_topology"
    },
    {
      "from": "check_edcm_fork_complete_coverage",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_complete_coverage",
      "to": "self::test_complete_recursive_lint_accepts_every_declared_fork"
    },
    {
      "from": "check_edcm_fork_complete_coverage",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_complete_coverage",
      "to": "edcm_fork_lint_complete_coverage"
    },
    {
      "from": "check_edcm_fork_dependency",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_dependency",
      "to": "self::test_direct_dependency_absence_is_typed"
    },
    {
      "from": "check_edcm_fork_dependency",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_dependency",
      "to": "edcm_fork_lint_dependency_visible"
    },
    {
      "from": "check_edcm_fork_drift",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_drift",
      "to": "self::test_payload_order_or_object_drift_fails_closed"
    },
    {
      "from": "check_edcm_fork_drift",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_drift",
      "to": "edcm_fork_lint_drift_rejected"
    },
    {
      "from": "check_edcm_fork_missing_extra",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_missing_extra",
      "to": "self::test_missing_duplicate_and_extra_declarations_fail_closed"
    },
    {
      "from": "check_edcm_fork_missing_extra",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_missing_extra",
      "to": "edcm_fork_lint_missing_extra_rejected"
    },
    {
      "from": "check_edcm_fork_no_inference",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_no_inference",
      "to": "self::test_single_payload_is_not_silently_typed_as_a_fork"
    },
    {
      "from": "check_edcm_fork_no_inference",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_no_inference",
      "to": "edcm_fork_lint_no_inference"
    },
    {
      "from": "check_edcm_fork_roundtrip",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_roundtrip",
      "to": "self::test_binding_roundtrip_is_strict_and_tamper_evident"
    },
    {
      "from": "check_edcm_fork_roundtrip",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_roundtrip",
      "to": "edcm_fork_binding_roundtrip"
    },
    {
      "from": "check_edcm_fork_status_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_status_firewall",
      "to": "self::test_valid_report_preserves_status_firewall"
    },
    {
      "from": "check_edcm_fork_status_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_fork_status_firewall",
      "to": "edcm_fork_lint_no_status_transfer"
    },
    {
      "from": "check_joint_runner_preserves_no_canon",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_joint_runner_preserves_no_canon",
      "to": "self::test_joint_runner_preserves_no_canon"
    },
    {
      "from": "check_joint_runner_preserves_no_canon",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_joint_runner_preserves_no_canon",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "check_joint_runner_preserves_no_canon",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_joint_runner_preserves_no_canon",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_program_structure",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_program_structure",
      "to": "self::test_default_program_structure"
    },
    {
      "from": "check_ucns_edcm_program_structure",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_program_structure",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "check_ucns_edcm_program_structure",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_program_structure",
      "to": "python3"
    },
    {
      "from": "edcm_ucns_fork_lint_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcm_ucns_fork_lint_docs",
      "to": "UCNSForkTopologyBinding"
    },
    {
      "from": "edcm_ucns_fork_lint_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcm_ucns_fork_lint_docs",
      "to": "build_fork_topology_binding"
    },
    {
      "from": "edcm_ucns_fork_lint_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcm_ucns_fork_lint_docs",
      "to": "lint_all_payload_forks"
    },
    {
      "from": "edcm_ucns_fork_lint_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcm_ucns_fork_lint_docs",
      "to": "lint_fork_topology"
    },
    {
      "from": "edcm_energy_claims",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_energy_claims",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_energy_claims",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_energy_claims",
      "to": "edcm_ucns_dependency"
    },
    {
      "from": "edcm_falsifiability_bridge",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_falsifiability_bridge",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_falsifiability_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_falsifiability_bridge",
      "to": "edcm_energy_claims"
    },
    {
      "from": "edcm_integrity",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_integrity",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_integrity",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_integrity",
      "to": "edcm_measurement"
    },
    {
      "from": "edcm_integrity",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_integrity",
      "to": "edcm_ucns_objects"
    },
    {
      "from": "edcm_language_affixes",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_affixes",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_affixes",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_affixes",
      "to": "edcm measurement canon bones_affixes_v1.json"
    },
    {
      "from": "edcm_language_artifacts",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_artifacts",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_artifacts",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_artifacts",
      "to": "edcmbone_ucns_v04"
    },
    {
      "from": "edcm_language_composition",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_composition",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_composition",
      "to": "edcm_language_model"
    },
    {
      "from": "edcm_language_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_composition",
      "to": "edcmbone_ucns_v04"
    },
    {
      "from": "edcm_language_glyph_floor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_glyph_floor",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_glyph_floor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_glyph_floor",
      "to": "edcm_language_manifest"
    },
    {
      "from": "edcm_language_manifest",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_manifest",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_manifest",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_manifest",
      "to": "none"
    },
    {
      "from": "edcm_language_model",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_model",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_model",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_model",
      "to": "none"
    },
    {
      "from": "edcm_language_morphology",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_morphology",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_morphology",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_morphology",
      "to": "edcm_language_affixes"
    },
    {
      "from": "edcm_language_morphology",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_morphology",
      "to": "edcm_language_model"
    },
    {
      "from": "edcm_language_morphology",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_morphology",
      "to": "edcm_language_rendering"
    },
    {
      "from": "edcm_language_oewn_source",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_oewn_source",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_oewn_source",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_oewn_source",
      "to": "PyYAML only during artifact construction"
    },
    {
      "from": "edcm_language_package",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_affixes"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_artifacts"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_composition"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_glyph_floor"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_manifest"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_model"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_morphology"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_oewn_source"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_placement"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_rendering"
    },
    {
      "from": "edcm_language_placement",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_placement",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_placement",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_placement",
      "to": "edcm_language_manifest"
    },
    {
      "from": "edcm_language_rendering",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_rendering",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_rendering",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_rendering",
      "to": "edcm_language_affixes"
    },
    {
      "from": "edcm_layers",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_layers",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_layers",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_layers",
      "to": "edcm_measurement"
    },
    {
      "from": "edcm_layers",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_layers",
      "to": "edcm_metapat_adapter"
    },
    {
      "from": "edcm_layers",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_layers",
      "to": "edcm_shared_stack"
    },
    {
      "from": "edcm_layers",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_layers",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_metapat_adapter",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_metapat_adapter",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_metapat_adapter",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_metapat_adapter",
      "to": "optional metapat package"
    },
    {
      "from": "edcm_package",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_energy_claims"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_falsifiability_bridge"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_integrity"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_language_package"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_layers"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_metapat_adapter"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_shared_stack"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_ucns_fork_lint"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_ucns_metrics"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcm_ucns_objects"
    },
    {
      "from": "edcm_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_package",
      "to": "edcmucns_package"
    },
    {
      "from": "edcm_shared_stack",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_shared_stack",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_shared_stack",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_shared_stack",
      "to": "edcm_measurement"
    },
    {
      "from": "edcm_shared_stack",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_shared_stack",
      "to": "edcm_metapat_adapter"
    },
    {
      "from": "edcm_shared_stack",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_shared_stack",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_shared_stack",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_shared_stack",
      "to": "edcmucns_manifest"
    },
    {
      "from": "edcm_ucns_adapter",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_adapter",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_adapter",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_adapter",
      "to": "optional ucns package public surface including UCNSBridgeRecord and UCNSFactorizationEvidence"
    },
    {
      "from": "edcm_ucns_dependency",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_dependency",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_dependency",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_dependency",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_ucns_edcm_experiments",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_edcm_experiments",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments",
      "to": "edcm_package"
    },
    {
      "from": "edcm_ucns_edcm_experiments",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcm_ucns_edcm_experiments",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcm_ucns_fork_lint",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_fork_lint",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_fork_lint",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_fork_lint",
      "to": "edcm_metapat_adapter"
    },
    {
      "from": "edcm_ucns_fork_lint",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_fork_lint",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_ucns_metrics",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_metrics",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_metrics",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_metrics",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_ucns_objects",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_objects",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_objects",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_objects",
      "to": "none"
    },
    {
      "from": "edcmbone_canon_loader",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_canon_loader",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_canon_loader",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_canon_loader",
      "to": "none"
    },
    {
      "from": "edcmbone_compress",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_compress",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcmbone_compress",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_canon_loader"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_metrics_risk"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_metrics_stats"
    },
    {
      "from": "edcmbone_metrics_matrix",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_matrix",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_matrix",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_matrix",
      "to": "none"
    },
    {
      "from": "edcmbone_metrics_projection",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_projection",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_projection",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_projection",
      "to": "edcmbone_metrics_matrix"
    },
    {
      "from": "edcmbone_metrics_risk",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_risk",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_risk",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_risk",
      "to": "none"
    },
    {
      "from": "edcmbone_metrics_stats",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_stats",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_stats",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_stats",
      "to": "none"
    },
    {
      "from": "edcmbone_parser_turns_rounds",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_parser_turns_rounds",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_parser_turns_rounds",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_parser_turns_rounds",
      "to": "edcmbone_canon_loader"
    },
    {
      "from": "edcmbone_ucns_closed_tokens",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_closed_tokens",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_ucns_closed_tokens",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_closed_tokens",
      "to": "edcmbone_ucns_v04"
    },
    {
      "from": "edcmbone_ucns_v04",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_v04",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_ucns_v04",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_v04",
      "to": "none"
    },
    {
      "from": "edcmucns_composer",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_composer",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_composer",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_composer",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_encoder",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_encoder",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_encoder",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_encoder",
      "to": "edcmucns_geometry"
    },
    {
      "from": "edcmucns_encoder",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_encoder",
      "to": "edcmucns_manifest"
    },
    {
      "from": "edcmucns_encoder",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_encoder",
      "to": "edcmucns_provenance"
    },
    {
      "from": "edcmucns_encoder",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_encoder",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_epochs",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_epochs",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_epochs",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_epochs",
      "to": "edcmucns_composer"
    },
    {
      "from": "edcmucns_epochs",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_epochs",
      "to": "edcmucns_manifest"
    },
    {
      "from": "edcmucns_epochs",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_epochs",
      "to": "edcmucns_provenance"
    },
    {
      "from": "edcmucns_epochs",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_epochs",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_equivalence",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_equivalence",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_equivalence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_equivalence",
      "to": "edcmucns_geometry"
    },
    {
      "from": "edcmucns_equivalence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_equivalence",
      "to": "edcmucns_provenance"
    },
    {
      "from": "edcmucns_equivalence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_equivalence",
      "to": "edcmucns_scopes"
    },
    {
      "from": "edcmucns_equivalence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_equivalence",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_field_reader",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_field_reader",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_field_reader",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_field_reader",
      "to": "edcm.ucns_objects"
    },
    {
      "from": "edcmucns_field_reader",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_field_reader",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_geometry",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_geometry",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_geometry",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_geometry",
      "to": "edcmucns_types"
    },
    {
      "from": "edcmucns_manifest",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_manifest",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_manifest",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_manifest",
      "to": "none"
    },
    {
      "from": "edcmucns_package",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_package",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_package",
      "to": "edcm.ucns_objects"
    },
    {
      "from": "edcmucns_provenance",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_provenance",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_provenance",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_provenance",
      "to": "none"
    },
    {
      "from": "edcmucns_scopes",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_scopes",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_scopes",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_scopes",
      "to": "none"
    },
    {
      "from": "edcmucns_types",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_types",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_types",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_types",
      "to": "edcmucns_provenance"
    },
    {
      "from": "edcmucns_validation",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_validation",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmucns_validation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_validation",
      "to": "edcmucns_geometry"
    },
    {
      "from": "edcmucns_validation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_validation",
      "to": "edcmucns_manifest"
    },
    {
      "from": "edcmucns_validation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_validation",
      "to": "edcmucns_provenance"
    },
    {
      "from": "edcmucns_validation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmucns_validation",
      "to": "edcmucns_types"
    }
  ],
  "gaps": [],
  "repo": "The-Interdependency/edcm"
});
