"""Lossless, resumable full-corpus runner for the admitted MultiWOZ 2.1 ZIP.

Usage guidance
--------------
Keep the raw Cambridge archive outside Git, check out the exact UCNS profile
commit, and run:

    python -m edcm.corpora.multiwoz21 \
      --archive /path/to/MULTIWOZ2.1.zip \
      --ucns-source-root /path/to/ucns-at-pinned-commit \
      --output experiments/corpora/results/multiwoz-2.1-full.json \
      --receipt experiments/corpora/receipts/multiwoz-2.1-complete.json \
      --checkpoint /tmp/multiwoz-2.1.checkpoint.json

The runner verifies the admission manifest before reading dialogue evidence,
streams the top-level JSON object in source order, and sends every exact turn
through EDCM's pinned UCNS word-gonol consumer. A second authenticated pass
must also earn the pinned UCNS v0.14.1 full-corpus completion receipt over the
same source-native turn chain. The runner emits aggregate counts,
cryptographic identities, reconciliation, and a completion or incompletion
receipt. It never emits raw dialogue text.

SPACE-boundary, leading, trailing, and repeated-run metrics come from the
profile carrier assignment ``alphabet_position == 0``. The serialized token
records independently reconstruct each exact source value and code point.

The zero-based even=user, odd=system speaker label is an explicit adapter
convention because ``data.json`` has no speaker field. It is not promoted into
source truth. Goal, metadata, dialogue-act, ontology, and database evidence
remain source-native noninputs to this profile run.
"""

# === MODULE_BUILD ===
# id: edcm_multiwoz21_corpus
#   module_name: multiwoz21
#   module_kind: adapter
#   summary: verifies, streams, and reconciles every exact MultiWOZ 2.1 speaker turn through the pinned EDCM UCNS word-gonol profile and v0.14.1 completion gate from the reviewed v0.19 producer without committing raw text
#   owner: Erin Spencer
#   public_surface: AdmissionManifest, CorpusRunError, load_admission_manifest, iter_top_level_object, run_archive, main
#   internal_surface: UCNSFullCorpusGate, _archive_identity, _load_partition_ids, _load_pinned_runtime, _verify_git_tree, _git_commit, _git_tree_identity, _iter_ucns_full_corpus_turns, _new_state, _ordered_token_records, _space_shape, _observe_dialogue, _build_report, _build_receipt, _write_json_atomic, _sealed_main, _run_in_fresh_process
#   auth_boundary: none
#   storage_boundary: reads a caller-held archive and writes only caller-selected aggregate report, receipt, and resumable checkpoint paths
#   network_boundary: none; source acquisition is separate and the runner requires local pinned bytes
#   user_data_boundary: exact dialogue text is processed in memory and represented only by counts and cryptographic identities in written outputs
#   admin_only: false
#   tests: tests.test_multiwoz21_corpus
#   rollout: explicit admitted full-corpus command; no sampling and no default measurement or canon selection
#   rollback: remove the adapter and supersede its aggregate receipts by identity; raw source remains outside Git
#   requires: edcm_ucns_adapter, ucns.edcm and ucns.full_corpus at 872f53571d5dc2f133ff1813b7bdffd3a9c309f8
#   since: 2026-07-28
#   unresolved: source-native semantic labels for correction, retraction, and unresolved reference; formal UCNS geometry and lawful EDCM projection
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: multiwoz21_admission_precedes_execution
#   given: a caller supplies a local MultiWOZ 2.1 archive
#   then: archive bytes and every logical member match the committed Cambridge admission manifest before any dialogue is observed
#   class: provenance
#   since: 2026-07-28
#
# id: multiwoz21_every_turn_is_observed_exactly_once
#   given: an admitted archive contains the complete top-level dialogue object
#   then: every log text is processed once in source dialogue and turn order with no normalization, sampling, sorting, or deduplication
#   class: evidence
#   since: 2026-07-28
#
# id: multiwoz21_completion_requires_reconciliation
#   given: source streaming reaches valid EOF
#   then: completion is emitted only when dialogue, partition, source-turn, adapter-turn, and unit-support counts reconcile exactly
#   class: safety
#   since: 2026-07-28
#
# id: multiwoz21_failure_is_receipted
#   given: archive, schema, adapter, checkpoint, or reconciliation processing fails
#   then: the command emits an incomplete receipt with the last completed and active source position and the exact failure class and reason
#   class: safety
#   since: 2026-07-28
#
# id: multiwoz21_written_outputs_exclude_raw_text
#   given: a run succeeds or fails
#   then: written reports, receipts, and checkpoints contain aggregates and identities but no source turn text
#   class: privacy
#   since: 2026-07-28
#
# id: multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run
#   given: the source-native EDCM pass reconciles the admitted archive
#   then: completion also requires a UCNS v0.14.1 execution-generated receipt whose exhausted turn count and independently repeated exact-turn chain match the source-native pass
#   class: evidence
#   since: 2026-07-31
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import importlib
import importlib.resources
import io
import json
import os
import subprocess
import sys
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any
from zipfile import BadZipFile, ZipFile

from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    PINNED_UCNS_COMMIT,
    UCNSAdapterConstructionError,
    _is_runtime_cache,
    _verify_cached_bytecode,
)


RUNNER_SCHEMA_ID = "edcm.multiwoz21-full-corpus"
RUNNER_SCHEMA_VERSION = "1.3.0"
_SEALED_WORKER_FLAG = "--edcm-sealed-worker"
_SEALED_REPOSITORY_ROOT_ENV = "EDCM_SEALED_REPOSITORY_ROOT"
_SEALED_EDCM_COMMIT_ENV = "EDCM_SEALED_COMMIT"
_SEALED_EDCM_TREE_ENV = "EDCM_SEALED_TREE"
_BOOTSTRAP_ADMISSION_DIGEST = (
    "dfe7b65a9f4af739a4d149e65e60674333e87f56ff9db3cd07c144b9cab85fc2"
)
_ISOLATED_WORKER_BOOTSTRAP = """
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile
import tempfile

repository_root = sys.argv.pop(1)
environment = dict(os.environ)
environment["GIT_NO_REPLACE_OBJECTS"] = "1"

def option_value(name):
    prefix = f"{name}="
    for index, argument in enumerate(sys.argv):
        if argument == name:
            return sys.argv[index + 1] if index + 1 < len(sys.argv) else None
        if argument.startswith(prefix):
            return argument[len(prefix):]
    return None

def write_bootstrap_failure(reason, edcm_tree=None):
    receipt_value = option_value("--receipt")
    if receipt_value is None:
        return
    archive_value = option_value("--archive")
    receipt = {
        "admission_digest": "__BOOTSTRAP_ADMISSION_DIGEST__",
        "corpus_id": "multiwoz-2.1",
        "error": {"code": "GIT_IDENTITY", "reason": reason},
        "identities": {
            "archive_sha256": None,
            "edcm_tree": edcm_tree,
            "ucns_commit": "872f53571d5dc2f133ff1813b7bdffd3a9c309f8",
        },
        "last_completed": {"dialogue_id": None, "dialogue_index": None},
        "next_or_active": {
            "dialogue_id": None,
            "dialogue_index": None,
            "turn_index": None,
        },
        "processed": {"adapter_turns": 0, "dialogues": 0, "source_turns": 0},
        "reconciliation": None,
        "report_digest": None,
        "report_sha256": None,
        "schema_id": "edcm.corpus-run-receipt",
        "schema_version": "1.3.0",
        "source_artifact_filename": (
            None if archive_value is None else Path(archive_value).name
        ),
        "status": "incomplete",
        "ucns_full_corpus": None,
    }
    receipt["receipt_digest"] = hashlib.sha256(
        json.dumps(
            receipt,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    receipt_path = Path(receipt_value).resolve()
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = receipt_path.with_name(f".{receipt_path.name}.tmp")
    temporary.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\\n",
        encoding="utf-8",
        newline="\\n",
    )
    temporary.replace(receipt_path)
    print(
        json.dumps(
            {
                "error_code": "GIT_IDENTITY",
                "reason": reason,
                "receipt": str(receipt_path),
                "status": "incomplete",
            },
            sort_keys=True,
        ),
        file=sys.stderr,
    )

def extract_source_only(package, snapshot):
    for member in package:
        parts = member.name.split("/")
        if (
            not parts
            or parts[0] != "edcm"
            or any(part in {"", ".", ".."} for part in parts)
        ):
            raise RuntimeError("unsafe sealed-source archive path")
        if member.name.endswith(".pyc") or "__pycache__" in parts:
            continue
        target = os.path.join(snapshot, *parts)
        if member.isdir():
            os.makedirs(target, exist_ok=True)
            continue
        if not member.isfile():
            raise RuntimeError("unsafe sealed-source archive member type")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        source = package.extractfile(member)
        if source is None:
            raise RuntimeError("sealed-source archive member cannot be read")
        with source, open(target, "xb") as destination:
            shutil.copyfileobj(source, destination)

edcm_tree = None
snapshot_context = None
try:
    commit = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout.strip()
    edcm_tree = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}:edcm"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout.strip()
    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit, "edcm"],
        cwd=repository_root,
        check=True,
        capture_output=True,
        env=environment,
    ).stdout
    snapshot_context = tempfile.TemporaryDirectory(prefix="edcm-sealed-source-")
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as package:
        extract_source_only(package, snapshot_context.name)
except (OSError, subprocess.CalledProcessError, tarfile.TarError, RuntimeError) as error:
    if snapshot_context is not None:
        snapshot_context.cleanup()
    reason = f"sealed bootstrap failed: {type(error).__name__}: {error}"
    try:
        write_bootstrap_failure(reason, edcm_tree)
    except OSError as receipt_error:
        print(
            f"{reason}; receipt failure: {type(receipt_error).__name__}: {receipt_error}",
            file=sys.stderr,
        )
    raise SystemExit(1)
else:
    with snapshot_context as snapshot:
        os.environ["EDCM_SEALED_REPOSITORY_ROOT"] = repository_root
        os.environ["EDCM_SEALED_COMMIT"] = commit
        os.environ["EDCM_SEALED_TREE"] = edcm_tree
        sys.dont_write_bytecode = True
        sys.path.insert(0, snapshot)
        runpy.run_module("edcm.corpora.multiwoz21", run_name="__main__")
""".replace(
    "__BOOTSTRAP_ADMISSION_DIGEST__",
    _BOOTSTRAP_ADMISSION_DIGEST,
)
RECEIPT_SCHEMA_ID = "edcm.corpus-run-receipt"
RECEIPT_SCHEMA_VERSION = "1.3.0"
CHECKPOINT_SCHEMA_ID = "edcm.multiwoz21-checkpoint"
CHECKPOINT_SCHEMA_VERSION = "1.3.0"
UCNS_FULL_CORPUS_SCHEMA_ID = "ucns.edcm.full-corpus-execution"
UCNS_FULL_CORPUS_SCHEMA_VERSION = "0.14.1"
EMPTY_CHAIN_DIGEST = sha256(b"").hexdigest()
CHUNK_SIZE = 1024 * 1024


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


def _sha256_path(path: Path) -> tuple[int, str]:
    digest = sha256()
    size = 0
    with path.open("rb") as handle:
        while block := handle.read(CHUNK_SIZE):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


@dataclass(frozen=True)
class AdmissionManifest:
    """Validated access to the committed admission record."""

    payload: Mapping[str, Any]

    @property
    def corpus_id(self) -> str:
        return str(self.payload["corpus_id"])

    @property
    def archive(self) -> Mapping[str, Any]:
        return self.payload["source"]["archive"]

    @property
    def source(self) -> Mapping[str, Any]:
        return self.payload["source"]

    @property
    def expected(self) -> Mapping[str, Any]:
        return self.payload["expected"]

    @property
    def ucns_full_corpus(self) -> Mapping[str, Any]:
        return self.payload["ucns_full_corpus"]

    @property
    def digest(self) -> str:
        return _digest(self.payload)


class CorpusRunError(RuntimeError):
    """A fail-closed corpus error carrying non-text progress for a receipt."""

    def __init__(
        self,
        reason: str,
        *,
        code: str,
        state: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(reason)
        self.code = code
        self.state = dict(state or {})


def load_admission_manifest() -> AdmissionManifest:
    """Load and minimally validate the packaged MultiWOZ 2.1 admission."""

    resource = importlib.resources.files("edcm.corpora").joinpath(
        "data/multiwoz_2_1_admission.json"
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
        "ucns_full_corpus",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise CorpusRunError(
            f"admission manifest is missing fields: {', '.join(missing)}",
            code="ADMISSION_SCHEMA",
        )
    if (
        payload["schema_id"] != "edcm.corpus-admission"
        or payload["schema_version"] != "1.1.0"
        or payload["corpus_id"] != "multiwoz-2.1"
        or payload["status"] != "admitted"
    ):
        raise CorpusRunError(
            "admission manifest identity or status mismatch",
            code="ADMISSION_IDENTITY",
        )
    return AdmissionManifest(payload)


class UCNSFullCorpusGate:
    """Consume the exact public UCNS v0.14.1 execution/receipt surface."""

    _REQUIRED_SURFACES = (
        "AdmittedCorpusManifest",
        "CorpusAdapterIdentity",
        "execute_admitted_corpus",
        "issue_full_corpus_completion_receipt",
    )

    def __init__(self, module: ModuleType) -> None:
        self.module = module
        missing = tuple(
            name for name in self._REQUIRED_SURFACES if not hasattr(module, name)
        )
        if missing:
            raise CorpusRunError(
                "UCNS full-corpus surface missing: " + ", ".join(missing),
                code="UCNS_FULL_CORPUS_SURFACE",
            )
        if (
            getattr(module, "V014_FULL_CORPUS_SCHEMA_ID", None)
            != UCNS_FULL_CORPUS_SCHEMA_ID
            or getattr(module, "V014_FULL_CORPUS_SCHEMA_VERSION", None)
            != UCNS_FULL_CORPUS_SCHEMA_VERSION
        ):
            raise CorpusRunError(
                "UCNS full-corpus schema identity mismatch",
                code="UCNS_FULL_CORPUS_SCHEMA",
            )

    def execute(
        self,
        manifest: AdmissionManifest,
        turns: Iterable[tuple[str, str]],
    ) -> dict[str, Any]:
        """Execute the public gate and serialize only bounded aggregate evidence."""

        contract = manifest.ucns_full_corpus
        adapter_contract = contract["adapter"]
        native_manifest = self.module.AdmittedCorpusManifest(
            corpus_id=manifest.corpus_id,
            corpus_version=str(contract["corpus_version"]),
            source_artifact_sha256=str(manifest.archive["sha256"]),
            expected_turn_count=int(manifest.expected["turn_count"]),
            license_id=str(manifest.payload["license"]["spdx"]),
            privacy_treatment=str(contract["privacy_treatment"]),
            redaction_policy=str(contract["redaction_policy"]),
            admission_decision_id=str(contract["admission_decision_id"]),
            adapter=self.module.CorpusAdapterIdentity(
                adapter_id=str(adapter_contract["adapter_id"]),
                adapter_version=str(adapter_contract["adapter_version"]),
                code_reference=str(adapter_contract["code_reference"]),
            ),
        )
        native_report = self.module.execute_admitted_corpus(
            native_manifest,
            turns,
        )
        status = native_report.status.value
        receipt = (
            self.module.issue_full_corpus_completion_receipt(native_report)
            if status == "complete"
            else None
        )
        failure = native_report.failure
        return {
            "activations": {
                "edcm": native_report.edcm_activation,
                "metapat": native_report.metapat_activation,
                "selection_effect": native_report.selection_effect,
            },
            "exact_observation_stream_sha256": (
                native_report.exact_observation_stream_sha256
            ),
            "exact_source_stream_sha256": (
                native_report.exact_source_stream_sha256
            ),
            "failure": (
                None
                if failure is None
                else {
                    "detail": failure.detail,
                    "exception_type": failure.exception_type,
                    "kind": failure.kind.value,
                    "stopping_turn_index": failure.stopping_turn_index,
                }
            ),
            "gate_effect": native_report.post_run_gate,
            "iterator_exhausted": native_report.iterator_exhausted,
            "manifest": {
                "adapter": {
                    "adapter_id": native_manifest.adapter.adapter_id,
                    "adapter_version": native_manifest.adapter.adapter_version,
                    "code_reference": native_manifest.adapter.code_reference,
                },
                "admission_decision_id": (
                    native_manifest.admission_decision_id
                ),
                "corpus_id": native_manifest.corpus_id,
                "corpus_version": native_manifest.corpus_version,
                "expected_turn_count": native_manifest.expected_turn_count,
                "license_id": native_manifest.license_id,
                "privacy_treatment": native_manifest.privacy_treatment,
                "redaction_policy": native_manifest.redaction_policy,
                "source_artifact_sha256": (
                    native_manifest.source_artifact_sha256
                ),
            },
            "observations": {
                "carrier_unassigned_count": (
                    native_report.carrier_unassigned_count
                ),
                "space_boundary_count": native_report.space_boundary_count,
                "word_gonol_count": native_report.word_gonol_count,
            },
            "processed_turn_count": native_report.processed_turn_count,
            "profile": {
                "profile_id": native_report.profile_id,
                "profile_scope": native_report.profile_scope,
                "profile_version": native_report.profile_version,
            },
            "receipt": (
                None
                if receipt is None
                else {
                    "edcm_activation": receipt.edcm_activation,
                    "gate_effect": receipt.gate_effect,
                    "metapat_activation": receipt.metapat_activation,
                    "receipt_id": receipt.receipt_id,
                    "selection_effect": receipt.selection_effect,
                }
            ),
            "schema_id": native_report.schema_id,
            "schema_version": native_report.schema_version,
            "status": status,
        }


class _StreamingObjectReader:
    """Incrementally decode one top-level JSON object without reordering it."""

    def __init__(self, handle: io.TextIOBase, *, chunk_size: int = CHUNK_SIZE) -> None:
        self.handle = handle
        self.chunk_size = chunk_size
        self.buffer = ""
        self.position = 0
        self.eof = False
        self.decoder = json.JSONDecoder()

    def _fill(self) -> bool:
        if self.eof:
            return False
        chunk = self.handle.read(self.chunk_size)
        if chunk == "":
            self.eof = True
            return False
        self.buffer += chunk
        return True

    def _compact(self) -> None:
        if self.position >= self.chunk_size * 4:
            self.buffer = self.buffer[self.position :]
            self.position = 0

    def _skip_space(self) -> None:
        while True:
            while self.position < len(self.buffer) and self.buffer[
                self.position
            ] in " \t\r\n":
                self.position += 1
            if self.position < len(self.buffer) or not self._fill():
                return

    def _character(self) -> str:
        self._skip_space()
        while self.position >= len(self.buffer):
            if not self._fill():
                raise CorpusRunError(
                    "unexpected EOF while reading top-level JSON object",
                    code="SOURCE_JSON_EOF",
                )
        return self.buffer[self.position]

    def _decode(self) -> tuple[Any, int]:
        self._skip_space()
        while True:
            try:
                return self.decoder.raw_decode(self.buffer, self.position)
            except json.JSONDecodeError as exc:
                if self._fill():
                    continue
                raise CorpusRunError(
                    f"invalid source JSON at character {exc.pos}: {exc.msg}",
                    code="SOURCE_JSON_INVALID",
                ) from exc

    def entries(self) -> Iterator[tuple[str, Any, str]]:
        if self._character() != "{":
            raise CorpusRunError(
                "data member must be one top-level JSON object",
                code="SOURCE_JSON_SHAPE",
            )
        self.position += 1
        if self._character() == "}":
            self.position += 1
            return

        while True:
            key, end = self._decode()
            if not isinstance(key, str):
                raise CorpusRunError(
                    "top-level dialogue key must be a string",
                    code="SOURCE_DIALOGUE_ID",
                )
            self.position = end
            if self._character() != ":":
                raise CorpusRunError(
                    f"missing value separator after dialogue key {key!r}",
                    code="SOURCE_JSON_INVALID",
                )
            self.position += 1
            self._skip_space()
            value_start = self.position
            value, value_end = self._decode()
            raw_value = self.buffer[value_start:value_end]
            self.position = value_end
            yield key, value, sha256(raw_value.encode("utf-8")).hexdigest()

            marker = self._character()
            if marker == ",":
                self.position += 1
                self._compact()
                continue
            if marker == "}":
                self.position += 1
                break
            raise CorpusRunError(
                f"invalid top-level separator after dialogue {key!r}",
                code="SOURCE_JSON_INVALID",
            )

        self._skip_space()
        if self.position < len(self.buffer):
            raise CorpusRunError(
                "non-whitespace data follows the top-level JSON object",
                code="SOURCE_JSON_TRAILING_DATA",
            )
        while self._fill():
            if self.buffer[self.position :].strip():
                raise CorpusRunError(
                    "non-whitespace data follows the top-level JSON object",
                    code="SOURCE_JSON_TRAILING_DATA",
                )
            self.position = len(self.buffer)


def iter_top_level_object(
    handle: io.TextIOBase,
    *,
    chunk_size: int = CHUNK_SIZE,
) -> Iterator[tuple[str, Any, str]]:
    """Yield ``(key, value, exact_value_sha256)`` in source order."""

    yield from _StreamingObjectReader(handle, chunk_size=chunk_size).entries()


def _logical_member(info: Any) -> bool:
    path = PurePosixPath(info.filename)
    return (
        not info.is_dir()
        and not info.filename.startswith("__MACOSX/")
        and not path.name.startswith(".")
    )


def _archive_identity(
    archive_path: Path,
    manifest: AdmissionManifest,
) -> tuple[dict[str, Any], ZipFile]:
    size, archive_sha256 = _sha256_path(archive_path)
    expected_archive = manifest.archive
    if size != int(expected_archive["bytes"]):
        raise CorpusRunError(
            f"archive byte count mismatch: expected {expected_archive['bytes']}, got {size}",
            code="ARCHIVE_BYTES",
        )
    if archive_sha256 != expected_archive["sha256"]:
        raise CorpusRunError(
            "archive SHA-256 does not match admitted Cambridge artifact",
            code="ARCHIVE_SHA256",
        )
    try:
        archive = ZipFile(archive_path)
        bad_member = archive.testzip()
    except (BadZipFile, OSError) as exc:
        raise CorpusRunError(
            f"archive cannot be read: {type(exc).__name__}: {exc}",
            code="ARCHIVE_INVALID",
        ) from exc
    if bad_member is not None:
        archive.close()
        raise CorpusRunError(
            f"ZIP integrity failure at member {bad_member}",
            code="ARCHIVE_CRC",
        )

    names = [info.filename for info in archive.infolist()]
    if len(names) != len(set(names)):
        archive.close()
        raise CorpusRunError(
            "ZIP contains duplicate member names",
            code="ARCHIVE_DUPLICATE_MEMBER",
        )

    actual_members: list[dict[str, Any]] = []
    for info in archive.infolist():
        if not _logical_member(info):
            continue
        member_digest = sha256()
        with archive.open(info, "r") as member:
            while block := member.read(CHUNK_SIZE):
                member_digest.update(block)
        actual_members.append(
            {
                "bytes": info.file_size,
                "path": info.filename,
                "sha256": member_digest.hexdigest(),
            }
        )
    actual_members.sort(key=lambda value: value["path"])
    expected_members = sorted(
        (dict(value) for value in expected_archive["logical_members"]),
        key=lambda value: value["path"],
    )
    if actual_members != expected_members:
        archive.close()
        raise CorpusRunError(
            "logical ZIP member inventory differs from admission manifest",
            code="ARCHIVE_MEMBER_INVENTORY",
        )
    return (
        {
            "bytes": size,
            "filename": expected_archive["filename"],
            "logical_members": actual_members,
            "sha256": archive_sha256,
        },
        archive,
    )


def _load_partition_ids(archive: ZipFile, member_name: str) -> tuple[str, ...]:
    try:
        raw = archive.read(member_name)
    except KeyError as exc:
        raise CorpusRunError(
            f"partition member missing: {member_name}",
            code="PARTITION_MEMBER_MISSING",
        ) from exc
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CorpusRunError(
            f"partition member is not strict UTF-8: {member_name}",
            code="PARTITION_UTF8",
        ) from exc
    lines = text.splitlines()
    if any(not line or line != line.strip() for line in lines):
        raise CorpusRunError(
            f"partition member contains blank or padded identifiers: {member_name}",
            code="PARTITION_IDENTIFIER",
        )
    if len(lines) != len(set(lines)):
        raise CorpusRunError(
            f"partition member contains duplicate identifiers: {member_name}",
            code="PARTITION_DUPLICATE",
        )
    return tuple(lines)


def _new_state(
    *,
    archive_sha256: str,
    admission_digest: str,
    edcm_tree: str,
    ucns_commit: str,
) -> dict[str, Any]:
    return {
        "active_dialogue_id": None,
        "active_dialogue_index": None,
        "active_turn_index": None,
        "adapter_turns": 0,
        "admission_digest": admission_digest,
        "archive_sha256": archive_sha256,
        "code_points": 0,
        "dialogues": 0,
        "dialogues_with_odd_turn_count": 0,
        "edcm_tree": edcm_tree,
        "empty_turns": 0,
        "first_dialogue_id": None,
        "last_completed_dialogue_id": None,
        "last_completed_dialogue_index": None,
        "leading_space_turns": 0,
        "newline_turns": 0,
        "non_ascii_turns": 0,
        "out_of_alphabet_affected_turns": 0,
        "out_of_alphabet_affected_word_gonols": 0,
        "out_of_alphabet_by_code_point": {},
        "out_of_alphabet_occurrences": 0,
        "partitions": {"test": 0, "train": 0, "validation": 0},
        "profile_identity": None,
        "profile_observation_digest_chain": EMPTY_CHAIN_DIGEST,
        "repeated_space_excess": 0,
        "source_declared_fail_book_dialogues": 0,
        "source_declared_fail_book_domain_occurrences": 0,
        "source_declared_fail_info_dialogues": 0,
        "source_declared_fail_info_domain_occurrences": 0,
        "source_declared_failure_dialogues": 0,
        "source_dialogue_digest_chain": EMPTY_CHAIN_DIGEST,
        "source_turns": 0,
        "space_boundaries": 0,
        "trailing_space_turns": 0,
        "turn_evidence_digest_chain": EMPTY_CHAIN_DIGEST,
        "ucns_commit": ucns_commit,
        "ucns_full_corpus_gate": None,
        "unit_support_total": 0,
        "utf8_bytes": 0,
        "word_gonols": 0,
    }


def _iter_ucns_full_corpus_turns(
    archive: ZipFile,
    manifest: AdmissionManifest,
    tracker: dict[str, Any],
) -> Iterator[tuple[str, str]]:
    """Repeat the authenticated source-native turn stream for UCNS v0.14.1."""

    data_member = str(manifest.source["data_member"])
    try:
        binary = archive.open(data_member, "r")
    except KeyError as exc:
        raise CorpusRunError(
            f"data member missing during UCNS pass: {data_member}",
            code="DATA_MEMBER_MISSING",
        ) from exc

    seen_ids: set[str] = set()
    with binary, io.TextIOWrapper(
        binary,
        encoding="utf-8",
        errors="strict",
        newline="",
    ) as text:
        for dialogue_index, (
            dialogue_id,
            dialogue,
            _raw_value_sha256,
        ) in enumerate(iter_top_level_object(text)):
            if dialogue_id in seen_ids:
                raise CorpusRunError(
                    f"duplicate dialogue identifier: {dialogue_id}",
                    code="DIALOGUE_DUPLICATE",
                )
            seen_ids.add(dialogue_id)
            if not isinstance(dialogue, Mapping):
                raise CorpusRunError(
                    "dialogue value is not an object during UCNS pass",
                    code="DIALOGUE_SHAPE",
                )
            log = dialogue.get("log")
            if not isinstance(log, list):
                raise CorpusRunError(
                    "dialogue log is not a list during UCNS pass",
                    code="DIALOGUE_LOG_SHAPE",
                )
            for turn_index, turn in enumerate(log):
                if not isinstance(turn, Mapping) or "text" not in turn:
                    raise CorpusRunError(
                        "turn is not an object with a text field during UCNS pass",
                        code="TURN_SHAPE",
                    )
                source_text = turn["text"]
                if not isinstance(source_text, str):
                    raise CorpusRunError(
                        "turn text is not a string during UCNS pass",
                        code="TURN_TEXT_TYPE",
                    )
                speaker_id = _speaker_id(turn_index)
                source_bytes = source_text.encode("utf-8")
                tracker["turn_evidence_digest_chain"] = _chain(
                    tracker["turn_evidence_digest_chain"],
                    {
                        "dialogue_id": dialogue_id,
                        "dialogue_index": dialogue_index,
                        "speaker_id": speaker_id,
                        "text_code_points": len(source_text),
                        "text_sha256": sha256(source_bytes).hexdigest(),
                        "text_utf8_bytes": len(source_bytes),
                        "turn_index": turn_index,
                    },
                )
                tracker["turns"] += 1
                yield speaker_id, source_text
            tracker["dialogues"] += 1


def _profile_identity(evidence: Mapping[str, Any]) -> dict[str, Any]:
    identity = {
        "corpus_execution": evidence["corpus_execution"],
        "evidence_mode": evidence["evidence_mode"],
        "gonol_initiation": evidence["gonol_initiation"],
        "measurement_validity_claim": evidence["measurement_validity_claim"],
        "normalization_policy": evidence["normalization_policy"],
        "options": evidence["options"],
        "profile_id": evidence["profile_id"],
        "profile_scope": evidence["profile_scope"],
        "profile_version": evidence["profile_version"],
        "projection_status": evidence["projection_status"],
        "smallest_gonol": evidence["smallest_gonol"],
        "source_domain": evidence["source_domain"],
        "space_assignment_policy": evidence["space_assignment_policy"],
        "space_code_point_labels": evidence["space_code_point_labels"],
        "space_code_points_sha256": evidence["space_code_points_sha256"],
        "source_commit": evidence["source_commit"],
        "source_repository": evidence["source_repository"],
        "support_policy": evidence["support_policy"],
        "theorem_status_transfer": evidence["theorem_status_transfer"],
        "token_alphabet_sha256": evidence["token_alphabet_sha256"],
        "token_alphabet_size": evidence["token_alphabet_size"],
    }
    # Checkpoints are JSON. Normalize tuple/list container representation once
    # so a resumed run is byte-identical to an uninterrupted run.
    return json.loads(json.dumps(identity, ensure_ascii=False))


def _speaker_id(turn_index: int) -> str:
    return "user" if turn_index % 2 == 0 else "system"


def _ordered_token_records(
    observed: Mapping[str, Any],
    *,
    state: Mapping[str, Any],
) -> tuple[Mapping[str, Any], ...]:
    segments = observed.get("segments")
    if not isinstance(segments, (tuple, list)):
        raise CorpusRunError(
            "UCNS profile segment evidence has an invalid shape",
            code="UCNS_SEGMENT_EVIDENCE",
            state=state,
        )
    ordered: list[Mapping[str, Any]] = []
    for segment in segments:
        if not isinstance(segment, Mapping):
            raise CorpusRunError(
                "UCNS profile segment evidence has an invalid shape",
                code="UCNS_SEGMENT_EVIDENCE",
                state=state,
            )
        kind = segment.get("kind")
        if kind == "word-gonol":
            tokens = segment.get("tokens")
            if not isinstance(tokens, (tuple, list)):
                raise CorpusRunError(
                    "UCNS word-gonol token evidence has an invalid shape",
                    code="UCNS_TOKEN_EVIDENCE",
                    state=state,
                )
        elif kind == "superpositioned-space-boundary":
            tokens = (segment.get("token"),)
        else:
            raise CorpusRunError(
                "UCNS profile emitted an unknown segment kind",
                code="UCNS_SEGMENT_EVIDENCE",
                state=state,
            )
        for token in tokens:
            if not isinstance(token, Mapping):
                raise CorpusRunError(
                    "UCNS token evidence has an invalid shape",
                    code="UCNS_TOKEN_EVIDENCE",
                    state=state,
                )
            ordered.append(token)
        if kind == "word-gonol":
            carrier_unassigned = segment.get("carrier_unassigned")
            out_of_alphabet = segment.get("out_of_alphabet")
            expected_unassigned = tuple(
                token
                for token in tokens
                if not token.get("has_carrier_assignment")
            )
            if (
                not isinstance(carrier_unassigned, (tuple, list))
                or not isinstance(out_of_alphabet, (tuple, list))
                or tuple(carrier_unassigned) != expected_unassigned
                or tuple(out_of_alphabet) != expected_unassigned
            ):
                raise CorpusRunError(
                    "UCNS word carrier-unassigned evidence is inconsistent",
                    code="UCNS_TOKEN_EVIDENCE",
                    state=state,
                )
    return tuple(ordered)


def _space_shape(
    tokens: tuple[Mapping[str, Any], ...],
) -> tuple[int, bool, bool]:
    assignments = tuple(token.get("alphabet_position") == 0 for token in tokens)
    repeated_excess = 0
    previous_space = False
    for is_space in assignments:
        if is_space:
            if previous_space:
                repeated_excess += 1
            previous_space = True
        else:
            previous_space = False
    return (
        repeated_excess,
        bool(assignments and assignments[0]),
        bool(assignments and assignments[-1]),
    )


def _source_failure_flags(dialogue: Mapping[str, Any]) -> tuple[int, int]:
    goal = dialogue.get("goal")
    if not isinstance(goal, Mapping):
        return 0, 0
    fail_book = 0
    fail_info = 0
    for domain_value in goal.values():
        if not isinstance(domain_value, Mapping):
            continue
        if isinstance(domain_value.get("fail_book"), Mapping) and domain_value[
            "fail_book"
        ]:
            fail_book += 1
        if isinstance(domain_value.get("fail_info"), Mapping) and domain_value[
            "fail_info"
        ]:
            fail_info += 1
    return fail_book, fail_info


def _observe_dialogue(
    *,
    adapter: ActualUCNSAdapter,
    dialogue_index: int,
    dialogue_id: str,
    dialogue: Any,
    partition: str,
    raw_value_sha256: str,
    state: dict[str, Any],
) -> None:
    state["active_dialogue_index"] = dialogue_index
    state["active_dialogue_id"] = dialogue_id
    state["active_turn_index"] = None
    if not isinstance(dialogue, Mapping):
        raise CorpusRunError(
            "dialogue value is not an object",
            code="DIALOGUE_SHAPE",
            state=state,
        )
    log = dialogue.get("log")
    if not isinstance(log, list):
        raise CorpusRunError(
            "dialogue log is not a list",
            code="DIALOGUE_LOG_SHAPE",
            state=state,
        )

    turns: list[tuple[str, str]] = []
    for turn_index, turn in enumerate(log):
        state["active_turn_index"] = turn_index
        if not isinstance(turn, Mapping) or "text" not in turn:
            raise CorpusRunError(
                "turn is not an object with a text field",
                code="TURN_SHAPE",
                state=state,
            )
        text = turn["text"]
        if not isinstance(text, str):
            raise CorpusRunError(
                "turn text is not a string",
                code="TURN_TEXT_TYPE",
                state=state,
            )
        turns.append((_speaker_id(turn_index), text))

    try:
        adapted = adapter.normalize(
            {
                "source_ref": f"cam.41572:data.json:{dialogue_id}",
                "ucns_turns": tuple(turns),
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
    if not isinstance(observed_turns, (tuple, list)):
        raise CorpusRunError(
            "UCNS profile turn evidence has an invalid shape",
            code="UCNS_TURN_EVIDENCE",
            state=state,
        )
    if len(observed_turns) != len(turns):
        raise CorpusRunError(
            "source and adapter turn counts differ within a dialogue",
            code="TURN_RECONCILIATION",
            state=state,
        )

    fail_book, fail_info = _source_failure_flags(dialogue)
    state["source_declared_fail_book_domain_occurrences"] += fail_book
    state["source_declared_fail_info_domain_occurrences"] += fail_info
    state["source_declared_fail_book_dialogues"] += int(fail_book > 0)
    state["source_declared_fail_info_dialogues"] += int(fail_info > 0)
    state["source_declared_failure_dialogues"] += int(
        fail_book > 0 or fail_info > 0
    )

    state["source_dialogue_digest_chain"] = _chain(
        state["source_dialogue_digest_chain"],
        {
            "dialogue_id": dialogue_id,
            "dialogue_index": dialogue_index,
            "raw_value_sha256": raw_value_sha256,
        },
    )
    state["profile_observation_digest_chain"] = _chain(
        state["profile_observation_digest_chain"],
        {
            "dialogue_id": dialogue_id,
            "dialogue_index": dialogue_index,
            "observation_digest": evidence["observation_digest"],
        },
    )

    for turn_index, (source_turn, observed) in enumerate(
        zip(turns, observed_turns, strict=True)
    ):
        state["active_turn_index"] = turn_index
        speaker_id, text = source_turn
        if (
            observed["speaker_id"] != speaker_id
            or observed["turn_index"] != turn_index
            or observed["raw_text"] != text
        ):
            raise CorpusRunError(
                "adapter turn does not reconstruct the exact source turn",
                code="TURN_EXACTNESS",
                state=state,
            )
        text_bytes = text.encode("utf-8")
        state["turn_evidence_digest_chain"] = _chain(
            state["turn_evidence_digest_chain"],
            {
                "dialogue_id": dialogue_id,
                "dialogue_index": dialogue_index,
                "speaker_id": speaker_id,
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

        token_records = _ordered_token_records(observed, state=state)
        source_values: list[str] = []
        for offset, token in enumerate(token_records):
            source_value = token.get("source_value")
            source_code_point = token.get("source_code_point")
            carrier_position = token.get("carrier_position")
            alphabet_position = token.get("alphabet_position")
            if (
                not isinstance(source_value, str)
                or len(source_value) != 1
                or token.get("value") != source_value
                or source_code_point != f"U+{ord(source_value):04X}"
                or token.get("code_point") != source_code_point
                or token.get("codepoint_offset") != offset
                or carrier_position != alphabet_position
                or token.get("is_space_manifestation")
                != (alphabet_position == 0)
                or token.get("has_carrier_assignment")
                != (alphabet_position is not None)
                or token.get("in_alphabet")
                != token.get("has_carrier_assignment")
                or not isinstance(token.get("is_public_gonol_token"), bool)
            ):
                raise CorpusRunError(
                    "UCNS token source/carrier witness is inconsistent",
                    code="UCNS_TOKEN_EVIDENCE",
                    state=state,
                )
            if alphabet_position == 0 and token.get("carrier_token") != " ":
                raise CorpusRunError(
                    "UCNS origin-assigned SPACE witness has the wrong carrier token",
                    code="UCNS_TOKEN_EVIDENCE",
                    state=state,
                )
            source_values.append(source_value)
        if "".join(source_values) != text:
            raise CorpusRunError(
                "UCNS token evidence does not reconstruct the exact source turn",
                code="TURN_EXACTNESS",
                state=state,
            )

        carrier_unassigned = observed.get("carrier_unassigned")
        out_of_alphabet = observed.get("out_of_alphabet")
        expected_unassigned = tuple(
            token
            for token in token_records
            if not token["has_carrier_assignment"]
        )
        if (
            not isinstance(carrier_unassigned, (tuple, list))
            or not isinstance(out_of_alphabet, (tuple, list))
            or tuple(carrier_unassigned) != expected_unassigned
            or tuple(out_of_alphabet) != expected_unassigned
            or observed.get("has_complete_carrier_assignment")
            != (not expected_unassigned)
            or observed.get("has_complete_alphabet_coverage")
            != observed.get("has_complete_carrier_assignment")
        ):
            raise CorpusRunError(
                "UCNS turn carrier-unassigned evidence is inconsistent",
                code="UCNS_TOKEN_EVIDENCE",
                state=state,
            )

        repeated, leading, trailing = _space_shape(token_records)
        state["repeated_space_excess"] += repeated
        state["leading_space_turns"] += int(leading)
        state["trailing_space_turns"] += int(trailing)

        state["out_of_alphabet_occurrences"] += len(carrier_unassigned)
        state["out_of_alphabet_affected_turns"] += int(bool(carrier_unassigned))
        for token in carrier_unassigned:
            code_point = token["source_code_point"]
            histogram = state["out_of_alphabet_by_code_point"]
            histogram[code_point] = histogram.get(code_point, 0) + 1
        for segment in observed["segments"]:
            if segment["kind"] != "word-gonol":
                continue
            if segment["carrier_unassigned"]:
                state["out_of_alphabet_affected_word_gonols"] += 1

    state["dialogues"] += 1
    state["dialogues_with_odd_turn_count"] += int(len(turns) % 2 == 1)
    state["partitions"][partition] += 1
    if state["first_dialogue_id"] is None:
        state["first_dialogue_id"] = dialogue_id
    state["last_completed_dialogue_id"] = dialogue_id
    state["last_completed_dialogue_index"] = dialogue_index
    state["active_dialogue_id"] = None
    state["active_dialogue_index"] = None
    state["active_turn_index"] = None


def _checkpoint_payload(state: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": CHECKPOINT_SCHEMA_ID,
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "state": dict(state),
    }


def _write_json_atomic(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
    return sha256(text.encode("utf-8")).hexdigest()


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
    *,
    seen_dialogue_count: int,
    seen_test_ids: set[str],
    seen_validation_ids: set[str],
    test_ids: set[str],
    validation_ids: set[str],
) -> dict[str, Any]:
    expected_dialogues = int(manifest.expected["dialogue_count"])
    expected_partitions = dict(manifest.expected["partition_counts"])
    checks = {
        "adapter_turns_equal_source_turns": (
            state["adapter_turns"] == state["source_turns"]
        ),
        "all_test_ids_seen": seen_test_ids == test_ids,
        "all_validation_ids_seen": seen_validation_ids == validation_ids,
        "dialogue_count_matches_manifest": (
            state["dialogues"] == expected_dialogues
        ),
        "partition_counts_match_manifest": (
            state["partitions"] == expected_partitions
        ),
        "stream_count_equals_processed_count": (
            seen_dialogue_count == state["dialogues"]
        ),
        "unit_support_equals_adapter_turns": (
            state["unit_support_total"] == state["adapter_turns"]
        ),
    }
    return {
        "checks": checks,
        "complete": all(checks.values()),
        "expected_dialogues": expected_dialogues,
        "expected_partitions": expected_partitions,
        "observed_dialogues": state["dialogues"],
        "observed_partitions": state["partitions"],
    }


def _build_report(
    *,
    manifest: AdmissionManifest,
    archive_identity: Mapping[str, Any],
    state: Mapping[str, Any],
    reconciliation: Mapping[str, Any],
) -> dict[str, Any]:
    histogram = [
        {"code_point": code_point, "occurrences": occurrences}
        for code_point, occurrences in sorted(
            state["out_of_alphabet_by_code_point"].items()
        )
    ]
    carrier_unassigned_summary = {
        "affected_turns": state["out_of_alphabet_affected_turns"],
        "affected_word_gonols": state[
            "out_of_alphabet_affected_word_gonols"
        ],
        "by_code_point": histogram,
        "occurrences": state["out_of_alphabet_occurrences"],
        "unique_code_points": len(histogram),
    }
    report: dict[str, Any] = {
        "admission": {
            "admission_digest": manifest.digest,
            "corpus_id": manifest.corpus_id,
            "evidence_state": manifest.payload["evidence_state"],
            "license": manifest.payload["license"],
            "status": manifest.payload["status"],
        },
        "canon_selection": None,
        "execution": {
            "adapter_turns": state["adapter_turns"],
            "code_points": state["code_points"],
            "dialogues": state["dialogues"],
            "first_dialogue_id": state["first_dialogue_id"],
            "last_dialogue_id": state["last_completed_dialogue_id"],
            "partitions": state["partitions"],
            "profile_unit_support_total": state["unit_support_total"],
            "source_turns": state["source_turns"],
            "utf8_bytes": state["utf8_bytes"],
        },
        "failure_seeking_observations": {
            "definitions": {
                "carrier_unassigned": "exact non-SPACE source code points without a pinned public-gonol carrier assignment; out_of_alphabet is the compatibility alias",
                "leading_space_turns": "turns whose first exact source code point is assigned to carrier position zero by the pinned SPACE policy",
                "repeated_space_excess": "origin-assigned SPACE manifestations after the first in each contiguous carrier-SPACE run",
                "space_boundaries": "exact source code points assigned to carrier position zero and emitted as superpositioned SPACE boundaries",
                "source_declared_fail_book": "nonempty goal.<domain>.fail_book mappings; source annotation, not EDCM inference",
                "source_declared_fail_info": "nonempty goal.<domain>.fail_info mappings; source annotation, not EDCM inference",
                "trailing_space_turns": "turns whose final exact source code point is assigned to carrier position zero by the pinned SPACE policy",
            },
            "dialogues_with_odd_turn_count": state[
                "dialogues_with_odd_turn_count"
            ],
            "empty_turns": state["empty_turns"],
            "leading_space_turns": state["leading_space_turns"],
            "newline_turns": state["newline_turns"],
            "non_ascii_turns": state["non_ascii_turns"],
            "carrier_unassigned": carrier_unassigned_summary,
            "out_of_alphabet": carrier_unassigned_summary,
            "repeated_space_excess": state["repeated_space_excess"],
            "source_declared_fail_book_dialogues": state[
                "source_declared_fail_book_dialogues"
            ],
            "source_declared_fail_book_domain_occurrences": state[
                "source_declared_fail_book_domain_occurrences"
            ],
            "source_declared_fail_info_dialogues": state[
                "source_declared_fail_info_dialogues"
            ],
            "source_declared_fail_info_domain_occurrences": state[
                "source_declared_fail_info_domain_occurrences"
            ],
            "source_declared_failure_dialogues": state[
                "source_declared_failure_dialogues"
            ],
            "space_boundaries": state["space_boundaries"],
            "trailing_space_turns": state["trailing_space_turns"],
            "word_gonols": state["word_gonols"],
        },
        "hmmm": manifest.payload["hmmm"],
        "identities": {
            "archive": dict(archive_identity),
            "edcm_tree": state["edcm_tree"],
            "profile_observation_digest_chain": state[
                "profile_observation_digest_chain"
            ],
            "source_dialogue_digest_chain": state[
                "source_dialogue_digest_chain"
            ],
            "turn_evidence_digest_chain": state[
                "turn_evidence_digest_chain"
            ],
            "ucns_commit": state["ucns_commit"],
        },
        "information_boundaries": {
            **manifest.payload["information_boundaries"],
            "candidate_measurement": "not-run",
            "formal_ucns_geometry": "NA",
            "profile_output_committed": "aggregate-only",
            "proof_status_transfers_to_measurement_validity": False,
            "raw_source_committed": False,
        },
        "profile": state["profile_identity"],
        "reconciliation": dict(reconciliation),
        "schema_id": RUNNER_SCHEMA_ID,
        "schema_version": RUNNER_SCHEMA_VERSION,
        "ucns_full_corpus_gate": state["ucns_full_corpus_gate"],
    }
    report["report_digest"] = _digest(report)
    return report


def _build_receipt(
    *,
    manifest: AdmissionManifest,
    state: Mapping[str, Any],
    status: str,
    report_digest: str | None = None,
    report_sha256: str | None = None,
    reconciliation: Mapping[str, Any] | None = None,
    error_code: str | None = None,
    error_reason: str | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "admission_digest": manifest.digest,
        "corpus_id": manifest.corpus_id,
        "error": (
            None
            if error_code is None
            else {"code": error_code, "reason": error_reason}
        ),
        "identities": {
            "archive_sha256": state.get("archive_sha256"),
            "edcm_tree": state.get("edcm_tree"),
            "ucns_commit": state.get("ucns_commit"),
        },
        "last_completed": {
            "dialogue_id": state.get("last_completed_dialogue_id"),
            "dialogue_index": state.get("last_completed_dialogue_index"),
        },
        "next_or_active": {
            "dialogue_id": state.get("active_dialogue_id"),
            "dialogue_index": state.get("active_dialogue_index"),
            "turn_index": state.get("active_turn_index"),
        },
        "processed": {
            "adapter_turns": state.get("adapter_turns", 0),
            "dialogues": state.get("dialogues", 0),
            "source_turns": state.get("source_turns", 0),
        },
        "reconciliation": reconciliation,
        "report_digest": report_digest,
        "report_sha256": report_sha256,
        "schema_id": RECEIPT_SCHEMA_ID,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "status": status,
        "ucns_full_corpus": (
            None
            if not isinstance(state.get("ucns_full_corpus_gate"), Mapping)
            else {
                "failure": state["ucns_full_corpus_gate"].get("failure"),
                "gate_effect": state["ucns_full_corpus_gate"]["gate_effect"],
                "processed_turn_count": state["ucns_full_corpus_gate"][
                    "processed_turn_count"
                ],
                "receipt_id": (
                    state["ucns_full_corpus_gate"]["receipt"]["receipt_id"]
                    if state["ucns_full_corpus_gate"]["receipt"] is not None
                    else None
                ),
                "source_native_reconciliation": state[
                    "ucns_full_corpus_gate"
                ].get("source_native_reconciliation"),
                "status": state["ucns_full_corpus_gate"]["status"],
            }
        ),
    }
    receipt["receipt_digest"] = _digest(receipt)
    return receipt


def run_archive(
    archive_path: Path,
    *,
    adapter: ActualUCNSAdapter,
    full_corpus_gate: UCNSFullCorpusGate,
    edcm_tree: str,
    ucns_commit: str,
    manifest: AdmissionManifest | None = None,
    checkpoint_path: Path | None = None,
    checkpoint_every: int = 100,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Run and reconcile the entire admitted archive.

    ``adapter``, ``full_corpus_gate``, and immutable producer identities are explicit
    so tests can exercise the runner without installing optional siblings.
    Production CLI use loads and verifies the pinned UCNS checkout and clean
    EDCM package tree first.
    """

    manifest = manifest or load_admission_manifest()
    if checkpoint_every < 1:
        raise CorpusRunError(
            "checkpoint_every must be positive",
            code="CHECKPOINT_INTERVAL",
        )
    archive_identity, archive = _archive_identity(archive_path, manifest)
    state = _new_state(
        archive_sha256=archive_identity["sha256"],
        admission_digest=manifest.digest,
        edcm_tree=edcm_tree,
        ucns_commit=ucns_commit,
    )
    try:
        test_ids = set(
            _load_partition_ids(archive, str(manifest.source["test_member"]))
        )
        validation_ids = set(
            _load_partition_ids(
                archive, str(manifest.source["validation_member"])
            )
        )
        if test_ids.intersection(validation_ids):
            raise CorpusRunError(
                "test and validation dialogue identifiers overlap",
                code="PARTITION_OVERLAP",
                state=state,
            )

        expected_checkpoint_identity = {
            "admission_digest": manifest.digest,
            "archive_sha256": archive_identity["sha256"],
            "edcm_tree": edcm_tree,
            "ucns_commit": ucns_commit,
        }
        resumed = (
            _load_checkpoint(
                checkpoint_path,
                expected=expected_checkpoint_identity,
            )
            if checkpoint_path is not None
            else None
        )
        if resumed is not None:
            state = resumed
        resume_dialogues = int(state["dialogues"])
        verified_prefix = EMPTY_CHAIN_DIGEST
        seen_ids: set[str] = set()
        seen_test_ids: set[str] = set()
        seen_validation_ids: set[str] = set()

        data_member = str(manifest.source["data_member"])
        try:
            binary = archive.open(data_member, "r")
        except KeyError as exc:
            raise CorpusRunError(
                f"data member missing: {data_member}",
                code="DATA_MEMBER_MISSING",
                state=state,
            ) from exc
        with binary, io.TextIOWrapper(
            binary,
            encoding="utf-8",
            errors="strict",
            newline="",
        ) as text:
            for dialogue_index, (
                dialogue_id,
                dialogue,
                raw_value_sha256,
            ) in enumerate(iter_top_level_object(text)):
                if dialogue_id in seen_ids:
                    raise CorpusRunError(
                        f"duplicate dialogue identifier: {dialogue_id}",
                        code="DIALOGUE_DUPLICATE",
                        state=state,
                    )
                seen_ids.add(dialogue_id)
                if dialogue_id in test_ids:
                    partition = "test"
                    seen_test_ids.add(dialogue_id)
                elif dialogue_id in validation_ids:
                    partition = "validation"
                    seen_validation_ids.add(dialogue_id)
                else:
                    partition = "train"

                source_record = {
                    "dialogue_id": dialogue_id,
                    "dialogue_index": dialogue_index,
                    "raw_value_sha256": raw_value_sha256,
                }
                if dialogue_index < resume_dialogues:
                    verified_prefix = _chain(verified_prefix, source_record)
                    if dialogue_index == resume_dialogues - 1:
                        if (
                            verified_prefix
                            != state["source_dialogue_digest_chain"]
                            or dialogue_id
                            != state["last_completed_dialogue_id"]
                        ):
                            raise CorpusRunError(
                                "checkpoint source prefix does not match the archive",
                                code="CHECKPOINT_PREFIX",
                                state=state,
                            )
                    continue

                _observe_dialogue(
                    adapter=adapter,
                    dialogue_index=dialogue_index,
                    dialogue_id=dialogue_id,
                    dialogue=dialogue,
                    partition=partition,
                    raw_value_sha256=raw_value_sha256,
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

        reconciliation = _reconciliation(
            state,
            manifest,
            seen_dialogue_count=len(seen_ids),
            seen_test_ids=seen_test_ids,
            seen_validation_ids=seen_validation_ids,
            test_ids=test_ids,
            validation_ids=validation_ids,
        )
        if not reconciliation["complete"]:
            raise CorpusRunError(
                "full-corpus reconciliation failed",
                code="RECONCILIATION_FAILED",
                state=state,
            )
        ucns_tracker = {
            "dialogues": 0,
            "turn_evidence_digest_chain": EMPTY_CHAIN_DIGEST,
            "turns": 0,
        }
        ucns_turns = _iter_ucns_full_corpus_turns(
            archive,
            manifest,
            ucns_tracker,
        )
        try:
            ucns_gate_report = full_corpus_gate.execute(
                manifest,
                ucns_turns,
            )
        finally:
            ucns_turns.close()
        source_native_checks = {
            "dialogue_count_matches_source_native_pass": (
                ucns_tracker["dialogues"] == state["dialogues"]
            ),
            "turn_count_matches_source_native_pass": (
                ucns_tracker["turns"] == state["source_turns"]
                and ucns_gate_report["processed_turn_count"]
                == state["source_turns"]
            ),
            "turn_evidence_chain_matches_source_native_pass": (
                ucns_tracker["turn_evidence_digest_chain"]
                == state["turn_evidence_digest_chain"]
            ),
        }
        ucns_gate_report["source_native_reconciliation"] = {
            "checks": source_native_checks,
            "complete": all(source_native_checks.values()),
            "dialogues": ucns_tracker["dialogues"],
            "turn_evidence_digest_chain": ucns_tracker[
                "turn_evidence_digest_chain"
            ],
            "turns": ucns_tracker["turns"],
        }
        state["ucns_full_corpus_gate"] = ucns_gate_report
        if (
            ucns_gate_report["status"] != "complete"
            or ucns_gate_report["receipt"] is None
            or not ucns_gate_report["source_native_reconciliation"]["complete"]
        ):
            raise CorpusRunError(
                "UCNS v0.14.1 full-corpus completion gate did not reconcile",
                code="UCNS_FULL_CORPUS_INCOMPLETE",
                state=state,
            )
        report = _build_report(
            manifest=manifest,
            archive_identity=archive_identity,
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
            report_digest=report["report_digest"],
            report_sha256=sha256(report_text.encode("utf-8")).hexdigest(),
            reconciliation=reconciliation,
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
    finally:
        archive.close()


def _verify_git_tree(
    root: Path,
    pathspec: str,
    *,
    environment: dict[str, str],
    treeish: str = "HEAD",
    producer_name: str = "EDCM",
) -> None:
    dirty_code = f"{producer_name}_DIRTY"
    try:
        tree_output = subprocess.run(
            [
                "git",
                "ls-tree",
                "-r",
                "-z",
                "--name-only",
                treeish,
                "--",
                pathspec,
            ],
            cwd=root,
            check=True,
            capture_output=True,
            env=environment,
        ).stdout
        tracked_paths = {
            Path(os.fsdecode(raw_path))
            for raw_path in tree_output.split(b"\0")
            if raw_path
        }
        scope = root / pathspec
        actual_paths = (
            {path.relative_to(root) for path in scope.rglob("*") if path.is_file()}
            if scope.is_dir()
            else {scope.relative_to(root)}
        )
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise CorpusRunError(
            f"{producer_name} package tree cannot be verified",
            code="GIT_IDENTITY",
        ) from exc
    unexpected_paths = {
        path
        for path in actual_paths - tracked_paths
        if not (path.suffix == ".pyc" and "__pycache__" in path.parts)
    }
    if tracked_paths - actual_paths or unexpected_paths:
        raise CorpusRunError(
            f"{producer_name} package files differ from the sealed commit",
            code=dirty_code,
        )
    for relative_path in sorted(tracked_paths):
        try:
            expected = subprocess.run(
                [
                    "git",
                    "cat-file",
                    "blob",
                    f"{treeish}:{relative_path.as_posix()}",
                ],
                cwd=root,
                check=True,
                capture_output=True,
                env=environment,
            ).stdout
            observed = (root / relative_path).read_bytes()
        except (OSError, subprocess.CalledProcessError) as exc:
            raise CorpusRunError(
                f"{producer_name} package bytes cannot be verified",
                code="GIT_IDENTITY",
            ) from exc
        if observed != expected:
            raise CorpusRunError(
                f"{producer_name} package file differs from the sealed commit: {relative_path}",
                code=dirty_code,
            )
    verified_paths = {(root / path).resolve() for path in tracked_paths}
    for cached_path in scope.rglob("*.pyc") if scope.is_dir() else ():
        if not _is_runtime_cache(cached_path):
            continue
        try:
            source_path = Path(
                importlib.util.source_from_cache(str(cached_path))
            ).resolve()
        except ValueError:
            continue
        if source_path not in verified_paths:
            continue
        try:
            _verify_cached_bytecode(
                cached_path.resolve(),
                verified_paths=verified_paths,
            )
        except UCNSAdapterConstructionError as exc:
            raise CorpusRunError(
                f"{producer_name} cached bytecode differs from the sealed source: {cached_path.name}",
                code=dirty_code,
            ) from exc


def _git_commit(
    root: Path,
    *,
    require_clean: bool,
    verify_tree: str | None = None,
    producer_name: str = "EDCM",
    expected_commit: str | None = None,
) -> str:
    environment = dict(os.environ)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD^{commit}"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CorpusRunError(
            f"Git identity cannot be resolved: {type(exc).__name__}",
            code="GIT_IDENTITY",
        ) from exc
    if require_clean and status:
        raise CorpusRunError(
            f"{producer_name} tracked files must be clean before a sealed corpus run",
            code=f"{producer_name}_DIRTY",
        )
    if expected_commit is not None and commit != expected_commit:
        raise CorpusRunError(
            f"{producer_name} checkout changed after sealed snapshot creation",
            code="GIT_IDENTITY",
        )
    if verify_tree is not None:
        _verify_git_tree(
            root,
            verify_tree,
            environment=environment,
            treeish=commit,
            producer_name=producer_name,
        )
    return commit


def _git_tree_identity(
    root: Path,
    pathspec: str,
    *,
    treeish: str = "HEAD",
) -> str:
    environment = dict(os.environ)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    try:
        tree = subprocess.run(
            ["git", "rev-parse", "--verify", f"{treeish}:{pathspec}"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CorpusRunError(
            "Git package-tree identity cannot be resolved",
            code="GIT_IDENTITY",
        ) from exc
    if len(tree) != 40 or any(character not in "0123456789abcdef" for character in tree):
        raise CorpusRunError(
            "Git package-tree identity is malformed",
            code="GIT_IDENTITY",
        )
    return tree


def _load_pinned_runtime(
    ucns_source_root: Path,
) -> tuple[ActualUCNSAdapter, UCNSFullCorpusGate]:
    source_path = (ucns_source_root / "src").resolve()
    if not source_path.is_dir():
        raise CorpusRunError(
            "UCNS checkout has no src directory",
            code="UCNS_SOURCE_LAYOUT",
        )
    commit = _git_commit(
        ucns_source_root,
        require_clean=True,
        verify_tree="src/ucns",
        producer_name="UCNS",
    )
    if commit != PINNED_UCNS_COMMIT:
        raise CorpusRunError(
            f"UCNS checkout mismatch: expected {PINNED_UCNS_COMMIT}, got {commit}",
            code="UCNS_COMMIT",
        )
    for name in tuple(sys.modules):
        if name == "ucns" or name.startswith("ucns."):
            sys.modules.pop(name, None)
    importlib.invalidate_caches()
    sys.path.insert(0, str(source_path))
    try:
        module = importlib.import_module("ucns")
    except Exception as exc:
        raise CorpusRunError(
            f"authenticated UCNS import failed: {type(exc).__name__}: {exc}",
            code="UCNS_IMPORT",
        ) from exc
    finally:
        sys.path.remove(str(source_path))
    module_path = Path(module.__file__).resolve()
    if not module_path.is_relative_to(source_path):
        raise CorpusRunError(
            "imported UCNS module is not from the pinned checkout",
            code="UCNS_IMPORT_IDENTITY",
        )
    try:
        adapter = ActualUCNSAdapter(module)
        return adapter, UCNSFullCorpusGate(adapter._module)
    except UCNSAdapterConstructionError as exc:
        raise CorpusRunError(
            f"UCNS adapter construction failed: {exc}",
            code="UCNS_ADAPTER_CONSTRUCTION",
        ) from exc


def _incomplete_receipt(
    *,
    manifest: AdmissionManifest,
    error: CorpusRunError,
    archive_path: Path,
    edcm_tree: str | None,
    ucns_commit: str,
) -> dict[str, Any]:
    state = dict(error.state)
    state.setdefault("archive_sha256", None)
    state.setdefault("edcm_tree", edcm_tree)
    state.setdefault("ucns_commit", ucns_commit)
    state.setdefault("last_completed_dialogue_id", None)
    state.setdefault("last_completed_dialogue_index", None)
    state.setdefault("active_dialogue_id", None)
    state.setdefault("active_dialogue_index", None)
    state.setdefault("active_turn_index", None)
    state.setdefault("adapter_turns", 0)
    state.setdefault("dialogues", 0)
    state.setdefault("source_turns", 0)
    receipt = _build_receipt(
        manifest=manifest,
        state=state,
        status="incomplete",
        error_code=error.code,
        error_reason=str(error),
    )
    receipt["source_artifact_filename"] = archive_path.name
    receipt["receipt_digest"] = _digest(
        {key: value for key, value in receipt.items() if key != "receipt_digest"}
    )
    return receipt


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--ucns-source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--checkpoint-every", type=int, default=100)
    return parser.parse_args(argv)


def _sealed_main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    manifest = load_admission_manifest()
    sealed_repository_root = os.environ.get(_SEALED_REPOSITORY_ROOT_ENV)
    repository_root = (
        Path(sealed_repository_root).resolve()
        if sealed_repository_root is not None
        else Path(__file__).resolve().parents[2]
    )
    sealed_commit = os.environ.get(_SEALED_EDCM_COMMIT_ENV)
    sealed_tree = os.environ.get(_SEALED_EDCM_TREE_ENV)
    edcm_tree: str | None = None

    def emit_failure(error: CorpusRunError) -> int:
        receipt = _incomplete_receipt(
            manifest=manifest,
            error=error,
            archive_path=args.archive,
            edcm_tree=edcm_tree,
            ucns_commit=PINNED_UCNS_COMMIT,
        )
        try:
            _write_json_atomic(args.receipt.resolve(), receipt)
        except OSError as receipt_error:
            print(
                json.dumps(
                    {
                        "error_code": error.code,
                        "reason": str(error),
                        "receipt_error": (
                            f"{type(receipt_error).__name__}: {receipt_error}"
                        ),
                        "status": "incomplete-receipt-write-failed",
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            return 1
        print(
            json.dumps(
                {
                    "error_code": error.code,
                    "reason": str(error),
                    "receipt": str(args.receipt),
                    "status": "incomplete",
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1

    try:
        commit = _git_commit(
            repository_root,
            require_clean=True,
            verify_tree="edcm",
            expected_commit=sealed_commit,
        )
        edcm_tree = _git_tree_identity(
            repository_root,
            "edcm",
            treeish=commit,
        )
        if sealed_tree is not None and edcm_tree != sealed_tree:
            raise CorpusRunError(
                "EDCM package tree differs from the sealed bootstrap snapshot",
                code="GIT_IDENTITY",
            )
        adapter, full_corpus_gate = _load_pinned_runtime(
            args.ucns_source_root.resolve()
        )
        report, receipt = run_archive(
            args.archive.resolve(),
            adapter=adapter,
            full_corpus_gate=full_corpus_gate,
            edcm_tree=edcm_tree,
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
                    "dialogues": report["execution"]["dialogues"],
                    "receipt": str(args.receipt),
                    "report": str(args.output),
                    "status": "complete",
                    "turns": report["execution"]["source_turns"],
                },
                sort_keys=True,
            )
        )
        return 0
    except CorpusRunError as exc:
        return emit_failure(exc)
    except OSError as exc:
        return emit_failure(
            CorpusRunError(
                f"output storage failed: {type(exc).__name__}: {exc}",
                code="OUTPUT_IO",
            )
        )


def _run_in_fresh_process(
    argv: list[str],
    *,
    repository_root: Path | None = None,
) -> int:
    source_repository_root = (
        Path(__file__).resolve().parents[2]
        if repository_root is None
        else repository_root.resolve()
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            _ISOLATED_WORKER_BOOTSTRAP,
            str(source_repository_root),
            _SEALED_WORKER_FLAG,
            *argv,
        ],
        check=False,
    )
    return completed.returncode


def main(argv: list[str] | None = None) -> int:
    """Run the seal in an isolated interpreter with a fresh EDCM module graph."""

    return _run_in_fresh_process(
        list(sys.argv[1:] if argv is None else argv)
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == _SEALED_WORKER_FLAG:
        raise SystemExit(_sealed_main(sys.argv[2:]))
    raise SystemExit(main())
