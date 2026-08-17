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
        "public_surface": "__version__, build_default_layers, EDCMLayers, LayerProvenance, ConsolidatedMeasurementLayer, CompositeSemanticsLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, MissingUCNSProfileLayer, UCNSProfileLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, ActualMetapatAdapter, MetapatIntegrationStatus, MetapatSemanticEvidence, select_metapat_adapter, inspect_metapat_adapter, ActualUCNSAdapter, UCNSIntegrationStatus, UCNSProfileObservationEvidence, select_ucns_adapter, inspect_ucns_adapter, AuthorizedUCNSFork, UCNSForkTopologyBinding, UCNSForkLintReport, ForkLintDependencyError, ForkTopologyError, build_fork_topology_binding, enumerate_payload_fork_paths, lint_fork_topology, lint_all_payload_forks, EDCMResultContract, build_result_contract, RESULT_SCHEMA_ID, RESULT_SCHEMA_VERSION, IntegrityFinding, IntegrityReport, run_integrity_gate, verify_frozen_canon, verify_measurement_authority, verify_orthogonality_alias, audit_energy_text, audit_energy_claim, extract_energy_claim_candidates, audit_falsifiability_preservation, EnergyAuditReport, AuditFlag, EnergyClaim, EDCMBONE_FAILURE_TAXONOMY, BOUNDARY_NOTE, AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, canonical_axes, field_motion_fixture, FIELD_MOTION_FIXTURE_MATRIX, SIGNED_TERNARY, GRAINS, CONTACT_SIGN, RESOLUTION_SIGN, measurement, language, edcmucns, CanonLoader, parse_transcript, ParsedTranscript, compute_transcript, RoundMetrics, project_transcript, AgentMetrics, fire_alerts",
        "requires": "edcm_layers, edcm_metapat_adapter, edcm_ucns_adapter, edcm_ucns_fork_lint, edcm_shared_stack, edcm_integrity, edcm_energy_claims, edcm_falsifiability_bridge, edcm_ucns_objects, edcmucns_package, edcm_language_package",
        "rollback": "remove new exports and restore prior package root only with a result-schema migration",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "EDCM package root \u2014 declares package identity and re-exports provenance-bearing shared-stack layers, canonical METAPAT consumer surfaces, the exact EDCM UCNS word-gonol observation profile consumer, historical fork-topology research surfaces, result contracts, integrity gates, energy audit, EDCM objects, edcmucns architecture, and canonical maintained measurement.",
        "tests": "tests.test_measurement, tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_metapat_adapter, tests.test_shared_stack_contract, tests.test_integrity, tests.test_ucns_objects, tests.test_ucns_fork_lint, tests.test_energy_claims, tests.test_packaging",
        "unresolved": "UCNS observation digests and historical fork topology bindings provide content identity but not cryptographic producer authentication; formal Mobius coordinates and higher-gonol composition remain open",
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
        "module_kind": "adapter",
        "module_name": "corpora",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "load_multiwoz21_admission, run_multiwoz21_archive",
        "requires": "edcm_ucns_adapter",
        "rollback": "remove the corpus package and generated aggregate evidence; frozen measurement and historical experiments remain unchanged",
        "rollout": "explicit per-corpus command after admission-manifest verification",
        "since": "2026-07-28",
        "storage_boundary": "caller-selected aggregate reports, receipts, and checkpoints only; raw corpora remain external",
        "summary": "source-native full-corpus execution surfaces with admission, reconciliation, and completion or incompletion receipts",
        "tests": "tests.test_multiwoz21_corpus",
        "unresolved": "admission and adapter design for the six queued corpora after MultiWOZ 2.1",
        "user_data_boundary": "source evidence is read locally and only non-text aggregates and cryptographic identities are emitted"
      },
      "file": "edcm/corpora/__init__.py",
      "id": "edcm_corpora_package"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "provenance",
        "given": "a caller supplies a local MultiWOZ 2.1 archive",
        "since": "2026-07-28",
        "then": "archive bytes and every logical member match the committed Cambridge admission manifest before any dialogue is observed"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_admission_precedes_execution"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "source streaming reaches valid EOF",
        "since": "2026-07-28",
        "then": "completion is emitted only when dialogue, partition, source-turn, adapter-turn, and unit-support counts reconcile exactly"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_completion_requires_reconciliation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "an admitted archive contains the complete top-level dialogue object",
        "since": "2026-07-28",
        "then": "every log text is processed once in source dialogue and turn order with no normalization, sampling, sorting, or deduplication"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_every_turn_is_observed_exactly_once"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "archive, schema, adapter, checkpoint, or reconciliation processing fails",
        "since": "2026-07-28",
        "then": "the command emits an incomplete receipt with the last completed and active source position and the exact failure class and reason"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_failure_is_receipted"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the source-native EDCM pass reconciles the admitted archive",
        "since": "2026-07-31",
        "then": "completion also requires a UCNS v0.14.1 execution-generated receipt whose exhausted turn count and independently repeated exact-turn chain match the source-native pass"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "privacy",
        "given": "a run succeeds or fails",
        "since": "2026-07-28",
        "then": "written reports, receipts, and checkpoints contain aggregates and identities but no source turn text"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "multiwoz21_written_outputs_exclude_raw_text"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "UCNSFullCorpusGate, _archive_identity, _load_partition_ids, _load_pinned_runtime, _verify_git_tree, _git_commit, _git_tree_identity, _iter_ucns_full_corpus_turns, _new_state, _ordered_token_records, _space_shape, _observe_dialogue, _build_report, _build_receipt, _write_json_atomic, _sealed_worker_arguments, _sealed_main",
        "module_kind": "adapter",
        "module_name": "multiwoz21",
        "network_boundary": "none; source acquisition is separate and the runner requires local pinned bytes",
        "owner": "Erin Spencer",
        "public_surface": "AdmissionManifest, CorpusRunError, load_admission_manifest, iter_top_level_object, run_archive",
        "requires": "edcm_ucns_adapter, ucns.edcm and ucns.full_corpus at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97",
        "rollback": "remove the adapter and supersede its aggregate receipts by identity; raw source remains outside Git",
        "rollout": "explicit admitted full-corpus command; no sampling and no default measurement or canon selection",
        "since": "2026-07-28",
        "storage_boundary": "reads a caller-held archive and writes only caller-selected aggregate report, receipt, and resumable checkpoint paths",
        "summary": "verifies, streams, and reconciles every exact MultiWOZ 2.1 speaker turn through the pinned EDCM UCNS word-gonol profile and v0.14.1 completion gate from the merged v0.19 producer with final integrity repairs without committing raw text",
        "tests": "tests.test_multiwoz21_corpus",
        "unresolved": "source-native semantic labels for correction, retraction, and unresolved reference; formal UCNS geometry and lawful EDCM projection",
        "user_data_boundary": "exact dialogue text is processed in memory and represented only by counts and cryptographic identities in written outputs"
      },
      "file": "edcm/corpora/multiwoz21.py",
      "id": "edcm_multiwoz21_corpus"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "admitted development, validation, and test outcome events",
        "since": "2026-08-02",
        "then": "development alone fits the Platt map, validation alone selects the threshold, and the frozen calibration digest exists before test evaluation"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_calibration_precedes_test"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a caller-held source archive plus report and receipt destinations including their atomic temporary paths and existing filesystem aliases",
        "since": "2026-08-03",
        "then": "any cross-artifact or artifact-to-archive collision fails before archive evaluation or artifact writes begin"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_destinations_do_not_collide"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a frozen sensitivity, specificity, discrimination, or calibration hypothesis is not met",
        "since": "2026-08-02",
        "then": "the report records a falsified finding without converting that scientific result into an execution failure"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_hypothesis_failure_is_evidence"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a source dialogue-act turn contains exactly one admitted booking outcome label",
        "since": "2026-08-02",
        "then": "candidate measurement consumes only exact preceding data.json turns and never the labelled system response, later text, labels, goals, metadata, ontology, or databases"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_labelled_response_is_withheld"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "one holdout execution renders its aggregate report deterministically",
        "since": "2026-08-03",
        "then": "the complete-run repeat hypothesis remains not-evaluated until evidence from a separate complete execution is compared outside that single run"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_repeat_requires_complete_execution"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "privacy",
        "given": "the holdout run completes or fails",
        "since": "2026-08-02",
        "then": "written report and receipt contain aggregate counts, metrics, boundaries, and identities but no dialogue ids, source turns, normalized turns, per-event scores, or slot values"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_report_is_aggregate_only"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a caller supplies a clean EDCM repository and expected producer commit",
        "since": "2026-08-03",
        "then": "every loaded experiment and score-affecting measurement module and helper binding is inside one runtime package tree, one authenticated in-memory canon is used throughout scoring, and the runtime bytes match the recorded commit before canon load and after scoring"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_runtime_matches_recorded_checkout"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the admitted archive, exact UCNS represented-evidence seal, and candidate EDCM report reconcile",
        "since": "2026-08-02",
        "then": "canon selection remains null, formal geometry and higher-gonol composition remain NA, production activation remains inactive, and proof, theorem, measurement-validity, semantic-authority, certification, and empirical status do not transfer"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_status_does_not_transfer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "repeated source outcome events may share one dialogue",
        "since": "2026-08-02",
        "then": "sensitivity and specificity carry Wilson intervals while balanced accuracy, Brier score, and ECE carry deterministic dialogue-cluster bootstrap intervals"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "multiwoz_booking_outcome_uncertainty_is_cluster_aware"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_bootstrap_intervals, _build_report, _candidate_score, _confusion, _ece10, _extract_partition, _require_distinct_output_destinations, _verify_represented_evidence_seal, _verify_runtime_checkout, _wilson_interval",
        "module_kind": "experiment",
        "module_name": "multiwoz21_booking_holdout",
        "network_boundary": "none; source acquisition and publication are separate",
        "owner": "Erin Spencer",
        "public_surface": "OutcomeEvent, PlattCalibration, fit_platt_calibration, select_operating_threshold, evaluate_outcomes, run_holdout, main",
        "requires": "edcm_multiwoz21_corpus, edcmbone_parser_turns_rounds, edcmbone_metrics_compute, ucns.profile.edcm-word-gonol at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97",
        "rollback": "remove the experiment module and supersede its aggregate evidence by identity; raw source remains outside Git",
        "rollout": "explicit sealed experiment command only; no default measurement, production activation, or canon selection",
        "since": "2026-08-02",
        "storage_boundary": "reads a caller-held admitted archive plus tracked represented-evidence seals and writes caller-selected aggregate report and receipt paths",
        "summary": "evaluates the maintained EDCM terminal-progress candidate against externally authored MultiWOZ 2.1 booking outcome events after development calibration and validation threshold freeze",
        "tests": "tests.test_multiwoz21_booking_holdout",
        "unresolved": "externally hidden holdout custody, independent human task-success adjudication, formal higher-gonol composition, independent replication, and joint canon authority",
        "user_data_boundary": "exact source turns and dialogue ids are processed in memory but written outputs contain only aggregates and cryptographic chains"
      },
      "file": "edcm/corpora/multiwoz21_booking_holdout.py",
      "id": "edcm_multiwoz21_booking_outcome_holdout"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "directly executed source is the bootstrap trust root and the child admits only the exact archived edcm tree",
        "internal_surface": "_git_environment, _option_value, _pop_repository_root, _write_bootstrap_failure, _extract_source_only",
        "module_kind": "adapter",
        "module_name": "run_multiwoz21_seal",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "main",
        "requires": "git, python3, edcm_multiwoz21_corpus",
        "rollback": "remove the launcher and supersede evidence produced by its edcm tree identity",
        "rollout": "invoke this source file directly from a clean repository checkout",
        "since": "2026-08-01",
        "storage_boundary": "reads a caller-held archive and writes only caller-selected aggregate, receipt, and checkpoint paths",
        "summary": "establishes a cache-independent replacement-disabled Git snapshot before importing the sealed MultiWOZ runner",
        "tests": "tests.test_multiwoz21_corpus",
        "unresolved": "the host Python interpreter and Git executable remain external trust roots",
        "user_data_boundary": "does not inspect dialogue text; the isolated runner owns in-memory source processing"
      },
      "file": "edcm/corpora/run_multiwoz21_seal.py",
      "id": "edcm_multiwoz21_seal_launcher"
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
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a goal component has not received an explicit fixture claim",
        "since": "2026-08-02",
        "then": "its state is serialized as NA with no sign or magnitude and scalar projections retain a separate NA count"
      },
      "file": "edcm/goal_vector_experiment.py",
      "id": "edcm_goal_vector_na_not_zero"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the controlled candidate emits a contradiction ledger and goal-motion variance",
        "since": "2026-08-02",
        "then": "formal geometry, formal completion, empirical validity, METAPAT attachment, proof transfer, and canon selection remain absent or false"
      },
      "file": "edcm/goal_vector_experiment.py",
      "id": "edcm_goal_vector_no_status_transfer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the fixed resolved and active-contradiction cases contain the same source occurrences in different orders",
        "since": "2026-08-02",
        "then": "occurrence multiset identity agrees while ordered identity, exact UCNS observation identity, terminal contradiction state, and candidate trajectory remain independently visible"
      },
      "file": "edcm/goal_vector_experiment.py",
      "id": "edcm_goal_vector_same_occurrences_preserve_order"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canonical_bytes, _digest, _fraction_record, _variance, _state_snapshot, _verify_requested_ucns_source_root, _observe_case, _evaluate_findings",
        "module_kind": "experiment",
        "module_name": "goal_vector_experiment",
        "network_boundary": "none; exact UCNS producer must already be installed",
        "owner": "Erin Spencer",
        "public_surface": "GoalDimension, DeclaredGoal, GoalClaim, SourceOccurrence, GoalVectorCase, GoalVectorExperimentReport, build_goal_vector_program, evaluate_case, run_goal_vector_experiment, main",
        "requires": "edcm_ucns_adapter",
        "rollback": "remove this module, its test, workflow invocation, design note, and versioned evidence without changing the frozen measurement baseline",
        "rollout": "explicit controlled candidate experiment; no default activation or canon selection",
        "since": "2026-08-02",
        "storage_boundary": "writes only caller-selected report path",
        "summary": "runs a controlled same-occurrences/different-order contradiction experiment through the exact current UCNS observation profile and an inspectable EDCM goal-state candidate",
        "tests": "tests/test_goal_vector_experiment.py",
        "unresolved": "independent semantic annotation, real-dialogue goal authority, formal higher-gonol composition, calibration, holdout replication, and human outcome validation",
        "user_data_boundary": "fixed synthetic utterances only"
      },
      "file": "edcm/goal_vector_experiment.py",
      "id": "edcm_goal_vector_experiment"
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
        "auth_boundary": "exact OEWN and UCNS producer commits",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "language",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "source, affix, rendering, morphology, model, manifest, and relational-bridge names listed in __all__",
        "requires": "edcm_language_manifest, edcm_language_model, edcm_language_oewn_source, edcm_language_affixes, edcm_language_rendering, edcm_language_morphology, edcm_language_relational_bridge",
        "rollback": "remove relational bridge while retaining EDCM evidence modules",
        "rollout": "explicit lexical-floor construction; no measurement or higher-language activation",
        "since": "2026-08-16",
        "storage_boundary": "caller-selected lexical artifact directory",
        "summary": "exposes exact OEWN evidence, reversible lexical candidates, and independent EDCM-to-UCNS relational branch construction without EDCM-owned geometry",
        "tests": "tests.test_language_full_run, tests.test_language_relational_bridge",
        "unresolved": "UCNS geometry and higher-gonol composition remain absent; lexical decomposition remains dictionary-and-inventory bounded evidence",
        "user_data_boundary": "public licensed lexical evidence only"
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
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the English lexical-floor manifest is inspected",
        "since": "2026-08-16",
        "then": "EDCM owns English evidence, UCNS owns representation, and geometry, proof, measurement, empirical, and canon transfer remain false"
      },
      "file": "edcm/language/manifest.py",
      "id": "lexical_manifest_preserves_authority_firewall"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "exact producer commits",
        "internal_surface": "none",
        "module_kind": "policy",
        "module_name": "manifest",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EnglishEmbeddingManifest, embedding_manifest, SOURCE_DICTIONARY",
        "requires": "edcm_language_oewn_source, ucns_relational_carrier",
        "rollback": "restore fail-closed bridge state without restoring retired placement",
        "rollout": "active lexical-floor bridge",
        "since": "2026-08-16",
        "storage_boundary": "none",
        "summary": "pins OEWN evidence and the exact UCNS relational producer while forbidding geometry and status transfer",
        "tests": "tests.test_language_relational_bridge",
        "unresolved": "geometry, canonical English decomposition, measurement validity, and producer signatures",
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
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a branch comparison is requested",
        "since": "2026-08-16",
        "then": "both immutable branch files and their recorded digests are validated before any comparison is emitted"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "comparison_requires_two_prior_freezes"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "either branch is frozen",
        "since": "2026-08-16",
        "then": "English labels and provenance appear only in the external binding while intrinsic bytes are produced by the pinned UCNS carrier API"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "english_metadata_is_external_to_ucns_carrier"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "direct-atomic and molecular branch builders run",
        "since": "2026-08-16",
        "then": "the direct builder consumes only OEWN lexical and semantic evidence while the molecular builder independently consumes surfaces, declared affixes, and reversible decompositions"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "lexical_branches_are_independently_constructed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "one branch freeze or within-run branch comparison completes",
        "since": "2026-08-16",
        "then": "its status is UNRESOLVED until a separately recorded clean independent replay agrees byte-for-byte"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "lexical_pre_replay_status_is_unresolved"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "direct semantic evidence or molecular alternatives contain repeated relation occurrences",
        "since": "2026-08-16",
        "then": "every occurrence remains in supplied order in the UCNS relational input without deduplication"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "lexical_relation_multiplicity_is_preserved"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "EDCM opens the UCNS relational construction API",
        "since": "2026-08-16",
        "then": "the checkout HEAD equals the merged producer commit and the imported producer module is the exact source-root file whose bytes match the verification receipt"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "lexical_ucns_producer_is_exactly_verified"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "exact UCNS producer commit is pinned by package profile and work-graph artifact",
        "internal_surface": "_ucns_api, _digest, _relation_codes, _git",
        "module_kind": "adapter",
        "module_name": "relational_bridge",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNS_RELATIONAL_COMMIT, UCNSProducerVerification, DirectAtomicFreeze, MolecularFreeze, verify_ucns_producer, build_direct_atomic, build_molecular, freeze_branch, validate_frozen_branch, compare_frozen_branches, canonical_json_bytes",
        "requires": "ucns_relational_carrier, edcm_language_oewn_source, edcm_language_affixes, edcm_language_morphology",
        "rollback": "remove adapter and generated lexical artifacts while preserving source evidence modules",
        "rollout": "explicit lexical-floor builder; no geometry, measurement, canon, or higher-language activation",
        "since": "2026-08-16",
        "storage_boundary": "writes caller-selected frozen artifacts only",
        "summary": "independently constructs direct-atomic and molecular OEWN relation inputs for the UCNS metadata-free relational carrier and freezes external identity bindings before comparison",
        "tests": "tests.test_language_relational_bridge",
        "unresolved": "geometric placement, canonical English morphology, closed compounds, pronunciation, phrase and higher semantics",
        "user_data_boundary": "OEWN evidence remains in external bindings and never enters intrinsic UCNS bytes"
      },
      "file": "edcm/language/relational_bridge.py",
      "id": "edcm_language_relational_bridge"
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
        "public_surface": "LayerProvenance, MeasurementLayer, SemanticsLayer, CompositionLayer, DeliveryLayer, DefaultMeasurementLayer, DefaultCompositionLayer, DefaultDeliveryLayer, MissingMetapatSemanticAuthorityLayer, MetapatSemanticAuthorityLayer, MissingUCNSProfileLayer, UCNSProfileLayer, CompositeSemanticsLayer, ConsolidatedMeasurementLayer, SharedStackCompositionLayer, SharedStackDeliveryLayer, EDCMLayers, build_default_layers",
        "requires": "edcm_metapat_adapter, edcm_ucns_adapter, edcm_measurement, edcm_shared_stack",
        "rollback": "restore prior layer assembly and remove shared-stack result delivery",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Provenance-bearing EDCM stack with independently selected METAPAT semantic authority, exact UCNS word-gonol observation profile or typed absence, canonical local measurement, shared-stack composition, and final result-contract delivery.",
        "tests": "tests.test_measurement, tests.test_ucns_adapter, tests.test_metapat_adapter, tests.test_shared_stack_contract",
        "unresolved": "formal Mobius coordinates and higher-gonol composition remain unattached; profile observations do not supply geometry, factorization, or theorem status",
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
        "rollback": "remove the profile-observation compartment and restore the prior result schema only with a versioned migration",
        "rollout": "default_enabled",
        "since": "2026-07-12",
        "storage_boundary": "no persistence; emits deterministic JSON-compatible records",
        "summary": "deterministic final EDCM result contract separating source evidence, METAPAT semantic authority, exact UCNS word-gonol observations, typed UCNS geometry and factorization absence, EDCM policy identity, implementation provenance, readouts/NA, unresolved constraints, and attachment states.",
        "tests": "tests.test_shared_stack_contract, tests.test_ucns_adapter",
        "unresolved": "UCNS observation digests provide content identity but not signed producer authentication; profile observations do not supply formal geometry",
        "user_data_boundary": "hashes caller transcript content and preserves caller source reference without external transmission"
      },
      "file": "edcm/shared_stack.py",
      "id": "edcm_shared_stack"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "an importable UCNS package is considered for activation",
        "since": "2026-07-25",
        "then": "checkout package bytes match the pinned Git tree or installed package bytes match the EDCM-pinned producer manifest plus raw RECORD as applicable, the verified UCNS module graph is freshly loaded, every runtime-loadable cached bytecode file derives from its verified source, and any producer-owned commit identity plus every profile identity, option, Unicode-scalar source domain, 25-value SPACE pin, public-alphabet invariant, and producer type match the pinned EDCM word-gonol surface or the adapter remains suspended"
      },
      "file": "edcm/ucns_adapter.py",
      "id": "edcm_ucns_exact_profile_only"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "ordered ucns_turns enter the active adapter",
        "since": "2026-07-25",
        "then": "all turns are observed in order with exact Unicode source witnesses, one unit of support per speaker turn, explicit origin-assigned SPACE boundaries, and retained non-SPACE out-of-alphabet evidence"
      },
      "file": "edcm/ucns_adapter.py",
      "id": "edcm_ucns_full_turn_observation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "exact profile observations are attached",
        "since": "2026-07-25",
        "then": "geometry, factorization, theorem, certification, and measurement-validity attachment flags remain false"
      },
      "file": "edcm/ucns_adapter.py",
      "id": "edcm_ucns_no_geometry_or_proof_transfer"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canonical_bytes, _digest, _package_present, _run_git, _verify_checkout_package_tree, _source_checkout_commit, _code_semantic_identity, _is_runtime_cache, _verify_cached_bytecode, _verify_active_source_caches, _verify_pinned_package_tree, _verify_distribution_files, _reload_verified_ucns_module, _resolve_ucns_producer, _token_record, _segment_record, _turn_record",
        "module_kind": "adapter",
        "module_name": "ucns_adapter",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ActualUCNSAdapter, UCNSProfileObservationEvidence, UCNSIntegrationStatus, UCNSAdapterSelection, select_ucns_adapter, inspect_ucns_adapter",
        "requires": "ucns.edcm at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97",
        "rollback": "suspend the optional adapter; base EDCM measurement remains operational",
        "rollout": "optional exact-profile activation only when the pinned producer commit and profile surface match",
        "since": "2026-07-25",
        "storage_boundary": "none",
        "summary": "fail-closed consumer for the exact EDCM-only UCNS word-gonol profile from the merged v0.19 producer with final integrity repairs, preserving full-corpus speaker-turn observations without coordinate, geometry, or proof transfer",
        "tests": "tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_shared_stack_contract",
        "unresolved": "consumption of the upstream nonselected ordered source-coordinate candidate, higher-gonol composition, and projection policies remain outside this observation adapter",
        "user_data_boundary": "exact source turns remain in caller-owned in-memory results and are not transmitted"
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
        "public_surface": "INSTALL_HINT, require_ucns, ucns_available, ucns_dependency_report",
        "requires": "edcm_ucns_adapter",
        "rollback": "report typed dependency absence while base EDCM remains operational",
        "rollout": "optional dependency diagnostic",
        "since": "2026-07-25",
        "storage_boundary": "none",
        "summary": "diagnostics and fail-closed loading for the optional exact EDCM UCNS word-gonol profile",
        "tests": "tests.test_ucns_dependency",
        "unresolved": "installed package provenance is enforced by the exact optional-dependency pin and profile invariants rather than a signed runtime attestation",
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
        "internal_surface": "_candidate_targets, _apply_edges, _graph_view, _build_ucns_graph_envelope, _resolution_values, _pair_findings",
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
        "call": "self::test_resolved_and_active_contradictions_have_exact_candidate_variances",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_goal_vector_same_occurrences_preserve_order",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_goal_vector_experiment.py",
      "id": "check_goal_vector_contradiction_and_variance"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_exact_ucns_report_is_deterministic_and_no_canon",
        "cleanup": "pytest tmp_path",
        "mutates": "temporary report only",
        "proves": "edcm_goal_vector_same_occurrences_preserve_order, edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_goal_vector_experiment.py",
      "id": "check_goal_vector_exact_ucns_report"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_na_is_typed_and_nonclaims_remain_absent",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_goal_vector_experiment.py",
      "id": "check_goal_vector_na_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_same_occurrences_different_order_preserve_distinct_trajectories",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_goal_vector_same_occurrences_preserve_order",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_goal_vector_experiment.py",
      "id": "check_goal_vector_same_occurrences_order"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sealed_goal_vector_evidence_matches_exact_producer",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_goal_vector_same_occurrences_preserve_order, edcm_goal_vector_na_not_zero, edcm_goal_vector_no_status_transfer",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_goal_vector_experiment.py",
      "id": "check_goal_vector_sealed_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_independent_branches_freeze_before_comparison",
        "cleanup": "pytest tmp_path",
        "mutates": "tmp_path only",
        "proves": "lexical_branches_are_independently_constructed, english_metadata_is_external_to_ucns_carrier, lexical_ucns_producer_is_exactly_verified, lexical_relation_multiplicity_is_preserved, lexical_pre_replay_status_is_unresolved, comparison_requires_two_prior_freezes, lexical_manifest_preserves_authority_firewall",
        "timeout": "30"
      },
      "file": "tests/test_language_relational_bridge.py",
      "id": "language_relational_branch_check"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_builder_contract_is_pinned_and_freeze_order_is_explicit",
        "cleanup": "none",
        "mutates": "none",
        "proves": "oewn_source_is_exact_pinned_and_resumable, incomplete_or_altered_lexical_resume_fails_closed, lexical_comparison_occurs_after_freeze",
        "timeout": "30"
      },
      "file": "tests/test_language_relational_bridge.py",
      "id": "oewn_builder_order_check"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_calibration_and_threshold_depend_only_on_development_and_validation",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_calibration_precedes_test",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_calibration_precedes_test"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_output_destinations_reject_aliases_before_any_write",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_destinations_do_not_collide",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_destinations_do_not_collide"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_falsified_finding_is_serialized_without_raising",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_hypothesis_failure_is_evidence",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_source_outcome_response_and_later_turns_are_withheld",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_labelled_response_is_withheld",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_labelled_response_is_withheld"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_single_run_leaves_complete_repeat_not_evaluated",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_repeat_requires_complete_execution",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_repeat_requires_complete_execution"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_report_schema_retains_aggregate_boundaries_without_event_locators",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_report_is_aggregate_only",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_report_is_aggregate_only"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_runtime_binding_rejects_a_foreign_score_helper",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_runtime_matches_recorded_checkout",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sealed_holdout_evidence_matches_exact_producer_and_receipt",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_calibration_precedes_test, multiwoz_booking_outcome_report_is_aggregate_only, multiwoz_booking_outcome_hypothesis_failure_is_evidence, multiwoz_booking_outcome_status_does_not_transfer",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_sealed_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_report_schema_retains_aggregate_boundaries_without_event_locators",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_status_does_not_transfer",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_status_does_not_transfer"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_evaluation_reports_confusion_wilson_and_cluster_intervals",
        "cleanup": "none",
        "mutates": "none",
        "proves": "multiwoz_booking_outcome_uncertainty_is_cluster_aware",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_booking_holdout.py",
      "id": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_archive_mutation_fails_before_dialogue_observation",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_admission_precedes_execution",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_admission_precedes_execution"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_manifest_count_mismatch_refuses_completion",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_completion_requires_reconciliation",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_completion_requires_reconciliation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_every_turn_is_observed_exactly_once",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_every_turn_is_observed_exactly_once"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_invalid_turn_reports_exact_active_source_position",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_failure_is_receipted",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_failure_is_receipted"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_claimed_gate_without_source_exhaustion_cannot_complete",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_ucns_v0141_false_receipt_rejected"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_report_and_checkpoint_exclude_source_turn_text",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "multiwoz21_written_outputs_exclude_raw_text",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_multiwoz21_corpus.py",
      "id": "check_multiwoz21_written_outputs_exclude_raw_text"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_manifest_rejects_auto_fetch_without_public_domain_rights",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_acquisition_fetches_only_authorized_public_domain_bytes",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_corpus_acquisition.py",
      "id": "check_tarot_auto_fetch_rights_gate"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_completed_resume_reuses_exact_state_and_rejects_tamper",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_acquisition_resume_fails_closed",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_corpus_acquisition.py",
      "id": "check_tarot_completed_resume_fails_closed"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_acquisition_fetches_only_public_domain_and_seals_source_identity",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_acquisition_fetches_only_authorized_public_domain_bytes, tarot_metadata_only_sources_are_not_downloaded, tarot_acquisition_preserves_source_identity",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_corpus_acquisition.py",
      "id": "check_tarot_fetch_authority_and_metadata_only_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_interrupted_resume_keeps_verified_completed_sources",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_acquisition_resume_fails_closed, tarot_acquisition_preserves_source_identity",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_corpus_acquisition.py",
      "id": "check_tarot_interrupted_resume_checkpoint"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_committed_manifest_validates_without_tarot_ontology",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_manifest_preserves_preontology_boundary",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_corpus_acquisition.py",
      "id": "check_tarot_manifest_preserves_preontology_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_normalization_distance_and_empty_page_rule",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v4_applies_frozen_accuracy_rule"
      },
      "file": "tests/test_tarot_ocr_v4.py",
      "id": "check_tarot_ocr_v4_accuracy"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_canonical_serialization_is_byte_deterministic",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v4_serialization_is_deterministic"
      },
      "file": "tests/test_tarot_ocr_v4.py",
      "id": "check_tarot_ocr_v4_determinism"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_frozen_identity_constants_and_record_verification",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_ocr_v4_verifies_every_frozen_identity, tarot_ocr_v4_resume_fails_closed"
      },
      "file": "tests/test_tarot_ocr_v4.py",
      "id": "check_tarot_ocr_v4_identity_and_resume"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_record_preserves_hashes_confidence_and_page_identity",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_ocr_v4_preserves_raw_page_evidence"
      },
      "file": "tests/test_tarot_ocr_v4.py",
      "id": "check_tarot_ocr_v4_raw_evidence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v5_protocol_and_instrument_identities_are_frozen",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v5_retains_v4_evidence_contracts"
      },
      "file": "tests/test_tarot_ocr_v5.py",
      "id": "check_tarot_ocr_v5_core_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v5_ocr_command_is_exact_single_threshold_change",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v5_changes_only_frozen_thresholding"
      },
      "file": "tests/test_tarot_ocr_v5.py",
      "id": "check_tarot_ocr_v5_single_change"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v6_protocol_and_instrument_identities_are_frozen",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v6_retains_v4_evidence_contracts"
      },
      "file": "tests/test_tarot_ocr_v6.py",
      "id": "check_tarot_ocr_v6_core_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v6_model_verification_fails_closed",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_ocr_v6_verifies_historic_model"
      },
      "file": "tests/test_tarot_ocr_v6.py",
      "id": "check_tarot_ocr_v6_model_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_v6_ocr_command_is_exact_model_change",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_ocr_v6_changes_only_frozen_model"
      },
      "file": "tests/test_tarot_ocr_v6.py",
      "id": "check_tarot_ocr_v6_single_change"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_frozen_thresholds_accept_only_adequate_pages",
        "cleanup": "none",
        "mutates": "none",
        "proves": "tarot_text_gate_applies_frozen_adequacy_rule, tarot_text_gate_retains_nonclaims_and_failure",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_pdf_text_layer_gate.py",
      "id": "check_tarot_text_gate_frozen_thresholds"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_discovery_requires_sealed_acquisition_and_is_byte_deterministic",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_discovery_consumes_only_complete_sealed_acquisition, tarot_discovery_is_byte_deterministic",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_relation_discovery.py",
      "id": "check_tarot_discovery_complete_acquisition_and_determinism"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_documented_direct_cli_executes",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_discovery_is_byte_deterministic",
        "requires": "python3, posix_shell",
        "timeout": "20"
      },
      "file": "tests/test_tarot_relation_discovery.py",
      "id": "check_tarot_discovery_documented_cli"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_discovery_preserves_order_exact_values_and_typed_absence",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_discovery_preserves_exact_source_order_and_values, tarot_discovery_preserves_typed_absence_and_nonclaims",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_relation_discovery.py",
      "id": "check_tarot_discovery_exact_order_values_and_absence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_discovery_emits_only_frozen_relations_and_enforces_bounds",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "tarot_discovery_relations_are_mechanical_and_bounded",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_tarot_relation_discovery.py",
      "id": "check_tarot_discovery_mechanical_bounds"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_exact_profile_activates_and_option_drift_suspends",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_exact_profile_only"
      },
      "file": "tests/test_ucns_adapter.py",
      "id": "check_edcm_ucns_exact_profile_only"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_full_turn_observation"
      },
      "file": "tests/test_ucns_adapter.py",
      "id": "check_edcm_ucns_full_turn_observation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_live_profile_attaches_observation_without_geometry_or_proof_transfer",
        "cleanup": "none",
        "mutates": "none",
        "proves": "edcm_ucns_no_geometry_or_proof_transfer"
      },
      "file": "tests/test_ucns_adapter.py",
      "id": "check_edcm_ucns_no_geometry_or_proof_transfer"
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
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a source requests automatic byte acquisition",
        "since": "2026-08-16",
        "then": "the source must declare an HTTPS content URL, a safe artifact name, expected media type, and public-domain or Public Domain Mark rights before any network request occurs"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "tarot_acquisition_fetches_only_authorized_public_domain_bytes"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a Tarot source is admitted to an acquisition run",
        "since": "2026-08-16",
        "then": "its exact manifest entry digest, locator, retrieval policy, rights state, and any fetched byte digest are recorded without semantic normalization"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "tarot_acquisition_preserves_source_identity"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a completed or interrupted Tarot acquisition is resumed",
        "since": "2026-08-16",
        "then": "manifest identity, checkpoint entries, byte digests, and the exact output file set are validated; altered, missing, stale, or injected state is rejected"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "tarot_acquisition_resume_fails_closed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a Tarot corpus manifest is loaded",
        "since": "2026-08-16",
        "then": "only the frozen evidence-envelope schema is accepted and ontology, canonical-deck, canonical-card-count, cross-source card identity, and I Ching inclusion remain explicitly unselected"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "tarot_manifest_preserves_preontology_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a source is metadata_only or manual_review",
        "since": "2026-08-16",
        "then": "no content request is issued and the source remains a provenance-bearing locator in the evidence index"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "tarot_metadata_only_sources_are_not_downloaded"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_fetch_https, _write_checkpoint, _validate_completed_run, _canonical_bytes",
        "module_kind": "instrument",
        "module_name": "tarot_corpus_acquirer",
        "network_boundary": "external",
        "owner": "Erin Spencer",
        "public_surface": "validate_manifest, acquire_manifest, main",
        "requires": "none",
        "rollback": "remove this tool and its corpus/artifact documentation; generated artifacts are reproducible caches and remain noncanonical",
        "rollout": "explicit CLI only; no automatic embedding or corpus download",
        "since": "2026-08-16",
        "storage_boundary": "write",
        "summary": "validates a provenance-only Tarot source manifest, acquires only explicitly authorized public-domain bytes, and seals deterministic evidence receipts without defining Tarot ontology",
        "tests": "tests.test_tarot_corpus_acquisition",
        "unresolved": "source-specific item licensing and child-object identities beyond pinned public-domain downloads; OCR, transcription, semantic extraction, and EDCM embedding remain separate stages",
        "user_data_boundary": "none; public cultural and archival evidence only"
      },
      "file": "tools/acquire_tarot_corpus.py",
      "id": "edcm_tarot_corpus_acquirer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "resume state is partial, noncanonical, stale, producer-mismatched, status-promoted, missing, or digest-altered",
        "since": "2026-08-16",
        "then": "no completed run is reused and altered complete state raises an explicit error"
      },
      "file": "tools/build_oewn2025_embeddings.py",
      "id": "incomplete_or_altered_lexical_resume_fails_closed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a complete lexical-floor build runs",
        "since": "2026-08-16",
        "then": "direct and molecular artifacts are written and receipted before the comparison function reads them"
      },
      "file": "tools/build_oewn2025_embeddings.py",
      "id": "lexical_comparison_occurs_after_freeze"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the lexical-floor builder consumes or acquires OEWN",
        "since": "2026-08-16",
        "then": "exact repository commit, tag, counts, tree digest, license, and provenance are frozen and a complete run may be reused only after every listed artifact, branch, producer, status, and comparison identity validates"
      },
      "file": "tools/build_oewn2025_embeddings.py",
      "id": "oewn_source_is_exact_pinned_and_resumable"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "verifies exact OEWN and UCNS commits",
        "internal_surface": "_git, _acquire, _source_manifest",
        "module_kind": "instrument",
        "module_name": "build_oewn2025_embeddings",
        "network_boundary": "git clone only when --acquire is explicitly supplied",
        "owner": "Erin Spencer",
        "public_surface": "command line, build",
        "requires": "edcm_language_relational_bridge",
        "rollback": "remove builder and generated artifacts",
        "rollout": "explicit builder",
        "since": "2026-08-16",
        "storage_boundary": "caller-selected cache and output directories",
        "summary": "acquires or verifies the pinned OEWN source and independently freezes direct-atomic and molecular UCNS relational artifacts before comparison",
        "tests": "tests.test_language_relational_bridge",
        "unresolved": "upstream cryptographic signatures are unavailable; Git and tree digests are identity, not authentication",
        "user_data_boundary": "public licensed lexical evidence only"
      },
      "file": "tools/build_oewn2025_embeddings.py",
      "id": "edcm_oewn2025_lexical_floor_builder"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "Tarot relation discovery is requested",
        "since": "2026-08-16",
        "then": "the exact acquisition receipt, manifest identities, evidence index digest, every listed artifact digest, and complete file set validate before discovery"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "tarot_discovery_consumes_only_complete_sealed_acquisition"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the same validated acquisition and frozen algorithm identity are processed twice",
        "since": "2026-08-16",
        "then": "canonical report bytes are identical"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "tarot_discovery_is_byte_deterministic"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a validated evidence index is discovered",
        "since": "2026-08-16",
        "then": "every source remains in manifest order and every admitted field value remains exact without case folding, tokenization, OCR, or semantic normalization"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "tarot_discovery_preserves_exact_source_order_and_values"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a source field is absent or the report completes",
        "since": "2026-08-16",
        "then": "absence remains explicit and the report selects no ontology, card identity, geometry, measurement, or canon"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "tarot_discovery_preserves_typed_absence_and_nonclaims"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "source-envelope relations are emitted",
        "since": "2026-08-16",
        "then": "relations are limited to ordered adjacency, exact field assertions, fetched-artifact binding, and same-field exact-value agreement within declared resource bounds"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "tarot_discovery_relations_are_mechanical_and_bounded"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_canonical_bytes, _digest, _value_identity, _load_validated_acquisition",
        "module_kind": "instrument",
        "module_name": "tarot_relation_discovery",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "discover_relations, validate_discovery, main",
        "requires": "edcm_tarot_corpus_acquirer",
        "rollback": "remove this tool, its tests, docs, and generated discovery reports without altering acquisition evidence",
        "rollout": "explicit CLI after a complete tarot corpus acquisition; no automatic UCNS or EDCM measurement activation",
        "since": "2026-08-16",
        "storage_boundary": "read sealed acquisition and write one caller-selected report",
        "summary": "validates a sealed Tarot acquisition and discovers only ordered source-envelope assertions and exact-value agreements without selecting Tarot ontology",
        "tests": "tests.test_tarot_relation_discovery",
        "unresolved": "OCR, image interpretation, cross-source card identity, semantic relation discovery, UCNS recursive representation, and EDCM measurement",
        "user_data_boundary": "none; public cultural and archival evidence only"
      },
      "file": "tools/discover_tarot_relations.py",
      "id": "edcm_tarot_relation_discovery"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "exact per-page text bytes are extracted",
        "since": "2026-08-16",
        "then": "only preregistered non-whitespace, alphanumeric, replacement, coverage, and total thresholds determine the verdict"
      },
      "file": "tools/evaluate_tarot_pdf_text_layer.py",
      "id": "tarot_text_gate_applies_frozen_adequacy_rule"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the gate completes or fails",
        "since": "2026-08-16",
        "then": "FALSIFIED, SURVIVED, or BLOCKED is recorded without OCR fallback, semantic inspection, ontology, geometry, measurement, or canon escalation"
      },
      "file": "tools/evaluate_tarot_pdf_text_layer.py",
      "id": "tarot_text_gate_retains_nonclaims_and_failure"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the embedded-text gate runs",
        "since": "2026-08-16",
        "then": "both PDF digests, page counts, MuPDF version, executable digest, command, and timeout match the preregistration"
      },
      "file": "tools/evaluate_tarot_pdf_text_layer.py",
      "id": "tarot_text_gate_uses_exact_frozen_inputs_and_backend"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_verify_backend, _extract_pages, _canonical_bytes",
        "module_kind": "experiment",
        "module_name": "tarot_pdf_text_layer_gate",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "evaluate_pages, run_gate, main",
        "requires": "edcm_tarot_corpus_acquirer",
        "rollback": "remove experiment tool, tests, reports, and protocol without changing source evidence",
        "rollout": "explicit CLI after frozen preregistration only",
        "since": "2026-08-16",
        "storage_boundary": "read exact acquired PDFs, temporary extracted pages, and one caller-selected report",
        "summary": "executes the frozen MuPDF embedded-text adequacy gate over the two exact acquired Wellcome PDFs without OCR or semantic inspection",
        "tests": "tests.test_tarot_pdf_text_layer_gate",
        "unresolved": "OCR backend and accuracy law if embedded text is insufficient",
        "user_data_boundary": "none; public-domain archival evidence only"
      },
      "file": "tools/evaluate_tarot_pdf_text_layer.py",
      "id": "edcm_tarot_pdf_text_layer_gate"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the sealed independent reference and complete OCR outputs",
        "then": "inherited normalization, CER/WER thresholds, replacement check, and exact-empty rule produce only FALSIFIED, UNRESOLVED, or BLOCKED for one run"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "tarot_ocr_v4_applies_frozen_accuracy_rule"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "an admitted PDF page",
        "then": "exact grayscale PNG, raw UTF-8 TXT, raw TSV, hashes, bytes, confidences, page identity, and typed unavailable alternatives are retained"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "tarot_ocr_v4_preserves_raw_page_evidence"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "an interrupted or completed output directory",
        "then": "only checkpoint-bound exact files are reused and any missing, injected, or changed file blocks continuation"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "tarot_ocr_v4_resume_fails_closed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "identical producer outputs and inputs",
        "then": "canonical manifest, checkpoint, and evaluation bytes are identical"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "tarot_ocr_v4_serialization_is_deterministic"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a protocol execution request",
        "then": "both PDFs, renderer, OCR executable, French model, versions, page counts, and reference bytes must match before a producer runs"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "tarot_ocr_v4_verifies_every_frozen_identity"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "producer verification, render/OCR execution, checkpoint verification, TSV reconstruction, CER/WER scoring",
        "module_kind": "experiment",
        "module_name": "tarot_ocr_v4_runner",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line interface",
        "requires": "edcm_tarot_corpus_acquirer",
        "rollback": "remove this runner without altering frozen protocol or result receipts",
        "rollout": "explicit CLI only after validation reference commit aed1cf7de3df80da104daf2b3c46246ff5c3fe39",
        "storage_boundary": "write",
        "summary": "executes the frozen Tarot OCR v4 protocol with exact producer identities, resumable raw outputs, deterministic manifests, and independent-reference scoring",
        "tests": "tests.test_tarot_ocr_v4",
        "user_data_boundary": "none"
      },
      "file": "tools/run_tarot_ocr_v4.py",
      "id": "edcm_tarot_ocr_v4_runner"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a v5 page OCR request",
        "then": "the exact v4 command gains only thresholding_method=2 and retains raw TXT/TSV evidence"
      },
      "file": "tools/run_tarot_ocr_v5.py",
      "id": "tarot_ocr_v5_changes_only_frozen_thresholding"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a complete or resumed v5 run",
        "then": "frozen identities, page evidence, validation, deterministic serialization, and fail-closed resume use the v4 core with v5 identities"
      },
      "file": "tools/run_tarot_ocr_v5.py",
      "id": "tarot_ocr_v5_retains_v4_evidence_contracts"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "frozen Sauvola OCR command and v4 resumable corpus core",
        "module_kind": "experiment",
        "module_name": "tarot_ocr_v5_runner",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line interface",
        "requires": "edcm_tarot_ocr_v4_runner",
        "rollback": "remove this adapter without altering v4 evidence or protocols",
        "rollout": "explicit CLI only after protocol commit 9199f2d",
        "storage_boundary": "write",
        "summary": "executes the frozen Tarot OCR v5 adaptive-threshold protocol through the v4 evidence-preserving core",
        "tests": "tests.test_tarot_ocr_v5",
        "user_data_boundary": "none"
      },
      "file": "tools/run_tarot_ocr_v5.py",
      "id": "edcm_tarot_ocr_v5_runner"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a v6 page OCR request",
        "then": "the v5 command replaces only the language model and model directory while retaining Sauvola, OEM, PSM, TXT, and TSV"
      },
      "file": "tools/run_tarot_ocr_v6.py",
      "id": "tarot_ocr_v6_changes_only_frozen_model"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a complete or resumed v6 run",
        "then": "frozen sources, page evidence, validation, serialization, resources, and fail-closed resume use the shared core with v6 identities"
      },
      "file": "tools/run_tarot_ocr_v6.py",
      "id": "tarot_ocr_v6_retains_v4_evidence_contracts"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a v6 execution request",
        "then": "the external model filename, byte count, and SHA-256 must match before any producer runs"
      },
      "file": "tools/run_tarot_ocr_v6.py",
      "id": "tarot_ocr_v6_verifies_historic_model"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "historic-model verification, frozen OCR command, and v4 resumable corpus core",
        "module_kind": "experiment",
        "module_name": "tarot_ocr_v6_runner",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line interface",
        "requires": "edcm_tarot_ocr_v4_runner",
        "rollback": "remove this adapter without altering earlier evidence or protocols",
        "rollout": "explicit CLI only after protocol commit c63ad40",
        "storage_boundary": "write",
        "summary": "executes the frozen Tarot OCR v6 historic-print model protocol through the v4 evidence-preserving core",
        "tests": "tests.test_tarot_ocr_v6",
        "user_data_boundary": "none"
      },
      "file": "tools/run_tarot_ocr_v6.py",
      "id": "edcm_tarot_ocr_v6_runner"
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
      "from": "check_edcm_ucns_exact_profile_only",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_exact_profile_only",
      "to": "self::test_exact_profile_activates_and_option_drift_suspends"
    },
    {
      "from": "check_edcm_ucns_exact_profile_only",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_exact_profile_only",
      "to": "edcm_ucns_exact_profile_only"
    },
    {
      "from": "check_edcm_ucns_full_turn_observation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_full_turn_observation",
      "to": "self::test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures"
    },
    {
      "from": "check_edcm_ucns_full_turn_observation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_full_turn_observation",
      "to": "edcm_ucns_full_turn_observation"
    },
    {
      "from": "check_edcm_ucns_no_geometry_or_proof_transfer",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_no_geometry_or_proof_transfer",
      "to": "self::test_live_profile_attaches_observation_without_geometry_or_proof_transfer"
    },
    {
      "from": "check_edcm_ucns_no_geometry_or_proof_transfer",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_edcm_ucns_no_geometry_or_proof_transfer",
      "to": "edcm_ucns_no_geometry_or_proof_transfer"
    },
    {
      "from": "check_goal_vector_contradiction_and_variance",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_contradiction_and_variance",
      "to": "self::test_resolved_and_active_contradictions_have_exact_candidate_variances"
    },
    {
      "from": "check_goal_vector_contradiction_and_variance",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_contradiction_and_variance",
      "to": "edcm_goal_vector_same_occurrences_preserve_order"
    },
    {
      "from": "check_goal_vector_contradiction_and_variance",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_contradiction_and_variance",
      "to": "python3"
    },
    {
      "from": "check_goal_vector_exact_ucns_report",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_exact_ucns_report",
      "to": "self::test_exact_ucns_report_is_deterministic_and_no_canon"
    },
    {
      "from": "check_goal_vector_exact_ucns_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_exact_ucns_report",
      "to": "edcm_goal_vector_na_not_zero"
    },
    {
      "from": "check_goal_vector_exact_ucns_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_exact_ucns_report",
      "to": "edcm_goal_vector_no_status_transfer"
    },
    {
      "from": "check_goal_vector_exact_ucns_report",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_exact_ucns_report",
      "to": "edcm_goal_vector_same_occurrences_preserve_order"
    },
    {
      "from": "check_goal_vector_exact_ucns_report",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_exact_ucns_report",
      "to": "python3"
    },
    {
      "from": "check_goal_vector_na_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_na_boundary",
      "to": "self::test_na_is_typed_and_nonclaims_remain_absent"
    },
    {
      "from": "check_goal_vector_na_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_na_boundary",
      "to": "edcm_goal_vector_na_not_zero"
    },
    {
      "from": "check_goal_vector_na_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_na_boundary",
      "to": "edcm_goal_vector_no_status_transfer"
    },
    {
      "from": "check_goal_vector_na_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_na_boundary",
      "to": "python3"
    },
    {
      "from": "check_goal_vector_same_occurrences_order",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_same_occurrences_order",
      "to": "self::test_same_occurrences_different_order_preserve_distinct_trajectories"
    },
    {
      "from": "check_goal_vector_same_occurrences_order",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_same_occurrences_order",
      "to": "edcm_goal_vector_same_occurrences_preserve_order"
    },
    {
      "from": "check_goal_vector_same_occurrences_order",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_same_occurrences_order",
      "to": "python3"
    },
    {
      "from": "check_goal_vector_sealed_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_sealed_evidence",
      "to": "self::test_sealed_goal_vector_evidence_matches_exact_producer"
    },
    {
      "from": "check_goal_vector_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_sealed_evidence",
      "to": "edcm_goal_vector_na_not_zero"
    },
    {
      "from": "check_goal_vector_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_sealed_evidence",
      "to": "edcm_goal_vector_no_status_transfer"
    },
    {
      "from": "check_goal_vector_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_sealed_evidence",
      "to": "edcm_goal_vector_same_occurrences_preserve_order"
    },
    {
      "from": "check_goal_vector_sealed_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_goal_vector_sealed_evidence",
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
      "from": "check_multiwoz21_admission_precedes_execution",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_admission_precedes_execution",
      "to": "self::test_archive_mutation_fails_before_dialogue_observation"
    },
    {
      "from": "check_multiwoz21_admission_precedes_execution",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_admission_precedes_execution",
      "to": "multiwoz21_admission_precedes_execution"
    },
    {
      "from": "check_multiwoz21_admission_precedes_execution",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_admission_precedes_execution",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_completion_requires_reconciliation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_completion_requires_reconciliation",
      "to": "self::test_manifest_count_mismatch_refuses_completion"
    },
    {
      "from": "check_multiwoz21_completion_requires_reconciliation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_completion_requires_reconciliation",
      "to": "multiwoz21_completion_requires_reconciliation"
    },
    {
      "from": "check_multiwoz21_completion_requires_reconciliation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_completion_requires_reconciliation",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "to": "self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts"
    },
    {
      "from": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "to": "multiwoz21_every_turn_is_observed_exactly_once"
    },
    {
      "from": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_every_turn_is_observed_exactly_once",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_failure_is_receipted",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_failure_is_receipted",
      "to": "self::test_invalid_turn_reports_exact_active_source_position"
    },
    {
      "from": "check_multiwoz21_failure_is_receipted",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_failure_is_receipted",
      "to": "multiwoz21_failure_is_receipted"
    },
    {
      "from": "check_multiwoz21_failure_is_receipted",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_failure_is_receipted",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "to": "self::test_claimed_gate_without_source_exhaustion_cannot_complete"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "to": "multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_false_receipt_rejected",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "to": "self::test_full_fixture_run_preserves_order_exact_text_and_profile_counts"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "to": "multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run"
    },
    {
      "from": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_ucns_v0141_receipt_matches_source_native_run",
      "to": "python3"
    },
    {
      "from": "check_multiwoz21_written_outputs_exclude_raw_text",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_written_outputs_exclude_raw_text",
      "to": "self::test_report_and_checkpoint_exclude_source_turn_text"
    },
    {
      "from": "check_multiwoz21_written_outputs_exclude_raw_text",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_written_outputs_exclude_raw_text",
      "to": "multiwoz21_written_outputs_exclude_raw_text"
    },
    {
      "from": "check_multiwoz21_written_outputs_exclude_raw_text",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz21_written_outputs_exclude_raw_text",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "to": "self::test_calibration_and_threshold_depend_only_on_development_and_validation"
    },
    {
      "from": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "to": "multiwoz_booking_outcome_calibration_precedes_test"
    },
    {
      "from": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_calibration_precedes_test",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "to": "self::test_output_destinations_reject_aliases_before_any_write"
    },
    {
      "from": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "to": "multiwoz_booking_outcome_destinations_do_not_collide"
    },
    {
      "from": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_destinations_do_not_collide",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "to": "self::test_falsified_finding_is_serialized_without_raising"
    },
    {
      "from": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "to": "multiwoz_booking_outcome_hypothesis_failure_is_evidence"
    },
    {
      "from": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_hypothesis_failure_is_evidence",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "to": "self::test_source_outcome_response_and_later_turns_are_withheld"
    },
    {
      "from": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "to": "multiwoz_booking_outcome_labelled_response_is_withheld"
    },
    {
      "from": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_labelled_response_is_withheld",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "to": "self::test_single_run_leaves_complete_repeat_not_evaluated"
    },
    {
      "from": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "to": "multiwoz_booking_outcome_repeat_requires_complete_execution"
    },
    {
      "from": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_repeat_requires_complete_execution",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "to": "self::test_report_schema_retains_aggregate_boundaries_without_event_locators"
    },
    {
      "from": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "to": "multiwoz_booking_outcome_report_is_aggregate_only"
    },
    {
      "from": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_report_is_aggregate_only",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "to": "self::test_runtime_binding_rejects_a_foreign_score_helper"
    },
    {
      "from": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "to": "multiwoz_booking_outcome_runtime_matches_recorded_checkout"
    },
    {
      "from": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_runtime_matches_recorded_checkout",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "self::test_sealed_holdout_evidence_matches_exact_producer_and_receipt"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "multiwoz_booking_outcome_calibration_precedes_test"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "multiwoz_booking_outcome_hypothesis_failure_is_evidence"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "multiwoz_booking_outcome_report_is_aggregate_only"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "multiwoz_booking_outcome_status_does_not_transfer"
    },
    {
      "from": "check_multiwoz_booking_outcome_sealed_evidence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_sealed_evidence",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "to": "self::test_report_schema_retains_aggregate_boundaries_without_event_locators"
    },
    {
      "from": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "to": "multiwoz_booking_outcome_status_does_not_transfer"
    },
    {
      "from": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_status_does_not_transfer",
      "to": "python3"
    },
    {
      "from": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
      "to": "self::test_evaluation_reports_confusion_wilson_and_cluster_intervals"
    },
    {
      "from": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
      "to": "multiwoz_booking_outcome_uncertainty_is_cluster_aware"
    },
    {
      "from": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_multiwoz_booking_outcome_uncertainty_is_cluster_aware",
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
      "from": "check_tarot_auto_fetch_rights_gate",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_auto_fetch_rights_gate",
      "to": "self::test_manifest_rejects_auto_fetch_without_public_domain_rights"
    },
    {
      "from": "check_tarot_auto_fetch_rights_gate",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_auto_fetch_rights_gate",
      "to": "tarot_acquisition_fetches_only_authorized_public_domain_bytes"
    },
    {
      "from": "check_tarot_auto_fetch_rights_gate",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_auto_fetch_rights_gate",
      "to": "python3"
    },
    {
      "from": "check_tarot_completed_resume_fails_closed",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_completed_resume_fails_closed",
      "to": "self::test_completed_resume_reuses_exact_state_and_rejects_tamper"
    },
    {
      "from": "check_tarot_completed_resume_fails_closed",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_completed_resume_fails_closed",
      "to": "tarot_acquisition_resume_fails_closed"
    },
    {
      "from": "check_tarot_completed_resume_fails_closed",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_completed_resume_fails_closed",
      "to": "python3"
    },
    {
      "from": "check_tarot_discovery_complete_acquisition_and_determinism",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_complete_acquisition_and_determinism",
      "to": "self::test_discovery_requires_sealed_acquisition_and_is_byte_deterministic"
    },
    {
      "from": "check_tarot_discovery_complete_acquisition_and_determinism",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_complete_acquisition_and_determinism",
      "to": "tarot_discovery_consumes_only_complete_sealed_acquisition"
    },
    {
      "from": "check_tarot_discovery_complete_acquisition_and_determinism",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_complete_acquisition_and_determinism",
      "to": "tarot_discovery_is_byte_deterministic"
    },
    {
      "from": "check_tarot_discovery_complete_acquisition_and_determinism",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_complete_acquisition_and_determinism",
      "to": "python3"
    },
    {
      "from": "check_tarot_discovery_documented_cli",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_documented_cli",
      "to": "self::test_documented_direct_cli_executes"
    },
    {
      "from": "check_tarot_discovery_documented_cli",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_documented_cli",
      "to": "tarot_discovery_is_byte_deterministic"
    },
    {
      "from": "check_tarot_discovery_documented_cli",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_documented_cli",
      "to": "posix_shell"
    },
    {
      "from": "check_tarot_discovery_documented_cli",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_documented_cli",
      "to": "python3"
    },
    {
      "from": "check_tarot_discovery_exact_order_values_and_absence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_exact_order_values_and_absence",
      "to": "self::test_discovery_preserves_order_exact_values_and_typed_absence"
    },
    {
      "from": "check_tarot_discovery_exact_order_values_and_absence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_exact_order_values_and_absence",
      "to": "tarot_discovery_preserves_exact_source_order_and_values"
    },
    {
      "from": "check_tarot_discovery_exact_order_values_and_absence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_exact_order_values_and_absence",
      "to": "tarot_discovery_preserves_typed_absence_and_nonclaims"
    },
    {
      "from": "check_tarot_discovery_exact_order_values_and_absence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_exact_order_values_and_absence",
      "to": "python3"
    },
    {
      "from": "check_tarot_discovery_mechanical_bounds",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_mechanical_bounds",
      "to": "self::test_discovery_emits_only_frozen_relations_and_enforces_bounds"
    },
    {
      "from": "check_tarot_discovery_mechanical_bounds",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_mechanical_bounds",
      "to": "tarot_discovery_relations_are_mechanical_and_bounded"
    },
    {
      "from": "check_tarot_discovery_mechanical_bounds",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_discovery_mechanical_bounds",
      "to": "python3"
    },
    {
      "from": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "to": "self::test_acquisition_fetches_only_public_domain_and_seals_source_identity"
    },
    {
      "from": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "to": "tarot_acquisition_fetches_only_authorized_public_domain_bytes"
    },
    {
      "from": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "to": "tarot_acquisition_preserves_source_identity"
    },
    {
      "from": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "to": "tarot_metadata_only_sources_are_not_downloaded"
    },
    {
      "from": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_fetch_authority_and_metadata_only_boundary",
      "to": "python3"
    },
    {
      "from": "check_tarot_interrupted_resume_checkpoint",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_interrupted_resume_checkpoint",
      "to": "self::test_interrupted_resume_keeps_verified_completed_sources"
    },
    {
      "from": "check_tarot_interrupted_resume_checkpoint",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_interrupted_resume_checkpoint",
      "to": "tarot_acquisition_preserves_source_identity"
    },
    {
      "from": "check_tarot_interrupted_resume_checkpoint",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_interrupted_resume_checkpoint",
      "to": "tarot_acquisition_resume_fails_closed"
    },
    {
      "from": "check_tarot_interrupted_resume_checkpoint",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_interrupted_resume_checkpoint",
      "to": "python3"
    },
    {
      "from": "check_tarot_manifest_preserves_preontology_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_manifest_preserves_preontology_boundary",
      "to": "self::test_committed_manifest_validates_without_tarot_ontology"
    },
    {
      "from": "check_tarot_manifest_preserves_preontology_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_manifest_preserves_preontology_boundary",
      "to": "tarot_manifest_preserves_preontology_boundary"
    },
    {
      "from": "check_tarot_manifest_preserves_preontology_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_manifest_preserves_preontology_boundary",
      "to": "python3"
    },
    {
      "from": "check_tarot_ocr_v4_accuracy",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_accuracy",
      "to": "self::test_normalization_distance_and_empty_page_rule"
    },
    {
      "from": "check_tarot_ocr_v4_accuracy",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_accuracy",
      "to": "tarot_ocr_v4_applies_frozen_accuracy_rule"
    },
    {
      "from": "check_tarot_ocr_v4_determinism",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_determinism",
      "to": "self::test_canonical_serialization_is_byte_deterministic"
    },
    {
      "from": "check_tarot_ocr_v4_determinism",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_determinism",
      "to": "tarot_ocr_v4_serialization_is_deterministic"
    },
    {
      "from": "check_tarot_ocr_v4_identity_and_resume",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_identity_and_resume",
      "to": "self::test_frozen_identity_constants_and_record_verification"
    },
    {
      "from": "check_tarot_ocr_v4_identity_and_resume",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_identity_and_resume",
      "to": "tarot_ocr_v4_resume_fails_closed"
    },
    {
      "from": "check_tarot_ocr_v4_identity_and_resume",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_identity_and_resume",
      "to": "tarot_ocr_v4_verifies_every_frozen_identity"
    },
    {
      "from": "check_tarot_ocr_v4_raw_evidence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_raw_evidence",
      "to": "self::test_record_preserves_hashes_confidence_and_page_identity"
    },
    {
      "from": "check_tarot_ocr_v4_raw_evidence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v4_raw_evidence",
      "to": "tarot_ocr_v4_preserves_raw_page_evidence"
    },
    {
      "from": "check_tarot_ocr_v5_core_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v5_core_identity",
      "to": "self::test_v5_protocol_and_instrument_identities_are_frozen"
    },
    {
      "from": "check_tarot_ocr_v5_core_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v5_core_identity",
      "to": "tarot_ocr_v5_retains_v4_evidence_contracts"
    },
    {
      "from": "check_tarot_ocr_v5_single_change",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v5_single_change",
      "to": "self::test_v5_ocr_command_is_exact_single_threshold_change"
    },
    {
      "from": "check_tarot_ocr_v5_single_change",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v5_single_change",
      "to": "tarot_ocr_v5_changes_only_frozen_thresholding"
    },
    {
      "from": "check_tarot_ocr_v6_core_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_core_identity",
      "to": "self::test_v6_protocol_and_instrument_identities_are_frozen"
    },
    {
      "from": "check_tarot_ocr_v6_core_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_core_identity",
      "to": "tarot_ocr_v6_retains_v4_evidence_contracts"
    },
    {
      "from": "check_tarot_ocr_v6_model_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_model_identity",
      "to": "self::test_v6_model_verification_fails_closed"
    },
    {
      "from": "check_tarot_ocr_v6_model_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_model_identity",
      "to": "tarot_ocr_v6_verifies_historic_model"
    },
    {
      "from": "check_tarot_ocr_v6_single_change",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_single_change",
      "to": "self::test_v6_ocr_command_is_exact_model_change"
    },
    {
      "from": "check_tarot_ocr_v6_single_change",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_ocr_v6_single_change",
      "to": "tarot_ocr_v6_changes_only_frozen_model"
    },
    {
      "from": "check_tarot_text_gate_frozen_thresholds",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_tarot_text_gate_frozen_thresholds",
      "to": "self::test_frozen_thresholds_accept_only_adequate_pages"
    },
    {
      "from": "check_tarot_text_gate_frozen_thresholds",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_text_gate_frozen_thresholds",
      "to": "tarot_text_gate_applies_frozen_adequacy_rule"
    },
    {
      "from": "check_tarot_text_gate_frozen_thresholds",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_tarot_text_gate_frozen_thresholds",
      "to": "tarot_text_gate_retains_nonclaims_and_failure"
    },
    {
      "from": "check_tarot_text_gate_frozen_thresholds",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_tarot_text_gate_frozen_thresholds",
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
      "from": "language_relational_branch_check",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "self::test_independent_branches_freeze_before_comparison"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "comparison_requires_two_prior_freezes"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "english_metadata_is_external_to_ucns_carrier"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "lexical_branches_are_independently_constructed"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "lexical_manifest_preserves_authority_firewall"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "lexical_pre_replay_status_is_unresolved"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "lexical_relation_multiplicity_is_preserved"
    },
    {
      "from": "language_relational_branch_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "language_relational_branch_check",
      "to": "lexical_ucns_producer_is_exactly_verified"
    },
    {
      "from": "oewn_builder_order_check",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "oewn_builder_order_check",
      "to": "self::test_builder_contract_is_pinned_and_freeze_order_is_explicit"
    },
    {
      "from": "oewn_builder_order_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "oewn_builder_order_check",
      "to": "incomplete_or_altered_lexical_resume_fails_closed"
    },
    {
      "from": "oewn_builder_order_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "oewn_builder_order_check",
      "to": "lexical_comparison_occurs_after_freeze"
    },
    {
      "from": "oewn_builder_order_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "oewn_builder_order_check",
      "to": "oewn_source_is_exact_pinned_and_resumable"
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
      "from": "edcm_corpora_package",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_corpora_package",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_corpora_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_corpora_package",
      "to": "edcm_ucns_adapter"
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
      "from": "edcm_goal_vector_experiment",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_goal_vector_experiment",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_goal_vector_experiment",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_goal_vector_experiment",
      "to": "edcm_ucns_adapter"
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
      "to": "edcm_language_oewn_source"
    },
    {
      "from": "edcm_language_manifest",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_manifest",
      "to": "ucns_relational_carrier"
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
      "to": "edcm_language_relational_bridge"
    },
    {
      "from": "edcm_language_package",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_package",
      "to": "edcm_language_rendering"
    },
    {
      "from": "edcm_language_relational_bridge",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_relational_bridge",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_language_relational_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_relational_bridge",
      "to": "edcm_language_affixes"
    },
    {
      "from": "edcm_language_relational_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_relational_bridge",
      "to": "edcm_language_morphology"
    },
    {
      "from": "edcm_language_relational_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_relational_bridge",
      "to": "edcm_language_oewn_source"
    },
    {
      "from": "edcm_language_relational_bridge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_language_relational_bridge",
      "to": "ucns_relational_carrier"
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
      "from": "edcm_multiwoz21_booking_outcome_holdout",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_booking_outcome_holdout",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_multiwoz21_booking_outcome_holdout",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_booking_outcome_holdout",
      "to": "edcm_multiwoz21_corpus"
    },
    {
      "from": "edcm_multiwoz21_booking_outcome_holdout",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_booking_outcome_holdout",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcm_multiwoz21_booking_outcome_holdout",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_booking_outcome_holdout",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcm_multiwoz21_booking_outcome_holdout",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_booking_outcome_holdout",
      "to": "ucns.profile.edcm-word-gonol at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
    },
    {
      "from": "edcm_multiwoz21_corpus",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_corpus",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_multiwoz21_corpus",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_corpus",
      "to": "edcm_ucns_adapter"
    },
    {
      "from": "edcm_multiwoz21_corpus",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_corpus",
      "to": "ucns.edcm and ucns.full_corpus at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
    },
    {
      "from": "edcm_multiwoz21_seal_launcher",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_seal_launcher",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_multiwoz21_seal_launcher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_seal_launcher",
      "to": "edcm_multiwoz21_corpus"
    },
    {
      "from": "edcm_multiwoz21_seal_launcher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_seal_launcher",
      "to": "git"
    },
    {
      "from": "edcm_multiwoz21_seal_launcher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_multiwoz21_seal_launcher",
      "to": "python3"
    },
    {
      "from": "edcm_oewn2025_lexical_floor_builder",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_oewn2025_lexical_floor_builder",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_oewn2025_lexical_floor_builder",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_oewn2025_lexical_floor_builder",
      "to": "edcm_language_relational_bridge"
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
      "from": "edcm_tarot_corpus_acquirer",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_corpus_acquirer",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_corpus_acquirer",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_corpus_acquirer",
      "to": "none"
    },
    {
      "from": "edcm_tarot_ocr_v4_runner",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v4_runner",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_ocr_v4_runner",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v4_runner",
      "to": "edcm_tarot_corpus_acquirer"
    },
    {
      "from": "edcm_tarot_ocr_v5_runner",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v5_runner",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_ocr_v5_runner",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v5_runner",
      "to": "edcm_tarot_ocr_v4_runner"
    },
    {
      "from": "edcm_tarot_ocr_v6_runner",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v6_runner",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_ocr_v6_runner",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_ocr_v6_runner",
      "to": "edcm_tarot_ocr_v4_runner"
    },
    {
      "from": "edcm_tarot_pdf_text_layer_gate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_pdf_text_layer_gate",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_pdf_text_layer_gate",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_pdf_text_layer_gate",
      "to": "edcm_tarot_corpus_acquirer"
    },
    {
      "from": "edcm_tarot_relation_discovery",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_relation_discovery",
      "to": "Erin Spencer"
    },
    {
      "from": "edcm_tarot_relation_discovery",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcm_tarot_relation_discovery",
      "to": "edcm_tarot_corpus_acquirer"
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
      "to": "ucns.edcm at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
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
