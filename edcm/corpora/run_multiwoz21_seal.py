#!/usr/bin/env python3
"""Trusted source launcher for the sealed MultiWOZ 2.1 corpus runner.

Execute this file directly. Python executes a script from its source bytes and
does not substitute a sibling bytecode cache before this launcher establishes
the replacement-disabled Git snapshot boundary.
"""

# === MODULE_BUILD ===
# id: edcm_multiwoz21_seal_launcher
#   module_name: run_multiwoz21_seal
#   module_kind: adapter
#   summary: establishes a cache-independent replacement-disabled Git snapshot before importing the sealed MultiWOZ runner
#   owner: Erin Spencer
#   public_surface: main
#   internal_surface: _git_environment, _option_value, _pop_repository_root, _write_bootstrap_failure, _extract_source_only
#   auth_boundary: directly executed source is the bootstrap trust root and the child admits only the exact archived edcm tree
#   storage_boundary: reads a caller-held archive and writes only caller-selected aggregate, receipt, and checkpoint paths
#   network_boundary: none
#   user_data_boundary: does not inspect dialogue text; the isolated runner owns in-memory source processing
#   admin_only: false
#   tests: tests.test_multiwoz21_corpus
#   rollout: invoke this source file directly from a clean repository checkout
#   rollback: remove the launcher and supersede evidence produced by its edcm tree identity
#   requires: git, python3, edcm_multiwoz21_corpus
#   since: 2026-08-01
#   unresolved: the host Python interpreter and Git executable remain external trust roots
# === END MODULE_BUILD ===


from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile


BOOTSTRAP_ADMISSION_DIGEST = (
    "dfe7b65a9f4af739a4d149e65e60674333e87f56ff9db3cd07c144b9cab85fc2"
)
PINNED_UCNS_COMMIT = "872f53571d5dc2f133ff1813b7bdffd3a9c309f8"
REPOSITORY_ROOT_OPTION = "--edcm-repository-root"
SEALED_REPOSITORY_ROOT_ENV = "EDCM_SEALED_REPOSITORY_ROOT"
SEALED_EDCM_COMMIT_ENV = "EDCM_SEALED_COMMIT"
SEALED_EDCM_TREE_ENV = "EDCM_SEALED_TREE"
SEALED_SNAPSHOT_ROOT_ENV = "EDCM_SEALED_SNAPSHOT_ROOT"
WORKER_ENTRY = """
import runpy
import sys

snapshot = sys.argv.pop(1)
sys.dont_write_bytecode = True
sys.pycache_prefix = None
sys.path.insert(0, snapshot)
runpy.run_module("edcm.corpora.multiwoz21", run_name="__main__")
"""


def _git_environment() -> dict[str, str]:
    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _option_value(arguments: list[str], name: str) -> str | None:
    prefix = f"{name}="
    for index, argument in enumerate(arguments):
        if argument == name:
            return arguments[index + 1] if index + 1 < len(arguments) else None
        if argument.startswith(prefix):
            return argument[len(prefix) :]
    return None


def _pop_repository_root(arguments: list[str]) -> tuple[Path, list[str]]:
    remaining = list(arguments)
    values: list[str] = []
    index = 0
    prefix = f"{REPOSITORY_ROOT_OPTION}="
    while index < len(remaining):
        argument = remaining[index]
        if argument == REPOSITORY_ROOT_OPTION:
            if index + 1 >= len(remaining):
                raise ValueError(f"{REPOSITORY_ROOT_OPTION} requires a path")
            values.append(remaining[index + 1])
            del remaining[index : index + 2]
            continue
        if argument.startswith(prefix):
            values.append(argument[len(prefix) :])
            del remaining[index]
            continue
        index += 1
    if len(values) > 1:
        raise ValueError(f"{REPOSITORY_ROOT_OPTION} may be supplied only once")
    root = (
        Path(values[0])
        if values
        else Path(__file__).resolve().parents[2]
    )
    return root.resolve(), remaining


def _write_bootstrap_failure(
    arguments: list[str],
    reason: str,
    edcm_tree: str | None,
) -> None:
    receipt_value = _option_value(arguments, "--receipt")
    if receipt_value is None:
        return
    archive_value = _option_value(arguments, "--archive")
    receipt = {
        "admission_digest": BOOTSTRAP_ADMISSION_DIGEST,
        "corpus_id": "multiwoz-2.1",
        "error": {"code": "GIT_IDENTITY", "reason": reason},
        "identities": {
            "archive_sha256": None,
            "edcm_tree": edcm_tree,
            "ucns_commit": PINNED_UCNS_COMMIT,
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
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
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


def _extract_source_only(package: tarfile.TarFile, snapshot: str) -> None:
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


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    try:
        repository_root, worker_arguments = _pop_repository_root(arguments)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    environment = _git_environment()
    edcm_tree: str | None = None
    snapshot_context: tempfile.TemporaryDirectory[str] | None = None
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
        snapshot_context = tempfile.TemporaryDirectory(
            prefix="edcm-sealed-source-"
        )
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as package:
            _extract_source_only(package, snapshot_context.name)
    except (
        OSError,
        subprocess.CalledProcessError,
        tarfile.TarError,
        RuntimeError,
    ) as error:
        if snapshot_context is not None:
            snapshot_context.cleanup()
        reason = f"sealed bootstrap failed: {type(error).__name__}: {error}"
        try:
            _write_bootstrap_failure(worker_arguments, reason, edcm_tree)
        except OSError as receipt_error:
            print(
                f"{reason}; receipt failure: "
                f"{type(receipt_error).__name__}: {receipt_error}",
                file=sys.stderr,
            )
        return 1

    with snapshot_context as snapshot:
        child_environment = dict(environment)
        child_environment[SEALED_REPOSITORY_ROOT_ENV] = str(repository_root)
        child_environment[SEALED_EDCM_COMMIT_ENV] = commit
        child_environment[SEALED_EDCM_TREE_ENV] = edcm_tree
        child_environment[SEALED_SNAPSHOT_ROOT_ENV] = snapshot
        child_environment.pop("PYTHONPYCACHEPREFIX", None)
        completed = subprocess.run(
            [
                sys.executable,
                "-I",
                "-c",
                WORKER_ENTRY,
                snapshot,
                *worker_arguments,
            ],
            check=False,
            env=child_environment,
        )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
