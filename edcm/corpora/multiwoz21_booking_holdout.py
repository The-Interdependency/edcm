"""Sealed EDCM-only MultiWOZ 2.1 booking-outcome holdout runner.

Usage guidance
--------------
Keep the admitted Cambridge archive outside Git. From a clean EDCM producer
commit, run:

    python -m edcm.corpora.multiwoz21_booking_holdout \
      --archive /path/to/MULTIWOZ2.1.zip \
      --edcm-repository-root /path/to/edcm \
      --edcm-commit "$(git rev-parse HEAD)" \
      --output /tmp/multiwoz-booking-holdout.json \
      --receipt /tmp/multiwoz-booking-holdout-complete.json

The source-native ``Booking-Book`` and ``Booking-NoBook`` system-act labels
are targets only. The labelled response, later turns, goals, metadata,
dialogue acts, ontology, and databases never enter the candidate measurement.
Only aggregate evidence and content identities are written; raw dialogue text
stays outside Git.
"""

# === MODULE_BUILD ===
# id: edcm_multiwoz21_booking_outcome_holdout
#   module_name: multiwoz21_booking_holdout
#   module_kind: experiment
#   summary: evaluates the maintained EDCM terminal-progress candidate against externally authored MultiWOZ 2.1 booking outcome events after development calibration and validation threshold freeze
#   owner: Erin Spencer
#   public_surface: OutcomeEvent, PlattCalibration, fit_platt_calibration, select_operating_threshold, evaluate_outcomes, run_holdout, main
#   internal_surface: _bootstrap_intervals, _build_report, _candidate_score, _confusion, _ece10, _extract_partition, _verify_represented_evidence_seal, _wilson_interval
#   auth_boundary: none
#   storage_boundary: reads a caller-held admitted archive plus tracked represented-evidence seals and writes caller-selected aggregate report and receipt paths
#   network_boundary: none; source acquisition and publication are separate
#   user_data_boundary: exact source turns and dialogue ids are processed in memory but written outputs contain only aggregates and cryptographic chains
#   admin_only: false
#   tests: tests.test_multiwoz21_booking_holdout
#   rollout: explicit sealed experiment command only; no default measurement, production activation, or canon selection
#   rollback: remove the experiment module and supersede its aggregate evidence by identity; raw source remains outside Git
#   requires: edcm_multiwoz21_corpus, edcmbone_parser_turns_rounds, edcmbone_metrics_compute, ucns.profile.edcm-word-gonol at a98c9e6c69804a8a08d0786b1d8b450bb2c49a97
#   since: 2026-08-02
#   unresolved: externally hidden holdout custody, independent human task-success adjudication, formal higher-gonol composition, independent replication, and joint canon authority
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: multiwoz_booking_outcome_labelled_response_is_withheld
#   given: a source dialogue-act turn contains exactly one admitted booking outcome label
#   then: candidate measurement consumes only exact preceding data.json turns and never the labelled system response, later text, labels, goals, metadata, ontology, or databases
#   class: safety
#   since: 2026-08-02
#
# id: multiwoz_booking_outcome_calibration_precedes_test
#   given: admitted development, validation, and test outcome events
#   then: development alone fits the Platt map, validation alone selects the threshold, and the frozen calibration digest exists before test evaluation
#   class: evidence
#   since: 2026-08-02
#
# id: multiwoz_booking_outcome_report_is_aggregate_only
#   given: the holdout run completes or fails
#   then: written report and receipt contain aggregate counts, metrics, boundaries, and identities but no dialogue ids, source turns, normalized turns, per-event scores, or slot values
#   class: privacy
#   since: 2026-08-02
#
# id: multiwoz_booking_outcome_uncertainty_is_cluster_aware
#   given: repeated source outcome events may share one dialogue
#   then: sensitivity and specificity carry Wilson intervals while balanced accuracy, Brier score, and ECE carry deterministic dialogue-cluster bootstrap intervals
#   class: evidence
#   since: 2026-08-02
#
# id: multiwoz_booking_outcome_hypothesis_failure_is_evidence
#   given: a frozen sensitivity, specificity, discrimination, or calibration hypothesis is not met
#   then: the report records a falsified finding without converting that scientific result into an execution failure
#   class: evidence
#   since: 2026-08-02
#
# id: multiwoz_booking_outcome_status_does_not_transfer
#   given: the admitted archive, exact UCNS represented-evidence seal, and candidate EDCM report reconcile
#   then: canon selection remains null, formal geometry and higher-gonol composition remain NA, production activation remains inactive, and proof, theorem, measurement-validity, semantic-authority, certification, and empirical status do not transfer
#   class: doctrine
#   since: 2026-08-02
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from edcm.measurement.metrics.compute import compute_transcript
from edcm.measurement.parser.turns_rounds import parse_transcript

from .multiwoz21 import (
    CorpusRunError,
    _archive_identity,
    _git_commit,
    _git_tree_identity,
    _load_partition_ids,
    _write_json_atomic,
    load_admission_manifest,
)


SCHEMA_ID = "edcm.multiwoz21-booking-outcome-holdout"
SCHEMA_VERSION = "0.1.0"
RECEIPT_SCHEMA_ID = "edcm.multiwoz21-booking-outcome-holdout-receipt"
RECEIPT_SCHEMA_VERSION = "0.1.0"
CANDIDATE_ID = "edcm.maintained-terminal-progress/0.1.0"
POSITIVE_LABEL = "Booking-Book"
NEGATIVE_LABEL = "Booking-NoBook"
PINNED_UCNS_COMMIT = "a98c9e6c69804a8a08d0786b1d8b450bb2c49a97"
PINNED_SKILL_LIB_COMMIT = "2b24be24947223b86440f59f1bd9766130f9cc11"
ARCHIVE_SHA256 = "d377a176f5ec82dc9f6a97e4653d4eddc6cad917704c1aaaa5a8ee3e79f63a8e"
REPRESENTED_REPORT_PATH = Path(
    "experiments/corpora/results/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-full.json"
)
REPRESENTED_RECEIPT_PATH = Path(
    "experiments/corpora/receipts/2026-08-01-multiwoz-2.1-ucns-v0.19-integrated-complete.json"
)
REPRESENTED_REPORT_FILE_SHA256 = "e228b9cb74c60ec4d6efb66f1d86c38069f613a875fa4c91f2973b46d20436f6"
REPRESENTED_RECEIPT_FILE_SHA256 = "8d20f99f3f788e09e9edad40f7d28a2b97de9d634868652bd058e50d504fe9c9"
REPRESENTED_REPORT_DIGEST = "ddc0996126bd4903ca3ec08b043f2b949bcc3bed9077f01d7a609e3e54e3b03d"
REPRESENTED_UCNS_RECEIPT_ID = "921ceacad026de1d884eec3e049b090246014706c937c062bd32f40bbff01f0c"
EMPTY_CHAIN_DIGEST = sha256(b"").hexdigest()
PLATT_RIDGE = 1e-6
PLATT_MAX_ITERATIONS = 100
PLATT_TOLERANCE = 1e-12
BOOTSTRAP_REPLICATES = 2000
BOOTSTRAP_SEED = 20260802
EXPECTED_EVENT_COUNTS = {
    "development": {"negative": 1050, "positive": 4164, "excluded_ambiguous": 19},
    "validation": {"negative": 113, "positive": 543, "excluded_ambiguous": 0},
    "test": {"negative": 131, "positive": 530, "excluded_ambiguous": 0},
}


class OutcomeHoldoutError(RuntimeError):
    """Fail-closed experiment error with a non-source-text code."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical_bytes(value)).hexdigest()


def _chain(previous: str, record: Any) -> str:
    return sha256(bytes.fromhex(previous) + _canonical_bytes(record)).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def _sigmoid(value: float) -> float:
    if value >= 0:
        return 1.0 / (1.0 + math.exp(-min(value, 709.0)))
    exp_value = math.exp(max(value, -709.0))
    return exp_value / (1.0 + exp_value)


@dataclass(frozen=True)
class OutcomeEvent:
    """One in-memory event; identity and raw locators are never serialized."""

    dialogue_id: str
    source_turn_id: int
    label: int
    score: float
    context_turn_count: int


@dataclass(frozen=True)
class PlattCalibration:
    """Frozen development-only standardization and logistic coefficients."""

    score_mean: float
    score_population_stddev: float
    intercept: float
    slope: float
    iterations: int
    converged: bool
    ridge: float = PLATT_RIDGE

    def probability(self, score: float) -> float:
        z_score = (score - self.score_mean) / self.score_population_stddev
        return _sigmoid(self.intercept + self.slope * z_score)

    def as_dict(self) -> dict[str, Any]:
        return {
            "converged": self.converged,
            "intercept": self.intercept,
            "iterations": self.iterations,
            "ridge": self.ridge,
            "score_mean": self.score_mean,
            "score_population_stddev": self.score_population_stddev,
            "slope": self.slope,
        }


def fit_platt_calibration(events: Sequence[OutcomeEvent]) -> PlattCalibration:
    """Fit the frozen two-parameter Platt map on development events only."""

    if not events or {event.label for event in events} != {0, 1}:
        raise OutcomeHoldoutError(
            "development calibration requires both source outcome classes",
            code="CALIBRATION_CLASSES",
        )
    scores = [event.score for event in events]
    mean = statistics.fmean(scores)
    stddev = statistics.pstdev(scores)
    if not math.isfinite(stddev) or stddev <= 0.0:
        raise OutcomeHoldoutError(
            "development score variance must be positive",
            code="CALIBRATION_VARIANCE",
        )
    x_values = [(score - mean) / stddev for score in scores]
    y_values = [event.label for event in events]
    positives = sum(y_values)
    negatives = len(y_values) - positives
    intercept = math.log((positives + 0.5) / (negatives + 0.5))
    slope = 0.0
    converged = False
    iterations = 0
    for iterations in range(1, PLATT_MAX_ITERATIONS + 1):
        probabilities = [
            _sigmoid(intercept + slope * x_value) for x_value in x_values
        ]
        weights = [max(probability * (1.0 - probability), 1e-15) for probability in probabilities]
        gradient_intercept = sum(
            probability - label
            for probability, label in zip(probabilities, y_values, strict=True)
        )
        gradient_slope = sum(
            (probability - label) * x_value
            for probability, label, x_value in zip(
                probabilities, y_values, x_values, strict=True
            )
        ) + PLATT_RIDGE * slope
        h_00 = sum(weights)
        h_01 = sum(
            weight * x_value
            for weight, x_value in zip(weights, x_values, strict=True)
        )
        h_11 = sum(
            weight * x_value * x_value
            for weight, x_value in zip(weights, x_values, strict=True)
        ) + PLATT_RIDGE
        determinant = h_00 * h_11 - h_01 * h_01
        if determinant <= 0.0 or not math.isfinite(determinant):
            raise OutcomeHoldoutError(
                "Platt Hessian is singular",
                code="CALIBRATION_SINGULAR",
            )
        delta_intercept = (
            h_11 * gradient_intercept - h_01 * gradient_slope
        ) / determinant
        delta_slope = (
            -h_01 * gradient_intercept + h_00 * gradient_slope
        ) / determinant
        intercept -= delta_intercept
        slope -= delta_slope
        if max(abs(delta_intercept), abs(delta_slope)) <= PLATT_TOLERANCE:
            converged = True
            break
    if not converged:
        raise OutcomeHoldoutError(
            "Platt calibration did not converge",
            code="CALIBRATION_CONVERGENCE",
        )
    return PlattCalibration(
        score_mean=mean,
        score_population_stddev=stddev,
        intercept=intercept,
        slope=slope,
        iterations=iterations,
        converged=True,
    )


def _confusion(
    labelled_probabilities: Sequence[tuple[int, float]],
    threshold: float,
) -> dict[str, int]:
    counts = {
        "true_positive": 0,
        "false_positive": 0,
        "false_negative": 0,
        "true_negative": 0,
    }
    for label, probability in labelled_probabilities:
        predicted = int(probability >= threshold)
        if label == 1 and predicted == 1:
            counts["true_positive"] += 1
        elif label == 0 and predicted == 1:
            counts["false_positive"] += 1
        elif label == 1:
            counts["false_negative"] += 1
        else:
            counts["true_negative"] += 1
    return counts


def _rates(counts: Mapping[str, int]) -> tuple[float, float, float]:
    positive_total = counts["true_positive"] + counts["false_negative"]
    negative_total = counts["true_negative"] + counts["false_positive"]
    if positive_total == 0 or negative_total == 0:
        raise OutcomeHoldoutError(
            "evaluation requires both source outcome classes",
            code="EVALUATION_CLASSES",
        )
    sensitivity = counts["true_positive"] / positive_total
    specificity = counts["true_negative"] / negative_total
    return sensitivity, specificity, (sensitivity + specificity) / 2.0


def select_operating_threshold(
    events: Sequence[OutcomeEvent],
    calibration: PlattCalibration,
) -> tuple[float, dict[str, int], int]:
    """Select one validation threshold by balanced accuracy and frozen ties."""

    probabilities = [calibration.probability(event.score) for event in events]
    unique = sorted(set(probabilities))
    candidates = {0.0, 1.0, *unique}
    candidates.update(
        (left + right) / 2.0 for left, right in zip(unique, unique[1:])
    )
    labelled = [(event.label, probability) for event, probability in zip(events, probabilities, strict=True)]
    ranked: list[tuple[float, float, float, dict[str, int]]] = []
    for threshold in sorted(candidates):
        counts = _confusion(labelled, threshold)
        _, _, balanced_accuracy = _rates(counts)
        ranked.append(
            (
                -balanced_accuracy,
                abs(threshold - 0.5),
                threshold,
                counts,
            )
        )
    _, _, threshold, counts = min(ranked, key=lambda value: value[:3])
    return threshold, counts, len(candidates)


def _wilson_interval(successes: int, total: int) -> dict[str, Any]:
    if total <= 0:
        raise OutcomeHoldoutError(
            "Wilson interval requires positive support",
            code="UNCERTAINTY_SUPPORT",
        )
    z_value = 1.959963984540054
    estimate = successes / total
    denominator = 1.0 + z_value * z_value / total
    centre = (estimate + z_value * z_value / (2.0 * total)) / denominator
    half_width = (
        z_value
        * math.sqrt(
            estimate * (1.0 - estimate) / total
            + z_value * z_value / (4.0 * total * total)
        )
        / denominator
    )
    return {
        "confidence": 0.95,
        "high": min(1.0, centre + half_width),
        "low": max(0.0, centre - half_width),
        "method": "wilson-score",
        "support": total,
    }


def _ece10(labelled_probabilities: Sequence[tuple[int, float]]) -> float:
    bins: list[list[tuple[int, float]]] = [[] for _ in range(10)]
    for label, probability in labelled_probabilities:
        bin_index = min(9, int(probability * 10.0))
        bins[bin_index].append((label, probability))
    total = len(labelled_probabilities)
    return sum(
        len(bin_values)
        / total
        * abs(
            statistics.fmean(probability for _, probability in bin_values)
            - statistics.fmean(label for label, _ in bin_values)
        )
        for bin_values in bins
        if bin_values
    )


def _brier(labelled_probabilities: Sequence[tuple[int, float]]) -> float:
    return statistics.fmean(
        (probability - label) ** 2
        for label, probability in labelled_probabilities
    )


def _percentile(values: Sequence[float], quantile: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def _bootstrap_intervals(
    events: Sequence[OutcomeEvent],
    calibration: PlattCalibration,
    threshold: float,
) -> dict[str, dict[str, Any]]:
    clusters: dict[str, list[tuple[int, float]]] = defaultdict(list)
    for event in events:
        clusters[event.dialogue_id].append(
            (event.label, calibration.probability(event.score))
        )
    cluster_ids = sorted(clusters)
    rng = random.Random(BOOTSTRAP_SEED)
    samples: dict[str, list[float]] = {
        "balanced_accuracy": [],
        "brier_score": [],
        "ece_10": [],
    }
    for _ in range(BOOTSTRAP_REPLICATES):
        selected = [rng.choice(cluster_ids) for _ in cluster_ids]
        labelled = [item for cluster_id in selected for item in clusters[cluster_id]]
        counts = _confusion(labelled, threshold)
        try:
            _, _, balanced_accuracy = _rates(counts)
        except OutcomeHoldoutError:
            continue
        samples["balanced_accuracy"].append(balanced_accuracy)
        samples["brier_score"].append(_brier(labelled))
        samples["ece_10"].append(_ece10(labelled))
    if any(not values for values in samples.values()):
        raise OutcomeHoldoutError(
            "cluster bootstrap produced no valid replicates",
            code="UNCERTAINTY_BOOTSTRAP",
        )
    return {
        metric: {
            "cluster_count": len(cluster_ids),
            "confidence": 0.95,
            "high": _percentile(values, 0.975),
            "low": _percentile(values, 0.025),
            "method": "dialogue-cluster-percentile-bootstrap",
            "replicates_requested": BOOTSTRAP_REPLICATES,
            "replicates_valid": len(values),
            "seed": BOOTSTRAP_SEED,
        }
        for metric, values in samples.items()
    }


def evaluate_outcomes(
    events: Sequence[OutcomeEvent],
    calibration: PlattCalibration,
    threshold: float,
) -> dict[str, Any]:
    """Evaluate aggregate confusion, discrimination, calibration, and intervals."""

    labelled = [
        (event.label, calibration.probability(event.score)) for event in events
    ]
    counts = _confusion(labelled, threshold)
    sensitivity, specificity, balanced_accuracy = _rates(counts)
    intervals = _bootstrap_intervals(events, calibration, threshold)
    return {
        "balanced_accuracy": {
            "estimate": balanced_accuracy,
            "interval": intervals["balanced_accuracy"],
        },
        "brier_score": {
            "estimate": _brier(labelled),
            "interval": intervals["brier_score"],
        },
        "calibration_error": {
            "bins": 10,
            "estimate": _ece10(labelled),
            "interval": intervals["ece_10"],
            "metric": "expected-calibration-error",
        },
        "confusion_counts": counts,
        "sensitivity": {
            "estimate": sensitivity,
            "interval": _wilson_interval(
                counts["true_positive"],
                counts["true_positive"] + counts["false_negative"],
            ),
        },
        "specificity": {
            "estimate": specificity,
            "interval": _wilson_interval(
                counts["true_negative"],
                counts["true_negative"] + counts["false_positive"],
            ),
        },
    }


def _candidate_score(context_turns: Sequence[str]) -> float:
    lines = []
    for turn_index, text in enumerate(context_turns):
        speaker = "USER" if turn_index % 2 == 0 else "SYSTEM"
        presentation = text.replace("\r", " ").replace("\n", " ")
        lines.append(f"{speaker}: {presentation}")
    parsed = parse_transcript("\n".join(lines), round_strategy="cycle")
    metrics = compute_transcript(parsed)
    if not metrics:
        raise OutcomeHoldoutError(
            "candidate context produced no EDCM rounds",
            code="CANDIDATE_EMPTY",
        )
    score = float(metrics[-1].P)
    if not math.isfinite(score) or not 0.0 <= score <= 1.0:
        raise OutcomeHoldoutError(
            "terminal progress score is outside [0,1]",
            code="CANDIDATE_RANGE",
        )
    return score


def _partition_name(
    dialogue_id: str,
    test_ids: set[str],
    validation_ids: set[str],
) -> str:
    base = dialogue_id[:-5] if dialogue_id.endswith(".json") else dialogue_id
    if base in test_ids or dialogue_id in test_ids:
        return "test"
    if base in validation_ids or dialogue_id in validation_ids:
        return "validation"
    return "development"


def _source_turn_sort_key(item: tuple[Any, Any]) -> tuple[int, int | str]:
    try:
        return (0, int(item[0]))
    except (TypeError, ValueError):
        return (1, str(item[0]))


def _extract_partition(
    *,
    partition: str,
    data: Mapping[str, Any],
    dialogue_acts: Mapping[str, Any],
    test_ids: set[str],
    validation_ids: set[str],
    score_fn: Callable[[Sequence[str]], float] = _candidate_score,
) -> tuple[list[OutcomeEvent], dict[str, Any]]:
    events: list[OutcomeEvent] = []
    source_chain = EMPTY_CHAIN_DIGEST
    candidate_chain = EMPTY_CHAIN_DIGEST
    excluded_ambiguous = 0
    context_turns_total = 0
    dialogue_count = 0
    dialogues_with_events: set[str] = set()
    for dialogue_id, dialogue in data.items():
        if _partition_name(dialogue_id, test_ids, validation_ids) != partition:
            continue
        dialogue_count += 1
        if not isinstance(dialogue, Mapping) or not isinstance(dialogue.get("log"), list):
            raise OutcomeHoldoutError(
                "data.json dialogue has invalid log structure",
                code="SOURCE_DIALOGUE_SCHEMA",
            )
        base = dialogue_id[:-5] if dialogue_id.endswith(".json") else dialogue_id
        turn_acts = dialogue_acts.get(base, dialogue_acts.get(dialogue_id))
        if not isinstance(turn_acts, Mapping):
            raise OutcomeHoldoutError(
                "dialogue_acts.json is missing a dialogue mapping",
                code="SOURCE_ACT_SCHEMA",
            )
        log = dialogue["log"]
        for source_turn_id_text, act_payload in sorted(
            turn_acts.items(), key=_source_turn_sort_key
        ):
            if not isinstance(act_payload, Mapping):
                continue
            labels = {POSITIVE_LABEL, NEGATIVE_LABEL}.intersection(act_payload)
            if not labels:
                continue
            if len(labels) == 2:
                excluded_ambiguous += 1
                continue
            try:
                source_turn_id = int(source_turn_id_text)
            except (TypeError, ValueError) as exc:
                raise OutcomeHoldoutError(
                    "booking outcome turn id is not a decimal integer",
                    code="SOURCE_TURN_ID",
                ) from exc
            response_index = 2 * source_turn_id - 1
            if source_turn_id <= 0 or response_index >= len(log) or response_index % 2 != 1:
                raise OutcomeHoldoutError(
                    "booking outcome turn id does not map to an in-range system response",
                    code="SOURCE_TURN_MAPPING",
                )
            context: list[str] = []
            context_chain = EMPTY_CHAIN_DIGEST
            for turn_index, turn in enumerate(log[:response_index]):
                if not isinstance(turn, Mapping) or not isinstance(turn.get("text"), str):
                    raise OutcomeHoldoutError(
                        "candidate context contains a non-string source turn",
                        code="SOURCE_TURN_SCHEMA",
                    )
                text = turn["text"]
                context.append(text)
                text_bytes = text.encode("utf-8")
                context_chain = _chain(
                    context_chain,
                    {
                        "speaker": "user" if turn_index % 2 == 0 else "system",
                        "text_code_points": len(text),
                        "text_sha256": sha256(text_bytes).hexdigest(),
                        "text_utf8_bytes": len(text_bytes),
                        "turn_index": turn_index,
                    },
                )
            response = log[response_index]
            if not isinstance(response, Mapping) or not isinstance(response.get("text"), str):
                raise OutcomeHoldoutError(
                    "labelled response contains a non-string source turn",
                    code="SOURCE_TURN_SCHEMA",
                )
            label = int(POSITIVE_LABEL in labels)
            score = score_fn(tuple(context))
            event = OutcomeEvent(
                dialogue_id=dialogue_id,
                source_turn_id=source_turn_id,
                label=label,
                score=score,
                context_turn_count=len(context),
            )
            events.append(event)
            dialogues_with_events.add(dialogue_id)
            context_turns_total += len(context)
            response_bytes = response["text"].encode("utf-8")
            event_locator_digest = _digest(
                {"dialogue_id": dialogue_id, "source_turn_id": source_turn_id}
            )
            source_chain = _chain(
                source_chain,
                {
                    "context_chain": context_chain,
                    "context_turn_count": len(context),
                    "event_locator_digest": event_locator_digest,
                    "label": POSITIVE_LABEL if label else NEGATIVE_LABEL,
                    "response_index": response_index,
                    "response_text_sha256": sha256(response_bytes).hexdigest(),
                },
            )
            presentation_digest = sha256(
                "\n".join(
                    f"{'USER' if index % 2 == 0 else 'SYSTEM'}: "
                    + text.replace("\r", " ").replace("\n", " ")
                    for index, text in enumerate(context)
                ).encode("utf-8")
            ).hexdigest()
            candidate_chain = _chain(
                candidate_chain,
                {
                    "context_turn_count": len(context),
                    "event_locator_digest": event_locator_digest,
                    "presentation_sha256": presentation_digest,
                    "score": score,
                },
            )
    counts = Counter(event.label for event in events)
    return events, {
        "candidate_input_digest_chain": candidate_chain,
        "context_turns": context_turns_total,
        "dialogues": dialogue_count,
        "dialogues_with_events": len(dialogues_with_events),
        "excluded_ambiguous": excluded_ambiguous,
        "negative": counts[0],
        "positive": counts[1],
        "source_event_digest_chain": source_chain,
    }


def _load_json_member(archive: ZipFile, member: str) -> Mapping[str, Any]:
    try:
        payload = json.loads(archive.read(member).decode("utf-8", errors="strict"))
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OutcomeHoldoutError(
            "admitted JSON member cannot be decoded",
            code="SOURCE_JSON",
        ) from exc
    if not isinstance(payload, Mapping):
        raise OutcomeHoldoutError(
            "admitted JSON member is not a top-level object",
            code="SOURCE_JSON_SCHEMA",
        )
    return payload


def _verify_represented_evidence_seal(repository_root: Path) -> dict[str, Any]:
    report_path = repository_root / REPRESENTED_REPORT_PATH
    receipt_path = repository_root / REPRESENTED_RECEIPT_PATH
    if (
        _file_sha256(report_path) != REPRESENTED_REPORT_FILE_SHA256
        or _file_sha256(receipt_path) != REPRESENTED_RECEIPT_FILE_SHA256
    ):
        raise OutcomeHoldoutError(
            "pinned represented-evidence seal file identity differs",
            code="REPRESENTED_SEAL_FILE",
        )
    report = json.loads(report_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks = (
        report.get("schema_id") == "edcm.multiwoz21-full-corpus",
        report.get("schema_version") == "1.3.0",
        report.get("canon_selection") is None,
        report.get("identities", {}).get("archive", {}).get("sha256") == ARCHIVE_SHA256,
        report.get("identities", {}).get("ucns_commit") == PINNED_UCNS_COMMIT,
        report.get("execution", {}).get("source_turns") == 143048,
        report.get("reconciliation", {}).get("complete") is True,
        receipt.get("status") == "complete",
        receipt.get("report_digest") == REPRESENTED_REPORT_DIGEST,
        receipt.get("report_sha256") == REPRESENTED_REPORT_FILE_SHA256,
        receipt.get("identities", {}).get("ucns_commit") == PINNED_UCNS_COMMIT,
        receipt.get("ucns_full_corpus", {}).get("status") == "complete",
        receipt.get("ucns_full_corpus", {}).get("receipt_id") == REPRESENTED_UCNS_RECEIPT_ID,
    )
    if not all(checks):
        raise OutcomeHoldoutError(
            "pinned represented-evidence seal does not reconcile",
            code="REPRESENTED_SEAL_SCHEMA",
        )
    return {
        "profile_id": report["profile"]["profile_id"],
        "profile_version": report["profile"]["profile_version"],
        "report_digest": REPRESENTED_REPORT_DIGEST,
        "report_file_sha256": REPRESENTED_REPORT_FILE_SHA256,
        "receipt_file_sha256": REPRESENTED_RECEIPT_FILE_SHA256,
        "source_turns": 143048,
        "ucns_commit": PINNED_UCNS_COMMIT,
        "ucns_receipt_id": REPRESENTED_UCNS_RECEIPT_ID,
    }


def _score_summary(events: Sequence[OutcomeEvent]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for label, name in ((0, "negative"), (1, "positive")):
        values = [event.score for event in events if event.label == label]
        summary[name] = {
            "count": len(values),
            "maximum": max(values),
            "mean": statistics.fmean(values),
            "minimum": min(values),
            "population_stddev": statistics.pstdev(values),
        }
    return summary


def _work_graph(edcm_commit: str, edcm_tree: str) -> dict[str, Any]:
    repositories = [
        {
            "authority": "candidate measurement implementation and aggregate evidence",
            "commit": edcm_commit,
            "relation": f"producer edcm-tree={edcm_tree}",
            "repository": "The-Interdependency/edcm",
        },
        {
            "authority": "exact word-gonol observation profile and full-corpus receipt",
            "commit": PINNED_UCNS_COMMIT,
            "relation": "represented-evidence provenance only; no candidate-score authority",
            "repository": "The-Interdependency/ucns",
        },
        {
            "authority": "build, metadata, contract, and evidence discipline",
            "commit": PINNED_SKILL_LIB_COMMIT,
            "relation": "pinned consumer doctrine",
            "repository": "The-Interdependency/skill-lib",
        },
        {
            "authority": "source text, outcome labels, and partition membership",
            "commit": ARCHIVE_SHA256,
            "relation": "admitted Cambridge MultiWOZ 2.1 archive identity",
            "repository": "doi:10.17863/CAM.41572",
        },
    ]
    boundaries = {
        "agent_scope": "edcm-only-booking-outcome-holdout",
        "authority_transfer": False,
        "hmmm": [
            "content digests are not producer signatures",
            "public test membership is not independently hidden custody",
        ],
        "measurement_status_transfer": False,
        "proof_status_transfer": False,
        "semantic_mapping": "external-provenance",
    }
    return {
        "boundaries": boundaries,
        "repositories": repositories,
        "schema": "the-interdependency.stack-manifest",
        "version": "1.0.0",
        "work_graph_sha256": _digest(
            {"boundaries": boundaries, "repositories": repositories}
        ),
    }


def _finding(
    finding_id: str,
    supported: bool,
    *,
    observed: Any,
    expected: str,
) -> dict[str, Any]:
    return {
        "expected": expected,
        "finding_id": finding_id,
        "observed": observed,
        "status": "supported" if supported else "falsified",
    }


def _build_report(
    *,
    archive_identity: Mapping[str, Any],
    manifest_digest: str,
    represented_seal: Mapping[str, Any],
    edcm_commit: str,
    edcm_tree: str,
    rows: Mapping[str, Sequence[OutcomeEvent]],
    inventories: Mapping[str, Mapping[str, Any]],
    calibration: PlattCalibration,
    threshold: float,
    threshold_candidates: int,
    validation_counts: Mapping[str, int],
    calibration_digest: str,
    test_evaluation: Mapping[str, Any],
) -> dict[str, Any]:
    sensitivity = test_evaluation["sensitivity"]["estimate"]
    specificity = test_evaluation["specificity"]["estimate"]
    balanced_accuracy = test_evaluation["balanced_accuracy"]["estimate"]
    calibration_error = test_evaluation["calibration_error"]["estimate"]
    reconciliation_checks = {
        partition: {
            "excluded_ambiguous": inventory["excluded_ambiguous"]
            == EXPECTED_EVENT_COUNTS[partition]["excluded_ambiguous"],
            "negative": inventory["negative"]
            == EXPECTED_EVENT_COUNTS[partition]["negative"],
            "positive": inventory["positive"]
            == EXPECTED_EVENT_COUNTS[partition]["positive"],
        }
        for partition, inventory in inventories.items()
    }
    all_reconciled = all(
        value for checks in reconciliation_checks.values() for value in checks.values()
    )
    findings = [
        _finding(
            "test-sensitivity-at-least-half",
            sensitivity >= 0.5,
            observed=sensitivity,
            expected=">= 0.50",
        ),
        _finding(
            "test-specificity-at-least-half",
            specificity >= 0.5,
            observed=specificity,
            expected=">= 0.50",
        ),
        _finding(
            "test-balanced-accuracy-above-chance",
            balanced_accuracy > 0.5,
            observed=balanced_accuracy,
            expected="> 0.50",
        ),
        _finding(
            "test-ece-at-most-one-tenth",
            calibration_error <= 0.1,
            observed=calibration_error,
            expected="<= 0.10",
        ),
        _finding(
            "source-and-leakage-boundary-reconciled",
            all_reconciled,
            observed=reconciliation_checks,
            expected="all frozen partition, class, exclusion, and input-boundary checks true",
        ),
        _finding(
            "byte-identical-render-repeat",
            True,
            observed="two canonical render operations are byte-identical; full command repeat is a release gate",
            expected="byte-identical aggregate serialization",
        ),
    ]
    report = {
        "admission": {
            "admission_digest": manifest_digest,
            "archive": dict(archive_identity),
            "corpus_id": "multiwoz-2.1",
        },
        "calibration": {
            "calibration_digest": calibration_digest,
            "development_fit": calibration.as_dict(),
            "fit_partition": "development",
            "operating_threshold": threshold,
            "selection_objective": "maximum-balanced-accuracy",
            "selection_partition": "validation",
            "threshold_candidate_count": threshold_candidates,
            "tie_break": ["closest-to-0.5", "lowest-threshold"],
            "validation_confusion_counts": dict(validation_counts),
        },
        "candidate": {
            "candidate_id": CANDIDATE_ID,
            "candidate_measurement_status": "candidate-measured-evidence",
            "input": "preceding-turns-only",
            "metric": "terminal-P-progress-proxy",
            "presentation_transform": "speaker-prefix; each CR and LF mapped to SPACE for maintained parser only",
            "source_label_is_predictor_input": False,
            "source_response_is_predictor_input": False,
        },
        "canon_selection": None,
        "findings": findings,
        "hmmm": [
            "The public test partition is identity-sealed but not hidden by an external custodian.",
            "Dialogue acts are externally authored source labels, not independent human adjudications of universal task success.",
            "The maintained progress proxy is lexical/statistical and may not discriminate booking outcomes.",
            "Formal higher-gonol composition, signed producer authentication, independent replication, and joint canon authority remain unresolved.",
        ],
        "identities": {
            "edcm_commit": edcm_commit,
            "edcm_tree": edcm_tree,
            "represented_evidence_seal": dict(represented_seal),
            "ucns_commit": PINNED_UCNS_COMMIT,
        },
        "information_boundaries": {
            "candidate_noninputs": [
                "labelled-system-response",
                "later-turns",
                "dialogue-act-payload",
                "goal",
                "turn-metadata",
                "ontology",
                "domain-databases",
            ],
            "raw_corpus_in_git": False,
            "written_event_locators": False,
            "written_per_event_labels": False,
            "written_per_event_scores": False,
            "written_source_text": False,
        },
        "partitions": {
            partition: {
                **dict(inventories[partition]),
                "score_summary_by_source_class": _score_summary(rows[partition]),
            }
            for partition in ("development", "validation", "test")
        },
        "reconciliation": {
            "checks": reconciliation_checks,
            "complete": all_reconciled,
            "freeze_order": [
                "development-fit",
                "validation-threshold",
                "calibration-digest",
                "test-evaluation",
            ],
        },
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "source_label_policy": {
            "ambiguous_both_labels": "exclude-and-count",
            "negative": NEGATIVE_LABEL,
            "positive": POSITIVE_LABEL,
            "response_log_index": "2 * source_dialogue_act_turn_id - 1",
            "scope": "source-native-booking-action-outcome-not-universal-task-success",
        },
        "status_boundaries": {
            "certification_status_transfer": False,
            "edcm_production_activation": "inactive",
            "empirical_status_transfer": False,
            "formal_higher_gonol_composition": "NA",
            "formal_ucns_geometry": "NA",
            "measurement_validity_claim": False,
            "measurement_status_transfer": False,
            "metapat_production_activation": "inactive",
            "proof_status_transfer": False,
            "semantic_authority_transfer": False,
            "theorem_status_transfer": False,
        },
        "test_evaluation": dict(test_evaluation),
        "work_graph": _work_graph(edcm_commit, edcm_tree),
    }
    first_render = _canonical_bytes(report)
    if first_render != _canonical_bytes(json.loads(first_render)):
        raise OutcomeHoldoutError(
            "canonical report rendering is not deterministic",
            code="REPORT_DETERMINISM",
        )
    return report


def run_holdout(
    *,
    archive_path: Path,
    repository_root: Path,
    edcm_commit: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run the frozen development -> validation -> sealed-test program."""

    repository_root = repository_root.resolve()
    observed_commit = _git_commit(
        repository_root,
        require_clean=True,
        verify_tree="edcm",
        expected_commit=edcm_commit,
    )
    edcm_tree = _git_tree_identity(repository_root, "edcm", treeish=observed_commit)
    represented_seal = _verify_represented_evidence_seal(repository_root)
    manifest = load_admission_manifest()
    try:
        archive_identity, archive = _archive_identity(archive_path.resolve(), manifest)
    except CorpusRunError as exc:
        raise OutcomeHoldoutError(str(exc), code=exc.code) from exc
    try:
        test_ids = set(_load_partition_ids(archive, str(manifest.source["test_member"])))
        validation_ids = set(
            _load_partition_ids(archive, str(manifest.source["validation_member"]))
        )
        data = _load_json_member(archive, str(manifest.source["data_member"]))
        dialogue_acts = _load_json_member(
            archive, "MULTIWOZ2.1/dialogue_acts.json"
        )
    finally:
        archive.close()
    if len(data) != 10438 or len(dialogue_acts) != 10438:
        raise OutcomeHoldoutError(
            "source dialogue inventories do not match admission",
            code="SOURCE_DIALOGUE_COUNT",
        )

    rows: dict[str, Sequence[OutcomeEvent]] = {}
    inventories: dict[str, Mapping[str, Any]] = {}
    development_rows, development_inventory = _extract_partition(
        partition="development",
        data=data,
        dialogue_acts=dialogue_acts,
        test_ids=test_ids,
        validation_ids=validation_ids,
    )
    rows["development"] = development_rows
    inventories["development"] = development_inventory
    _require_expected_inventory("development", development_inventory)
    calibration = fit_platt_calibration(development_rows)

    validation_rows, validation_inventory = _extract_partition(
        partition="validation",
        data=data,
        dialogue_acts=dialogue_acts,
        test_ids=test_ids,
        validation_ids=validation_ids,
    )
    rows["validation"] = validation_rows
    inventories["validation"] = validation_inventory
    _require_expected_inventory("validation", validation_inventory)
    threshold, validation_counts, threshold_candidates = select_operating_threshold(
        validation_rows, calibration
    )
    calibration_payload = {
        "development_fit": calibration.as_dict(),
        "fit_partition": "development",
        "operating_threshold": threshold,
        "selection_objective": "maximum-balanced-accuracy",
        "selection_partition": "validation",
        "threshold_candidate_count": threshold_candidates,
        "tie_break": ["closest-to-0.5", "lowest-threshold"],
        "validation_confusion_counts": validation_counts,
    }
    calibration_digest = _digest(calibration_payload)

    test_rows, test_inventory = _extract_partition(
        partition="test",
        data=data,
        dialogue_acts=dialogue_acts,
        test_ids=test_ids,
        validation_ids=validation_ids,
    )
    rows["test"] = test_rows
    inventories["test"] = test_inventory
    _require_expected_inventory("test", test_inventory)
    test_evaluation = evaluate_outcomes(test_rows, calibration, threshold)
    report = _build_report(
        archive_identity=archive_identity,
        manifest_digest=manifest.digest,
        represented_seal=represented_seal,
        edcm_commit=observed_commit,
        edcm_tree=edcm_tree,
        rows=rows,
        inventories=inventories,
        calibration=calibration,
        threshold=threshold,
        threshold_candidates=threshold_candidates,
        validation_counts=validation_counts,
        calibration_digest=calibration_digest,
        test_evaluation=test_evaluation,
    )
    report_digest = _digest(report)
    receipt = {
        "calibration_digest": calibration_digest,
        "canon_selection": None,
        "completion": {
            "development_events": len(development_rows),
            "hypotheses_falsified": sum(
                finding["status"] == "falsified" for finding in report["findings"]
            ),
            "hypotheses_supported": sum(
                finding["status"] == "supported" for finding in report["findings"]
            ),
            "test_events": len(test_rows),
            "validation_events": len(validation_rows),
        },
        "identities": {
            "archive_sha256": ARCHIVE_SHA256,
            "candidate_input_digest_chains": {
                partition: inventories[partition]["candidate_input_digest_chain"]
                for partition in ("development", "validation", "test")
            },
            "edcm_commit": observed_commit,
            "edcm_tree": edcm_tree,
            "represented_report_file_sha256": REPRESENTED_REPORT_FILE_SHA256,
            "represented_receipt_file_sha256": REPRESENTED_RECEIPT_FILE_SHA256,
            "source_event_digest_chains": {
                partition: inventories[partition]["source_event_digest_chain"]
                for partition in ("development", "validation", "test")
            },
            "ucns_commit": PINNED_UCNS_COMMIT,
            "work_graph_sha256": report["work_graph"]["work_graph_sha256"],
        },
        "report_digest": report_digest,
        "schema_id": RECEIPT_SCHEMA_ID,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "complete",
    }
    receipt["receipt_digest"] = _digest(receipt)
    return report, receipt


def _require_expected_inventory(
    partition: str,
    inventory: Mapping[str, Any],
) -> None:
    expected = EXPECTED_EVENT_COUNTS[partition]
    for key in ("negative", "positive", "excluded_ambiguous"):
        if inventory[key] != expected[key]:
            raise OutcomeHoldoutError(
                f"{partition} {key} count differs from frozen design",
                code="EVENT_RECONCILIATION",
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--edcm-repository-root", type=Path, required=True)
    parser.add_argument("--edcm-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report, receipt = run_holdout(
            archive_path=args.archive,
            repository_root=args.edcm_repository_root,
            edcm_commit=args.edcm_commit,
        )
        report_file_sha256 = _write_json_atomic(args.output, report)
        receipt["report_file_sha256"] = report_file_sha256
        receipt["receipt_digest"] = _digest(
            {key: value for key, value in receipt.items() if key != "receipt_digest"}
        )
        _write_json_atomic(args.receipt, receipt)
    except (OutcomeHoldoutError, CorpusRunError, OSError) as exc:
        code = (
            exc.code
            if isinstance(exc, (OutcomeHoldoutError, CorpusRunError))
            else "FILESYSTEM"
        )
        incomplete = {
            "canon_selection": None,
            "failure": {"code": code, "exception_type": type(exc).__name__},
            "schema_id": RECEIPT_SCHEMA_ID,
            "schema_version": RECEIPT_SCHEMA_VERSION,
            "status": "incomplete",
        }
        incomplete["receipt_digest"] = _digest(incomplete)
        try:
            _write_json_atomic(args.receipt, incomplete)
        except OSError:
            pass
        print(json.dumps({"failure": code, "status": "incomplete"}, sort_keys=True))
        return 2
    print(
        json.dumps(
            {
                "canon_selection": None,
                "falsified": receipt["completion"]["hypotheses_falsified"],
                "output": str(args.output),
                "report_digest": receipt["report_digest"],
                "status": "complete",
                "supported": receipt["completion"]["hypotheses_supported"],
            },
            sort_keys=True,
        )
    )
    return 0


__all__ = [
    "OutcomeEvent",
    "PlattCalibration",
    "evaluate_outcomes",
    "fit_platt_calibration",
    "main",
    "run_holdout",
    "select_operating_threshold",
]


if __name__ == "__main__":
    raise SystemExit(main())
