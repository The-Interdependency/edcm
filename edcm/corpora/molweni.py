"""Lossless, resumable full-corpus runner for the admitted Molweni checkout.

Usage guidance
--------------
Keep the official repository checkout outside Git, leave it at the exact
admitted commit, check out the pinned UCNS profile commit, and run:

    python -m edcm.corpora.molweni \
      --source-root /path/to/Molweni \
      --ucns-source-root /path/to/ucns-at-pinned-commit \
      --output experiments/corpora/results/2026-07-28-molweni-full.json \
      --receipt experiments/corpora/receipts/2026-07-28-molweni-complete.json \
      --checkpoint /tmp/molweni.checkpoint.json

The discourse-parsing (DP) files are the complete 10,000-dialogue turn stream.
Every exact EDU text is observed once through the pinned EDCM UCNS word-gonol
profile, and every directed relation retains its split, dialogue, source
ordinal, target ordinal, label, and digest. Nonempty source speaker strings pass
unchanged. A released empty speaker string is retained as malformed source
evidence and receives a collision-checked ordinal sentinel only at the adapter
boundary because the pinned profile refuses empty speaker identifiers.

The machine-reading-comprehension (MRC) files are a differently partitioned
annotation view over the same dialogue source. Every context, EDU, relation,
question, answerability flag, answer, plausible answer, and exact answer span
is validated and digested, but the duplicated EDU text is not measured a
second time. Exact-EDU matches and relation-graph disagreements between the two
views remain visible. Written outputs contain aggregates and cryptographic
identities, never raw dialogue, question, answer, or speaker text.

Checkpoints resume the expensive DP profile phase. The smaller MRC annotation
phase restarts from its beginning after interruption so no annotation can be
silently skipped or double-counted.
"""

# === MODULE_BUILD ===
# id: edcm_molweni_corpus
#   module_name: molweni
#   module_kind: adapter
#   summary: verifies and reconciles every Molweni DP dialogue, exact EDU text, source speaker field, directed relation, and MRC annotation while observing each turn once through the pinned EDCM UCNS profile
#   owner: Erin Spencer
#   public_surface: load_admission_manifest, run_source, main
#   internal_surface: _verify_source, _new_state, _observe_dp_dialogue, _observe_mrc_dialogue, _reconciliation, _build_report, _build_receipt
#   auth_boundary: none
#   storage_boundary: reads a caller-held source checkout and writes only caller-selected aggregate report, receipt, and resumable checkpoint paths
#   network_boundary: none; source acquisition is separate and the runner requires local pinned bytes
#   user_data_boundary: exact Ubuntu-derived dialogue, question, answer, and speaker text is processed locally and represented only by counts and cryptographic identities in written outputs
#   admin_only: false
#   tests: tests.test_molweni_corpus
#   rollout: explicit admitted full-corpus command; no sampling, graph repair, default measurement, or canon selection
#   rollback: remove the adapter and supersede its aggregate receipts by source identity; raw source remains outside Git
#   requires: edcm_corpora_package, edcm_ucns_adapter, ucns.edcm at eb264fba18bd051c46b4853c81c8fb91ec6d5811
#   since: 2026-07-28
#   unresolved: upstream cause of released empty speaker fields; annotation effects inherited from the filtered Ubuntu source; semantic meaning of graph disagreement; formal UCNS geometry and lawful EDCM projection
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: molweni_admission_precedes_execution
#   given: a caller supplies a local Molweni repository checkout
#   then: the exact Git commit, clean tracked state, file bytes, and SHA-256 identities match the committed admission before dialogue evidence is observed
#   class: provenance
#   since: 2026-07-28
#
# id: molweni_every_dp_turn_and_relation_is_retained_once
#   given: the admitted DP train, dev, and test files are valid
#   then: all 10,000 dialogues, 88,303 exact EDU texts with retained source speaker fields, and 78,245 directed labeled relations are processed once in declared file and source order without text normalization, sampling, sorting, deduplication, or graph repair
#   class: evidence
#   since: 2026-07-28
#
# id: molweni_every_mrc_annotation_is_validated_without_duplicate_measurement
#   given: the admitted MRC train, dev, and test files are valid
#   then: every context, EDU, relation object including released invalid endpoints, question, answerability flag, answer, plausible answer, and exact span is validated while dialogue text already present in DP is not measured a second time
#   class: evidence
#   since: 2026-07-28
#
# id: molweni_completion_requires_cross_view_reconciliation
#   given: all admitted DP and MRC files reach valid EOF
#   then: completion is emitted only when source, adapter, unit-support, partition, graph, question, answer, and exact-EDU cross-view counts reconcile with the manifest
#   class: safety
#   since: 2026-07-28
#
# id: molweni_failure_is_receipted_at_source_position
#   given: provenance, schema, adapter, checkpoint, span, or reconciliation processing fails
#   then: the command emits an incomplete receipt with the active variant, split, dialogue, turn, relation, and question position plus the exact failure class and reason
#   class: safety
#   since: 2026-07-28
#
# id: molweni_written_outputs_exclude_raw_source_text
#   given: a run succeeds or fails
#   then: written reports, receipts, and checkpoints contain aggregates and identities but no source dialogue, question, answer, context, or speaker text
#   class: privacy
#   since: 2026-07-28
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import importlib.resources
import json
import sys
from collections.abc import Mapping
from hashlib import sha256
from pathlib import Path
from typing import Any

from edcm.corpora.multiwoz21 import (
    AdmissionManifest,
    CorpusRunError,
    _chain,
    _digest,
    _git_commit,
    _load_pinned_adapter,
    _profile_identity,
    _space_shape,
    _write_json_atomic,
)
from edcm.ucns_adapter import ActualUCNSAdapter, PINNED_UCNS_COMMIT


RUNNER_SCHEMA_ID = "edcm.molweni-full-corpus"
RUNNER_SCHEMA_VERSION = "1.0.0"
RECEIPT_SCHEMA_ID = "edcm.corpus-run-receipt"
RECEIPT_SCHEMA_VERSION = "1.0.0"
CHECKPOINT_SCHEMA_ID = "edcm.molweni-checkpoint"
CHECKPOINT_SCHEMA_VERSION = "1.0.0"
EMPTY_CHAIN_DIGEST = sha256(b"").hexdigest()
EMPTY_SPEAKER_SENTINEL_PREFIX = "edcm.molweni/source-empty-speaker/"
DP_SPLITS = ("train", "dev", "test")
MRC_SPLITS = ("train", "dev", "test")
CHUNK_SIZE = 1024 * 1024


def load_admission_manifest() -> AdmissionManifest:
    """Load and validate the packaged Molweni admission record."""

    resource = importlib.resources.files("edcm.corpora").joinpath(
        "data/molweni_admission.json"
    )
    payload = json.loads(resource.read_text(encoding="utf-8"))
    required = {
        "schema_id",
        "schema_version",
        "corpus_id",
        "status",
        "source",
        "expected",
        "execution_policy",
        "information_boundaries",
        "hmmm",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise CorpusRunError(
            f"admission manifest is missing fields: {', '.join(missing)}",
            code="ADMISSION_SCHEMA",
        )
    if (
        payload["schema_id"] != "edcm.corpus-admission"
        or payload["schema_version"] != "1.0.0"
        or payload["corpus_id"] != "molweni"
        or payload["status"] != "admitted"
    ):
        raise CorpusRunError(
            "admission manifest identity or status mismatch",
            code="ADMISSION_IDENTITY",
        )
    return AdmissionManifest(payload)


def _sha256_path(path: Path) -> tuple[int, str]:
    digest = sha256()
    size = 0
    with path.open("rb") as handle:
        while block := handle.read(CHUNK_SIZE):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def _verify_source(
    source_root: Path,
    manifest: AdmissionManifest,
) -> dict[str, Any]:
    if not source_root.is_dir():
        raise CorpusRunError(
            "Molweni source root is not a directory",
            code="SOURCE_ROOT",
        )
    commit = _git_commit(source_root, require_clean=True)
    expected_commit = str(manifest.source["commit"])
    if commit != expected_commit:
        raise CorpusRunError(
            f"Molweni checkout mismatch: expected {expected_commit}, got {commit}",
            code="SOURCE_COMMIT",
        )

    verified_files = []
    for expected in manifest.source["files"]:
        relative = Path(str(expected["path"]))
        path = source_root / relative
        try:
            resolved = path.resolve(strict=True)
        except OSError as exc:
            raise CorpusRunError(
                f"admitted source file is missing: {relative.as_posix()}",
                code="SOURCE_FILE_MISSING",
            ) from exc
        if not resolved.is_relative_to(source_root.resolve()) or not resolved.is_file():
            raise CorpusRunError(
                f"admitted source path is not a regular in-root file: {relative.as_posix()}",
                code="SOURCE_FILE_BOUNDARY",
            )
        size, digest = _sha256_path(resolved)
        if size != expected["bytes"] or digest != expected["sha256"]:
            raise CorpusRunError(
                f"admitted source file identity mismatch: {relative.as_posix()}",
                code="SOURCE_FILE_IDENTITY",
            )
        verified_files.append(
            {
                "bytes": size,
                "path": relative.as_posix(),
                "sha256": digest,
            }
        )
    return {
        "commit": commit,
        "files": verified_files,
        "repository": manifest.source["repository"],
        "tree": manifest.source["tree"],
    }


def _partition_template() -> dict[str, dict[str, int]]:
    return {
        split: {"dialogues": 0, "relations": 0, "turns": 0}
        for split in DP_SPLITS
    }


def _mrc_partition_template() -> dict[str, dict[str, int]]:
    return {
        split: {
            "answerable_questions": 0,
            "dialogues": 0,
            "plausible_answers": 0,
            "questions": 0,
            "relations": 0,
            "turns": 0,
            "unanswerable_questions": 0,
        }
        for split in MRC_SPLITS
    }


def _new_state(
    *,
    admission_digest: str,
    edcm_commit: str,
    source_commit: str,
    ucns_commit: str,
) -> dict[str, Any]:
    return {
        "active_dialogue_id": None,
        "active_dialogue_index": None,
        "active_question_index": None,
        "active_relation_index": None,
        "active_split": None,
        "active_turn_index": None,
        "active_variant": None,
        "adapter_turns": 0,
        "admission_digest": admission_digest,
        "answer_span_mismatches": 0,
        "code_points": 0,
        "completed_dp_dialogues": 0,
        "dialogues": 0,
        "dialogues_with_multiple_speakers": 0,
        "dp_partitions": _partition_template(),
        "edcm_commit": edcm_commit,
        "empty_turns": 0,
        "first_dialogue_id": None,
        "last_completed_dialogue_id": None,
        "last_completed_dialogue_index": None,
        "last_completed_split": None,
        "leading_space_turns": 0,
        "mrc_answerable_questions": 0,
        "mrc_annotation_digest_chain": EMPTY_CHAIN_DIGEST,
        "mrc_dialogues": 0,
        "mrc_edu_ambiguous_dp_matches": 0,
        "mrc_edu_exact_dp_matches": 0,
        "mrc_edu_missing_dp_matches": 0,
        "mrc_invalid_relation_endpoint_dialogues": 0,
        "mrc_invalid_relation_endpoints": 0,
        "mrc_partitions": _mrc_partition_template(),
        "mrc_plausible_answers": 0,
        "mrc_questions": 0,
        "mrc_relation_graph_disagreements": 0,
        "mrc_relation_graph_matches": 0,
        "mrc_relations": 0,
        "mrc_unanswerable_questions": 0,
        "mrc_turns": 0,
        "newline_turns": 0,
        "non_ascii_turns": 0,
        "out_of_alphabet_affected_turns": 0,
        "out_of_alphabet_affected_word_gonols": 0,
        "out_of_alphabet_by_code_point": {},
        "out_of_alphabet_occurrences": 0,
        "profile_identity": None,
        "profile_observation_digest_chain": EMPTY_CHAIN_DIGEST,
        "relation_label_counts": {},
        "relation_same_node": 0,
        "relation_source_follows_target": 0,
        "relation_source_precedes_target": 0,
        "relation_digest_chain": EMPTY_CHAIN_DIGEST,
        "relations": 0,
        "repeated_space_excess": 0,
        "source_commit": source_commit,
        "source_dialogue_digest_chain": EMPTY_CHAIN_DIGEST,
        "source_empty_speaker_dialogues": 0,
        "source_empty_speaker_turns": 0,
        "source_turns": 0,
        "speaker_count_per_dialogue": {},
        "space_boundaries": 0,
        "trailing_space_turns": 0,
        "turn_evidence_digest_chain": EMPTY_CHAIN_DIGEST,
        "ucns_commit": ucns_commit,
        "unit_support_total": 0,
        "utf8_bytes": 0,
        "word_gonols": 0,
    }


def _read_json(path: Path, *, state: Mapping[str, Any]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorpusRunError(
            f"source JSON cannot be read: {path.name}: {type(exc).__name__}: {exc}",
            code="SOURCE_JSON",
            state=state,
        ) from exc


def _dialogue_parts(
    dialogue: Any,
    *,
    allow_invalid_relation_endpoints: bool = False,
    state: dict[str, Any],
) -> tuple[list[tuple[str, str]], list[Mapping[str, Any]]]:
    if not isinstance(dialogue, Mapping):
        raise CorpusRunError(
            "dialogue is not an object",
            code="DIALOGUE_SHAPE",
            state=state,
        )
    edus = dialogue.get("edus")
    relations = dialogue.get("relations")
    if not isinstance(edus, list) or not isinstance(relations, list):
        raise CorpusRunError(
            "dialogue edus or relations is not a list",
            code="DIALOGUE_CONTENT_SHAPE",
            state=state,
        )

    turns = []
    for turn_index, edu in enumerate(edus):
        state["active_turn_index"] = turn_index
        if not isinstance(edu, Mapping):
            raise CorpusRunError(
                "EDU is not an object",
                code="EDU_SHAPE",
                state=state,
            )
        speaker = edu.get("speaker")
        text = edu.get("text")
        if not isinstance(speaker, str) or not isinstance(text, str):
            raise CorpusRunError(
                "EDU speaker or text is not a string",
                code="EDU_FIELD_TYPE",
                state=state,
            )
        turns.append((speaker, text))

    checked_relations = []
    for relation_index, relation in enumerate(relations):
        state["active_relation_index"] = relation_index
        if not isinstance(relation, Mapping):
            raise CorpusRunError(
                "relation is not an object",
                code="RELATION_SHAPE",
                state=state,
            )
        source = relation.get("x")
        target = relation.get("y")
        label = relation.get("type")
        if (
            isinstance(source, bool)
            or not isinstance(source, int)
            or isinstance(target, bool)
            or not isinstance(target, int)
            or not isinstance(label, str)
        ):
            raise CorpusRunError(
                "relation x, y, or type has an invalid type",
                code="RELATION_FIELD_TYPE",
                state=state,
            )
        if source < 0 or target < 0 or source >= len(turns) or target >= len(turns):
            if not allow_invalid_relation_endpoints:
                raise CorpusRunError(
                    "relation endpoint is outside the dialogue EDU sequence",
                    code="RELATION_ENDPOINT",
                    state=state,
                )
        checked_relations.append(relation)
    state["active_turn_index"] = None
    state["active_relation_index"] = None
    return turns, checked_relations


def _observe_dp_dialogue(
    *,
    adapter: ActualUCNSAdapter,
    dialogue: Mapping[str, Any],
    dialogue_id: str,
    dialogue_index: int,
    split: str,
    state: dict[str, Any],
) -> tuple[str, str]:
    state["active_variant"] = "DP"
    state["active_split"] = split
    state["active_dialogue_index"] = dialogue_index
    state["active_dialogue_id"] = dialogue_id
    turns, relations = _dialogue_parts(dialogue, state=state)
    source_speakers = {speaker for speaker, _text in turns}
    profile_turns = []
    empty_speaker_turns = 0
    for turn_index, (speaker, text) in enumerate(turns):
        profile_speaker = speaker
        if speaker == "":
            empty_speaker_turns += 1
            profile_speaker = (
                f"{EMPTY_SPEAKER_SENTINEL_PREFIX}{dialogue_id}/{turn_index}"
            )
            if profile_speaker in source_speakers:
                raise CorpusRunError(
                    "empty-speaker adapter sentinel collides with a source speaker identifier",
                    code="EMPTY_SPEAKER_SENTINEL_COLLISION",
                    state=state,
                )
        profile_turns.append((profile_speaker, text))

    try:
        adapted = adapter.normalize(
            {
                "source_ref": (
                    f"HIT-SCIR/Molweni@{state['source_commit']}:"
                    f"DP/{split}.json:{dialogue_id}"
                ),
                "ucns_turns": tuple(profile_turns),
            }
        )
    except Exception as exc:
        raise CorpusRunError(
            f"exact UCNS profile adapter failed: {type(exc).__name__}: {exc}",
            code="UCNS_PROFILE_ADAPTER",
            state=state,
        ) from exc
    evidence = adapted.get("ucns_profile_observation")
    if not isinstance(evidence, Mapping):
        raise CorpusRunError(
            "exact UCNS profile observation was not attached",
            code="UCNS_PROFILE_ABSENT",
            state=state,
        )
    identity = _profile_identity(evidence)
    if state["profile_identity"] is None:
        state["profile_identity"] = identity
    elif state["profile_identity"] != identity:
        raise CorpusRunError(
            "UCNS profile identity changed during the run",
            code="UCNS_PROFILE_DRIFT",
            state=state,
        )
    observed_turns = evidence.get("turns")
    if not isinstance(observed_turns, (tuple, list)) or len(observed_turns) != len(
        turns
    ):
        raise CorpusRunError(
            "source and profile turn sequences do not reconcile",
            code="TURN_RECONCILIATION",
            state=state,
        )

    dialogue_record = {
        "dialogue_id": dialogue_id,
        "dialogue_index": dialogue_index,
        "dialogue_sha256": _digest(dialogue),
        "split": split,
    }
    state["source_dialogue_digest_chain"] = _chain(
        state["source_dialogue_digest_chain"],
        dialogue_record,
    )
    state["profile_observation_digest_chain"] = _chain(
        state["profile_observation_digest_chain"],
        {
            "dialogue_id": dialogue_id,
            "dialogue_index": dialogue_index,
            "observation_digest": evidence["observation_digest"],
            "split": split,
        },
    )

    speakers = {speaker for speaker, _text in turns if speaker != ""}
    speaker_count = str(len(speakers))
    state["speaker_count_per_dialogue"][speaker_count] = (
        state["speaker_count_per_dialogue"].get(speaker_count, 0) + 1
    )
    state["dialogues_with_multiple_speakers"] += int(len(speakers) > 1)
    state["source_empty_speaker_dialogues"] += int(empty_speaker_turns > 0)
    state["source_empty_speaker_turns"] += empty_speaker_turns

    for turn_index, ((source_turn, profile_turn), observed) in enumerate(
        zip(zip(turns, profile_turns, strict=True), observed_turns, strict=True)
    ):
        state["active_turn_index"] = turn_index
        speaker, text = source_turn
        profile_speaker, profile_text = profile_turn
        if (
            observed["speaker_id"] != profile_speaker
            or observed["turn_index"] != turn_index
            or observed["raw_text"] != profile_text
            or profile_text != text
        ):
            raise CorpusRunError(
                "adapter turn does not reconstruct the exact source EDU",
                code="TURN_EXACTNESS",
                state=state,
            )
        text_bytes = text.encode("utf-8")
        state["turn_evidence_digest_chain"] = _chain(
            state["turn_evidence_digest_chain"],
            {
                "dialogue_id": dialogue_id,
                "dialogue_index": dialogue_index,
                "speaker_sha256": sha256(speaker.encode("utf-8")).hexdigest(),
                "split": split,
                "text_code_points": len(text),
                "text_sha256": sha256(text_bytes).hexdigest(),
                "text_utf8_bytes": len(text_bytes),
                "turn_index": turn_index,
            },
        )
        state["source_turns"] += 1
        state["adapter_turns"] += 1
        state["unit_support_total"] += observed["unit_support"]
        state["code_points"] += len(text)
        state["utf8_bytes"] += len(text_bytes)
        state["word_gonols"] += observed["word_count"]
        state["space_boundaries"] += observed["nesting_boundary_count"]
        state["empty_turns"] += int(text == "")
        state["newline_turns"] += int("\n" in text or "\r" in text)
        state["non_ascii_turns"] += int(any(ord(value) > 127 for value in text))
        repeated, leading, trailing = _space_shape(text)
        state["repeated_space_excess"] += repeated
        state["leading_space_turns"] += int(leading)
        state["trailing_space_turns"] += int(trailing)

        out_of_alphabet = observed["out_of_alphabet"]
        state["out_of_alphabet_occurrences"] += len(out_of_alphabet)
        state["out_of_alphabet_affected_turns"] += int(bool(out_of_alphabet))
        for token in out_of_alphabet:
            code_point = token["code_point"]
            histogram = state["out_of_alphabet_by_code_point"]
            histogram[code_point] = histogram.get(code_point, 0) + 1
        for segment in observed["segments"]:
            if segment["kind"] == "word-gonol" and any(
                not token["in_alphabet"] for token in segment["tokens"]
            ):
                state["out_of_alphabet_affected_word_gonols"] += 1

    for relation_index, relation in enumerate(relations):
        state["active_relation_index"] = relation_index
        source = relation["x"]
        target = relation["y"]
        label = relation["type"]
        state["relation_digest_chain"] = _chain(
            state["relation_digest_chain"],
            {
                "dialogue_id": dialogue_id,
                "dialogue_index": dialogue_index,
                "label": label,
                "relation_index": relation_index,
                "source": source,
                "split": split,
                "target": target,
            },
        )
        state["relations"] += 1
        state["relation_label_counts"][label] = (
            state["relation_label_counts"].get(label, 0) + 1
        )
        state["relation_source_precedes_target"] += int(source < target)
        state["relation_same_node"] += int(source == target)
        state["relation_source_follows_target"] += int(source > target)

    state["dialogues"] += 1
    state["completed_dp_dialogues"] += 1
    state["dp_partitions"][split]["dialogues"] += 1
    state["dp_partitions"][split]["turns"] += len(turns)
    state["dp_partitions"][split]["relations"] += len(relations)
    if state["first_dialogue_id"] is None:
        state["first_dialogue_id"] = dialogue_id
    state["last_completed_dialogue_id"] = dialogue_id
    state["last_completed_dialogue_index"] = dialogue_index
    state["last_completed_split"] = split
    state["active_dialogue_id"] = None
    state["active_dialogue_index"] = None
    state["active_relation_index"] = None
    state["active_split"] = None
    state["active_turn_index"] = None
    state["active_variant"] = None
    return _digest(dialogue["edus"]), _digest(dialogue["relations"])


def _reset_mrc_state(state: dict[str, Any]) -> None:
    state.update(
        {
            "answer_span_mismatches": 0,
            "mrc_answerable_questions": 0,
            "mrc_annotation_digest_chain": EMPTY_CHAIN_DIGEST,
            "mrc_dialogues": 0,
            "mrc_edu_ambiguous_dp_matches": 0,
            "mrc_edu_exact_dp_matches": 0,
            "mrc_edu_missing_dp_matches": 0,
            "mrc_invalid_relation_endpoint_dialogues": 0,
            "mrc_invalid_relation_endpoints": 0,
            "mrc_partitions": _mrc_partition_template(),
            "mrc_plausible_answers": 0,
            "mrc_questions": 0,
            "mrc_relation_graph_disagreements": 0,
            "mrc_relation_graph_matches": 0,
            "mrc_relations": 0,
            "mrc_turns": 0,
            "mrc_unanswerable_questions": 0,
        }
    )


def _validate_spans(
    spans: Any,
    *,
    context: str,
    code: str,
    state: dict[str, Any],
) -> int:
    if not isinstance(spans, list):
        raise CorpusRunError(
            "answer collection is not a list",
            code=code,
            state=state,
        )
    for span in spans:
        if not isinstance(span, Mapping):
            raise CorpusRunError(
                "answer span is not an object",
                code=code,
                state=state,
            )
        start = span.get("answer_start")
        text = span.get("text")
        if (
            isinstance(start, bool)
            or not isinstance(start, int)
            or start < 0
            or not isinstance(text, str)
            or context[start : start + len(text)] != text
        ):
            state["answer_span_mismatches"] += 1
            raise CorpusRunError(
                "answer span does not reconstruct exact context text",
                code=code,
                state=state,
            )
    return len(spans)


def _observe_mrc_dialogue(
    *,
    dialogue: Mapping[str, Any],
    dialogue_index: int,
    dp_index: Mapping[str, list[str]],
    question_ids: set[str],
    split: str,
    state: dict[str, Any],
) -> None:
    state["active_variant"] = "MRC(withDiscourse)"
    state["active_split"] = split
    state["active_dialogue_index"] = dialogue_index
    state["active_dialogue_id"] = None
    turns, relations = _dialogue_parts(
        dialogue,
        allow_invalid_relation_endpoints=True,
        state=state,
    )
    context = dialogue.get("context")
    qas = dialogue.get("qas")
    if not isinstance(context, str) or not isinstance(qas, list):
        raise CorpusRunError(
            "MRC context or qas has an invalid shape",
            code="MRC_DIALOGUE_SHAPE",
            state=state,
        )

    edu_digest = _digest(dialogue["edus"])
    relation_digest = _digest(dialogue["relations"])
    invalid_relation_endpoints = sum(
        relation["x"] < 0
        or relation["y"] < 0
        or relation["x"] >= len(turns)
        or relation["y"] >= len(turns)
        for relation in relations
    )
    state["mrc_invalid_relation_endpoints"] += invalid_relation_endpoints
    state["mrc_invalid_relation_endpoint_dialogues"] += int(
        invalid_relation_endpoints > 0
    )
    candidates = dp_index.get(edu_digest, [])
    if not candidates:
        state["mrc_edu_missing_dp_matches"] += 1
    else:
        state["mrc_edu_exact_dp_matches"] += 1
        state["mrc_edu_ambiguous_dp_matches"] += int(len(candidates) > 1)
        if relation_digest in candidates:
            state["mrc_relation_graph_matches"] += 1
        else:
            state["mrc_relation_graph_disagreements"] += 1

    answerable = 0
    unanswerable = 0
    plausible_count = 0
    for question_index, qa in enumerate(qas):
        state["active_question_index"] = question_index
        if not isinstance(qa, Mapping):
            raise CorpusRunError(
                "question annotation is not an object",
                code="QUESTION_SHAPE",
                state=state,
            )
        question_id = qa.get("id")
        question = qa.get("question")
        impossible = qa.get("is_impossible")
        if (
            not isinstance(question_id, str)
            or not isinstance(question, str)
            or not isinstance(impossible, bool)
        ):
            raise CorpusRunError(
                "question id, text, or answerability flag has an invalid type",
                code="QUESTION_FIELD_TYPE",
                state=state,
            )
        if question_id in question_ids:
            raise CorpusRunError(
                "question identifier is duplicated across MRC files",
                code="QUESTION_DUPLICATE",
                state=state,
            )
        question_ids.add(question_id)
        answer_count = _validate_spans(
            qa.get("answers"),
            context=context,
            code="ANSWER_SPAN",
            state=state,
        )
        plausible = qa.get("plausible_answers", [])
        plausible_for_question = _validate_spans(
            plausible,
            context=context,
            code="PLAUSIBLE_ANSWER_SPAN",
            state=state,
        )
        if impossible:
            if answer_count != 0 or plausible_for_question == 0:
                raise CorpusRunError(
                    "unanswerable question does not carry the expected plausible-answer shape",
                    code="UNANSWERABLE_SHAPE",
                    state=state,
                )
            unanswerable += 1
        else:
            if answer_count == 0 or plausible_for_question != 0:
                raise CorpusRunError(
                    "answerable question does not carry the expected answer shape",
                    code="ANSWERABLE_SHAPE",
                    state=state,
                )
            answerable += 1
        plausible_count += plausible_for_question

    state["mrc_annotation_digest_chain"] = _chain(
        state["mrc_annotation_digest_chain"],
        {
            "annotation_sha256": _digest(dialogue),
            "dialogue_index": dialogue_index,
            "edu_sha256": edu_digest,
            "relation_sha256": relation_digest,
            "split": split,
        },
    )
    state["mrc_dialogues"] += 1
    state["mrc_turns"] += len(turns)
    state["mrc_relations"] += len(relations)
    state["mrc_questions"] += len(qas)
    state["mrc_answerable_questions"] += answerable
    state["mrc_unanswerable_questions"] += unanswerable
    state["mrc_plausible_answers"] += plausible_count
    partition = state["mrc_partitions"][split]
    partition["dialogues"] += 1
    partition["turns"] += len(turns)
    partition["relations"] += len(relations)
    partition["questions"] += len(qas)
    partition["answerable_questions"] += answerable
    partition["unanswerable_questions"] += unanswerable
    partition["plausible_answers"] += plausible_count
    state["active_dialogue_index"] = None
    state["active_question_index"] = None
    state["active_relation_index"] = None
    state["active_split"] = None
    state["active_turn_index"] = None
    state["active_variant"] = None


def _checkpoint_payload(state: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": CHECKPOINT_SCHEMA_ID,
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "state": dict(state),
    }


def _load_checkpoint(
    path: Path,
    *,
    expected: Mapping[str, str],
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorpusRunError(
            f"checkpoint cannot be read: {type(exc).__name__}: {exc}",
            code="CHECKPOINT_INVALID",
        ) from exc
    if (
        payload.get("schema_id") != CHECKPOINT_SCHEMA_ID
        or payload.get("schema_version") != CHECKPOINT_SCHEMA_VERSION
        or not isinstance(payload.get("state"), dict)
    ):
        raise CorpusRunError(
            "checkpoint schema mismatch",
            code="CHECKPOINT_SCHEMA",
        )
    state = payload["state"]
    for key, value in expected.items():
        if state.get(key) != value:
            raise CorpusRunError(
                f"checkpoint identity mismatch for {key}",
                code="CHECKPOINT_IDENTITY",
            )
    return state


def _reconciliation(
    state: Mapping[str, Any],
    manifest: AdmissionManifest,
) -> dict[str, Any]:
    expected = manifest.expected
    checks = {
        "adapter_turns_equal_dp_source_turns": (
            state["adapter_turns"] == state["source_turns"]
        ),
        "dp_dialogues_match_manifest": (
            state["dialogues"] == expected["dp"]["dialogues"]
        ),
        "dp_partitions_match_manifest": (
            state["dp_partitions"] == expected["dp"]["partitions"]
        ),
        "dp_relations_match_manifest": (
            state["relations"] == expected["dp"]["relations"]
        ),
        "dp_turns_match_manifest": (
            state["source_turns"] == expected["dp"]["turns"]
        ),
        "mrc_answerable_match_manifest": (
            state["mrc_answerable_questions"]
            == expected["mrc"]["answerable_questions"]
        ),
        "mrc_dialogues_match_manifest": (
            state["mrc_dialogues"] == expected["mrc"]["dialogues"]
        ),
        "mrc_edus_all_match_dp": (
            state["mrc_edu_exact_dp_matches"] == state["mrc_dialogues"]
            and state["mrc_edu_missing_dp_matches"] == 0
        ),
        "mrc_partitions_match_manifest": (
            state["mrc_partitions"] == expected["mrc"]["partitions"]
        ),
        "mrc_invalid_relation_endpoints_match_manifest": (
            state["mrc_invalid_relation_endpoints"]
            == expected["mrc"]["invalid_relation_endpoints"]
            and state["mrc_invalid_relation_endpoint_dialogues"]
            == expected["mrc"]["invalid_relation_endpoint_dialogues"]
        ),
        "mrc_plausible_answers_match_manifest": (
            state["mrc_plausible_answers"]
            == expected["mrc"]["plausible_answers"]
        ),
        "mrc_questions_match_manifest": (
            state["mrc_questions"] == expected["mrc"]["questions"]
        ),
        "mrc_relation_disagreements_match_manifest": (
            state["mrc_relation_graph_disagreements"]
            == expected["cross_view"]["relation_graph_disagreements"]
        ),
        "mrc_relations_match_manifest": (
            state["mrc_relations"] == expected["mrc"]["relations"]
        ),
        "mrc_turns_match_manifest": (
            state["mrc_turns"] == expected["mrc"]["turns"]
        ),
        "mrc_unanswerable_match_manifest": (
            state["mrc_unanswerable_questions"]
            == expected["mrc"]["unanswerable_questions"]
        ),
        "unit_support_equals_adapter_turns": (
            state["unit_support_total"] == state["adapter_turns"]
        ),
    }
    return {"checks": checks, "complete": all(checks.values())}


def _build_report(
    *,
    manifest: AdmissionManifest,
    source_identity: Mapping[str, Any],
    state: Mapping[str, Any],
    reconciliation: Mapping[str, Any],
) -> dict[str, Any]:
    histogram = [
        {"code_point": code_point, "occurrences": occurrences}
        for code_point, occurrences in sorted(
            state["out_of_alphabet_by_code_point"].items()
        )
    ]
    report: dict[str, Any] = {
        "admission": {
            "admission_digest": manifest.digest,
            "corpus_id": manifest.corpus_id,
            "evidence_state": manifest.payload["evidence_state"],
            "license": manifest.payload["license"],
            "status": manifest.payload["status"],
        },
        "canon_selection": None,
        "cross_view_evidence": {
            "definition": "MRC exact-EDU sequences are matched against DP; relation equality is evaluated independently and disagreement is retained",
            "mrc_dialogues_with_ambiguous_dp_edu_match": state[
                "mrc_edu_ambiguous_dp_matches"
            ],
            "mrc_dialogues_with_exact_dp_edus": state[
                "mrc_edu_exact_dp_matches"
            ],
            "mrc_dialogues_without_exact_dp_edus": state[
                "mrc_edu_missing_dp_matches"
            ],
            "relation_graph_disagreements": state[
                "mrc_relation_graph_disagreements"
            ],
            "relation_graph_matches": state["mrc_relation_graph_matches"],
        },
        "discourse_parsing_execution": {
            "adapter_turns": state["adapter_turns"],
            "code_points": state["code_points"],
            "dialogues": state["dialogues"],
            "first_dialogue_id": state["first_dialogue_id"],
            "last_dialogue_id": state["last_completed_dialogue_id"],
            "partitions": state["dp_partitions"],
            "profile_unit_support_total": state["unit_support_total"],
            "relations": state["relations"],
            "source_turns": state["source_turns"],
            "utf8_bytes": state["utf8_bytes"],
        },
        "discourse_relation_evidence": {
            "direction": {
                "same_node": state["relation_same_node"],
                "source_follows_target": state[
                    "relation_source_follows_target"
                ],
                "source_precedes_target": state[
                    "relation_source_precedes_target"
                ],
            },
            "label_counts": [
                {"label": label, "relations": count}
                for label, count in sorted(state["relation_label_counts"].items())
            ],
            "relation_digest_chain": state["relation_digest_chain"],
        },
        "failure_seeking_observations": {
            "definitions": {
                "repeated_space_excess": "SPACE code points after the first SPACE in each contiguous SPACE run",
                "relation_graph_disagreement": "identical ordered EDU objects occur in DP and MRC while the complete directed labeled relation list differs",
            },
            "answer_span_mismatches": state["answer_span_mismatches"],
            "dialogues_with_multiple_speakers": state[
                "dialogues_with_multiple_speakers"
            ],
            "empty_turns": state["empty_turns"],
            "leading_space_turns": state["leading_space_turns"],
            "mrc_invalid_relation_endpoint_dialogues": state[
                "mrc_invalid_relation_endpoint_dialogues"
            ],
            "mrc_invalid_relation_endpoints": state[
                "mrc_invalid_relation_endpoints"
            ],
            "newline_turns": state["newline_turns"],
            "non_ascii_turns": state["non_ascii_turns"],
            "out_of_alphabet": {
                "affected_turns": state["out_of_alphabet_affected_turns"],
                "affected_word_gonols": state[
                    "out_of_alphabet_affected_word_gonols"
                ],
                "by_code_point": histogram,
                "occurrences": state["out_of_alphabet_occurrences"],
                "unique_code_points": len(histogram),
            },
            "repeated_space_excess": state["repeated_space_excess"],
            "speaker_count_per_dialogue": [
                {"dialogues": count, "speakers": int(speakers)}
                for speakers, count in sorted(
                    state["speaker_count_per_dialogue"].items(),
                    key=lambda item: int(item[0]),
                )
            ],
            "source_empty_speaker_dialogues": state[
                "source_empty_speaker_dialogues"
            ],
            "source_empty_speaker_turns": state["source_empty_speaker_turns"],
            "space_boundaries": state["space_boundaries"],
            "trailing_space_turns": state["trailing_space_turns"],
            "word_gonols": state["word_gonols"],
        },
        "hmmm": manifest.payload["hmmm"],
        "identity_chains": {
            "mrc_annotation_digest_chain": state[
                "mrc_annotation_digest_chain"
            ],
            "profile_observation_digest_chain": state[
                "profile_observation_digest_chain"
            ],
            "source_dialogue_digest_chain": state[
                "source_dialogue_digest_chain"
            ],
            "turn_evidence_digest_chain": state[
                "turn_evidence_digest_chain"
            ],
        },
        "information_boundaries": manifest.payload["information_boundaries"],
        "mrc_annotation_execution": {
            "answerable_questions": state["mrc_answerable_questions"],
            "dialogues": state["mrc_dialogues"],
            "partitions": state["mrc_partitions"],
            "plausible_answers": state["mrc_plausible_answers"],
            "questions": state["mrc_questions"],
            "relations": state["mrc_relations"],
            "turns_reconciled_not_remeasured": state["mrc_turns"],
            "unanswerable_questions": state["mrc_unanswerable_questions"],
        },
        "privacy_and_removal": manifest.payload["privacy_and_removal"],
        "profile": state["profile_identity"],
        "provenance": {
            "edcm_commit": state["edcm_commit"],
            "source": source_identity,
            "ucns_commit": state["ucns_commit"],
        },
        "reconciliation": reconciliation,
        "schema_id": RUNNER_SCHEMA_ID,
        "schema_version": RUNNER_SCHEMA_VERSION,
    }
    report["report_digest"] = _digest(report)
    return report


def _build_receipt(
    *,
    manifest: AdmissionManifest,
    state: Mapping[str, Any],
    status: str,
    reconciliation: Mapping[str, Any] | None = None,
    report_digest: str | None = None,
    report_sha256: str | None = None,
    error_code: str | None = None,
    error_reason: str | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "corpus_id": manifest.corpus_id,
        "identities": {
            "admission_digest": manifest.digest,
            "edcm_commit": state.get("edcm_commit"),
            "source_commit": state.get("source_commit"),
            "ucns_commit": state.get("ucns_commit"),
        },
        "progress": {
            "active_dialogue_id": state.get("active_dialogue_id"),
            "active_dialogue_index": state.get("active_dialogue_index"),
            "active_question_index": state.get("active_question_index"),
            "active_relation_index": state.get("active_relation_index"),
            "active_split": state.get("active_split"),
            "active_turn_index": state.get("active_turn_index"),
            "active_variant": state.get("active_variant"),
            "adapter_turns": state.get("adapter_turns", 0),
            "dp_dialogues": state.get("dialogues", 0),
            "dp_relations": state.get("relations", 0),
            "dp_source_turns": state.get("source_turns", 0),
            "last_completed_dialogue_id": state.get(
                "last_completed_dialogue_id"
            ),
            "last_completed_dialogue_index": state.get(
                "last_completed_dialogue_index"
            ),
            "last_completed_split": state.get("last_completed_split"),
            "mrc_dialogues": state.get("mrc_dialogues", 0),
            "mrc_questions": state.get("mrc_questions", 0),
        },
        "raw_source_in_git": False,
        "reconciliation": reconciliation,
        "report_digest": report_digest,
        "report_sha256": report_sha256,
        "schema_id": RECEIPT_SCHEMA_ID,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "status": status,
    }
    if error_code is not None:
        receipt["error"] = {"code": error_code, "reason": error_reason}
    receipt["receipt_digest"] = _digest(receipt)
    return receipt


def run_source(
    source_root: Path,
    *,
    adapter: ActualUCNSAdapter,
    edcm_commit: str,
    ucns_commit: str,
    manifest: AdmissionManifest | None = None,
    checkpoint_path: Path | None = None,
    checkpoint_every: int = 100,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run and reconcile every admitted Molweni DP and MRC record."""

    manifest = manifest or load_admission_manifest()
    if checkpoint_every <= 0:
        raise CorpusRunError(
            "checkpoint_every must be positive",
            code="CHECKPOINT_INTERVAL",
        )
    source_identity = _verify_source(source_root, manifest)
    expected_identity = {
        "admission_digest": manifest.digest,
        "edcm_commit": edcm_commit,
        "source_commit": str(source_identity["commit"]),
        "ucns_commit": ucns_commit,
    }
    state = (
        _load_checkpoint(checkpoint_path, expected=expected_identity)
        if checkpoint_path is not None
        else None
    )
    if state is None:
        state = _new_state(**expected_identity)

    resume_dialogues = int(state["completed_dp_dialogues"])
    verified_prefix = EMPTY_CHAIN_DIGEST
    global_dialogue_index = 0
    seen_dialogue_ids: set[str] = set()
    dp_index: dict[str, list[str]] = {}
    try:
        for split in DP_SPLITS:
            path = source_root / str(manifest.source["dp_files"][split])
            dialogues = _read_json(path, state=state)
            if not isinstance(dialogues, list):
                raise CorpusRunError(
                    "DP file top level is not a list",
                    code="DP_TOP_LEVEL",
                    state=state,
                )
            for dialogue in dialogues:
                state["active_variant"] = "DP"
                state["active_split"] = split
                state["active_dialogue_index"] = global_dialogue_index
                if not isinstance(dialogue, Mapping) or not isinstance(
                    dialogue.get("id"), str
                ):
                    raise CorpusRunError(
                        "DP dialogue has no string identifier",
                        code="DIALOGUE_ID",
                        state=state,
                    )
                dialogue_id = dialogue["id"]
                state["active_dialogue_id"] = dialogue_id
                if dialogue_id in seen_dialogue_ids:
                    raise CorpusRunError(
                        "DP dialogue identifier is duplicated",
                        code="DIALOGUE_DUPLICATE",
                        state=state,
                    )
                seen_dialogue_ids.add(dialogue_id)
                turns, _relations = _dialogue_parts(dialogue, state=state)
                edu_digest = _digest(dialogue["edus"])
                relation_digest = _digest(dialogue["relations"])
                dp_index.setdefault(edu_digest, []).append(relation_digest)
                record = {
                    "dialogue_id": dialogue_id,
                    "dialogue_index": global_dialogue_index,
                    "dialogue_sha256": _digest(dialogue),
                    "split": split,
                }
                if global_dialogue_index < resume_dialogues:
                    verified_prefix = _chain(verified_prefix, record)
                    if global_dialogue_index == resume_dialogues - 1 and (
                        verified_prefix != state["source_dialogue_digest_chain"]
                        or dialogue_id != state["last_completed_dialogue_id"]
                    ):
                        raise CorpusRunError(
                            "checkpoint source prefix does not match the admitted DP files",
                            code="CHECKPOINT_PREFIX",
                            state=state,
                        )
                else:
                    observed_edu_digest, observed_relation_digest = (
                        _observe_dp_dialogue(
                            adapter=adapter,
                            dialogue=dialogue,
                            dialogue_id=dialogue_id,
                            dialogue_index=global_dialogue_index,
                            split=split,
                            state=state,
                        )
                    )
                    if (
                        observed_edu_digest != edu_digest
                        or observed_relation_digest != relation_digest
                    ):
                        raise CorpusRunError(
                            "DP in-memory identity changed during observation",
                            code="DP_IDENTITY_DRIFT",
                            state=state,
                        )
                    if (
                        checkpoint_path is not None
                        and state["dialogues"] % checkpoint_every == 0
                    ):
                        _write_json_atomic(
                            checkpoint_path,
                            _checkpoint_payload(state),
                        )
                global_dialogue_index += 1

        if resume_dialogues > global_dialogue_index:
            raise CorpusRunError(
                "checkpoint contains more DP dialogues than the admitted source",
                code="CHECKPOINT_RANGE",
                state=state,
            )
        if checkpoint_path is not None:
            _write_json_atomic(checkpoint_path, _checkpoint_payload(state))

        _reset_mrc_state(state)
        question_ids: set[str] = set()
        for split in MRC_SPLITS:
            path = source_root / str(manifest.source["mrc_files"][split])
            payload = _read_json(path, state=state)
            if (
                not isinstance(payload, Mapping)
                or not isinstance(payload.get("data"), Mapping)
                or payload["data"].get("title") != split
                or not isinstance(payload["data"].get("dialogues"), list)
            ):
                raise CorpusRunError(
                    "MRC top-level data, title, or dialogues shape is invalid",
                    code="MRC_TOP_LEVEL",
                    state=state,
                )
            for dialogue_index, dialogue in enumerate(
                payload["data"]["dialogues"]
            ):
                _observe_mrc_dialogue(
                    dialogue=dialogue,
                    dialogue_index=dialogue_index,
                    dp_index=dp_index,
                    question_ids=question_ids,
                    split=split,
                    state=state,
                )

        reconciliation = _reconciliation(state, manifest)
        if not reconciliation["complete"]:
            raise CorpusRunError(
                "full-corpus reconciliation failed",
                code="RECONCILIATION_FAILED",
                state=state,
            )
        report = _build_report(
            manifest=manifest,
            source_identity=source_identity,
            state=state,
            reconciliation=reconciliation,
        )
        report_text = json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"
        receipt = _build_receipt(
            manifest=manifest,
            state=state,
            status="complete",
            reconciliation=reconciliation,
            report_digest=report["report_digest"],
            report_sha256=sha256(report_text.encode("utf-8")).hexdigest(),
        )
        if checkpoint_path is not None:
            _write_json_atomic(checkpoint_path, _checkpoint_payload(state))
        return report, receipt
    except CorpusRunError as exc:
        if exc.state:
            raise
        raise CorpusRunError(
            str(exc),
            code=exc.code,
            state=state,
        ) from exc
    except Exception as exc:
        raise CorpusRunError(
            f"{type(exc).__name__}: {exc}",
            code="UNEXPECTED_FAILURE",
            state=state,
        ) from exc


def _incomplete_receipt(
    *,
    manifest: AdmissionManifest,
    error: CorpusRunError,
    edcm_commit: str | None,
    source_root: Path,
    ucns_commit: str,
) -> dict[str, Any]:
    state = dict(error.state)
    state.setdefault("admission_digest", manifest.digest)
    state.setdefault("edcm_commit", edcm_commit)
    state.setdefault("source_commit", manifest.source["commit"])
    state.setdefault("ucns_commit", ucns_commit)
    receipt = _build_receipt(
        manifest=manifest,
        state=state,
        status="incomplete",
        error_code=error.code,
        error_reason=str(error),
    )
    receipt["source_checkout_name"] = source_root.name
    receipt["receipt_digest"] = _digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    return receipt


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--ucns-source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-every", type=int, default=100)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest = load_admission_manifest()
    repository_root = Path(__file__).resolve().parents[2]
    edcm_commit: str | None = None
    try:
        edcm_commit = _git_commit(repository_root, require_clean=True)
        adapter = _load_pinned_adapter(args.ucns_source_root.resolve())
        report, receipt = run_source(
            args.source_root.resolve(),
            adapter=adapter,
            edcm_commit=edcm_commit,
            ucns_commit=PINNED_UCNS_COMMIT,
            manifest=manifest,
            checkpoint_path=(
                args.checkpoint.resolve() if args.checkpoint is not None else None
            ),
            checkpoint_every=args.checkpoint_every,
        )
        _write_json_atomic(args.output.resolve(), report)
        _write_json_atomic(args.receipt.resolve(), receipt)
        print(
            json.dumps(
                {
                    "dialogues": report["discourse_parsing_execution"][
                        "dialogues"
                    ],
                    "questions": report["mrc_annotation_execution"]["questions"],
                    "receipt": str(args.receipt),
                    "relations": report["discourse_parsing_execution"][
                        "relations"
                    ],
                    "report": str(args.output),
                    "status": "complete",
                    "turns": report["discourse_parsing_execution"][
                        "source_turns"
                    ],
                },
                sort_keys=True,
            )
        )
        return 0
    except CorpusRunError as exc:
        receipt = _incomplete_receipt(
            manifest=manifest,
            error=exc,
            edcm_commit=edcm_commit,
            source_root=args.source_root,
            ucns_commit=PINNED_UCNS_COMMIT,
        )
        _write_json_atomic(args.receipt.resolve(), receipt)
        print(
            json.dumps(
                {
                    "error_code": exc.code,
                    "reason": str(exc),
                    "receipt": str(args.receipt),
                    "status": "incomplete",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
