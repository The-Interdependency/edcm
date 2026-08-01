"""Exact EDCM consumer for the UCNS word-gonol observation profile.

Usage guidance
--------------
Install the ``ucns-profile`` extra and pass ``ucns_turns`` as an ordered
sequence of exact ``(speaker_id, text)`` tuples. The adapter observes every
turn; it does not parse speaker boundaries from a flattened transcript.
Pinned Unicode SPACE manifestations share the public carrier at position zero,
while explicit source and carrier fields keep every original code point
recoverable without normalization.

The resulting ``ucns_profile_observation`` is exact corpus evidence. It is not
UCNS geometry, factorization evidence, theorem status, or an EDCM measurement
validity claim. The retired ordered-occurrence bridge input forms fail closed.
"""

# === MODULE_BUILD ===
# id: edcm_ucns_adapter
#   module_name: ucns_adapter
#   module_kind: adapter
#   summary: fail-closed consumer for the exact EDCM-only UCNS word-gonol profile from the reviewed v0.19 producer, preserving full-corpus speaker-turn observations without coordinate, geometry, or proof transfer
#   owner: Erin Spencer
#   public_surface: ActualUCNSAdapter, UCNSProfileObservationEvidence, UCNSIntegrationStatus, UCNSAdapterSelection, select_ucns_adapter, inspect_ucns_adapter
#   internal_surface: _canonical_bytes, _digest, _package_present, _verify_checkout_package_tree, _source_checkout_commit, _verify_cached_bytecode, _verify_distribution_files, _resolve_ucns_producer_commit, _token_record, _segment_record, _turn_record
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: exact source turns remain in caller-owned in-memory results and are not transmitted
#   admin_only: false
#   tests: tests.test_ucns_adapter, tests.test_ucns_dependency, tests.test_shared_stack_contract
#   rollout: optional exact-profile activation only when the pinned producer commit and profile surface match
#   rollback: suspend the optional adapter; base EDCM measurement remains operational
#   requires: ucns.edcm at 872f53571d5dc2f133ff1813b7bdffd3a9c309f8
#   since: 2026-07-25
#   unresolved: consumption of the upstream nonselected ordered source-coordinate candidate, higher-gonol composition, and projection policies remain outside this observation adapter
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: edcm_ucns_exact_profile_only
#   given: an importable UCNS package is considered for activation
#   then: the checkout package bytes match the pinned Git tree or the installed package inventory and RECORD hashes match with source-derived cached bytecode, and any producer-owned commit identity plus every profile identity, option, Unicode-scalar source domain, 25-value SPACE pin, public-alphabet invariant, and producer type match the pinned EDCM word-gonol surface or the adapter remains suspended
#   class: safety
#   since: 2026-07-25
#
# id: edcm_ucns_full_turn_observation
#   given: ordered ucns_turns enter the active adapter
#   then: all turns are observed in order with exact Unicode source witnesses, one unit of support per speaker turn, explicit origin-assigned SPACE boundaries, and retained non-SPACE out-of-alphabet evidence
#   class: evidence
#   since: 2026-07-25
#
# id: edcm_ucns_no_geometry_or_proof_transfer
#   given: exact profile observations are attached
#   then: geometry, factorization, theorem, certification, and measurement-validity attachment flags remain false
#   class: doctrine
#   since: 2026-07-25
# === END CONTRACTS ===

from __future__ import annotations

import base64
from dataclasses import asdict, dataclass, replace
import hashlib
import hmac
import importlib
from importlib import metadata as importlib_metadata
import importlib.util
import json
import marshal
import os
from pathlib import Path
import re
import subprocess
from types import CodeType, ModuleType
from typing import Any, Mapping, Protocol, Sequence
from urllib.parse import unquote, urlsplit
from urllib.request import url2pathname

UCNS_SOURCE_REPOSITORY = "https://github.com/The-Interdependency/ucns"
SUPPORTED_PROFILE = ("ucns.profile.edcm-word-gonol", "0.2.0")
SUPPORTED_PROFILE_SCOPE = "edcm-only"
PINNED_UCNS_COMMIT = "872f53571d5dc2f133ff1813b7bdffd3a9c309f8"
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_PUBLIC_GONOL_SHA256 = (
    "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
)
EXPECTED_SOURCE_DOMAIN = "unicode-scalar-values"
EXPECTED_SPACE_ASSIGNMENT_POLICY = "unicode-white-space-origin-v1"
EXPECTED_SPACE_CODE_POINT_LABELS = (
    "U+0009",
    "U+000A",
    "U+000B",
    "U+000C",
    "U+000D",
    "U+0020",
    "U+0085",
    "U+00A0",
    "U+1680",
    "U+2000",
    "U+2001",
    "U+2002",
    "U+2003",
    "U+2004",
    "U+2005",
    "U+2006",
    "U+2007",
    "U+2008",
    "U+2009",
    "U+200A",
    "U+2028",
    "U+2029",
    "U+202F",
    "U+205F",
    "U+3000",
)
EXPECTED_SPACE_CODE_POINTS_SHA256 = (
    "a5dc5ec34775d511a02b17911aa385c5d92908ee58749ea16d721cd53d19b944"
)
EXPECTED_PROFILE_OPTIONS = tuple(
    sorted(
        {
            "carrier_requirement": "mobius-origin-hidden-zero",
            "corpus_execution": "full-corpus",
            "gonol_initiation": "mobius-twist",
            "nesting_boundary": "superpositioned-space",
            "normalization": "none-preserve-source",
            "occurrence_operation": "ordered-concatenation",
            "out_of_alphabet": "retain-and-report",
            "profile_scope": "edcm-only",
            "smallest_gonol": "word",
            "source_domain": EXPECTED_SOURCE_DOMAIN,
            "space_assignment": EXPECTED_SPACE_ASSIGNMENT_POLICY,
            "support": "one-unit-per-speaker-turn",
            "token_alphabet": "public-gonol-157",
            "token_identity": "unicode-code-point",
        }.items()
    )
)
RESET_BOUNDARY_REASON = "exact EDCM UCNS word-gonol profile is unavailable or mismatched"
INSTALL_HINT = None
REJECTED_LEGACY_SCHEMAS = frozenset(
    {
        "ucns-canonical-json-v1",
        "ucns.bridge-record@1.0.0",
        "ucns.factorization-evidence@1.0.0",
        "ucns.bridge.edcm-metapat-ordered-occurrence",
    }
)
REJECTED_LEGACY_INPUTS = frozenset(
    {
        "ucns_object",
        "ucns_bridge_record",
        "ucns_bridge_record_json",
        "ucns_bridge_record_dict",
        "ucns_factorization_evidence",
        "ucns_factorization_evidence_json",
        "ucns_factorization_evidence_dict",
    }
)


class UCNSAdapterConstructionError(RuntimeError):
    """Raised when UCNS fails the exact EDCM profile contract."""


class UnsupportedUCNSSchemaError(UCNSAdapterConstructionError):
    """Raised for retired or otherwise unsupported producer identities."""


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    package_present: bool
    producer_recognized: bool
    profile_supported: bool
    adapter_active: bool
    ucns_profile_observation_attached: bool = False
    ucns_object_attached: bool = False
    ucns_bridge_record_attached: bool = False
    ucns_scope_metadata_attached: bool = False
    ucns_factorization_evidence_attached: bool = False
    ucns_negative_certification_attached: bool = False
    ucns_theorem_status_attached: bool = False
    implementation_id: str = "edcm.ucns_adapter.word_gonol_profile"
    implementation_version: str | None = "0.2.0"
    source_repository: str = UCNS_SOURCE_REPOSITORY
    selection: str = "suspended"
    unresolved_constraints: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    @property
    def ucns_package_available(self) -> bool:
        return self.package_present

    @property
    def ucns_adapter_active(self) -> bool:
        return self.adapter_active

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ucns_package_available"] = self.package_present
        data["ucns_adapter_active"] = self.adapter_active
        return data


@dataclass(frozen=True)
class UCNSProfileObservationEvidence:
    profile_id: str
    profile_version: str
    profile_scope: str
    source_repository: str
    source_commit: str
    options: tuple[tuple[str, str], ...]
    normalization_policy: str
    support_policy: str
    corpus_execution: str
    smallest_gonol: str
    gonol_initiation: str
    source_domain: str
    space_assignment_policy: str
    space_code_point_labels: tuple[str, ...]
    space_code_points_sha256: str
    token_alphabet_size: int
    token_alphabet_sha256: str
    turns: tuple[dict[str, Any], ...]
    observation_digest: str
    evidence_mode: str = "exact-observation"
    projection_status: str = "not-projected"
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class UCNSAdapter(Protocol):
    @property
    def status(self) -> UCNSIntegrationStatus: ...

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]: ...


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _repository_identity(value: str) -> str:
    normalized = value.strip().removeprefix("git+").rstrip("/")
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized.removeprefix(
            "git@github.com:"
        )
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    return normalized.lower()


def _module_file(module: ModuleType) -> Path:
    raw = getattr(module, "__file__", None)
    if not isinstance(raw, str) or not raw:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: module file is unknown"
        )
    return Path(raw).resolve()


def _verify_checkout_package_tree(root: Path, module_file: Path) -> None:
    try:
        package_root = module_file.parent
        package_relative = package_root.relative_to(root)
        tree_output = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-tree",
                "-r",
                "-z",
                "--name-only",
                "HEAD",
                "--",
                package_relative.as_posix(),
            ],
            check=True,
            capture_output=True,
        ).stdout
        tracked_paths = {
            Path(os.fsdecode(raw_path))
            for raw_path in tree_output.split(b"\0")
            if raw_path
        }
        relative_module = module_file.relative_to(root)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise UCNSAdapterConstructionError(
            "UCNS checkout package tree cannot be verified"
        ) from exc
    if relative_module not in tracked_paths:
        raise UCNSAdapterConstructionError(
            "UCNS imported module is not tracked at the checkout commit"
        )
    actual_paths = {
        path.relative_to(root)
        for path in package_root.rglob("*")
        if path.is_file()
    }
    missing_paths = tracked_paths - actual_paths
    unexpected_paths = {
        path
        for path in actual_paths - tracked_paths
        if not (path.suffix == ".pyc" and "__pycache__" in path.parts)
    }
    if missing_paths or unexpected_paths:
        raise UCNSAdapterConstructionError(
            "UCNS checkout package files differ from the pinned tree"
        )
    for relative_path in sorted(tracked_paths):
        try:
            expected = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "cat-file",
                    "blob",
                    f"HEAD:{relative_path.as_posix()}",
                ],
                check=True,
                capture_output=True,
            ).stdout
            observed = (root / relative_path).read_bytes()
        except (OSError, subprocess.CalledProcessError) as exc:
            raise UCNSAdapterConstructionError(
                "UCNS checkout package bytes cannot be verified"
            ) from exc
        if not hmac.compare_digest(observed, expected):
            raise UCNSAdapterConstructionError(
                f"UCNS checkout file differs from the pinned tree: {relative_path}"
            )


def _git_checkout_commit(
    root: Path,
    *,
    module_file: Path | None = None,
) -> str:
    try:
        remote_names = subprocess.run(
            ["git", "-C", str(root), "remote"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        remote_urls = tuple(
            url
            for name in remote_names
            for url in subprocess.run(
                ["git", "-C", str(root), "remote", "get-url", "--all", name],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.splitlines()
        )
        commit = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip().lower()
        status = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "status",
                "--porcelain",
                "--untracked-files=all",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        if module_file is not None:
            relative_module = module_file.relative_to(root)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "ls-files",
                    "--error-unmatch",
                    "--",
                    relative_module.as_posix(),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable from editable checkout"
        ) from exc
    if module_file is not None:
        _verify_checkout_package_tree(root, module_file)
    expected_repository = _repository_identity(UCNS_SOURCE_REPOSITORY)
    if not any(
        _repository_identity(remote) == expected_repository
        for remote in remote_urls
    ):
        raise UnsupportedUCNSSchemaError(
            "UCNS producer repository identity mismatch"
        )
    if status:
        raise UCNSAdapterConstructionError(
            "UCNS checkout has tracked or untracked modifications"
        )
    if not _COMMIT_RE.fullmatch(commit):
        raise UCNSAdapterConstructionError(
            "UCNS editable checkout commit identity is malformed"
        )
    return commit


def _source_checkout_commit(module: ModuleType) -> str | None:
    module_file = _module_file(module)
    try:
        root_text = subprocess.run(
            [
                "git",
                "-C",
                str(module_file.parent),
                "rev-parse",
                "--show-toplevel",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    root = Path(root_text).resolve()
    expected_modules = {
        (root / "src/ucns/__init__.py").resolve(),
        (root / "ucns/__init__.py").resolve(),
    }
    if module_file not in expected_modules:
        return None
    return _git_checkout_commit(root, module_file=module_file)


def _verify_cached_bytecode(
    installed_path: Path,
    *,
    verified_paths: set[Path],
) -> None:
    try:
        source_path = Path(
            importlib.util.source_from_cache(str(installed_path))
        ).resolve()
    except ValueError as exc:
        raise UCNSAdapterConstructionError(
            f"UCNS cached bytecode path is malformed: {installed_path.name}"
        ) from exc
    if source_path not in verified_paths:
        raise UCNSAdapterConstructionError(
            f"UCNS cached bytecode has no hash-verified source: {installed_path.name}"
        )
    optimization_match = re.search(r"\.opt-([0-2])\.pyc$", installed_path.name)
    if ".opt-" in installed_path.name and optimization_match is None:
        raise UCNSAdapterConstructionError(
            f"UCNS cached bytecode optimization is unsupported: {installed_path.name}"
        )
    optimization = (
        int(optimization_match.group(1))
        if optimization_match is not None
        else 0
    )
    try:
        bytecode = installed_path.read_bytes()
        if len(bytecode) < 16 or bytecode[:4] != importlib.util.MAGIC_NUMBER:
            raise ValueError("invalid bytecode header")
        cached_code = marshal.loads(bytecode[16:])
        source_code = compile(
            source_path.read_bytes(),
            str(source_path),
            "exec",
            dont_inherit=True,
            optimize=optimization,
        )
    except (EOFError, OSError, SyntaxError, TypeError, ValueError) as exc:
        raise UCNSAdapterConstructionError(
            f"UCNS cached bytecode is unverifiable: {installed_path.name}"
        ) from exc
    if not isinstance(cached_code, CodeType) or cached_code != source_code:
        raise UCNSAdapterConstructionError(
            f"UCNS cached bytecode does not match its hash-verified source: {installed_path.name}"
        )


def _verify_distribution_files(
    distribution: importlib_metadata.Distribution,
    *,
    module_file: Path,
) -> None:
    files = distribution.files
    if files is None:
        raise UCNSAdapterConstructionError(
            "UCNS producer distribution has no installed-file manifest"
        )
    verified_paths: set[Path] = set()
    cached_bytecode: set[Path] = set()
    direct_url_verified = False
    for entry in files:
        record_path = Path(str(entry))
        file_hash = entry.hash
        if file_hash is None:
            if (
                record_path.name == "RECORD"
                and record_path.parent.name.endswith(".dist-info")
            ):
                continue
            if (
                record_path.suffix == ".pyc"
                and "__pycache__" in record_path.parts
            ):
                installed_path = Path(distribution.locate_file(entry)).resolve()
                if not installed_path.is_file():
                    raise UCNSAdapterConstructionError(
                        f"UCNS installed file is missing: {record_path}"
                    )
                cached_bytecode.add(installed_path)
                continue
            raise UCNSAdapterConstructionError(
                f"UCNS installed file has no recorded hash: {record_path}"
            )
        if file_hash.mode != "sha256":
            raise UCNSAdapterConstructionError(
                f"UCNS installed file uses an unsupported hash: {record_path}"
            )
        installed_path = Path(distribution.locate_file(entry)).resolve()
        if not installed_path.is_file():
            raise UCNSAdapterConstructionError(
                f"UCNS installed file is missing: {record_path}"
            )
        if entry.size is not None and installed_path.stat().st_size != entry.size:
            raise UCNSAdapterConstructionError(
                f"UCNS installed file size mismatch: {record_path}"
            )
        with installed_path.open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").digest()
        encoded = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        if not hmac.compare_digest(encoded, file_hash.value):
            raise UCNSAdapterConstructionError(
                f"UCNS installed file hash mismatch: {record_path}"
            )
        verified_paths.add(installed_path)
        if (
            record_path.name == "direct_url.json"
            and record_path.parent.name.endswith(".dist-info")
        ):
            direct_url_verified = True
    if module_file not in verified_paths:
        raise UCNSAdapterConstructionError(
            "UCNS module is absent from the installed-file manifest"
        )
    if not direct_url_verified:
        raise UCNSAdapterConstructionError(
            "UCNS direct_url.json is absent from the installed-file manifest"
        )
    package_root = module_file.parent
    for installed_path in package_root.rglob("*"):
        if not installed_path.is_file():
            continue
        resolved_path = installed_path.resolve()
        if (
            installed_path.suffix == ".pyc"
            and "__pycache__" in installed_path.parts
        ):
            cached_bytecode.add(resolved_path)
        elif resolved_path not in verified_paths:
            raise UCNSAdapterConstructionError(
                f"UCNS installed package file is absent from RECORD: {installed_path.name}"
            )
    for installed_path in sorted(cached_bytecode):
        _verify_cached_bytecode(installed_path, verified_paths=verified_paths)


def _distribution_commit(module: ModuleType) -> str:
    checkout_commit = _source_checkout_commit(module)
    if checkout_commit is not None:
        return checkout_commit
    try:
        distribution = importlib_metadata.distribution("ucns")
    except importlib_metadata.PackageNotFoundError as exc:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable from distribution metadata"
        ) from exc
    try:
        direct_url_text = distribution.read_text("direct_url.json")
    except (OSError, UnicodeError) as exc:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: direct_url.json unreadable"
        ) from exc
    if not direct_url_text:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: direct_url.json missing"
        )
    try:
        direct_url = json.loads(direct_url_text)
    except (TypeError, json.JSONDecodeError) as exc:
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: direct_url.json invalid"
        ) from exc
    if not isinstance(direct_url, Mapping):
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: direct_url.json invalid"
        )
    module_file = _module_file(module)
    source_url = direct_url.get("url")
    if not isinstance(source_url, str):
        raise UCNSAdapterConstructionError(
            "UCNS producer commit identity unavailable: source URL missing"
        )
    vcs_info = direct_url.get("vcs_info")
    if isinstance(vcs_info, Mapping):
        if vcs_info.get("vcs") != "git":
            raise UnsupportedUCNSSchemaError(
                "UCNS producer distribution is not Git-backed"
            )
        if _repository_identity(source_url) != _repository_identity(
            UCNS_SOURCE_REPOSITORY
        ):
            raise UnsupportedUCNSSchemaError(
                "UCNS producer repository identity mismatch"
            )
        installed_module = Path(
            distribution.locate_file("ucns/__init__.py")
        ).resolve()
        if module_file != installed_module:
            raise UCNSAdapterConstructionError(
                "UCNS module does not belong to the identified distribution"
            )
        _verify_distribution_files(distribution, module_file=module_file)
        commit = str(vcs_info.get("commit_id", "")).lower()
        if not _COMMIT_RE.fullmatch(commit):
            raise UCNSAdapterConstructionError(
                "UCNS producer distribution commit identity is malformed"
            )
        return commit
    if isinstance(direct_url.get("dir_info"), Mapping):
        parsed = urlsplit(source_url)
        if parsed.scheme != "file":
            raise UCNSAdapterConstructionError(
                "UCNS editable distribution source is not a local checkout"
            )
        root = Path(url2pathname(unquote(parsed.path))).resolve()
        if not module_file.is_relative_to(root):
            raise UCNSAdapterConstructionError(
                "UCNS module does not belong to the editable distribution"
            )
        return _git_checkout_commit(root, module_file=module_file)
    raise UCNSAdapterConstructionError(
        "UCNS producer commit identity unavailable from distribution metadata"
    )


def _resolve_ucns_producer_commit(module: ModuleType) -> str:
    installed_commit = _distribution_commit(module)
    producer_commit = getattr(module, "UCNS_PRODUCER_COMMIT", None)
    if producer_commit is not None:
        declared_commit = str(producer_commit).lower()
        if not _COMMIT_RE.fullmatch(declared_commit):
            raise UCNSAdapterConstructionError(
                "UCNS producer-owned commit identity is malformed"
            )
        if declared_commit != installed_commit:
            raise UnsupportedUCNSSchemaError(
                "UCNS producer-owned and installed commit identities disagree"
            )
    return installed_commit


def _token_record(token: Any) -> dict[str, Any]:
    source_value = token.value
    source_code_point = token.code_point
    carrier_position = token.alphabet_position
    carrier_token = token.carrier_token
    is_space_manifestation = token.is_space
    has_carrier_assignment = token.has_carrier_assignment
    is_public_gonol_token = token.is_public_gonol_token
    if token.in_alphabet != has_carrier_assignment:
        raise ValueError(
            "UCNS token in_alphabet alias disagrees with carrier assignment"
        )
    return {
        # ``value`` and ``code_point`` remain for consumers of the 0.1 record.
        # Their meaning has always been the exact source witness.
        "value": source_value,
        "code_point": source_code_point,
        "codepoint_offset": token.codepoint_offset,
        "alphabet_position": carrier_position,
        "in_alphabet": token.in_alphabet,
        # The explicit names prevent carrier equivalence from looking like
        # Unicode normalization. Source bytes/code points remain recoverable.
        "source_value": source_value,
        "source_code_point": source_code_point,
        "carrier_token": carrier_token,
        "carrier_position": carrier_position,
        "is_space_manifestation": is_space_manifestation,
        "has_carrier_assignment": has_carrier_assignment,
        "is_public_gonol_token": is_public_gonol_token,
    }


def _segment_record(module: ModuleType, segment: Any) -> dict[str, Any]:
    if isinstance(segment, module.EdcmWordGonol):
        carrier_unassigned = tuple(
            _token_record(token) for token in segment.carrier_unassigned
        )
        out_of_alphabet = tuple(
            _token_record(token) for token in segment.out_of_alphabet
        )
        if carrier_unassigned != out_of_alphabet:
            raise ValueError(
                "UCNS word out_of_alphabet alias disagrees with carrier_unassigned"
            )
        return {
            "kind": "word-gonol",
            "word_index": segment.word_index,
            "raw_text": segment.raw_text,
            "source_start": segment.source_start,
            "source_end": segment.source_end,
            "initiation_event": segment.initiation_event,
            "tokens": tuple(_token_record(token) for token in segment.tokens),
            "carrier_unassigned": carrier_unassigned,
            "out_of_alphabet": out_of_alphabet,
        }
    if isinstance(segment, module.SuperpositionedSpaceBoundary):
        return {
            "kind": "superpositioned-space-boundary",
            "raw_text": segment.raw_text,
            "roles": tuple(segment.roles),
            "token": _token_record(segment.token),
        }
    raise TypeError("UCNS profile emitted an unknown segment type")


def _turn_record(module: ModuleType, observation: Any) -> dict[str, Any]:
    carrier_unassigned = tuple(
        _token_record(token) for token in observation.carrier_unassigned
    )
    out_of_alphabet = tuple(
        _token_record(token) for token in observation.out_of_alphabet
    )
    if carrier_unassigned != out_of_alphabet:
        raise ValueError(
            "UCNS turn out_of_alphabet alias disagrees with carrier_unassigned"
        )
    if (
        observation.has_complete_carrier_assignment
        != observation.has_complete_alphabet_coverage
    ):
        raise ValueError(
            "UCNS turn alphabet-coverage alias disagrees with carrier assignment"
        )
    return {
        "speaker_id": observation.speaker_id,
        "turn_index": observation.turn_index,
        "raw_text": observation.raw_text,
        "source_id": observation.source_id,
        "unit_support": observation.unit_support,
        "segments": tuple(
            _segment_record(module, segment) for segment in observation.segments
        ),
        "word_count": len(observation.word_gonols),
        "nesting_boundary_count": len(observation.nesting_boundaries),
        "carrier_unassigned": carrier_unassigned,
        "out_of_alphabet": out_of_alphabet,
        "has_complete_carrier_assignment": (
            observation.has_complete_carrier_assignment
        ),
        "has_complete_alphabet_coverage": (
            observation.has_complete_alphabet_coverage
        ),
    }


class SuspendedUCNSAdapter:
    def __init__(self, *, package_present: bool) -> None:
        self._status = suspended_ucns_status(package_present=package_present)

    @property
    def status(self) -> UCNSIntegrationStatus:
        return self._status

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        state["ucns_integration"] = self.status.as_dict()
        state.pop("ucns_profile_observation", None)
        return state


class ActualUCNSAdapter:
    """Consumer of only the exact EDCM word-gonol observation surface."""

    def __init__(self, module: ModuleType) -> None:
        required = (
            "EDCM_PROFILE_ID",
            "EDCM_PROFILE_VERSION",
            "EDCM_PROFILE_SCOPE",
            "EDCM_PROFILE_OPTIONS",
            "EDCM_NORMALIZATION_POLICY",
            "EDCM_SUPPORT_POLICY",
            "EDCM_CORPUS_EXECUTION",
            "EDCM_SMALLEST_GONOL",
            "EDCM_GONOL_INITIATION",
            "EDCM_SOURCE_DOMAIN",
            "EDCM_SPACE_ASSIGNMENT_POLICY",
            "EDCM_SPACE_CODE_POINTS",
            "PUBLIC_GONOL_157",
            "PUBLIC_GONOL_SHA256",
            "EdcmWordGonolProfile",
            "EdcmWordGonol",
            "SuperpositionedSpaceBoundary",
            "public_gonol_sha256",
        )
        missing = [name for name in required if not hasattr(module, name)]
        if missing:
            raise UCNSAdapterConstructionError(
                "UCNS exact EDCM profile surface missing: " + ", ".join(missing)
            )
        producer_commit = _resolve_ucns_producer_commit(module)
        if producer_commit != PINNED_UCNS_COMMIT:
            raise UnsupportedUCNSSchemaError(
                "UCNS producer commit mismatch: expected "
                f"{PINNED_UCNS_COMMIT}, observed {producer_commit}"
            )
        if (
            str(module.EDCM_PROFILE_ID),
            str(module.EDCM_PROFILE_VERSION),
        ) != SUPPORTED_PROFILE:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile identity mismatch")
        if str(module.EDCM_PROFILE_SCOPE) != SUPPORTED_PROFILE_SCOPE:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile scope mismatch")
        if tuple(module.EDCM_PROFILE_OPTIONS) != EXPECTED_PROFILE_OPTIONS:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile options mismatch")
        if (
            str(module.EDCM_SPACE_ASSIGNMENT_POLICY)
            != EXPECTED_SPACE_ASSIGNMENT_POLICY
        ):
            raise UnsupportedUCNSSchemaError(
                "UCNS EDCM SPACE-assignment policy mismatch"
            )
        if str(module.EDCM_SOURCE_DOMAIN) != EXPECTED_SOURCE_DOMAIN:
            raise UnsupportedUCNSSchemaError(
                "UCNS EDCM source domain mismatch"
            )
        space_code_points = tuple(module.EDCM_SPACE_CODE_POINTS)
        if (
            len(space_code_points) != len(EXPECTED_SPACE_CODE_POINT_LABELS)
            or not all(
                isinstance(value, str)
                and len(value) == 1
                and not 0xD800 <= ord(value) <= 0xDFFF
                for value in space_code_points
            )
        ):
            raise UnsupportedUCNSSchemaError(
                "UCNS EDCM SPACE code-point pin shape mismatch"
            )
        space_code_point_labels = tuple(
            f"U+{ord(value):04X}" for value in space_code_points
        )
        if space_code_point_labels != EXPECTED_SPACE_CODE_POINT_LABELS:
            raise UnsupportedUCNSSchemaError(
                "UCNS EDCM SPACE code-point pin mismatch"
            )
        if _digest(space_code_point_labels) != EXPECTED_SPACE_CODE_POINTS_SHA256:
            raise UnsupportedUCNSSchemaError(
                "EDCM-owned SPACE code-point identity mismatch"
            )
        alphabet = tuple(module.PUBLIC_GONOL_157)
        if (
            len(alphabet) != 157
            or not all(isinstance(token, str) and len(token) == 1 for token in alphabet)
            or len(set(alphabet)) != 157
            or alphabet[0] != " "
            or "0" not in alphabet
        ):
            raise UnsupportedUCNSSchemaError("UCNS public gonol invariant mismatch")
        behavior = {
            "normalization": str(module.EDCM_NORMALIZATION_POLICY),
            "support": str(module.EDCM_SUPPORT_POLICY),
            "corpus_execution": str(module.EDCM_CORPUS_EXECUTION),
            "smallest_gonol": str(module.EDCM_SMALLEST_GONOL),
            "gonol_initiation": str(module.EDCM_GONOL_INITIATION),
            "space_assignment": str(module.EDCM_SPACE_ASSIGNMENT_POLICY),
            "source_domain": str(module.EDCM_SOURCE_DOMAIN),
        }
        expected_behavior = {
            "normalization": "none-preserve-source",
            "support": "one-unit-per-speaker-turn",
            "corpus_execution": "full-corpus",
            "smallest_gonol": "word",
            "gonol_initiation": "mobius-twist",
            "space_assignment": EXPECTED_SPACE_ASSIGNMENT_POLICY,
            "source_domain": EXPECTED_SOURCE_DOMAIN,
        }
        if behavior != expected_behavior:
            raise UnsupportedUCNSSchemaError("UCNS EDCM profile behavior mismatch")
        if (
            str(module.PUBLIC_GONOL_SHA256) != EXPECTED_PUBLIC_GONOL_SHA256
            or str(module.public_gonol_sha256()) != EXPECTED_PUBLIC_GONOL_SHA256
        ):
            raise UnsupportedUCNSSchemaError("UCNS public gonol digest mismatch")
        self._module = module
        self._producer_commit = producer_commit
        self._space_code_point_labels = space_code_point_labels
        try:
            self._profile = module.EdcmWordGonolProfile()
        except (TypeError, ValueError) as exc:
            raise UCNSAdapterConstructionError(
                "UCNS EDCM profile construction failed"
            ) from exc

    @property
    def status(self) -> UCNSIntegrationStatus:
        return UCNSIntegrationStatus(
            package_present=True,
            producer_recognized=True,
            profile_supported=True,
            adapter_active=True,
            selection="exact_edcm_word_gonol_profile",
        )

    def normalize(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        state = dict(payload)
        legacy = sorted(REJECTED_LEGACY_INPUTS.intersection(state))
        if legacy:
            raise UnsupportedUCNSSchemaError(
                "retired UCNS bridge/object/factorization inputs are rejected: "
                + ", ".join(legacy)
            )

        raw_turns = state.get("ucns_turns")
        if raw_turns is None:
            state["ucns_integration"] = self.status.as_dict()
            state.pop("ucns_profile_observation", None)
            return state
        if isinstance(raw_turns, (str, bytes)) or not isinstance(
            raw_turns, Sequence
        ):
            raise TypeError("ucns_turns must be an ordered sequence of tuples")

        turns: list[tuple[str, str]] = []
        for turn in raw_turns:
            if not isinstance(turn, tuple) or len(turn) != 2:
                raise TypeError("each ucns_turns item must be (speaker_id, text)")
            speaker_id, text = turn
            if not isinstance(speaker_id, str) or not speaker_id:
                raise TypeError("speaker_id must be a non-empty string")
            if not isinstance(text, str):
                raise TypeError("turn text must be a string")
            turns.append((speaker_id, text))

        source_ref = state.get("source_ref")
        source_id = str(source_ref) if source_ref is not None else None
        observed = tuple(
            self._profile.observe_corpus(tuple(turns), source_id=source_id)
        )
        turn_records = tuple(
            _turn_record(self._module, observation) for observation in observed
        )
        evidence_fields = {
            "profile_id": self._module.EDCM_PROFILE_ID,
            "profile_version": self._module.EDCM_PROFILE_VERSION,
            "profile_scope": self._module.EDCM_PROFILE_SCOPE,
            "source_repository": UCNS_SOURCE_REPOSITORY,
            "source_commit": self._producer_commit,
            "options": EXPECTED_PROFILE_OPTIONS,
            "normalization_policy": self._module.EDCM_NORMALIZATION_POLICY,
            "support_policy": self._module.EDCM_SUPPORT_POLICY,
            "corpus_execution": self._module.EDCM_CORPUS_EXECUTION,
            "smallest_gonol": self._module.EDCM_SMALLEST_GONOL,
            "gonol_initiation": self._module.EDCM_GONOL_INITIATION,
            "source_domain": self._module.EDCM_SOURCE_DOMAIN,
            "space_assignment_policy": (
                self._module.EDCM_SPACE_ASSIGNMENT_POLICY
            ),
            "space_code_point_labels": self._space_code_point_labels,
            "space_code_points_sha256": EXPECTED_SPACE_CODE_POINTS_SHA256,
            "token_alphabet_size": len(self._module.PUBLIC_GONOL_157),
            "token_alphabet_sha256": self._module.PUBLIC_GONOL_SHA256,
            "turns": turn_records,
        }
        evidence = UCNSProfileObservationEvidence(
            **evidence_fields,
            observation_digest=_digest(evidence_fields),
        )
        status = replace(
            self.status,
            ucns_profile_observation_attached=True,
            ucns_scope_metadata_attached=True,
        )
        state["ucns_profile_observation"] = evidence.as_dict()
        state["ucns_integration"] = status.as_dict()
        state.pop("ucns_geometry", None)
        state.pop("ucns_factorization_evidence", None)
        return state


@dataclass(frozen=True)
class UCNSAdapterSelection:
    adapter: UCNSAdapter | None
    status: UCNSIntegrationStatus


def _package_present() -> bool:
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return "ucns" in __import__("sys").modules


def suspended_ucns_status(
    *,
    package_present: bool | None = None,
    error: str | None = None,
) -> UCNSIntegrationStatus:
    present = _package_present() if package_present is None else package_present
    return UCNSIntegrationStatus(
        package_present=present,
        producer_recognized=False,
        profile_supported=False,
        adapter_active=False,
        selection="suspended",
        unresolved_constraints=(RESET_BOUNDARY_REASON,),
        errors=((error or RESET_BOUNDARY_REASON),),
    )


def missing_ucns_status() -> UCNSIntegrationStatus:
    return suspended_ucns_status(package_present=False)


def select_ucns_adapter() -> UCNSAdapterSelection:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        status = suspended_ucns_status(package_present=False)
        return UCNSAdapterSelection(adapter=None, status=status)
    try:
        adapter = ActualUCNSAdapter(module)
    except UCNSAdapterConstructionError as exc:
        status = suspended_ucns_status(package_present=True, error=str(exc))
        return UCNSAdapterSelection(adapter=None, status=status)
    return UCNSAdapterSelection(adapter=adapter, status=adapter.status)


def inspect_ucns_adapter() -> UCNSIntegrationStatus:
    return select_ucns_adapter().status


__all__ = [
    "ActualUCNSAdapter",
    "EXPECTED_PROFILE_OPTIONS",
    "EXPECTED_PUBLIC_GONOL_SHA256",
    "EXPECTED_SOURCE_DOMAIN",
    "EXPECTED_SPACE_ASSIGNMENT_POLICY",
    "EXPECTED_SPACE_CODE_POINT_LABELS",
    "EXPECTED_SPACE_CODE_POINTS_SHA256",
    "INSTALL_HINT",
    "PINNED_UCNS_COMMIT",
    "REJECTED_LEGACY_INPUTS",
    "REJECTED_LEGACY_SCHEMAS",
    "RESET_BOUNDARY_REASON",
    "SUPPORTED_PROFILE",
    "SUPPORTED_PROFILE_SCOPE",
    "SuspendedUCNSAdapter",
    "UCNSAdapter",
    "UCNSAdapterConstructionError",
    "UCNSAdapterSelection",
    "UCNSIntegrationStatus",
    "UCNSProfileObservationEvidence",
    "UnsupportedUCNSSchemaError",
    "inspect_ucns_adapter",
    "missing_ucns_status",
    "select_ucns_adapter",
    "suspended_ucns_status",
]
