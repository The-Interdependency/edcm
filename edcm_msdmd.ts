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
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_phrase_counts, _v2_turn_signals, _build_v2_envelope, _candidate_values_for_case, _dose_curve_findings, _phrase_coverage_findings, _latency_findings, _support_findings",
        "module_kind": "instrument",
        "module_name": "ucns_edcm_experiments_v2",
        "network_boundary": "none; exact UCNS checkout and installed package are verified locally",
        "owner": "Erin Spencer",
        "public_surface": "V2ExperimentReport, DoseCurveFinding, PhraseCoverageFinding, LatencyFinding, SupportStabilityFinding, occurrence_coverage_readout, build_v2_program, run_v2_experiments, main",
        "requires": "edcm_ucns_edcm_experiments, edcmbone_parser_turns_rounds, edcmbone_metrics_compute",
        "rollback": "remove v0.2 module, workflow calls, and result; v0.1 and frozen baseline remain unchanged",
        "rollout": "explicit versioned research program; v0.1 evidence remains immutable and no canon selection is made",
        "since": "2026-07-21",
        "storage_boundary": "writes only caller-selected report path",
        "summary": "expands the joint UCNS-EDCM falsifier program across refusal dose, constraint paraphrase coverage, resolution latency, and explicit support-assignment stability",
        "tests": "tests/test_ucns_edcm_experiments_v2.py",
        "unresolved": "independent paraphrase corpus, external outcome labels, sealed holdout custody, replication, and joint canon decision authority",
        "user_data_boundary": "fixed synthetic development and holdout transcripts only"
      },
      "file": "edcm/ucns_edcm_experiments_v2.py",
      "id": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_split_scope_turns, _quote_spans, _mention_events, _repair_events, _extract_scope_events, _build_scope_envelope, _scope_signatures, _pair_findings",
        "module_kind": "instrument",
        "module_name": "ucns_edcm_experiments_v3",
        "network_boundary": "none; exact UCNS checkout and installed package are verified locally",
        "owner": "Erin Spencer",
        "public_surface": "ScopeEvent, ScopeSignatureRecord, ScopePairFinding, V3ExperimentReport, scope_assertion_readout, build_v3_program, run_v3_experiments, main",
        "requires": "edcm_ucns_edcm_experiments, edcm_ucns_edcm_experiments_v2, edcmbone_parser_turns_rounds, edcmbone_metrics_compute",
        "rollback": "remove v0.3 module, workflow calls, and result; earlier reports and frozen baseline remain unchanged",
        "rollout": "explicit versioned research program; v0.1 and v0.2 remain immutable and no canon selection is made",
        "since": "2026-07-21",
        "storage_boundary": "writes only caller-selected report path",
        "summary": "tests assertion, negation, quotation, hypotheticals, attribution, retraction, and repair order through scope-bearing EDCM events and UCNS structural projections",
        "tests": "tests/test_ucns_edcm_experiments_v3.py",
        "unresolved": "full discourse scope, independent annotation, multilingual scope, external replication, and joint canon decision authority",
        "user_data_boundary": "fixed synthetic development and holdout transcripts only"
      },
      "file": "edcm/ucns_edcm_experiments_v3.py",
      "id": "edcm_ucns_edcm_experiments_v3"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_candidate_targets, _apply_edges, _graph_views, _build_ucns_graph_envelope, _resolution_readout, _pair_findings",
        "module_kind": "instrument",
        "module_name": "ucns_edcm_experiments_v4",
        "network_boundary": "none; exact UCNS checkout and installed package are verified locally",
        "owner": "Erin Spencer",
        "public_surface": "DiscourseNode, ReferenceExpression, GraphEdge, GraphInterpretation, GraphResolution, GraphSignatureRecord, GraphPairFinding, V4ExperimentReport, build_v4_program, resolve_case, run_v4_experiments, main",
        "requires": "edcm_ucns_edcm_experiments, edcm_ucns_edcm_experiments_v2, edcm_ucns_edcm_experiments_v3, edcmbone_parser_turns_rounds, edcmbone_metrics_compute",
        "rollback": "remove v0.4 module, workflow calls, and result; earlier reports and frozen baseline remain unchanged",
        "rollout": "explicit versioned research program; v0.1-v0.3 remain immutable and no canon selection is made",
        "since": "2026-07-21",
        "storage_boundary": "writes only caller-selected report path",
        "summary": "tests cross-turn reference resolution, correction targets, anaphora, nested quotation, suspension, conditional activation, contradiction ownership, and competing discourse graphs",
        "tests": "tests/test_ucns_edcm_experiments_v4.py",
        "unresolved": "general anaphora, cyclic reference, independent annotation, multilingual discourse, external replication, and joint canon authority",
        "user_data_boundary": "fixed synthetic transcripts with declared node/reference annotations only"
      },
      "file": "edcm/ucns_edcm_experiments_v4.py",
      "id": "edcm_ucns_edcm_experiments_v4"
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
      "block": "LLMS",
      "fields": {
        "content": "- Skills live as root directories with SKILL.md files and optional helpers."
      },
      "file": "skill-lib/llms/metadata.py",
      "id": "architecture_summary"
    },
    {
      "block": "LLMS",
      "fields": {
        "msdmd": "Module Self-Declared Metadata in Markdown \u2014 the foundational convention where each source module declares its own structured metadata in a fenced comment block."
      },
      "file": "skill-lib/llms/metadata.py",
      "id": "key_definitions"
    },
    {
      "block": "LLMS",
      "fields": {
        "content": "skill-lib is the canonical organization-wide source for reusable agent skills in The Interdependency."
      },
      "file": "skill-lib/llms/metadata.py",
      "id": "project_overview"
    },
    {
      "block": "LLMS",
      "fields": {
        "content": "- Read AGENTS.md, skills.json, and the relevant skill file before changing a skill."
      },
      "file": "skill-lib/llms/metadata.py",
      "id": "usage_rules"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "`loto clear` on a scar",
        "then": "refused on dirty tree; on clean tree produces a commit touching zero files, carrying scar trailers, and deletes the scar"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_clear_is_empty_commit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "one in-scope mutation commit and passing test evidence; `loto close`",
        "then": ".loto/ is empty and HEAD carries Loto-* trailers; git is the only archive"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_close_deletes_tag"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a failing run of a test command followed by a passing run of the identical command",
        "then": "close proceeds; a distinct command whose latest run failed still blocks close"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_latest_test_wins"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "more than one commit between base and HEAD at close",
        "then": "close refuses (v0.1 invariant: one session, one mutation commit)"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_one_commit_per_session"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "clean working tree; `loto open` succeeds",
        "then": "working tree is still clean; exclusion went to .git/info/exclude, never .gitignore"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_open_never_dirties"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "an unacknowledged SCAR-*.json in .loto/",
        "then": "`loto open` refuses and `loto guard` exits nonzero"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_scar_blocks_work"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "files touched outside the declared --files globs",
        "then": "close refuses with the violating paths named"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "loto_scope_enforced"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load, _save, _touched_files, _scope_violations, _trailers, _digest, _commit, _git, _ensure_gitignored",
        "module_kind": "instrument",
        "module_name": "repo_loto",
        "network_boundary": "none",
        "owner": "Way Seer Erin",
        "public_surface": "loto open, loto run, loto test, loto close, loto fail, loto clear, loto status, loto guard, loto install-hook",
        "rollback": "rm -rf .loto/ and remove hook line",
        "rollout": "manual invocation; pre-push hook calls `loto guard`",
        "storage_boundary": "write",
        "summary": "delete-on-completion session gate for repo mutation; presence of state means open work, absence means clean",
        "tests": "tests/test_repo_loto.py (CHECKS-declared, reconciled via --audit)",
        "unresolved": "credential-gate integration, ratios bookends",
        "user_data_boundary": "none"
      },
      "file": "skill-lib/skill_lib/safety/repo_loto.py",
      "id": "repo_mutation_gate"
    },
    {
      "block": "DOCS",
      "fields": {
        "source": "docs/module.md",
        "status": "current",
        "summary": "module docs"
      },
      "file": "skill-lib/tests/test_collect.py",
      "id": "module_docs"
    },
    {
      "block": "LLMS",
      "fields": {
        "content": "example only"
      },
      "file": "skill-lib/tests/test_llms_build.py",
      "id": "project_overview"
    },
    {
      "block": "LLMS",
      "fields": {
        "content": "real declaration"
      },
      "file": "skill-lib/tests/test_llms_build.py",
      "id": "project_overview"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_clear_is_empty_commit",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_clear_is_empty_commit",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_clear_is_empty_commit"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_close_deletes_tag",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_close_deletes_tag",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_close_deletes_tag"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_latest_test_wins",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_latest_test_wins",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_latest_test_wins"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_one_commit_per_session",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_one_commit_per_session",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_one_commit_per_session"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_open_never_dirties",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_open_never_dirties",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_open_never_dirties"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_scar_blocks_work",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_scar_blocks_work",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_scar_blocks_work"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_scope_enforced",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "loto_scope_enforced",
        "requires": "git, python3, posix_shell",
        "timeout": "20"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "check_scope_enforced"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "internal_surface": "_mk_repo, _run, _loto, _parse_block, _resolve_call, _requires_met",
        "module_kind": "checks",
        "module_name": "test_repo_loto",
        "owner": "Way Seer Erin",
        "public_surface": "test_* functions, main, --audit",
        "summary": "evidentiary procedures for repo_loto CONTRACTS; standalone or pytest; --audit reconciles the declared graph without execution",
        "tests": "self",
        "unresolved": "mutation-level verification that checks actually exercise their contracts"
      },
      "file": "skill-lib/tests/test_repo_loto.py",
      "id": "repo_loto_evidence"
    },
    {
      "block": "DOCS",
      "fields": {
        "summary": "second"
      },
      "file": "skill-lib/tests/test_universal_parser.py",
      "id": "second_docs"
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
        "call": "self::test_occurrence_coverage_candidate_invariants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v2",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v2.py",
      "id": "check_occurrence_coverage_candidate"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v2_joint_report_preserves_prior_evidence_and_no_canon",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v2",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_ucns_edcm_experiments_v2.py",
      "id": "check_ucns_edcm_v2_joint_report"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v2_program_structure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v2",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v2.py",
      "id": "check_ucns_edcm_v2_program"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_scope_assertion_candidate_invariants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v3",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v3.py",
      "id": "check_scope_assertion_candidate"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v3_joint_report_preserves_scope_and_no_canon",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v3",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_ucns_edcm_experiments_v3.py",
      "id": "check_ucns_edcm_v3_joint_report"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v3_program_structure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v3",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v3.py",
      "id": "check_ucns_edcm_v3_program"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v4_joint_report_preserves_graphs_and_no_canon",
        "cleanup": "pytest tmp_path",
        "mutates": "temporary report only",
        "proves": "edcm_ucns_edcm_experiments_v4",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_ucns_edcm_experiments_v4.py",
      "id": "check_ucns_edcm_v4_joint_report"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v4_program_structure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v4",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v4.py",
      "id": "check_ucns_edcm_v4_program"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v4_resolver_contrasts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_edcm_experiments_v4",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_ucns_edcm_experiments_v4.py",
      "id": "check_ucns_edcm_v4_resolvers"
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
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_addition_boundary, test_r_additive_under_multiply, test_concat_is_associative, test_concat_right_distributive, test_concat_left_distributivity_fails, test_concat_noncommutative, test_mutation_caught",
        "module_kind": "experiment",
        "module_name": "addition_boundary",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "n/a",
        "rollout": "sets the full operation set for the base geometry",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "rule whether a primitive addition exists or radial growth stays derived",
        "tests": "contracts.test_addition_boundary",
        "unresolved": "none - ruled: no second primitive; concatenation stays derived",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_addition_boundary.py",
      "id": "addition_boundary"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_multiply_associativity, test_random_triples, test_adversarial_triples, test_full_sequence_carried, test_mutation_caught",
        "module_kind": "experiment",
        "module_name": "multiply_associativity",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "keep as open",
        "rollout": "gates every structure name in O6 (monoid requires it)",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "prove or bound (a x b) x c = a x (b x c)",
        "tests": "contracts.test_associativity_triples",
        "unresolved": "none - resolved: the payload carries the full angle sequence; mean-collapse exists only in the projection",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_associativity_triples.py",
      "id": "multiply_associativity"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_multiply_commutativity_ruling, test_noncommutative_witness, test_projection_always_commutes, test_towers_are_central, test_long_objects_not_central, test_nontower_payload_not_central, test_mutation_caught",
        "module_kind": "experiment",
        "module_name": "commutativity_ruling",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "n/a",
        "rollout": "fixes whether O5 needs left AND right division (it does)",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "prove non-commutative in general; characterize the commuting subclass",
        "tests": "contracts.test_commutator",
        "unresolved": "none - ruling landed: commutator lives in sequence ordering, not chirality",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_commutator.py",
      "id": "multiply_commutativity_ruling"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_multiply_identity, test_left_identity, test_right_identity, test_none_sentinel, test_unit_group_not_identity, test_mutation_caught",
        "module_kind": "engine",
        "module_name": "multiply_identity",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "n/a",
        "rollout": "required for any monoid/group claim in O6",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "prove the normalized factorization identity is two-sided; do not conflate it with the public-gonol SPACE/ZERO twist origin",
        "tests": "contracts.test_identity_two_sided",
        "unresolved": "bridge between the fixed-origin public gonol and ordinary normalized factorization objects remains hmmm",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_identity_two_sided.py",
      "id": "multiply_identity"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "test_singleton_gauge_collapse, test_product_closure, test_idempotent_census_bounded, test_local_groups_bounded, test_depth_two_ghost_home_relative, test_radius_max_law, test_breadth_plus_law, test_zero_breadth_spindle, test_first_level_fork_law, test_mutations_caught",
        "module_kind": "test",
        "module_name": "local_groups_and_relational_geometry",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "contract_local_groups_and_relational_geometry",
        "requires": "ucns_relational_geometry, ucns_canonical",
        "rollback": "remove contract and shim entry",
        "rollout": "default_enabled",
        "since": "2026-07-14",
        "storage_boundary": "none",
        "summary": "mutation-backed witnesses for idempotent towers, home-relative local groups, radius, breadth, spindle, and fork laws",
        "tests": "contracts.test_local_groups_and_geometry, tests.test_base_geometry_contracts",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_local_groups_and_geometry.py",
      "id": "local_groups_relational_geometry_contracts"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_multiply_well_defined, test_totality_and_grading, test_representation_independence, test_empty_carrier_boundary, test_mutation_caught",
        "module_kind": "engine",
        "module_name": "multiply_totality",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "revert to empirical closure",
        "rollout": "backbone; everything downstream assumes it",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "prove multiply is total and canonical (representation-independent) at all depths",
        "tests": "contracts.test_multiply_canonical",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_multiply_canonical.py",
      "id": "multiply_well_defined"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_division_theory, test_enumerator_exhaustive_universe, test_soundness_random, test_length_gate, test_multiplicity_towers, test_flat_divisor_cancellativity, test_cancellativity_dichotomy, test_v06_scope_correction, test_greedy_left_quotient_still_sound, test_mutation_caught",
        "module_kind": "engine",
        "module_name": "division_theory",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "rollback": "keep left_factors as standing hmmm",
        "rollout": "this IS \"division and the like\"",
        "since": "2026-07-10",
        "storage_boundary": "read",
        "summary": "left/right quotient solvability and multiplicity for multiply",
        "tests": "contracts.test_quotient_solvability",
        "unresolved": "AlignedComplete-domain cancellativity proof remains a formal/ obligation; canonical-choice procedure among multiple quotients remains open (structural, per O6)",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_quotient_solvability.py",
      "id": "division_theory"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "contract_structure_naming, test_monoid_axioms, test_grading, test_unit_group_is_z2, test_not_cancellative, test_center_sample, test_idempotents_exist, test_mutation_caught",
        "module_kind": "engine",
        "module_name": "structure_theorem",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "requires": "multiply_well_defined, multiply_identity, multiply_associativity, multiply_commutativity_ruling, division_theory",
        "rollback": "n/a",
        "rollout": "base geometry complete == this theorem lands",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "name the algebraic object (UCNS, multiply) given O1-O5 and the r-grading",
        "tests": "contracts.test_structure_axioms",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/contracts/test_structure_axioms.py",
      "id": "structure_naming"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "a0_safe",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "identity, describe, canonical, factor, UCNSObjectRecord, FactorizationResult",
        "requires": "ucns_object_record, ucns_factorization_result, ucns_serialization, ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "A0-safe public facade for inspecting, identifying, canonicalizing, and factoring UCNS objects via evidence-bearing scoped envelopes.",
        "tests": "ucns_recursive/tests/test_a0_safe.py, tests/test_certified_negative_results.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/a0_safe.py",
      "id": "ucns_a0_safe"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_object_to_data, _object_from_data, _require",
        "module_kind": "adapter",
        "module_name": "bridge",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "BRIDGE_SCHEMA, BRIDGE_SCHEMA_VERSION, BridgeValidationError, BridgeImport, export_bridge_record, import_bridge_record",
        "requires": "ucns_canonical, ucns_serialization",
        "rollback": "remove module and its re-exports; sibling adapters fall back to repo-local encodings",
        "rollout": "default_enabled additive public API; sibling repos consume the record shape, not UCNS internals",
        "since": "2026-07-12",
        "storage_boundary": "none",
        "summary": "Versioned neutral bridge record plus fail-closed import/export adapter between actual UCNSObjects and sibling repositories, preserving equality and stable hash and carrying provenance without theorem status.",
        "tests": "tests/test_bridge_round_trip.py, tests/test_stack_contract_suite.py, tests/test_bridge_certification_boundary.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/bridge.py",
      "id": "ucns_bridge"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_addition_boundary.contract_addition_boundary",
        "class": "correctness",
        "given": "the derived candidate addition (top-level sequence concatenation)",
        "then": "no second primitive operation exists in the base geometry; r is"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "addition_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_associativity_triples.contract_multiply_associativity",
        "class": "correctness",
        "given": "TRIPLES of normalized objects at mixed depths, including",
        "then": "multiply(multiply(a, b), c) == multiply(a, multiply(b, c));"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "multiply_associativity"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_commutator.contract_multiply_commutativity_ruling",
        "class": "correctness",
        "given": "normalized objects; the separating witnesses B1 = [0,1] and",
        "then": "multiply is non-commutative in general; the (r, theta, z, w)"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "multiply_commutativity_ruling"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_identity_two_sided.contract_multiply_identity",
        "class": "correctness",
        "given": "the normalized factorization identity e =",
        "then": "multiply(e, a) == a and multiply(a, e) == a (two-sided, checked"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "multiply_identity"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_multiply_canonical.contract_multiply_well_defined",
        "class": "correctness",
        "given": "ordinary normalized nonempty factorization UCNSObjects at mixed",
        "then": "multiply is total, its output is normalized with n_dec a multiple of"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "multiply_well_defined"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_structure_axioms.contract_structure_naming",
        "class": "correctness",
        "given": "obligations O1-O5 discharged (well-definedness, identity,",
        "then": "(nonempty normalized objects, multiply, e) is a non-commutative,"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "structure_naming"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "normalize, _compute_n_min, _star, _disk_flip",
        "module_kind": "engine",
        "module_name": "canonical",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSObject, multiply, is_unit, is_multiplicative_unit, lcm, UNIT",
        "requires": "none",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Core UCNS algebraic objects and operations - UCNSObject, the ordered-concatenation product, and unit predicates.",
        "tests": "ucns_recursive/tests/test_depth2_full_domain.py, ucns_recursive/tests/test_canonical_constructor_validation.py, tests/test_canonical_constructor_validation.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/canonical.py",
      "id": "ucns_canonical"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "service",
        "module_name": "canonical_factorization",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "enumerate_factorizations, canonical_factorization, canonical_key, SEQ_PRIME",
        "requires": "ucns_carrier_support_pruning",
        "rollback": "remove module and its re-exports",
        "rollout": "additive module; no existing surface modified",
        "since": "2026-06-10",
        "storage_boundary": "none",
        "summary": "Deterministic canonical choice among all catalogue-bounded left-factor factorizations of P, selected by lexicographic canonical-bytes order over a v0.6-complete enumeration.",
        "tests": "ucns.tests.test_canonical_factorization",
        "unresolved": "canonical selection under payload-catalogue (factor_search_v08) semantics",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/canonical_factorization.py",
      "id": "ucns_canonical_factor_selection"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_obj_key",
        "module_kind": "engine",
        "module_name": "catalogue",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "build_catalogue_d1, build_catalogue_d2_oracle",
        "requires": "ucns_canonical, ucns_domains",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Catalogue builders enumerating canonical depth-1 oracle atoms and depth-2 oracle-class UCNSObjects for factor decomposition.",
        "tests": "tests.test_catalogue, tests.test_oracle_catalogue_equivalence",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/catalogue.py",
      "id": "ucns_catalogue"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_required_catalogue_for_domain, _structural_tokens",
        "module_kind": "engine",
        "module_name": "catalogue_coverage",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CatalogueCoverage, CATALOGUE_COVERAGE_RULE_VERSION, COVERAGE_CANONICAL_EXACT, COVERAGE_CANONICAL_SUPERSET, COVERAGE_UNCERTIFIED, check_catalogue_coverage, validate_catalogue_coverage, coverage_matches_search_report",
        "requires": "ucns_domains, ucns_factor_search_v08, ucns_serialization",
        "rollback": "remove module and public re-exports",
        "rollout": "additive evidence surface; no FactorizationResult integration",
        "since": "2026-07-11",
        "storage_boundary": "none",
        "summary": "Recomputable catalogue-coverage records bound to an exact supplied catalogue fingerprint, domain label, and required catalogue rule version; makes no primality-certification claim.",
        "tests": "tests/test_catalogue_coverage.py",
        "unresolved": "negative-result certification deliberately remains separate",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/catalogue_coverage.py",
      "id": "ucns_catalogue_coverage"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_recursive_obj_key",
        "module_kind": "engine",
        "module_name": "catalogue_d3",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "is_in_oracle_class_d3, D3CatalogueResult, build_catalogue_d3_oracle",
        "requires": "ucns_canonical, ucns_domains, ucns_catalogue",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "DRAFT depth-3 oracle-class predicate and bounded catalogue enumerator (build_catalogue_d3_oracle) carrying a coverage attestation against Lemma 8.",
        "tests": "ucns.tests.test_catalogue_d3",
        "unresolved": "DRAFT - depth-3 constructive-vs-multiplicative D'' coverage equivalence, payload_basis/chirality interaction, and size-budget exhaustion gating are all unproven (hmmm A/B/C in module docstring)",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/catalogue_d3.py",
      "id": "ucns_catalogue_d3"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "service",
        "module_name": "catalogue_pruning",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PAYLOAD_PRUNING_RULE_NAME, PAYLOAD_PRUNING_RULE_VERSION, PAYLOAD_PRUNING_PRESERVES_COVERAGE, prime_support, carrier_lcm, prune_catalogue, payload_support, prune_payload_catalogue",
        "requires": "none",
        "rollback": "pass prune=False to factor_search_v08, or remove the module and the prune kwarg",
        "rollout": "prune_catalogue opt-in for left-factor catalogues; prune_payload_catalogue default-on inside factor_search_v08 (prune=False escape hatch)",
        "since": "2026-06-09",
        "storage_boundary": "none",
        "summary": "Sound named and versioned catalogue pre-filter removing factor candidates whose carrier prime support escapes the product carrier's prime support, justified by the Carrier-LCM Law.",
        "tests": "ucns.tests.test_catalogue_pruning, tests/test_factor_search_provenance.py, tests/test_certified_negative_results.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/catalogue_pruning.py",
      "id": "ucns_carrier_support_pruning"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "core",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCN, TAU",
        "requires": "none",
        "rollback": "remove after all legacy circular-embedding consumers migrate",
        "rollout": "compatibility_only",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "legacy local 2pi circular coordinate for periodic embeddings; explicitly not the fixed-origin public gonol or complete UCNS number-system primitive",
        "tests": "tests.test_core",
        "unresolved": "no public-gonol bridge is defined; this surface must remain scoped as a local 2pi coordinate",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/core.py",
      "id": "ucns_core"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "contracts.test_quotient_solvability.contract_division_theory",
        "class": "correctness",
        "given": "normalized nonempty A, P (left) or B, P (right) of finite depth",
        "then": "left_quotients/right_quotients return exactly the set of X over"
      },
      "file": "ucns-source/archive/ucns/division_theory.py",
      "id": "division_theory"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "left_quotients, right_quotients, _left_payload_solutions, _right_payload_solutions, _dedup",
        "module_kind": "engine",
        "module_name": "division_theory",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "none",
        "requires": "ucns_canonical",
        "rollback": "keep ucns.left_quotient greedy primitives as the standing surface",
        "rollout": "this IS \"division and the like\"; importable, not re-exported from ucns/__init__",
        "since": "2026-07-10",
        "storage_boundary": "none",
        "summary": "left/right quotient solvability and multiplicity for multiply - complete finite solution-set enumeration",
        "tests": "contracts.test_quotient_solvability",
        "unresolved": "none for enumeration; AlignedComplete cancellativity proof remains a formal/ obligation",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/division_theory.py",
      "id": "division_theory"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "domain_status",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "DomainProofStatus, DomainStatusMetadata, VERIFIED_DOMAIN_LABELS, domain_status_metadata, status_for_object, is_verified_domain_label, seq_prime_requires_scope",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Typed domain-level prerequisite metadata; bare labels never certify SEQ-PRIME, and result-level certainty is delegated to ucns.factorization_result.",
        "tests": "ucns_recursive/tests/test_domain_status.py, tests/test_certified_negative_results.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/domain_status.py",
      "id": "ucns_domain_status"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_generate_canonical_catalogue, _oracle_atom_key, _CANONICAL_ORACLE_KEYS",
        "module_kind": "engine",
        "module_name": "domains",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "DEPTH_MAX, A_PLUS_MAX, N_MIN_MAX, S2, ORACLE_ATOM_PAYLOADS, ORACLE_CATALOGUE_RULE_VERSION, generate_payload_catalogue, in_domain, depth_of, is_oracle_atom, is_in_oracle_class, verified_domain_status",
        "requires": "ucns_canonical",
        "rollback": "restore geometric-bounds oracle classification (reintroduces catalogue mismatch)",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Defines the frozen depth-2 geometry, canonical oracle catalogue, and exact catalogue-membership predicates used to scope oracle claims.",
        "tests": "tests/test_oracle_catalogue_equivalence.py, ucns_recursive/tests/test_depth2_full_domain.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/domains.py",
      "id": "ucns_domains"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_to_signal",
        "module_kind": "adapter",
        "module_name": "embedding",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNEmbedding",
        "requires": "ucns_epicycle",
        "rollback": "remove after legacy consumers migrate to explicitly named embedding surfaces",
        "rollout": "compatibility_only",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "legacy FFT phase-vector embedding over local 2pi coordinates; explicitly not the public-gonol encoder or a semantic/theorem surface",
        "tests": "tests.test_embedding",
        "unresolved": "no public-gonol or semantic bridge is defined",
        "user_data_boundary": "read"
      },
      "file": "ucns-source/archive/ucns/embedding.py",
      "id": "ucns_embedding"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_next_pow2, _fft_inplace",
        "module_kind": "adapter",
        "module_name": "epicycle",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "fft, ifft, EpicycleDecomposition",
        "requires": "none",
        "rollback": "remove after legacy FFT embedding consumers migrate",
        "rollout": "compatibility_only",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "legacy radix-2 FFT and epicycle signal decomposition over local 2pi phases; not the public-gonol frame",
        "tests": "tests.test_epicycle",
        "unresolved": "no public-gonol bridge is defined",
        "user_data_boundary": "read"
      },
      "file": "ucns-source/archive/ucns/epicycle.py",
      "id": "ucns_epicycle"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "evidence",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSEvidence, no_proof_status, evidence_from_construction, evidence_from_bridge_import, evidence_from_factorization_result",
        "requires": "ucns_canonical, ucns_factorization_result, ucns_domain_status, ucns_bridge",
        "rollback": "remove module and its re-exports; consumers fall back to reading FactorizationResult directly",
        "rollout": "default_enabled additive public API",
        "since": "2026-07-12",
        "storage_boundary": "none",
        "summary": "Non-boolean downstream evidence envelope distinguishing construction success, search exhaustion, validated coverage, certified domain-relative negatives, theorem-layer status vocabulary, and absence of proof status.",
        "tests": "tests/test_stack_contract_suite.py, tests/test_bridge_certification_boundary.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/evidence.py",
      "id": "ucns_evidence"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canonical_bytes, _digest, _exact_fields, _strict_bool, _strict_int, _strict_str, _strict_string_tuple, _strict_hex_digest, _status_values",
        "module_kind": "schema",
        "module_name": "evidence_envelope",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "BRIDGE_RECORD_SCHEMA_ID, BRIDGE_RECORD_SCHEMA_VERSION, FACTORIZATION_EVIDENCE_SCHEMA_ID, FACTORIZATION_EVIDENCE_SCHEMA_VERSION, UCNSBridgeRecord, UCNSFactorizationEvidence, bridge_record, factorization_evidence",
        "requires": "ucns_object_record, ucns_factorization_result, ucns_serialization, ucns_domain_status",
        "rollback": "remove envelope exports while preserving object_record and factorization_result",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "deterministic serialization only; no persistence",
        "summary": "versioned deterministic bridge records and factorization evidence envelopes binding UCNS stable identity, canonical serialization, typed domain status, exhaustive-search provenance, catalogue coverage, pruning policy, and negative-certification scope.",
        "tests": "tests.test_evidence_envelope",
        "unresolved": "cryptographic producer authentication is not provided; evidence digests are tamper-evident content identities only",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/evidence_envelope.py",
      "id": "ucns_evidence_envelope"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_prepare_search_catalogues, _search_exhaustive",
        "module_kind": "engine",
        "module_name": "factor_search_v08",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "factor_search_v08, factor_search_report, FactorSearchReport, payload_catalogue_fingerprint",
        "requires": "ucns_canonical, ucns_domains, ucns_host_recovery, ucns_payload_system, ucns_witness_matrix, ucns_serialization, ucns_carrier_support_pruning",
        "rollback": "remove report API while retaining factor_search_v08 and _search_exhaustive",
        "rollout": "factor_search_v08 unchanged; factor_search_report additive",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Exhaustive catalogue-bounded factorization with a compatibility sentinel API and a provenance-bearing search report that makes no certification claim.",
        "tests": "tests/test_exhaustive_factor_search.py, tests/test_factor_search_provenance.py, tests/test_certified_negative_results.py, ucns_recursive/tests/test_depth2_oracle.py",
        "unresolved": "negative-result certification lives only in ucns.factorization_result",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/factor_search_v08.py",
      "id": "ucns_factor_search_v08"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_pruning_is_recognized, _negative_certification_reasons, _claim_scope",
        "module_kind": "engine",
        "module_name": "factorization_result",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "FactorizationResultKind, FactorizationResult, NEGATIVE_CERTIFICATION_POLICY_VERSION, factorization_result",
        "requires": "ucns_canonical, ucns_domain_status, ucns_domains, ucns_factor_search_v08, ucns_catalogue_coverage, ucns_carrier_support_pruning, ucns_serialization",
        "rollback": "retain provenance and coverage evidence but set negative_result_certified and seq_prime_is_absolute false",
        "rollout": "default_enabled for A0-facing envelopes; raw factor_search_v08 remains catalogue-relative",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "A0-facing factorization envelope that certifies negative results only from frozen-domain membership, validated catalogue coverage, exact search-report binding, exhaustive untruncated search, recognized sound pruning, a complete declared domain, and a non-unit target.",
        "tests": "tests/test_certified_negative_results.py, tests/test_one_shot_catalogue.py, ucns_recursive/tests/test_factorization_result.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/factorization_result.py",
      "id": "ucns_factorization_result"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_r, _rho, _theta, _zw, ThetaDegenerate",
        "module_kind": "engine",
        "module_name": "geometry_bridge",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "GeometricPoint, ucns_a_to_g, compose, homomorphism_check, HomomorphismResult, check_injectivity",
        "requires": "ucns.canonical, ucns.relational_geometry",
        "rollback": "remove export from ucns/__init__.py",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "commutative audit projection via recursive radius, breadth, spinor angle, and chirality coordinates",
        "tests": "ucns_recursive.tests.test_geometry_bridge, contracts.test_local_groups_and_geometry",
        "unresolved": "injectivity-proof-analytical, degenerate-theta-canonical-form, quaternionic-axis-lift",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/geometry_bridge.py",
      "id": "ucns_geometry_bridge"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "host_recovery",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "recover_host_angles, recover_face_structures",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Recovers the candidate A/B host angle sequences and enumerates consistent face-bit assignments from a normalised product object P.",
        "tests": "ucns_recursive/tests/test_depth2_full_domain.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/host_recovery.py",
      "id": "ucns_host_recovery"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_left_quotient_payload",
        "module_kind": "engine",
        "module_name": "left_quotient",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "left_quotient, right_quotient",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Constructive left/right quotient primitives implementing the v0.6 left-quotient completeness theorem; recovers B (or A) from a product, else None.",
        "tests": "ucns.tests.test_left_quotient",
        "unresolved": "v0.6 completeness scope-corrected 2026-07-10 (counterexample; complete on flat divisors only; full enumeration in ucns.division_theory); right_quotient dual additionally uses the left payload helper and misses more",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/left_quotient.py",
      "id": "ucns_left_quotient"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "mobius",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "MobiusTransform, poincare_distance, disk_to_circle, circle_to_disk",
        "requires": "none",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Mobius (bilinear) transformations of the Poincare unit disk plus hyperbolic-distance and disk/circle projection helpers.",
        "tests": "tests.test_mobius",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/mobius.py",
      "id": "ucns_mobius"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "object_record",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSObjectRecord, object_record",
        "requires": "ucns_canonical, ucns_domain_status, ucns_domains, ucns_serialization",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Builds a self-describing inspection record (canonical identity, domain-status metadata, structural facts) for any UCNS object without invoking factorization.",
        "tests": "ucns.tests.test_object_record",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/object_record.py",
      "id": "ucns_object_record"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_globally_consistent",
        "module_kind": "engine",
        "module_name": "payload_system",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "normalize_payload_catalogue, iter_payload_system_solutions, solve_payload_system",
        "requires": "ucns_canonical",
        "rollback": "restore the greedy first-quotient solver",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Normalizes payload catalogues and exhaustively enumerates every assignment satisfying the coupled product equations, with a first-solution compatibility wrapper.",
        "tests": "tests/test_exhaustive_factor_search.py, tests/test_factor_search_provenance.py, ucns_recursive/tests/test_depth2_full_domain.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/payload_system.py",
      "id": "ucns_payload_system"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "UPPERCASE, LOWERCASE, DIGITS_ODD, DIGITS_EVEN, PAIRED_OPEN, PAIRED_CLOSE, UNPAIRED_ASCII, UNPAIRED_OPS, UNPAIRED_ALL",
        "module_kind": "engine",
        "module_name": "public_gonol",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "GonalSpec, build_gonal, validate_gonal, print_gonal, EXAMPLE_157, PUBLIC_GONOL_157, make_example_157, get_default, public_gonol_sha256, PUBLIC_GONOL_SHA256",
        "requires": "none",
        "rollback": "remove public exports after downstream consumers return to the pinned a0-betatest source",
        "rollout": "default_enabled",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "owns the exact public 157-gonal arrangement and fixed SPACE/ZERO twist origin promoted from a0-betatest",
        "tests": "tests.test_public_gonol",
        "unresolved": "hmmm \u2014 no continuous-angle projection is ratified by this promotion",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/public_gonol.py",
      "id": "ucns_public_gonol"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "public_gonol_faces",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "face, chirality, n_plus, n_minus, ARITY, ORIGIN, UPPER_ARC_RANGE, LOWER_ARC_RANGE",
        "requires": "ucns_public_gonol",
        "rollback": "remove exports after reverting consumers to the pinned a0-betatest source",
        "rollout": "default_enabled",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "preserves the exact public face, chirality, adjacency, arity, and fixed origin formulas from a0-betatest",
        "tests": "tests.test_public_gonol",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/public_gonol_faces.py",
      "id": "ucns_public_gonol_faces"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_ARRANGEMENT, _VERTEX_OF_CHAR",
        "module_kind": "engine",
        "module_name": "public_gonol_lifted_path",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encode_text_path, decode_text_path, vertex_of_char, char_of_vertex, is_seam_event, path_vertices, CarrierCharError, ARITY, ORIGIN",
        "requires": "ucns_public_gonol, ucns_public_gonol_faces",
        "rollback": "remove exports after reverting consumers to the pinned a0-betatest source",
        "rollout": "default_enabled",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "losslessly encodes and decodes text as the exact lifted traversal over the fixed-origin public gonol",
        "tests": "tests.test_public_gonol",
        "unresolved": "none",
        "user_data_boundary": "read"
      },
      "file": "ucns-source/archive/ucns/public_gonol_lifted_path.py",
      "id": "ucns_public_gonol_lifted_path"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "public_gonol_mirror",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "mirror_of",
        "requires": "ucns_public_gonol",
        "rollback": "remove export after reverting consumers to the pinned a0-betatest source",
        "rollout": "default_enabled",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "preserves the exact origin-fixed public-gonol mirror involution from a0-betatest",
        "tests": "tests.test_public_gonol",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/public_gonol_mirror.py",
      "id": "ucns_public_gonol_mirror"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "public_gonol_private",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PrivateGonal",
        "requires": "ucns_public_gonol, ucns_public_gonol_faces",
        "rollback": "remove export after reverting consumers to the pinned a0-betatest source",
        "rollout": "default_enabled",
        "since": "2026-07-16",
        "storage_boundary": "none",
        "summary": "preserves the exact A0 private phase and permutation law that fixes the public SPACE/ZERO twist origin",
        "tests": "tests.test_public_gonol",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/public_gonol_private.py",
      "id": "ucns_public_gonol_private"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_byte_to_angle, _angle_to_byte, _safe_n_dec, _make_sentinel_cells, _encode_bytes, _encode_list, _encode_dict, _count_leading_sentinels",
        "module_kind": "engine",
        "module_name": "recursive_codec",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "recursive_encode, recursive_decode, EncodingError",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Recursive encoder/decoder between Python values (bytes/list/tuple/dict and coercible leaves) and UCNSObject, with type recovered from leading-sentinel count.",
        "tests": "ucns.tests.test_recursive_codec",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/recursive_codec.py",
      "id": "ucns_codec"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "find_right_factor_or_sentinel, find_left_factor_or_sentinel",
        "module_kind": "engine",
        "module_name": "recursive_quotient",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "find_left_factor, find_right_factor, left_quotient, right_quotient",
        "requires": "ucns_canonical, ucns_left_quotient",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Payload-level single-equation factor finders (find_left_factor / find_right_factor) that enumerate a candidate catalogue, plus re-exports of the left/right quotient primitives.",
        "tests": "ucns.tests.test_left_quotient",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/recursive_quotient.py",
      "id": "ucns_quotient"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_face_tower_bits",
        "module_kind": "engine",
        "module_name": "relational_geometry",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "recursive_radius, breadth, first_level_fork_count, is_normalized, zero_faced_tower, face_tower, idempotent_tower_depth, is_local_group_pair, is_local_group_member, local_group_elements",
        "requires": "ucns_canonical",
        "rollback": "remove module and dependent contracts",
        "rollout": "default_enabled",
        "since": "2026-07-14",
        "storage_boundary": "none",
        "summary": "recursive radius, breadth, fork observables, idempotent towers, and home-relative local-group predicates",
        "tests": "contracts.test_local_groups_and_geometry, tests.test_base_geometry_contracts",
        "unresolved": "full fork-profile counting convention; METAPAT fork admissibility remains downstream",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/relational_geometry.py",
      "id": "ucns_relational_geometry"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_fraction_to_data",
        "module_kind": "engine",
        "module_name": "serialization",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CANONICAL_SERIALIZATION_VERSION, DEFAULT_HASH_ALGORITHM, canonical_data, canonical_json, canonical_bytes, stable_hash, stable_hash_bytes",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Canonical deterministic JSON serialization and stable SHA-256 hashing for UCNS recursive objects, mirroring UCNSObject equality policy for content addressing and identity.",
        "tests": "ucns.tests.test_serialization",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/serialization.py",
      "id": "ucns_serialization"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_check_same_length",
        "module_kind": "adapter",
        "module_name": "similarity",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "phase_cosine, arc_distance, hyperbolic_cosine, top_k_overlap",
        "requires": "none",
        "rollback": "remove after legacy embedding consumers migrate",
        "rollout": "compatibility_only",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "similarity and distance helpers for legacy local 2pi phase-vector embeddings; not public-gonol geometry",
        "tests": "tests.test_similarity",
        "unresolved": "no public-gonol or semantic metric bridge is defined",
        "user_data_boundary": "read"
      },
      "file": "ucns-source/archive/ucns/similarity.py",
      "id": "ucns_similarity"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "store",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSStore, Match, OutOfDomainError",
        "requires": "ucns_canonical, ucns_domains, ucns_left_quotient, ucns_codec",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "UCNSStore - an in-memory keyed corpus of UCNSObjects with proof-backed algebraic retrieval (left_factors, is_left_factor, factor_decompose) and optional verified-domain enforcement.",
        "tests": "ucns.tests.test_store",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/store.py",
      "id": "ucns_store"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "witness_matrix",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "Witness, WitnessMatrix, build_witness_matrix",
        "requires": "ucns_canonical",
        "rollback": "remove module and its re-exports",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Witness and WitnessMatrix types plus build_witness_matrix; verifies per-cell factor products and row/column global consistency for a host factorisation candidate.",
        "tests": "ucns.tests.test_failure_boundary_e109",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns/witness_matrix.py",
      "id": "ucns_witness_matrix"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "feature_flag": "A0_UCNS_CACHE for downstream a0-betatest integration",
        "internal_surface": "dependencies, keys, entries, primitive_streams, braider, store, policy, instrumentation",
        "module_kind": "experiment",
        "module_name": "ucns_cache",
        "network_boundary": "none",
        "owner": "Erin Spencer / Codex",
        "public_surface": "UCNSCacheKey, UCNSCacheEntry, PrimitiveStreams, BraiderOutput, CacheLookupResult, UCNSCacheStore, make_ucns_cache_key, derive_primitive_streams, braid_streams, factor_reuse_candidates",
        "rollback": "remove ucns_cache package, docs/ucns-native-caching.md, scripts/bench_ucns_cache.py, and tests/test_ucns_cache_*.py",
        "rollout": "opt-in prototype / downstream A0_UCNS_CACHE integration",
        "since": "2026-06-28",
        "storage_boundary": "none",
        "summary": "Software-only UCNS-native cache prototype for canonical keying, primitive streams, braider identity, and conservative structural reuse.",
        "tests": "tests/test_ucns_cache_keys.py, tests/test_ucns_cache_streams.py, tests/test_ucns_cache_store.py, tests/test_ucns_cache_factor_reuse.py",
        "unresolved": "a0-betatest checkout unavailable in this workspace, downstream inference hook not installed, stable shared-braid fixture pending",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/archive/ucns_cache/entries.py",
      "id": "ucns_native_cache"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a consumer imports ucns",
        "since": "2026-07-21",
        "then": "ratified foundations and explicit research infrastructure are exported without implying canonical M, B, factorization, theorem, or downstream status"
      },
      "file": "ucns-source/src/ucns/__init__.py",
      "id": "public_surface_exposes_only_ratified_foundations"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "ucns public surface",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "carrier, structure, policy, envelope, comparison, traversal, laboratory, layer-pairing, experiment, and candidate names listed in __all__",
        "requires": "directed_carrier_floor, structural_cell_support_floor, structural_choice_policy_layer, retained_structure_envelope, explicit_comparison_policy_layer, cycle_safe_traversal_policy, evaluator_candidate_laboratory, retained_layer_pairing_laboratory, reproducible_witness_experiment_pipeline, first_competing_evaluator_candidate_families",
        "rollback": "remove research exports while preserving carrier/support floors",
        "rollout": "importable foundations and candidate-research infrastructure only",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "exports ratified foundations plus option-preserving, reproducible candidate-research infrastructure",
        "tests": "tests/test_public_surface.py and all source-specific test modules",
        "unresolved": "canonical structural equivalence, canonical M, canonical B, complete UCNS object",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/__init__.py",
      "id": "foundations_public_surface"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "an initial equivalence, M, or B candidate is constructed",
        "since": "2026-07-21",
        "then": "it remains an EvaluatorCandidate and exposes no canonical or winner status"
      },
      "file": "ucns-source/src/ucns/candidates.py",
      "id": "candidate_constructors_do_not_promote_canon"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a cell-only M or B candidate receives retained evidence without a cell carrier",
        "since": "2026-07-21",
        "then": "evaluation raises CandidateScopeError rather than treating unmeasured layers as zero distinction"
      },
      "file": "ucns-source/src/ucns/candidates.py",
      "id": "cell_only_candidates_fail_outside_scope"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "multiple equivalence, product-character, or faithful-breadth candidates are constructed",
        "since": "2026-07-21",
        "then": "each has explicit version, code reference, scope, and policy dependencies and none is selected as canonical"
      },
      "file": "ucns-source/src/ucns/candidates.py",
      "id": "first_candidate_families_coexist_without_selection"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "positive-support carriers are paired by the established Cartesian law",
        "since": "2026-07-21",
        "then": "geometric-mean, maximum-support, and minimum-support candidates satisfy their declared multiplicativity fixtures"
      },
      "file": "ucns-source/src/ucns/candidates.py",
      "id": "initial_product_candidates_multiply_under_actual_pairing"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_digest, _carrier, _cell_supports",
        "module_kind": "instrument",
        "module_name": "candidates",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CandidateScopeError, exact_evidence_equivalence_candidate, policy_projection_equivalence_candidate, layer_scoped_equivalence_candidate, geometric_mean_product_candidate, maximum_support_product_candidate, minimum_support_product_candidate, cell_log_support_breadth_candidate, cell_detail_breadth_candidate, retained_presence_breadth_candidate",
        "requires": "evaluator_candidate_laboratory, reproducible_witness_experiment_pipeline",
        "rollback": "remove candidate constructors; laboratory and evidence remain",
        "rollout": "explicit candidate families only; no evaluator is canonical",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "supplies explicit noncanonical equivalence, product-character, and faithful-breadth candidate families for laboratory pressure",
        "tests": "tests/test_candidates.py",
        "unresolved": "canonical equivalence, canonical M, canonical B",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/candidates.py",
      "id": "first_competing_evaluator_candidate_families"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null carrier retains structure while an external payload value is numerically zero",
        "since": "2026-07-21",
        "then": "carrier identity remains non-null because payload algebra is outside the carrier floor"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "algebraic_zero_is_not_structural_null"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "any finite angular coordinate on a non-null carrier",
        "since": "2026-07-21",
        "then": "the coordinate is normalized modulo four pi and returns only after two visible laps"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "lifted_period_is_720_degrees"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a non-null lifted carrier point is constructed",
        "since": "2026-07-21",
        "then": "breadth is finite and strictly positive and radius lies strictly between zero and one"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "non_null_carrier_has_positive_breadth"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point translated by two pi",
        "since": "2026-07-21",
        "then": "its visible projection is unchanged while its lifted representative is distinct"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "one_visible_lap_is_deck_translation_only"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the carrier is constructed with zero faithful breadth",
        "since": "2026-07-21",
        "then": "the result is the unique Structural Null and exposes no angular coordinate"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "structural_null_is_unique_and_coordinate_free"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a 360-degree deck translation",
        "since": "2026-07-21",
        "then": "no negation, reflection, parity, chirality, frame inversion, or payload operation is inferred by the carrier API"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "topology_does_not_invent_orientation_algebra"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point translated twice by two pi",
        "since": "2026-07-21",
        "then": "the original lifted representative is restored"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "two_visible_laps_complete_return"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point",
        "since": "2026-07-21",
        "then": "projection is normalized modulo two pi and has exactly two lifted representatives"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "visible_projection_is_360_degrees"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_StructuralNull, _normalize_angle",
        "module_kind": "schema",
        "module_name": "carrier",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "STRUCTURAL_NULL, LiftedCarrierPoint, VisibleCarrierPoint, radius_from_breadth, carrier_from_breadth, project, deck_translate, lifted_preimages, same_lifted_position, same_visible_position",
        "requires": "canonical_chapter_one",
        "rollback": "remove public exports and this module",
        "rollout": "importable prototype only; no arithmetic or theorem promotion",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "represents the directed twofold branched angular carrier without defining full UCNS object semantics",
        "tests": "tests/test_carrier.py",
        "unresolved": "canonical evaluators for mu, W, M, and B; complete UCNS object schema",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/carrier.py",
      "id": "directed_carrier_floor"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a comparison policy name is already registered",
        "since": "2026-07-21",
        "then": "replacement fails unless replace is explicitly true"
      },
      "file": "ucns-source/src/ucns/comparison.py",
      "id": "comparison_policy_replacement_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "exact, relative, absolute, ULP, interval, or custom policies are registered",
        "since": "2026-07-21",
        "then": "every policy remains independently addressable and no default winner is appointed"
      },
      "file": "ucns-source/src/ucns/comparison.py",
      "id": "comparison_registry_preserves_multiple_policies"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a custom comparison implementation is constructed or pinned in an experiment",
        "since": "2026-07-21",
        "then": "a nonempty code reference distinguishes the implementation independently of name, version, and parameters"
      },
      "file": "ucns-source/src/ucns/comparison.py",
      "id": "custom_comparison_identity_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "candidate outputs or law evidence are compared",
        "since": "2026-07-21",
        "then": "an explicit named ComparisonPolicy performs the comparison and no hidden tolerance is selected"
      },
      "file": "ucns-source/src/ucns/comparison.py",
      "id": "evaluator_equality_requires_explicit_comparison_policy"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_numeric_pair, _ordered_float",
        "module_kind": "instrument",
        "module_name": "comparison",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ComparisonMode, ComparisonPolicy, ComparisonRegistry, exact_comparison_policy, absolute_comparison_policy, relative_comparison_policy, combined_comparison_policy, ulp_comparison_policy, interval_overlap_policy, custom_comparison_policy",
        "requires": "structural_choice_policy_layer",
        "rollback": "remove comparison exports and restore no implicit tolerance",
        "rollout": "explicit candidate-research comparison infrastructure only",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "defines versioned comparison policies with explicit implementation identity so evaluator laws never rely on hidden tolerance or callable inference",
        "tests": "tests/test_comparison.py, tests/test_laboratory.py, tests/test_experiments.py",
        "unresolved": "canonical numerical comparison policy",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/comparison.py",
      "id": "explicit_comparison_policy_layer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a cell carrier and optional retained layers are assembled",
        "since": "2026-07-21",
        "then": "Structural Null is returned exactly when no cell carrier and no retained layer occurrence remains"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_envelope_has_unique_complete_null"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "retained evidence may be falsey or equal to None",
        "since": "2026-07-21",
        "then": "presence is determined only by the retained flag rather than truthiness"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_layer_presence_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a selected retained layer is viewed through a structural policy",
        "since": "2026-07-21",
        "then": "the policy projection retains the untouched layer evidence and does not mutate the envelope"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_layer_projection_is_non_destructive"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "repeated or differently named structural layers are added",
        "since": "2026-07-21",
        "then": "every occurrence remains ordered and addressable and no earlier evidence is overwritten"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_layers_append_without_overwrite"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "receipts, metadata, relations, recursion, provenance, or state are retained",
        "since": "2026-07-21",
        "then": "cell_support_weight reports only the current cell carrier W and every other layer keeps explicit contribution status"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_layers_do_not_silently_enter_cell_support"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "envelope",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ContributionStatus, RetainedLayer, RetainedStructure, RetainedEnvelope, make_retained_structure, cell_support_weight, project_layer",
        "requires": "structural_cell_support_floor, structural_choice_policy_layer",
        "rollback": "remove public exports and this module",
        "rollout": "importable evidence envelope; not a complete UCNS object",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "retains optional structural layers without forcing them into cells or silently extending aggregate support",
        "tests": "tests/test_envelope.py",
        "unresolved": "layer measurement laws, canonical layer equivalence, complete UCNS object",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/envelope.py",
      "id": "retained_structure_envelope"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a witness case or candidate decision packet is content-addressed",
        "since": "2026-07-21",
        "then": "authorship role, author, provenance, and separate candidate, witness, and decision records remain identity-bearing evidence"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "candidate_witness_and_decision_authorship_are_recorded"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "witness cases are assembled into a corpus and decision packet",
        "since": "2026-07-21",
        "then": "development and holdout partitions remain explicit and a packet cannot be reviewable without passing holdout evidence for the same candidate"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "development_and_holdout_evidence_are_separate"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a candidate experiment is declared",
        "since": "2026-07-21",
        "then": "candidate code identity, law implementation and fixtures, corpus, policies, comparison, traversal, and environment are content-addressed in one manifest"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "experiment_manifests_pin_all_research_inputs"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "two complete ExperimentResult values claim the same manifest",
        "since": "2026-07-21",
        "then": "an explicit result adapter compares every result field or records why reproduction could not be established"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "reproduction_checks_report_match_or_reason"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "an arbitrary candidate-research subject is content-addressed",
        "since": "2026-07-21",
        "then": "a named versioned ContentAdapter supplies bytes and the stored record retains an isolated snapshot of those bytes and subject state"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "subject_identity_requires_explicit_adapter"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_digest_bytes, _canonical_json, _validate_report_owner",
        "module_kind": "instrument",
        "module_name": "experiments",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ContentAdapter, AdapterRegistry, json_content_adapter, text_content_adapter, bytes_content_adapter, SubjectRecord, WitnessOrigin, CorpusPartition, AuthorshipRecord, WitnessCase, WitnessCorpus, CandidateIdentity, PolicyDigest, LawSuiteDigest, ExperimentManifest, ExperimentResult, MetamorphicCase, MutationCase, Counterexample, NamedTransform, generate_metamorphic_cases, generate_mutation_cases, greedy_minimize_counterexample, HoldoutReport, CandidateDecisionPacket, ReproductionCheck, check_reproduction, build_candidate_decision_packet, comparison_policy_digest, traversal_policy_digest",
        "requires": "evaluator_candidate_laboratory, explicit_comparison_policy_layer, cycle_safe_traversal_policy",
        "rollback": "remove experiment exports; candidate laboratory remains process-local",
        "rollout": "reproducible candidate-research evidence infrastructure only",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "snapshots and content-addresses subjects, corpora, implementations, laws, manifests, holdouts, mutations, reproduction checks, and decision packets",
        "tests": "tests/test_experiments.py",
        "unresolved": "external sealed holdout storage and canonical decision authority",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/experiments.py",
      "id": "reproducible_witness_experiment_pipeline"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "competing candidates evaluate the same subjects",
        "since": "2026-07-21",
        "then": "outputs and disagreements are recorded under a named comparison policy without selecting a default, majority, best, or canonical candidate"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "candidate_comparison_exposes_disagreement_without_ranking"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "an evaluator candidate is constructed",
        "since": "2026-07-21",
        "then": "version, code reference, scope, and policy dependencies are recorded rather than inferred from a callable"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "evaluator_candidate_identity_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "multiple candidates of one evaluator kind are registered",
        "since": "2026-07-21",
        "then": "all remain independently addressable and callers must name a candidate or request the full set"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "evaluator_registry_has_no_implicit_winner"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a candidate name is already registered for an evaluator kind",
        "since": "2026-07-21",
        "then": "replacement fails unless replace is explicitly true"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "evaluator_replacement_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a law is admitted to a reproducible experiment manifest",
        "since": "2026-07-21",
        "then": "law name, version, code reference, and explicit fixture digest identify both implementation and retained evidence"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "law_identity_covers_implementation_and_fixtures"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "laws are run against an evaluator candidate",
        "since": "2026-07-21",
        "then": "pass, failure, and exception evidence are retained in one complete report"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "law_suites_capture_failures_and_errors"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "candidate law evidence is evaluated",
        "since": "2026-07-21",
        "then": "the LawSuite carries an explicit ComparisonPolicy and every equality decision uses it"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "law_suites_require_named_comparison_policy"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_evaluate_candidates",
        "module_kind": "instrument",
        "module_name": "laboratory",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EvaluatorKind, EvaluatorCandidate, EvaluatorRegistry, Witness, LawResult, Law, LawSuite, EvaluationReport, CandidateOutput, CandidateComparison, compare_candidates, null_zero_law, finite_nonnegative_law, pair_multiplicative_law, invariance_law, sensitivity_law, same_reference_different_candidate_law, same_candidate_different_reference_law",
        "requires": "structural_cell_support_floor, retained_structure_envelope, structural_choice_policy_layer, explicit_comparison_policy_layer",
        "rollback": "remove public exports and this module",
        "rollout": "candidate research infrastructure; no canonical evaluator",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "registers versioned evaluator candidates and versioned fixture-pinned laws under explicit comparison policies without selecting a winner",
        "tests": "tests/test_laboratory.py, tests/test_candidates.py, tests/test_experiments.py",
        "unresolved": "canonical equivalence, canonical M, canonical B, candidate promotion authority",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/laboratory.py",
      "id": "evaluator_candidate_laboratory"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a retained-layer pairing policy projects two layer occurrences",
        "since": "2026-07-21",
        "then": "both untouched sources, the projected view, and every declared information loss remain in the result evidence"
      },
      "file": "ucns-source/src/ucns/layer_pairing.py",
      "id": "layer_pairing_preserves_sources_and_declares_loss"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "two retained envelopes contain layer occurrences",
        "since": "2026-07-21",
        "then": "every consumed occurrence is selected by an explicit LayerPairRule and policy name"
      },
      "file": "ucns-source/src/ucns/layer_pairing.py",
      "id": "retained_layer_pairing_requires_explicit_plan"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "retained layers are paired into a result envelope",
        "since": "2026-07-21",
        "then": "their result layers remain unmeasured and do not silently enter W, M, or B"
      },
      "file": "ucns-source/src/ucns/layer_pairing.py",
      "id": "retained_pairing_does_not_extend_measurements"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "retained layer occurrences remain outside the plan",
        "since": "2026-07-21",
        "then": "pairing fails closed, preserves sided occurrences, or excludes them only according to the plan's explicit unmatched mode"
      },
      "file": "ucns-source/src/ucns/layer_pairing.py",
      "id": "unmatched_layers_follow_explicit_mode"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_no_losses, _as_structure, _select",
        "module_kind": "instrument",
        "module_name": "layer_pairing",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "LayerPairMode, UnmatchedLayerMode, LayerRef, LayerPairProjection, LayerPairPolicy, LayerPairRegistry, LayerPairRule, EnvelopePairPlan, LayerPairDecision, EnvelopePairResult, pair_retained, concatenate_layer_policy, cartesian_layer_policy, positional_zip_layer_policy, keep_sides_layer_policy, select_left_layer_policy, select_right_layer_policy, exclude_layer_policy, custom_layer_pair_policy",
        "requires": "retained_structure_envelope, structural_cell_support_floor",
        "rollback": "remove layer-pairing exports; retained envelopes remain unpaired",
        "rollout": "candidate envelope-pairing infrastructure; no canonical retained-layer product",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "composes retained layers through explicit occurrence-level pairing plans while preserving sources and losses",
        "tests": "tests/test_layer_pairing.py",
        "unresolved": "canonical retained-layer pairing laws and measurement contributions",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/layer_pairing.py",
      "id": "retained_layer_pairing_laboratory"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "multiset or set semantics are requested for arbitrary evidence",
        "since": "2026-07-21",
        "then": "the caller supplies the identity key and UCNS does not invent equality or hashing semantics"
      },
      "file": "ucns-source/src/ucns/policy.py",
      "id": "lossy_builtin_policies_require_explicit_keys"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "multiple named structural policies are registered",
        "since": "2026-07-21",
        "then": "every policy remains independently addressable and no default winner is appointed"
      },
      "file": "ucns-source/src/ucns/policy.py",
      "id": "policy_registry_preserves_multiple_choices"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a policy projects retained evidence into a view",
        "since": "2026-07-21",
        "then": "the untouched source remains attached and every ignored or discarded distinction is explicitly reported"
      },
      "file": "ucns-source/src/ucns/policy.py",
      "id": "projection_retains_source_and_declares_loss"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a caller requests a policy name absent from the selected registry",
        "since": "2026-07-21",
        "then": "policy application raises rather than choosing a fallback"
      },
      "file": "ucns-source/src/ucns/policy.py",
      "id": "unknown_policy_names_fail_closed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_no_losses, _require_hashable",
        "module_kind": "instrument",
        "module_name": "policy",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "InformationLoss, Projection, StructurePolicy, PolicyRegistry, OccurrenceGroup, SetEntry, apply_policy, ordered_sequence_policy, unordered_multiset_policy, set_policy",
        "requires": "structural_cell_support_floor",
        "rollback": "remove public exports and this module",
        "rollout": "importable candidate-policy infrastructure; no canonical structural policy",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "registers explicit structural interpretations and returns reversible projections with declared information loss",
        "tests": "tests/test_policy.py",
        "unresolved": "graph policy, tree policy, canonical structural equivalence",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/policy.py",
      "id": "structural_choice_policy_layer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a non-null carrier contains present cells",
        "since": "2026-07-21",
        "then": "support_weight returns the sum of their support weights and returns zero only for STRUCTURAL_NULL"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "aggregate_support_is_cell_sum"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a cell retains payload value zero with positive support",
        "since": "2026-07-21",
        "then": "the cell is present and may form a non-null carrier"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "algebraic_zero_payload_remains_structural"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "an iterable of potential cells contains no positive support after pruning",
        "since": "2026-07-21",
        "then": "make_carrier returns the unique STRUCTURAL_NULL rather than an empty Carrier"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "carrier_factory_returns_unique_null"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "Carrier is constructed directly",
        "since": "2026-07-21",
        "then": "it contains at least one present cell and contains no absent cells"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "carrier_is_non_null_by_construction"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "two non-null carriers are paired",
        "since": "2026-07-21",
        "then": "every present cell meets every present cell, paired support is multiplicative, aggregate support multiplies, and STRUCTURAL_NULL absorbs"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "carrier_pairing_is_cartesian_and_support_multiplicative"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a structural cell is constructed with support mu and optional retained fields",
        "since": "2026-07-21",
        "then": "mu is finite and nonnegative; mu is zero exactly for a field-empty absent cell; positive support requires retained distinction"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "cell_support_zero_test_is_fail_closed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "optional erasure is applied to a raw cell collection",
        "since": "2026-07-21",
        "then": "collapse returns STRUCTURAL_NULL exactly when no positive-support cells survive"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "collapse_requires_complete_structural_absence"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "potential cells contain zero-support absent cells and positive-support present cells",
        "since": "2026-07-21",
        "then": "prune removes only absent cells and preserves all present cells in order"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "pruning_removes_only_absent_cells"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "present cells retain order, multiplicity, or left/right operand distinctions while canonical structural interpretation remains unresolved",
        "since": "2026-07-21",
        "then": "make_carrier, prune, and pair preserve those distinctions without sorting, deduplicating, flattening, merging, or overwriting them"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "unresolved_structure_choices_are_preserved"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_has_distinction, _cells_from",
        "module_kind": "schema",
        "module_name": "structure",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "Cell, Carrier, Structure, make_carrier, support_weight, pair, prune, collapse",
        "requires": "directed_carrier_floor",
        "rollback": "remove exports and this module",
        "rollout": "importable foundations surface; no product character or faithful-breadth evaluator",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "defines canonical cells, non-null carriers, aggregate support, pairing, pruning, collapse, and choice-preserving structural evidence",
        "tests": "tests/test_structure.py",
        "unresolved": "domain-specific mu assignment, receipts, metadata, canonical structural equivalence, choice policy type, M, B",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/structure.py",
      "id": "structural_cell_support_floor"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "fixed-point cycle handling is selected",
        "since": "2026-07-21",
        "then": "construction fails unless both an explicit resolver and versioned resolver code reference are supplied"
      },
      "file": "ucns-source/src/ucns/traversal.py",
      "id": "fixed_point_traversal_requires_resolver"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "retained recursive evidence repeats an identity on the active path",
        "since": "2026-07-21",
        "then": "traversal rejects, references, depth-unfolds, or invokes a fixed-point resolver only as explicitly selected"
      },
      "file": "ucns-source/src/ucns/traversal.py",
      "id": "recursive_cycles_require_explicit_policy"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "reference traversal encounters an identity previously visited on another path",
        "since": "2026-07-21",
        "then": "traversal emits a ReferenceReceipt to the first path rather than double-counting or silently discarding shared structure"
      },
      "file": "ucns-source/src/ucns/traversal.py",
      "id": "shared_identity_references_are_retained"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "recursive traversal reaches a depth or node budget, including while iterating a large or unbounded child iterable",
        "since": "2026-07-21",
        "then": "traversal stops without materializing the remaining iterable and retains a TruncationReceipt"
      },
      "file": "ucns-source/src/ucns/traversal.py",
      "id": "traversal_budgets_emit_receipts"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "instrument",
        "module_name": "traversal",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CycleMode, TraversalBudget, TraversalPolicy, Visit, ReferenceReceipt, TruncationReceipt, FixedPointReceipt, TraversalResult, CycleDetectedError, traverse",
        "requires": "retained_structure_envelope",
        "rollback": "remove traversal exports; recursive candidates fail closed",
        "rollout": "recursive-evidence research infrastructure only",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "traverses recursive evidence under explicit cycle, shared-reference, implementation-identity, depth, node, and fixed-point policies",
        "tests": "tests/test_traversal.py, tests/test_experiments.py",
        "unresolved": "canonical recursive identity, sharing, and fixed-point semantics",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/src/ucns/traversal.py",
      "id": "cycle_safe_traversal_policy"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_candidate_family_coexistence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "first_candidate_families_coexist_without_selection",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_candidates.py",
      "id": "check_candidate_family_coexistence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_candidate_nonpromotion",
        "cleanup": "none",
        "mutates": "none",
        "proves": "candidate_constructors_do_not_promote_canon",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_candidates.py",
      "id": "check_candidate_nonpromotion"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_cell_candidate_scope_failure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "cell_only_candidates_fail_outside_scope",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_candidates.py",
      "id": "check_cell_candidate_scope_failure"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_initial_product_multiplicativity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "initial_product_candidates_multiply_under_actual_pairing",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_candidates.py",
      "id": "check_initial_product_multiplicativity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_lifted_period",
        "cleanup": "none",
        "mutates": "none",
        "proves": "lifted_period_is_720_degrees, two_visible_laps_complete_return",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_lifted_period"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_non_null_validation_and_radius",
        "cleanup": "none",
        "mutates": "none",
        "proves": "non_null_carrier_has_positive_breadth",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_non_null_validation_and_radius"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_one_lap_is_deck_translation",
        "cleanup": "none",
        "mutates": "none",
        "proves": "one_visible_lap_is_deck_translation_only, topology_does_not_invent_orientation_algebra",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_one_lap_is_deck_translation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_payload_zero_does_not_collapse_carrier",
        "cleanup": "none",
        "mutates": "none",
        "proves": "algebraic_zero_is_not_structural_null",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_payload_zero_does_not_collapse_carrier"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_structural_null_identity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "structural_null_is_unique_and_coordinate_free",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_structural_null_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_visible_projection_and_branch_law",
        "cleanup": "none",
        "mutates": "none",
        "proves": "visible_projection_is_360_degrees",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_carrier.py",
      "id": "check_visible_projection_and_branch_law"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_comparison_registry_choices",
        "cleanup": "none",
        "mutates": "none",
        "proves": "comparison_registry_preserves_multiple_policies",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_comparison.py",
      "id": "check_comparison_registry_choices"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_comparison_replacement",
        "cleanup": "none",
        "mutates": "none",
        "proves": "comparison_policy_replacement_is_explicit",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_comparison.py",
      "id": "check_comparison_replacement"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_custom_comparison_identity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "custom_comparison_identity_is_explicit",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_comparison.py",
      "id": "check_custom_comparison_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_explicit_comparison_policies",
        "cleanup": "none",
        "mutates": "none",
        "proves": "evaluator_equality_requires_explicit_comparison_policy",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_comparison.py",
      "id": "check_explicit_comparison_policies"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_falsey_retained_evidence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_layer_presence_is_explicit",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_envelope.py",
      "id": "check_falsey_retained_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_layer_append_behavior",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_layers_append_without_overwrite",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_envelope.py",
      "id": "check_layer_append_behavior"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_layer_measurement_firewall",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_layers_do_not_silently_enter_cell_support",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_envelope.py",
      "id": "check_layer_measurement_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_layer_projection",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_layer_projection_is_non_destructive",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_envelope.py",
      "id": "check_layer_projection"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_retained_null_boundary",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_envelope_has_unique_complete_null",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_envelope.py",
      "id": "check_retained_null_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_explicit_subject_adapters",
        "cleanup": "none",
        "mutates": "none",
        "proves": "subject_identity_requires_explicit_adapter",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_experiments.py",
      "id": "check_explicit_subject_adapters"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_holdout_decision_guard",
        "cleanup": "none",
        "mutates": "none",
        "proves": "development_and_holdout_evidence_are_separate",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_experiments.py",
      "id": "check_holdout_decision_guard"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_manifest_pins_research_inputs",
        "cleanup": "none",
        "mutates": "none",
        "proves": "experiment_manifests_pin_all_research_inputs",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_experiments.py",
      "id": "check_manifest_pins_research_inputs"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_reproduction_reporting",
        "cleanup": "none",
        "mutates": "none",
        "proves": "reproduction_checks_report_match_or_reason",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_experiments.py",
      "id": "check_reproduction_reporting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_separate_authorship_records",
        "cleanup": "none",
        "mutates": "none",
        "proves": "candidate_witness_and_decision_authorship_are_recorded",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_experiments.py",
      "id": "check_separate_authorship_records"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_candidate_comparison",
        "cleanup": "none",
        "mutates": "none",
        "proves": "candidate_comparison_exposes_disagreement_without_ranking",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_candidate_comparison"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_evaluator_identity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "evaluator_candidate_identity_is_explicit",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_evaluator_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_evaluator_registry_choices",
        "cleanup": "none",
        "mutates": "none",
        "proves": "evaluator_registry_has_no_implicit_winner",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_evaluator_registry_choices"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_evaluator_replacement",
        "cleanup": "none",
        "mutates": "none",
        "proves": "evaluator_replacement_is_explicit",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_evaluator_replacement"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_explicit_law_comparison",
        "cleanup": "none",
        "mutates": "none",
        "proves": "law_suites_require_named_comparison_policy",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_explicit_law_comparison"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_law_suite_evidence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "law_suites_capture_failures_and_errors",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_law_suite_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_separation_law_builders",
        "cleanup": "none",
        "mutates": "none",
        "proves": "law_suites_capture_failures_and_errors",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_laboratory.py",
      "id": "check_separation_law_builders"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_law_identity_covers_fixtures",
        "cleanup": "none",
        "mutates": "none",
        "proves": "law_identity_covers_implementation_and_fixtures",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_law_identity.py",
      "id": "check_law_identity_covers_fixtures"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_explicit_layer_pair_plan",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_layer_pairing_requires_explicit_plan",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_layer_pairing.py",
      "id": "check_explicit_layer_pair_plan"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_layer_pair_source_and_loss_evidence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "layer_pairing_preserves_sources_and_declares_loss",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_layer_pairing.py",
      "id": "check_layer_pair_source_and_loss_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_retained_pair_measurement_firewall",
        "cleanup": "none",
        "mutates": "none",
        "proves": "retained_pairing_does_not_extend_measurements",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_layer_pairing.py",
      "id": "check_retained_pair_measurement_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_unmatched_layer_modes",
        "cleanup": "none",
        "mutates": "none",
        "proves": "unmatched_layers_follow_explicit_mode",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_layer_pairing.py",
      "id": "check_unmatched_layer_modes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_explicit_policy_keys",
        "cleanup": "none",
        "mutates": "none",
        "proves": "lossy_builtin_policies_require_explicit_keys",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_policy.py",
      "id": "check_explicit_policy_keys"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_policy_registry_choices",
        "cleanup": "none",
        "mutates": "none",
        "proves": "policy_registry_preserves_multiple_choices",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_policy.py",
      "id": "check_policy_registry_choices"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_projection_loss_evidence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "projection_retains_source_and_declares_loss",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_policy.py",
      "id": "check_projection_loss_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_unknown_policy_failure",
        "cleanup": "none",
        "mutates": "none",
        "proves": "unknown_policy_names_fail_closed",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_policy.py",
      "id": "check_unknown_policy_failure"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_public_surface_is_bounded",
        "cleanup": "none",
        "mutates": "none",
        "proves": "public_surface_exposes_only_ratified_foundations",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_public_surface.py",
      "id": "check_public_surface_is_bounded"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contract_audit_detects_gaps",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_reports_graph_gaps",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_skill_lib_contracts.py",
      "id": "check_contract_audit_detects_gaps"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contract_audit_no_exec",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_is_no_exec",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_skill_lib_contracts.py",
      "id": "check_contract_audit_no_exec"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_repository_contract_graph",
        "cleanup": "none",
        "mutates": "none",
        "proves": "contract_audit_accepts_closed_graph",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_skill_lib_contracts.py",
      "id": "check_repository_contract_graph"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_aggregate_support",
        "cleanup": "none",
        "mutates": "none",
        "proves": "aggregate_support_is_cell_sum",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_aggregate_support"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_algebraic_zero_cell",
        "cleanup": "none",
        "mutates": "none",
        "proves": "algebraic_zero_payload_remains_structural",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_algebraic_zero_cell"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_carrier_constructor",
        "cleanup": "none",
        "mutates": "none",
        "proves": "carrier_is_non_null_by_construction",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_carrier_constructor"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_carrier_factory_null",
        "cleanup": "none",
        "mutates": "none",
        "proves": "carrier_factory_returns_unique_null",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_carrier_factory_null"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_cell_support_zero_test",
        "cleanup": "none",
        "mutates": "none",
        "proves": "cell_support_zero_test_is_fail_closed",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_cell_support_zero_test"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_collapse",
        "cleanup": "none",
        "mutates": "none",
        "proves": "collapse_requires_complete_structural_absence",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_complete_collapse"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_pairing_support_law",
        "cleanup": "none",
        "mutates": "none",
        "proves": "carrier_pairing_is_cartesian_and_support_multiplicative",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_pairing_support_law"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_pruning_rule",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pruning_removes_only_absent_cells",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_pruning_rule"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_unresolved_choice_preservation",
        "cleanup": "none",
        "mutates": "none",
        "proves": "unresolved_structure_choices_are_preserved",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_structure.py",
      "id": "check_unresolved_choice_preservation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fixed_point_requires_resolver",
        "cleanup": "none",
        "mutates": "none",
        "proves": "fixed_point_traversal_requires_resolver",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_traversal.py",
      "id": "check_fixed_point_requires_resolver"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_recursive_cycle_modes",
        "cleanup": "none",
        "mutates": "none",
        "proves": "recursive_cycles_require_explicit_policy",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_traversal.py",
      "id": "check_recursive_cycle_modes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_shared_identity_reference",
        "cleanup": "none",
        "mutates": "none",
        "proves": "shared_identity_references_are_retained",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_traversal.py",
      "id": "check_shared_identity_reference"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_traversal_budget_receipts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "traversal_budgets_emit_receipts",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "ucns-source/tests/test_traversal.py",
      "id": "check_traversal_budget_receipts"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every declared contract has a resolving check and every check names known contracts",
        "since": "2026-07-21",
        "then": "the audit exits successfully"
      },
      "file": "ucns-source/tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_accepts_closed_graph"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "the repository contract graph is audited",
        "since": "2026-07-21",
        "then": "Python source is parsed without importing product or test modules"
      },
      "file": "ucns-source/tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_is_no_exec"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a contract, check target, or self call is missing or unknown",
        "since": "2026-07-21",
        "then": "the audit reports the gap and exits nonzero"
      },
      "file": "ucns-source/tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_reports_graph_gaps"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "parse_blocks, audit_repository",
        "module_kind": "instrument",
        "module_name": "verify_skill_lib_contracts",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line audit",
        "rollback": "remove workflow invocation and script",
        "rollout": "required CI gate",
        "since": "2026-07-21",
        "storage_boundary": "read",
        "summary": "performs a no-exec reconciliation of skill-lib MODULE_BUILD, CONTRACTS, and CHECKS declarations",
        "tests": "tests/test_skill_lib_contracts.py",
        "unresolved": "mutation-level verification beyond planted graph gaps",
        "user_data_boundary": "none"
      },
      "file": "ucns-source/tools/verify_skill_lib_contracts.py",
      "id": "skill_lib_contract_audit"
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
      "from": "check_aggregate_support",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_aggregate_support",
      "to": "self::test_aggregate_support"
    },
    {
      "from": "check_aggregate_support",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_aggregate_support",
      "to": "aggregate_support_is_cell_sum"
    },
    {
      "from": "check_aggregate_support",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_aggregate_support",
      "to": "python3"
    },
    {
      "from": "check_algebraic_zero_cell",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_algebraic_zero_cell",
      "to": "self::test_algebraic_zero_cell"
    },
    {
      "from": "check_algebraic_zero_cell",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_algebraic_zero_cell",
      "to": "algebraic_zero_payload_remains_structural"
    },
    {
      "from": "check_algebraic_zero_cell",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_algebraic_zero_cell",
      "to": "python3"
    },
    {
      "from": "check_candidate_comparison",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_candidate_comparison",
      "to": "self::test_candidate_comparison"
    },
    {
      "from": "check_candidate_comparison",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_candidate_comparison",
      "to": "candidate_comparison_exposes_disagreement_without_ranking"
    },
    {
      "from": "check_candidate_comparison",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_candidate_comparison",
      "to": "python3"
    },
    {
      "from": "check_candidate_family_coexistence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_candidate_family_coexistence",
      "to": "self::test_candidate_family_coexistence"
    },
    {
      "from": "check_candidate_family_coexistence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_candidate_family_coexistence",
      "to": "first_candidate_families_coexist_without_selection"
    },
    {
      "from": "check_candidate_family_coexistence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_candidate_family_coexistence",
      "to": "python3"
    },
    {
      "from": "check_candidate_nonpromotion",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_candidate_nonpromotion",
      "to": "self::test_candidate_nonpromotion"
    },
    {
      "from": "check_candidate_nonpromotion",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_candidate_nonpromotion",
      "to": "candidate_constructors_do_not_promote_canon"
    },
    {
      "from": "check_candidate_nonpromotion",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_candidate_nonpromotion",
      "to": "python3"
    },
    {
      "from": "check_carrier_constructor",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_carrier_constructor",
      "to": "self::test_carrier_constructor"
    },
    {
      "from": "check_carrier_constructor",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_carrier_constructor",
      "to": "carrier_is_non_null_by_construction"
    },
    {
      "from": "check_carrier_constructor",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_carrier_constructor",
      "to": "python3"
    },
    {
      "from": "check_carrier_factory_null",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_carrier_factory_null",
      "to": "self::test_carrier_factory_null"
    },
    {
      "from": "check_carrier_factory_null",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_carrier_factory_null",
      "to": "carrier_factory_returns_unique_null"
    },
    {
      "from": "check_carrier_factory_null",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_carrier_factory_null",
      "to": "python3"
    },
    {
      "from": "check_cell_candidate_scope_failure",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_cell_candidate_scope_failure",
      "to": "self::test_cell_candidate_scope_failure"
    },
    {
      "from": "check_cell_candidate_scope_failure",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_cell_candidate_scope_failure",
      "to": "cell_only_candidates_fail_outside_scope"
    },
    {
      "from": "check_cell_candidate_scope_failure",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_cell_candidate_scope_failure",
      "to": "python3"
    },
    {
      "from": "check_cell_support_zero_test",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_cell_support_zero_test",
      "to": "self::test_cell_support_zero_test"
    },
    {
      "from": "check_cell_support_zero_test",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_cell_support_zero_test",
      "to": "cell_support_zero_test_is_fail_closed"
    },
    {
      "from": "check_cell_support_zero_test",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_cell_support_zero_test",
      "to": "python3"
    },
    {
      "from": "check_clear_is_empty_commit",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_clear_is_empty_commit",
      "to": "self::test_clear_is_empty_commit"
    },
    {
      "from": "check_clear_is_empty_commit",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_clear_is_empty_commit",
      "to": "loto_clear_is_empty_commit"
    },
    {
      "from": "check_clear_is_empty_commit",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_clear_is_empty_commit",
      "to": "git"
    },
    {
      "from": "check_clear_is_empty_commit",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_clear_is_empty_commit",
      "to": "posix_shell"
    },
    {
      "from": "check_clear_is_empty_commit",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_clear_is_empty_commit",
      "to": "python3"
    },
    {
      "from": "check_close_deletes_tag",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_close_deletes_tag",
      "to": "self::test_close_deletes_tag"
    },
    {
      "from": "check_close_deletes_tag",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_close_deletes_tag",
      "to": "loto_close_deletes_tag"
    },
    {
      "from": "check_close_deletes_tag",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_close_deletes_tag",
      "to": "git"
    },
    {
      "from": "check_close_deletes_tag",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_close_deletes_tag",
      "to": "posix_shell"
    },
    {
      "from": "check_close_deletes_tag",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_close_deletes_tag",
      "to": "python3"
    },
    {
      "from": "check_comparison_registry_choices",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_comparison_registry_choices",
      "to": "self::test_comparison_registry_choices"
    },
    {
      "from": "check_comparison_registry_choices",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_comparison_registry_choices",
      "to": "comparison_registry_preserves_multiple_policies"
    },
    {
      "from": "check_comparison_registry_choices",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_comparison_registry_choices",
      "to": "python3"
    },
    {
      "from": "check_comparison_replacement",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_comparison_replacement",
      "to": "self::test_comparison_replacement"
    },
    {
      "from": "check_comparison_replacement",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_comparison_replacement",
      "to": "comparison_policy_replacement_is_explicit"
    },
    {
      "from": "check_comparison_replacement",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_comparison_replacement",
      "to": "python3"
    },
    {
      "from": "check_complete_collapse",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_complete_collapse",
      "to": "self::test_complete_collapse"
    },
    {
      "from": "check_complete_collapse",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_complete_collapse",
      "to": "collapse_requires_complete_structural_absence"
    },
    {
      "from": "check_complete_collapse",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_complete_collapse",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "self::test_contract_audit_detects_gaps"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "contract_audit_reports_graph_gaps"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "self::test_contract_audit_no_exec"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "contract_audit_is_no_exec"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "python3"
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
      "from": "check_custom_comparison_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_custom_comparison_identity",
      "to": "self::test_custom_comparison_identity"
    },
    {
      "from": "check_custom_comparison_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_custom_comparison_identity",
      "to": "custom_comparison_identity_is_explicit"
    },
    {
      "from": "check_custom_comparison_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_custom_comparison_identity",
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
      "from": "check_evaluator_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_identity",
      "to": "self::test_evaluator_identity"
    },
    {
      "from": "check_evaluator_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_identity",
      "to": "evaluator_candidate_identity_is_explicit"
    },
    {
      "from": "check_evaluator_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_identity",
      "to": "python3"
    },
    {
      "from": "check_evaluator_registry_choices",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_registry_choices",
      "to": "self::test_evaluator_registry_choices"
    },
    {
      "from": "check_evaluator_registry_choices",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_registry_choices",
      "to": "evaluator_registry_has_no_implicit_winner"
    },
    {
      "from": "check_evaluator_registry_choices",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_registry_choices",
      "to": "python3"
    },
    {
      "from": "check_evaluator_replacement",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_replacement",
      "to": "self::test_evaluator_replacement"
    },
    {
      "from": "check_evaluator_replacement",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_replacement",
      "to": "evaluator_replacement_is_explicit"
    },
    {
      "from": "check_evaluator_replacement",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_evaluator_replacement",
      "to": "python3"
    },
    {
      "from": "check_explicit_comparison_policies",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_explicit_comparison_policies",
      "to": "self::test_explicit_comparison_policies"
    },
    {
      "from": "check_explicit_comparison_policies",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_explicit_comparison_policies",
      "to": "evaluator_equality_requires_explicit_comparison_policy"
    },
    {
      "from": "check_explicit_comparison_policies",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_explicit_comparison_policies",
      "to": "python3"
    },
    {
      "from": "check_explicit_law_comparison",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_explicit_law_comparison",
      "to": "self::test_explicit_law_comparison"
    },
    {
      "from": "check_explicit_law_comparison",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_explicit_law_comparison",
      "to": "law_suites_require_named_comparison_policy"
    },
    {
      "from": "check_explicit_law_comparison",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_explicit_law_comparison",
      "to": "python3"
    },
    {
      "from": "check_explicit_layer_pair_plan",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_explicit_layer_pair_plan",
      "to": "self::test_explicit_layer_pair_plan"
    },
    {
      "from": "check_explicit_layer_pair_plan",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_explicit_layer_pair_plan",
      "to": "retained_layer_pairing_requires_explicit_plan"
    },
    {
      "from": "check_explicit_layer_pair_plan",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_explicit_layer_pair_plan",
      "to": "python3"
    },
    {
      "from": "check_explicit_policy_keys",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_explicit_policy_keys",
      "to": "self::test_explicit_policy_keys"
    },
    {
      "from": "check_explicit_policy_keys",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_explicit_policy_keys",
      "to": "lossy_builtin_policies_require_explicit_keys"
    },
    {
      "from": "check_explicit_policy_keys",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_explicit_policy_keys",
      "to": "python3"
    },
    {
      "from": "check_explicit_subject_adapters",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_explicit_subject_adapters",
      "to": "self::test_explicit_subject_adapters"
    },
    {
      "from": "check_explicit_subject_adapters",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_explicit_subject_adapters",
      "to": "subject_identity_requires_explicit_adapter"
    },
    {
      "from": "check_explicit_subject_adapters",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_explicit_subject_adapters",
      "to": "python3"
    },
    {
      "from": "check_falsey_retained_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_falsey_retained_evidence",
      "to": "self::test_falsey_retained_evidence"
    },
    {
      "from": "check_falsey_retained_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_falsey_retained_evidence",
      "to": "retained_layer_presence_is_explicit"
    },
    {
      "from": "check_falsey_retained_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_falsey_retained_evidence",
      "to": "python3"
    },
    {
      "from": "check_fixed_point_requires_resolver",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_fixed_point_requires_resolver",
      "to": "self::test_fixed_point_requires_resolver"
    },
    {
      "from": "check_fixed_point_requires_resolver",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_fixed_point_requires_resolver",
      "to": "fixed_point_traversal_requires_resolver"
    },
    {
      "from": "check_fixed_point_requires_resolver",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_fixed_point_requires_resolver",
      "to": "python3"
    },
    {
      "from": "check_holdout_decision_guard",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_holdout_decision_guard",
      "to": "self::test_holdout_decision_guard"
    },
    {
      "from": "check_holdout_decision_guard",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_holdout_decision_guard",
      "to": "development_and_holdout_evidence_are_separate"
    },
    {
      "from": "check_holdout_decision_guard",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_holdout_decision_guard",
      "to": "python3"
    },
    {
      "from": "check_initial_product_multiplicativity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_initial_product_multiplicativity",
      "to": "self::test_initial_product_multiplicativity"
    },
    {
      "from": "check_initial_product_multiplicativity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_initial_product_multiplicativity",
      "to": "initial_product_candidates_multiply_under_actual_pairing"
    },
    {
      "from": "check_initial_product_multiplicativity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_initial_product_multiplicativity",
      "to": "python3"
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
      "from": "check_latest_test_wins",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_latest_test_wins",
      "to": "self::test_latest_test_wins"
    },
    {
      "from": "check_latest_test_wins",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_latest_test_wins",
      "to": "loto_latest_test_wins"
    },
    {
      "from": "check_latest_test_wins",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_latest_test_wins",
      "to": "git"
    },
    {
      "from": "check_latest_test_wins",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_latest_test_wins",
      "to": "posix_shell"
    },
    {
      "from": "check_latest_test_wins",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_latest_test_wins",
      "to": "python3"
    },
    {
      "from": "check_law_identity_covers_fixtures",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_law_identity_covers_fixtures",
      "to": "self::test_law_identity_covers_fixtures"
    },
    {
      "from": "check_law_identity_covers_fixtures",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_law_identity_covers_fixtures",
      "to": "law_identity_covers_implementation_and_fixtures"
    },
    {
      "from": "check_law_identity_covers_fixtures",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_law_identity_covers_fixtures",
      "to": "python3"
    },
    {
      "from": "check_law_suite_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_law_suite_evidence",
      "to": "self::test_law_suite_evidence"
    },
    {
      "from": "check_law_suite_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_law_suite_evidence",
      "to": "law_suites_capture_failures_and_errors"
    },
    {
      "from": "check_law_suite_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_law_suite_evidence",
      "to": "python3"
    },
    {
      "from": "check_layer_append_behavior",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_layer_append_behavior",
      "to": "self::test_layer_append_behavior"
    },
    {
      "from": "check_layer_append_behavior",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_layer_append_behavior",
      "to": "retained_layers_append_without_overwrite"
    },
    {
      "from": "check_layer_append_behavior",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_layer_append_behavior",
      "to": "python3"
    },
    {
      "from": "check_layer_measurement_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_layer_measurement_firewall",
      "to": "self::test_layer_measurement_firewall"
    },
    {
      "from": "check_layer_measurement_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_layer_measurement_firewall",
      "to": "retained_layers_do_not_silently_enter_cell_support"
    },
    {
      "from": "check_layer_measurement_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_layer_measurement_firewall",
      "to": "python3"
    },
    {
      "from": "check_layer_pair_source_and_loss_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_layer_pair_source_and_loss_evidence",
      "to": "self::test_layer_pair_source_and_loss_evidence"
    },
    {
      "from": "check_layer_pair_source_and_loss_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_layer_pair_source_and_loss_evidence",
      "to": "layer_pairing_preserves_sources_and_declares_loss"
    },
    {
      "from": "check_layer_pair_source_and_loss_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_layer_pair_source_and_loss_evidence",
      "to": "python3"
    },
    {
      "from": "check_layer_projection",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_layer_projection",
      "to": "self::test_layer_projection"
    },
    {
      "from": "check_layer_projection",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_layer_projection",
      "to": "retained_layer_projection_is_non_destructive"
    },
    {
      "from": "check_layer_projection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_layer_projection",
      "to": "python3"
    },
    {
      "from": "check_lifted_period",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "self::test_lifted_period"
    },
    {
      "from": "check_lifted_period",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "lifted_period_is_720_degrees"
    },
    {
      "from": "check_lifted_period",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "two_visible_laps_complete_return"
    },
    {
      "from": "check_lifted_period",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "python3"
    },
    {
      "from": "check_manifest_pins_research_inputs",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_manifest_pins_research_inputs",
      "to": "self::test_manifest_pins_research_inputs"
    },
    {
      "from": "check_manifest_pins_research_inputs",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_manifest_pins_research_inputs",
      "to": "experiment_manifests_pin_all_research_inputs"
    },
    {
      "from": "check_manifest_pins_research_inputs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_manifest_pins_research_inputs",
      "to": "python3"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "self::test_non_null_validation_and_radius"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "non_null_carrier_has_positive_breadth"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "python3"
    },
    {
      "from": "check_occurrence_coverage_candidate",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_occurrence_coverage_candidate",
      "to": "self::test_occurrence_coverage_candidate_invariants"
    },
    {
      "from": "check_occurrence_coverage_candidate",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_occurrence_coverage_candidate",
      "to": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "from": "check_occurrence_coverage_candidate",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_occurrence_coverage_candidate",
      "to": "python3"
    },
    {
      "from": "check_one_commit_per_session",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_one_commit_per_session",
      "to": "self::test_one_commit_per_session"
    },
    {
      "from": "check_one_commit_per_session",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_one_commit_per_session",
      "to": "loto_one_commit_per_session"
    },
    {
      "from": "check_one_commit_per_session",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_one_commit_per_session",
      "to": "git"
    },
    {
      "from": "check_one_commit_per_session",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_one_commit_per_session",
      "to": "posix_shell"
    },
    {
      "from": "check_one_commit_per_session",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_one_commit_per_session",
      "to": "python3"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "self::test_one_lap_is_deck_translation"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "one_visible_lap_is_deck_translation_only"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "topology_does_not_invent_orientation_algebra"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "python3"
    },
    {
      "from": "check_open_never_dirties",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_open_never_dirties",
      "to": "self::test_open_never_dirties"
    },
    {
      "from": "check_open_never_dirties",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_open_never_dirties",
      "to": "loto_open_never_dirties"
    },
    {
      "from": "check_open_never_dirties",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_open_never_dirties",
      "to": "git"
    },
    {
      "from": "check_open_never_dirties",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_open_never_dirties",
      "to": "posix_shell"
    },
    {
      "from": "check_open_never_dirties",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_open_never_dirties",
      "to": "python3"
    },
    {
      "from": "check_pairing_support_law",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pairing_support_law",
      "to": "self::test_pairing_support_law"
    },
    {
      "from": "check_pairing_support_law",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pairing_support_law",
      "to": "carrier_pairing_is_cartesian_and_support_multiplicative"
    },
    {
      "from": "check_pairing_support_law",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pairing_support_law",
      "to": "python3"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "self::test_payload_zero_does_not_collapse_carrier"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "algebraic_zero_is_not_structural_null"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "python3"
    },
    {
      "from": "check_policy_registry_choices",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_policy_registry_choices",
      "to": "self::test_policy_registry_choices"
    },
    {
      "from": "check_policy_registry_choices",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_policy_registry_choices",
      "to": "policy_registry_preserves_multiple_choices"
    },
    {
      "from": "check_policy_registry_choices",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_policy_registry_choices",
      "to": "python3"
    },
    {
      "from": "check_projection_loss_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_projection_loss_evidence",
      "to": "self::test_projection_loss_evidence"
    },
    {
      "from": "check_projection_loss_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_projection_loss_evidence",
      "to": "projection_retains_source_and_declares_loss"
    },
    {
      "from": "check_projection_loss_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_projection_loss_evidence",
      "to": "python3"
    },
    {
      "from": "check_pruning_rule",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pruning_rule",
      "to": "self::test_pruning_rule"
    },
    {
      "from": "check_pruning_rule",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pruning_rule",
      "to": "pruning_removes_only_absent_cells"
    },
    {
      "from": "check_pruning_rule",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pruning_rule",
      "to": "python3"
    },
    {
      "from": "check_public_surface_is_bounded",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_public_surface_is_bounded",
      "to": "self::test_public_surface_is_bounded"
    },
    {
      "from": "check_public_surface_is_bounded",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_public_surface_is_bounded",
      "to": "public_surface_exposes_only_ratified_foundations"
    },
    {
      "from": "check_public_surface_is_bounded",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_public_surface_is_bounded",
      "to": "python3"
    },
    {
      "from": "check_recursive_cycle_modes",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_recursive_cycle_modes",
      "to": "self::test_recursive_cycle_modes"
    },
    {
      "from": "check_recursive_cycle_modes",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_recursive_cycle_modes",
      "to": "recursive_cycles_require_explicit_policy"
    },
    {
      "from": "check_recursive_cycle_modes",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_recursive_cycle_modes",
      "to": "python3"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "self::test_repository_contract_graph"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "contract_audit_accepts_closed_graph"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "python3"
    },
    {
      "from": "check_reproduction_reporting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_reproduction_reporting",
      "to": "self::test_reproduction_reporting"
    },
    {
      "from": "check_reproduction_reporting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_reproduction_reporting",
      "to": "reproduction_checks_report_match_or_reason"
    },
    {
      "from": "check_reproduction_reporting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_reproduction_reporting",
      "to": "python3"
    },
    {
      "from": "check_retained_null_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_retained_null_boundary",
      "to": "self::test_retained_null_boundary"
    },
    {
      "from": "check_retained_null_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_retained_null_boundary",
      "to": "retained_envelope_has_unique_complete_null"
    },
    {
      "from": "check_retained_null_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_retained_null_boundary",
      "to": "python3"
    },
    {
      "from": "check_retained_pair_measurement_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_retained_pair_measurement_firewall",
      "to": "self::test_retained_pair_measurement_firewall"
    },
    {
      "from": "check_retained_pair_measurement_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_retained_pair_measurement_firewall",
      "to": "retained_pairing_does_not_extend_measurements"
    },
    {
      "from": "check_retained_pair_measurement_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_retained_pair_measurement_firewall",
      "to": "python3"
    },
    {
      "from": "check_scar_blocks_work",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_scar_blocks_work",
      "to": "self::test_scar_blocks_work"
    },
    {
      "from": "check_scar_blocks_work",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_scar_blocks_work",
      "to": "loto_scar_blocks_work"
    },
    {
      "from": "check_scar_blocks_work",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scar_blocks_work",
      "to": "git"
    },
    {
      "from": "check_scar_blocks_work",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scar_blocks_work",
      "to": "posix_shell"
    },
    {
      "from": "check_scar_blocks_work",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scar_blocks_work",
      "to": "python3"
    },
    {
      "from": "check_scope_assertion_candidate",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_scope_assertion_candidate",
      "to": "self::test_scope_assertion_candidate_invariants"
    },
    {
      "from": "check_scope_assertion_candidate",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_scope_assertion_candidate",
      "to": "edcm_ucns_edcm_experiments_v3"
    },
    {
      "from": "check_scope_assertion_candidate",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scope_assertion_candidate",
      "to": "python3"
    },
    {
      "from": "check_scope_enforced",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_scope_enforced",
      "to": "self::test_scope_enforced"
    },
    {
      "from": "check_scope_enforced",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_scope_enforced",
      "to": "loto_scope_enforced"
    },
    {
      "from": "check_scope_enforced",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scope_enforced",
      "to": "git"
    },
    {
      "from": "check_scope_enforced",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scope_enforced",
      "to": "posix_shell"
    },
    {
      "from": "check_scope_enforced",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_scope_enforced",
      "to": "python3"
    },
    {
      "from": "check_separate_authorship_records",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_separate_authorship_records",
      "to": "self::test_separate_authorship_records"
    },
    {
      "from": "check_separate_authorship_records",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_separate_authorship_records",
      "to": "candidate_witness_and_decision_authorship_are_recorded"
    },
    {
      "from": "check_separate_authorship_records",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_separate_authorship_records",
      "to": "python3"
    },
    {
      "from": "check_separation_law_builders",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_separation_law_builders",
      "to": "self::test_separation_law_builders"
    },
    {
      "from": "check_separation_law_builders",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_separation_law_builders",
      "to": "law_suites_capture_failures_and_errors"
    },
    {
      "from": "check_separation_law_builders",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_separation_law_builders",
      "to": "python3"
    },
    {
      "from": "check_shared_identity_reference",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_shared_identity_reference",
      "to": "self::test_shared_identity_reference"
    },
    {
      "from": "check_shared_identity_reference",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_shared_identity_reference",
      "to": "shared_identity_references_are_retained"
    },
    {
      "from": "check_shared_identity_reference",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_shared_identity_reference",
      "to": "python3"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "self::test_structural_null_identity"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "structural_null_is_unique_and_coordinate_free"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "python3"
    },
    {
      "from": "check_traversal_budget_receipts",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_traversal_budget_receipts",
      "to": "self::test_traversal_budget_receipts"
    },
    {
      "from": "check_traversal_budget_receipts",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_traversal_budget_receipts",
      "to": "traversal_budgets_emit_receipts"
    },
    {
      "from": "check_traversal_budget_receipts",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_traversal_budget_receipts",
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
      "from": "check_ucns_edcm_v2_joint_report",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_joint_report",
      "to": "self::test_v2_joint_report_preserves_prior_evidence_and_no_canon"
    },
    {
      "from": "check_ucns_edcm_v2_joint_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_joint_report",
      "to": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "from": "check_ucns_edcm_v2_joint_report",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_joint_report",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v2_program",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_program",
      "to": "self::test_v2_program_structure"
    },
    {
      "from": "check_ucns_edcm_v2_program",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_program",
      "to": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "from": "check_ucns_edcm_v2_program",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v2_program",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v3_joint_report",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_joint_report",
      "to": "self::test_v3_joint_report_preserves_scope_and_no_canon"
    },
    {
      "from": "check_ucns_edcm_v3_joint_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_joint_report",
      "to": "edcm_ucns_edcm_experiments_v3"
    },
    {
      "from": "check_ucns_edcm_v3_joint_report",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_joint_report",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v3_program",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_program",
      "to": "self::test_v3_program_structure"
    },
    {
      "from": "check_ucns_edcm_v3_program",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_program",
      "to": "edcm_ucns_edcm_experiments_v3"
    },
    {
      "from": "check_ucns_edcm_v3_program",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v3_program",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v4_joint_report",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_joint_report",
      "to": "self::test_v4_joint_report_preserves_graphs_and_no_canon"
    },
    {
      "from": "check_ucns_edcm_v4_joint_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_joint_report",
      "to": "edcm_ucns_edcm_experiments_v4"
    },
    {
      "from": "check_ucns_edcm_v4_joint_report",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_joint_report",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v4_program",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_program",
      "to": "self::test_v4_program_structure"
    },
    {
      "from": "check_ucns_edcm_v4_program",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_program",
      "to": "edcm_ucns_edcm_experiments_v4"
    },
    {
      "from": "check_ucns_edcm_v4_program",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_program",
      "to": "python3"
    },
    {
      "from": "check_ucns_edcm_v4_resolvers",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_resolvers",
      "to": "self::test_v4_resolver_contrasts"
    },
    {
      "from": "check_ucns_edcm_v4_resolvers",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_resolvers",
      "to": "edcm_ucns_edcm_experiments_v4"
    },
    {
      "from": "check_ucns_edcm_v4_resolvers",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ucns_edcm_v4_resolvers",
      "to": "python3"
    },
    {
      "from": "check_unknown_policy_failure",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_unknown_policy_failure",
      "to": "self::test_unknown_policy_failure"
    },
    {
      "from": "check_unknown_policy_failure",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_unknown_policy_failure",
      "to": "unknown_policy_names_fail_closed"
    },
    {
      "from": "check_unknown_policy_failure",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_unknown_policy_failure",
      "to": "python3"
    },
    {
      "from": "check_unmatched_layer_modes",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_unmatched_layer_modes",
      "to": "self::test_unmatched_layer_modes"
    },
    {
      "from": "check_unmatched_layer_modes",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_unmatched_layer_modes",
      "to": "unmatched_layers_follow_explicit_mode"
    },
    {
      "from": "check_unmatched_layer_modes",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_unmatched_layer_modes",
      "to": "python3"
    },
    {
      "from": "check_unresolved_choice_preservation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_unresolved_choice_preservation",
      "to": "self::test_unresolved_choice_preservation"
    },
    {
      "from": "check_unresolved_choice_preservation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_unresolved_choice_preservation",
      "to": "unresolved_structure_choices_are_preserved"
    },
    {
      "from": "check_unresolved_choice_preservation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_unresolved_choice_preservation",
      "to": "python3"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "self::test_visible_projection_and_branch_law"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "visible_projection_is_360_degrees"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "python3"
    },
    {
      "from": "addition_boundary",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "addition_boundary",
      "to": "contracts.test_addition_boundary.contract_addition_boundary"
    },
    {
      "from": "division_theory",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "division_theory",
      "to": "contracts.test_quotient_solvability.contract_division_theory"
    },
    {
      "from": "multiply_associativity",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "multiply_associativity",
      "to": "contracts.test_associativity_triples.contract_multiply_associativity"
    },
    {
      "from": "multiply_commutativity_ruling",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "multiply_commutativity_ruling",
      "to": "contracts.test_commutator.contract_multiply_commutativity_ruling"
    },
    {
      "from": "multiply_identity",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "multiply_identity",
      "to": "contracts.test_identity_two_sided.contract_multiply_identity"
    },
    {
      "from": "multiply_well_defined",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "multiply_well_defined",
      "to": "contracts.test_multiply_canonical.contract_multiply_well_defined"
    },
    {
      "from": "structure_naming",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "structure_naming",
      "to": "contracts.test_structure_axioms.contract_structure_naming"
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
      "from": "addition_boundary",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "addition_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "cycle_safe_traversal_policy",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "cycle_safe_traversal_policy",
      "to": "Erin Spencer"
    },
    {
      "from": "cycle_safe_traversal_policy",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "cycle_safe_traversal_policy",
      "to": "retained_structure_envelope"
    },
    {
      "from": "directed_carrier_floor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "directed_carrier_floor",
      "to": "Erin Spencer"
    },
    {
      "from": "directed_carrier_floor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "directed_carrier_floor",
      "to": "canonical_chapter_one"
    },
    {
      "from": "division_theory",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "division_theory",
      "to": "Erin Spencer"
    },
    {
      "from": "division_theory",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "division_theory",
      "to": "Erin Spencer"
    },
    {
      "from": "division_theory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "division_theory",
      "to": "ucns_canonical"
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
      "from": "edcm_ucns_edcm_experiments_v2",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v2",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v2",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v2",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v2",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v2",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v2",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v2",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v3",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v3",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v3",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v3",
      "to": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v3",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v3",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
      "to": "edcm_ucns_edcm_experiments"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
      "to": "edcm_ucns_edcm_experiments_v2"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
      "to": "edcm_ucns_edcm_experiments_v3"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcm_ucns_edcm_experiments_v4",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_ucns_edcm_experiments_v4",
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
    },
    {
      "from": "evaluator_candidate_laboratory",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "evaluator_candidate_laboratory",
      "to": "Erin Spencer"
    },
    {
      "from": "evaluator_candidate_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "evaluator_candidate_laboratory",
      "to": "explicit_comparison_policy_layer"
    },
    {
      "from": "evaluator_candidate_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "evaluator_candidate_laboratory",
      "to": "retained_structure_envelope"
    },
    {
      "from": "evaluator_candidate_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "evaluator_candidate_laboratory",
      "to": "structural_cell_support_floor"
    },
    {
      "from": "evaluator_candidate_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "evaluator_candidate_laboratory",
      "to": "structural_choice_policy_layer"
    },
    {
      "from": "explicit_comparison_policy_layer",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "explicit_comparison_policy_layer",
      "to": "Erin Spencer"
    },
    {
      "from": "explicit_comparison_policy_layer",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "explicit_comparison_policy_layer",
      "to": "structural_choice_policy_layer"
    },
    {
      "from": "first_competing_evaluator_candidate_families",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "first_competing_evaluator_candidate_families",
      "to": "Erin Spencer"
    },
    {
      "from": "first_competing_evaluator_candidate_families",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "first_competing_evaluator_candidate_families",
      "to": "evaluator_candidate_laboratory"
    },
    {
      "from": "first_competing_evaluator_candidate_families",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "first_competing_evaluator_candidate_families",
      "to": "reproducible_witness_experiment_pipeline"
    },
    {
      "from": "foundations_public_surface",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "Erin Spencer"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "cycle_safe_traversal_policy"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "directed_carrier_floor"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "evaluator_candidate_laboratory"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "explicit_comparison_policy_layer"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "first_competing_evaluator_candidate_families"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "reproducible_witness_experiment_pipeline"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "retained_layer_pairing_laboratory"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "retained_structure_envelope"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "structural_cell_support_floor"
    },
    {
      "from": "foundations_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "foundations_public_surface",
      "to": "structural_choice_policy_layer"
    },
    {
      "from": "local_groups_relational_geometry_contracts",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "local_groups_relational_geometry_contracts",
      "to": "Erin Spencer"
    },
    {
      "from": "local_groups_relational_geometry_contracts",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "local_groups_relational_geometry_contracts",
      "to": "ucns_canonical"
    },
    {
      "from": "local_groups_relational_geometry_contracts",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "local_groups_relational_geometry_contracts",
      "to": "ucns_relational_geometry"
    },
    {
      "from": "multiply_associativity",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "multiply_associativity",
      "to": "Erin Spencer"
    },
    {
      "from": "multiply_commutativity_ruling",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "multiply_commutativity_ruling",
      "to": "Erin Spencer"
    },
    {
      "from": "multiply_identity",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "multiply_identity",
      "to": "Erin Spencer"
    },
    {
      "from": "multiply_well_defined",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "multiply_well_defined",
      "to": "Erin Spencer"
    },
    {
      "from": "repo_loto_evidence",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "repo_loto_evidence",
      "to": "Way Seer Erin"
    },
    {
      "from": "repo_mutation_gate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "repo_mutation_gate",
      "to": "Way Seer Erin"
    },
    {
      "from": "reproducible_witness_experiment_pipeline",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "reproducible_witness_experiment_pipeline",
      "to": "Erin Spencer"
    },
    {
      "from": "reproducible_witness_experiment_pipeline",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "reproducible_witness_experiment_pipeline",
      "to": "cycle_safe_traversal_policy"
    },
    {
      "from": "reproducible_witness_experiment_pipeline",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "reproducible_witness_experiment_pipeline",
      "to": "evaluator_candidate_laboratory"
    },
    {
      "from": "reproducible_witness_experiment_pipeline",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "reproducible_witness_experiment_pipeline",
      "to": "explicit_comparison_policy_layer"
    },
    {
      "from": "retained_layer_pairing_laboratory",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_layer_pairing_laboratory",
      "to": "Erin Spencer"
    },
    {
      "from": "retained_layer_pairing_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_layer_pairing_laboratory",
      "to": "retained_structure_envelope"
    },
    {
      "from": "retained_layer_pairing_laboratory",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_layer_pairing_laboratory",
      "to": "structural_cell_support_floor"
    },
    {
      "from": "retained_structure_envelope",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_structure_envelope",
      "to": "Erin Spencer"
    },
    {
      "from": "retained_structure_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_structure_envelope",
      "to": "structural_cell_support_floor"
    },
    {
      "from": "retained_structure_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "retained_structure_envelope",
      "to": "structural_choice_policy_layer"
    },
    {
      "from": "skill_lib_contract_audit",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "skill_lib_contract_audit",
      "to": "Erin Spencer"
    },
    {
      "from": "structural_cell_support_floor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "structural_cell_support_floor",
      "to": "Erin Spencer"
    },
    {
      "from": "structural_cell_support_floor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structural_cell_support_floor",
      "to": "directed_carrier_floor"
    },
    {
      "from": "structural_choice_policy_layer",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "structural_choice_policy_layer",
      "to": "Erin Spencer"
    },
    {
      "from": "structural_choice_policy_layer",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structural_choice_policy_layer",
      "to": "structural_cell_support_floor"
    },
    {
      "from": "structure_naming",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "Erin Spencer"
    },
    {
      "from": "structure_naming",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "division_theory"
    },
    {
      "from": "structure_naming",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "multiply_associativity"
    },
    {
      "from": "structure_naming",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "multiply_commutativity_ruling"
    },
    {
      "from": "structure_naming",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "multiply_identity"
    },
    {
      "from": "structure_naming",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "structure_naming",
      "to": "multiply_well_defined"
    },
    {
      "from": "ucns_a0_safe",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_a0_safe",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_a0_safe",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_a0_safe",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_a0_safe",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_a0_safe",
      "to": "ucns_factorization_result"
    },
    {
      "from": "ucns_a0_safe",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_a0_safe",
      "to": "ucns_object_record"
    },
    {
      "from": "ucns_a0_safe",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_a0_safe",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_bridge",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_bridge",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_bridge",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_bridge",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_canonical",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_canonical",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_canonical",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_canonical",
      "to": "none"
    },
    {
      "from": "ucns_canonical_factor_selection",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_canonical_factor_selection",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_canonical_factor_selection",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_canonical_factor_selection",
      "to": "ucns_carrier_support_pruning"
    },
    {
      "from": "ucns_carrier_support_pruning",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_carrier_support_pruning",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_carrier_support_pruning",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_carrier_support_pruning",
      "to": "none"
    },
    {
      "from": "ucns_catalogue",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_catalogue",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_catalogue",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_catalogue_coverage",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_coverage",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_catalogue_coverage",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_coverage",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_catalogue_coverage",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_coverage",
      "to": "ucns_factor_search_v08"
    },
    {
      "from": "ucns_catalogue_coverage",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_coverage",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_catalogue_d3",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_d3",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_catalogue_d3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_d3",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_catalogue_d3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_d3",
      "to": "ucns_catalogue"
    },
    {
      "from": "ucns_catalogue_d3",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_catalogue_d3",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_codec",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_codec",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_codec",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_codec",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_core",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_core",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_core",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_core",
      "to": "none"
    },
    {
      "from": "ucns_domain_status",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_domain_status",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_domain_status",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_domain_status",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_domains",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_domains",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_domains",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_domains",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_embedding",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_embedding",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_embedding",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_embedding",
      "to": "ucns_epicycle"
    },
    {
      "from": "ucns_epicycle",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_epicycle",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_epicycle",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_epicycle",
      "to": "none"
    },
    {
      "from": "ucns_evidence",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_evidence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence",
      "to": "ucns_bridge"
    },
    {
      "from": "ucns_evidence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_evidence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence",
      "to": "ucns_domain_status"
    },
    {
      "from": "ucns_evidence",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence",
      "to": "ucns_factorization_result"
    },
    {
      "from": "ucns_evidence_envelope",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence_envelope",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_evidence_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence_envelope",
      "to": "ucns_domain_status"
    },
    {
      "from": "ucns_evidence_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence_envelope",
      "to": "ucns_factorization_result"
    },
    {
      "from": "ucns_evidence_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence_envelope",
      "to": "ucns_object_record"
    },
    {
      "from": "ucns_evidence_envelope",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_evidence_envelope",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_carrier_support_pruning"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_host_recovery"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_payload_system"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_factor_search_v08",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factor_search_v08",
      "to": "ucns_witness_matrix"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_carrier_support_pruning"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_catalogue_coverage"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_domain_status"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_factor_search_v08"
    },
    {
      "from": "ucns_factorization_result",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_factorization_result",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_geometry_bridge",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_bridge",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_geometry_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_bridge",
      "to": "ucns.canonical"
    },
    {
      "from": "ucns_geometry_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_bridge",
      "to": "ucns.relational_geometry"
    },
    {
      "from": "ucns_host_recovery",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_host_recovery",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_host_recovery",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_host_recovery",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_left_quotient",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_left_quotient",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_left_quotient",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_left_quotient",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_mobius",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius",
      "to": "none"
    },
    {
      "from": "ucns_native_cache",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_native_cache",
      "to": "Erin Spencer / Codex"
    },
    {
      "from": "ucns_object_record",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_object_record",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_object_record",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_object_record",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_object_record",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_object_record",
      "to": "ucns_domain_status"
    },
    {
      "from": "ucns_object_record",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_object_record",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_object_record",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_object_record",
      "to": "ucns_serialization"
    },
    {
      "from": "ucns_payload_system",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_payload_system",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_payload_system",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_payload_system",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_public_gonol",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol",
      "to": "none"
    },
    {
      "from": "ucns_public_gonol_faces",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_faces",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol_faces",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_faces",
      "to": "ucns_public_gonol"
    },
    {
      "from": "ucns_public_gonol_lifted_path",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_lifted_path",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol_lifted_path",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_lifted_path",
      "to": "ucns_public_gonol"
    },
    {
      "from": "ucns_public_gonol_lifted_path",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_lifted_path",
      "to": "ucns_public_gonol_faces"
    },
    {
      "from": "ucns_public_gonol_mirror",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_mirror",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol_mirror",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_mirror",
      "to": "ucns_public_gonol"
    },
    {
      "from": "ucns_public_gonol_private",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_private",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol_private",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_private",
      "to": "ucns_public_gonol"
    },
    {
      "from": "ucns_public_gonol_private",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_private",
      "to": "ucns_public_gonol_faces"
    },
    {
      "from": "ucns_quotient",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_quotient",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_quotient",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_quotient",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_quotient",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_quotient",
      "to": "ucns_left_quotient"
    },
    {
      "from": "ucns_relational_geometry",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_relational_geometry",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_relational_geometry",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_relational_geometry",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_serialization",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_serialization",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_serialization",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_serialization",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_similarity",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_similarity",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_similarity",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_similarity",
      "to": "none"
    },
    {
      "from": "ucns_store",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_store",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_store",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_store",
      "to": "ucns_canonical"
    },
    {
      "from": "ucns_store",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_store",
      "to": "ucns_codec"
    },
    {
      "from": "ucns_store",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_store",
      "to": "ucns_domains"
    },
    {
      "from": "ucns_store",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_store",
      "to": "ucns_left_quotient"
    },
    {
      "from": "ucns_witness_matrix",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_witness_matrix",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_witness_matrix",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_witness_matrix",
      "to": "ucns_canonical"
    }
  ],
  "gaps": [],
  "repo": "The-Interdependency/edcm"
});
