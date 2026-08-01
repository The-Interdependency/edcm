"""Contracts for the exact EDCM UCNS word-gonol profile consumer."""

from __future__ import annotations

# === CHECKS ===
# id: check_edcm_ucns_exact_profile_only
#   proves: edcm_ucns_exact_profile_only
#   call: self::test_exact_profile_activates_and_option_drift_suspends
#   mutates: none
#   cleanup: none
#
# id: check_edcm_ucns_full_turn_observation
#   proves: edcm_ucns_full_turn_observation
#   call: self::test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures
#   mutates: none
#   cleanup: none
#
# id: check_edcm_ucns_no_geometry_or_proof_transfer
#   proves: edcm_ucns_no_geometry_or_proof_transfer
#   call: self::test_live_profile_attaches_observation_without_geometry_or_proof_transfer
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import base64
from hashlib import sha256
import importlib
import importlib.util
import os
from pathlib import Path
import py_compile
import subprocess
import sys
from types import ModuleType

import pytest

import edcm
import edcm.ucns_adapter as adapter_module
from edcm.ucns_adapter import (
    ActualUCNSAdapter,
    EXPECTED_PROFILE_OPTIONS,
    EXPECTED_PUBLIC_GONOL_SHA256,
    EXPECTED_SOURCE_DOMAIN,
    EXPECTED_SPACE_ASSIGNMENT_POLICY,
    EXPECTED_SPACE_CODE_POINT_LABELS,
    EXPECTED_SPACE_CODE_POINTS_SHA256,
    PINNED_UCNS_COMMIT,
    REJECTED_LEGACY_SCHEMAS,
    UCNSAdapterConstructionError,
    UnsupportedUCNSSchemaError,
    select_ucns_adapter,
)


@pytest.fixture(autouse=True)
def _identify_identity_only_fake_modules(monkeypatch):
    real_distribution_commit = adapter_module._distribution_commit

    def identify(module):
        if module.__name__ == "ucns" and getattr(module, "__file__", None) is None:
            return PINNED_UCNS_COMMIT
        return real_distribution_commit(module)

    monkeypatch.setattr(adapter_module, "_distribution_commit", identify)


def _exact_identity_module() -> ModuleType:
    module = ModuleType("ucns")
    module.UCNS_PRODUCER_COMMIT = PINNED_UCNS_COMMIT
    module.EDCM_PROFILE_ID, module.EDCM_PROFILE_VERSION = (
        adapter_module.SUPPORTED_PROFILE
    )
    module.EDCM_PROFILE_SCOPE = adapter_module.SUPPORTED_PROFILE_SCOPE
    module.EDCM_PROFILE_OPTIONS = EXPECTED_PROFILE_OPTIONS
    module.EDCM_NORMALIZATION_POLICY = "none-preserve-source"
    module.EDCM_SUPPORT_POLICY = "one-unit-per-speaker-turn"
    module.EDCM_CORPUS_EXECUTION = "full-corpus"
    module.EDCM_SMALLEST_GONOL = "word"
    module.EDCM_GONOL_INITIATION = "mobius-twist"
    module.EDCM_SOURCE_DOMAIN = EXPECTED_SOURCE_DOMAIN
    module.EDCM_SPACE_ASSIGNMENT_POLICY = EXPECTED_SPACE_ASSIGNMENT_POLICY
    module.EDCM_SPACE_CODE_POINTS = tuple(
        chr(int(label[2:], 16)) for label in EXPECTED_SPACE_CODE_POINT_LABELS
    )
    module.PUBLIC_GONOL_157 = (" ", "0", *(chr(0x1000 + i) for i in range(155)))
    module.PUBLIC_GONOL_SHA256 = EXPECTED_PUBLIC_GONOL_SHA256
    module.public_gonol_sha256 = lambda: EXPECTED_PUBLIC_GONOL_SHA256

    class Profile:
        def observe_corpus(self, turns, *, source_id=None):
            raise AssertionError("identity-only fake must not observe a corpus")

    module.EdcmWordGonolProfile = Profile
    module.EdcmWordGonol = type("EdcmWordGonol", (), {})
    module.SuperpositionedSpaceBoundary = type(
        "SuperpositionedSpaceBoundary", (), {}
    )
    return module


class _RecordedPath(str):
    def __new__(cls, value: str, payload: bytes):
        instance = super().__new__(cls, value)
        digest = base64.urlsafe_b64encode(sha256(payload).digest()).rstrip(b"=")
        instance.hash = type(
            "RecordedHash",
            (),
            {"mode": "sha256", "value": digest.decode("ascii")},
        )()
        instance.size = len(payload)
        return instance


def _vcs_distribution(monkeypatch, root, commit):
    module_payload = b"VALUE = 'trusted'\n"
    profile_payload = b"PROFILE = 'trusted'\n"
    direct_url_payload = adapter_module.json.dumps(
        {
            "url": "https://github.com/The-Interdependency/ucns.git",
            "vcs_info": {"vcs": "git", "commit_id": commit},
        }
    ).encode("utf-8")
    module_relative = "ucns/__init__.py"
    profile_relative = "ucns/profile.py"
    direct_url_relative = "ucns-0.0.0.dist-info/direct_url.json"
    module_path = root / module_relative
    profile_path = root / profile_relative
    direct_url_path = root / direct_url_relative
    module_path.parent.mkdir(parents=True)
    direct_url_path.parent.mkdir(parents=True)
    module_path.write_bytes(module_payload)
    profile_path.write_bytes(profile_payload)
    direct_url_path.write_bytes(direct_url_payload)
    bytecode_path = Path(importlib.util.cache_from_source(str(module_path)))
    py_compile.compile(str(module_path), cfile=str(bytecode_path), doraise=True)
    bytecode_relative = bytecode_path.relative_to(root).as_posix()
    monkeypatch.setattr(
        adapter_module,
        "PINNED_UCNS_PACKAGE_SHA256",
        {
            "__init__.py": sha256(module_payload).hexdigest(),
            "profile.py": sha256(profile_payload).hexdigest(),
        },
    )

    class Distribution:
        files = (
            _RecordedPath(module_relative, module_payload),
            _RecordedPath(profile_relative, profile_payload),
            _RecordedPath(direct_url_relative, direct_url_payload),
            type(
                "BytecodePath",
                (str,),
                {"hash": None, "size": None},
            )(bytecode_relative),
            type(
                "RecordPath",
                (str,),
                {"hash": None, "size": None},
            )("ucns-0.0.0.dist-info/RECORD"),
        )

        def read_text(self, name):
            if name == "direct_url.json":
                return direct_url_path.read_text(encoding="utf-8")
            if name == "RECORD":
                return "\n".join(
                    ",".join(
                        (
                            str(entry),
                            (
                                ""
                                if entry.hash is None
                                else f"{entry.hash.mode}={entry.hash.value}"
                            ),
                            "" if entry.size is None else str(entry.size),
                        )
                    )
                    for entry in self.files
                )
            raise AssertionError(name)

        def locate_file(self, path):
            return root / str(path)

    return Distribution(), module_path, bytecode_path


def test_absent_package_is_typed_suspension(monkeypatch):
    real_import = adapter_module.importlib.import_module

    def missing(name):
        if name == "ucns":
            raise ModuleNotFoundError("No module named ucns", name="ucns")
        return real_import(name)

    monkeypatch.setattr(adapter_module.importlib, "import_module", missing)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert selection.status.selection == "suspended"
    assert selection.status.ucns_profile_observation_attached is False


def test_pre_reset_metric_resolver_is_removed_from_public_surface():
    assert importlib.util.find_spec("edcm.ucns_metrics") is None
    for name in (
        "MetricDefinition",
        "ResolvedMetricUCNS",
        "UCNSMetricDependencyError",
        "UCNSMetricResolutionError",
        "METRIC_DEFINITIONS",
        "SYMBOL_TO_METRIC_ID",
        "resolve_metric_axis",
        "resolve_metric_value",
        "resolve_metric_vector",
        "resolve_round_metrics",
        "resolved_metric_objects_payload",
    ):
        assert not hasattr(edcm, name)


def test_archived_lookalike_cannot_activate(monkeypatch):
    fake = ModuleType("ucns")
    fake.UCNSObject = object
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: fake)
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.package_present is True
    assert selection.status.producer_recognized is False
    with pytest.raises(UCNSAdapterConstructionError, match="surface missing"):
        ActualUCNSAdapter(fake)


def test_exact_profile_activates_and_option_drift_suspends(monkeypatch):
    module = _exact_identity_module()
    assert len(EXPECTED_PROFILE_OPTIONS) == 14
    assert ("source_domain", EXPECTED_SOURCE_DOMAIN) in EXPECTED_PROFILE_OPTIONS
    assert (
        "space_assignment",
        EXPECTED_SPACE_ASSIGNMENT_POLICY,
    ) in EXPECTED_PROFILE_OPTIONS
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: module)
    selection = select_ucns_adapter()
    assert selection.adapter is not None
    assert selection.status.producer_recognized is True
    assert selection.status.profile_supported is True
    assert selection.status.adapter_active is True

    module.UCNS_PRODUCER_COMMIT = "868d80878c9ecd93ff30e91ca289122ded805a49"
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert (
        "producer-owned and installed commit identities disagree"
        in selection.status.errors[0]
    )

    module.UCNS_PRODUCER_COMMIT = PINNED_UCNS_COMMIT

    module.EDCM_PROFILE_OPTIONS = (*EXPECTED_PROFILE_OPTIONS[:-1], ("z", "drift"))
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "options mismatch" in selection.status.errors[0]

    module.EDCM_PROFILE_OPTIONS = EXPECTED_PROFILE_OPTIONS
    module.EDCM_SPACE_CODE_POINTS = (
        *module.EDCM_SPACE_CODE_POINTS[:-1],
        "\u3001",
    )
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "code-point pin mismatch" in selection.status.errors[0]

    module.EDCM_SPACE_CODE_POINTS = tuple(
        chr(int(label[2:], 16)) for label in EXPECTED_SPACE_CODE_POINT_LABELS
    )
    module.EDCM_SOURCE_DOMAIN = "all-unicode-code-points"
    selection = select_ucns_adapter()
    assert selection.adapter is None
    assert selection.status.adapter_active is False
    assert "source domain mismatch" in selection.status.errors[0]


def test_exact_surface_rejects_stale_or_missing_producer_identity(monkeypatch):
    module = _exact_identity_module()
    module.UCNS_PRODUCER_COMMIT = "868d80878c9ecd93ff30e91ca289122ded805a49"
    with pytest.raises(
        UnsupportedUCNSSchemaError,
        match="producer-owned and installed commit identities disagree",
    ):
        ActualUCNSAdapter(module)

    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = __file__

    def missing_distribution(name):
        raise adapter_module.importlib_metadata.PackageNotFoundError(name)

    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        missing_distribution,
    )
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="identity unavailable from distribution metadata",
    ):
        ActualUCNSAdapter(module)


def test_distribution_commit_identity_rejects_stale_lookalike(
    monkeypatch,
    tmp_path,
):
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    stale_distribution, module_path, _ = _vcs_distribution(
        monkeypatch,
        tmp_path / "stale",
        "868d80878c9ecd93ff30e91ca289122ded805a49",
    )
    module.__file__ = str(module_path)

    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: stale_distribution,
    )
    with pytest.raises(UnsupportedUCNSSchemaError, match="producer commit mismatch"):
        ActualUCNSAdapter(module)

    pinned_distribution, module_path, _ = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    module.__file__ = str(module_path)
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: pinned_distribution,
    )
    assert ActualUCNSAdapter(module).status.adapter_active is True

    module.UCNS_PRODUCER_COMMIT = (
        "868d80878c9ecd93ff30e91ca289122ded805a49"
    )
    with pytest.raises(
        UnsupportedUCNSSchemaError,
        match="producer-owned and installed commit identities disagree",
    ):
        ActualUCNSAdapter(module)

    del module.UCNS_PRODUCER_COMMIT
    module_path.write_text("# locally modified UCNS fixture\n", encoding="utf-8")
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="installed file (size|hash) mismatch",
    ):
        ActualUCNSAdapter(module)


def test_distribution_identity_rejects_timestamp_valid_altered_bytecode(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, bytecode_path = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    distribution.files = tuple(
        entry
        for entry in distribution.files
        if not str(entry).endswith(".pyc")
    )
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )
    assert ActualUCNSAdapter(module).status.adapter_active is True

    original_source = module_path.read_bytes()
    malicious_source = original_source.replace(b"trusted", b"altered")
    assert len(malicious_source) == len(original_source)
    module_path.write_bytes(malicious_source)
    py_compile.compile(str(module_path), cfile=str(bytecode_path), doraise=True)
    compiled_stat = module_path.stat()
    module_path.write_bytes(original_source)
    os.utime(
        module_path,
        ns=(compiled_stat.st_atime_ns, compiled_stat.st_mtime_ns),
    )
    bytecode = bytecode_path.read_bytes()
    assert int.from_bytes(bytecode[8:12], "little") == int(
        module_path.stat().st_mtime
    )
    assert int.from_bytes(bytecode[12:16], "little") == len(original_source)
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="cached bytecode does not match",
    ):
        ActualUCNSAdapter(module)


def test_distribution_identity_accepts_bytecode_without_debug_ranges(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, bytecode_path = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    subprocess.run(
        [
            sys.executable,
            "-X",
            "no_debug_ranges",
            "-c",
            (
                "import py_compile, sys; "
                "py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)"
            ),
            str(module_path),
            str(bytecode_path),
        ],
        check=True,
        capture_output=True,
    )
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )

    assert ActualUCNSAdapter(module).status.adapter_active is True


def test_cached_bytecode_identity_is_relocatable(tmp_path):
    original_root = tmp_path / "original"
    original_root.mkdir()
    original_source = original_root / "profile.py"
    original_source.write_text("VALUE = 'trusted'\n", encoding="utf-8")
    original_cache = Path(
        importlib.util.cache_from_source(str(original_source))
    )
    py_compile.compile(
        str(original_source),
        cfile=str(original_cache),
        doraise=True,
    )

    relocated_root = tmp_path / "relocated"
    original_root.rename(relocated_root)
    relocated_source = relocated_root / "profile.py"
    relocated_cache = Path(
        importlib.util.cache_from_source(str(relocated_source))
    )

    adapter_module._verify_cached_bytecode(
        relocated_cache,
        verified_paths={relocated_source.resolve()},
    )


def test_active_optimization_above_two_is_verified(tmp_path):
    script = """
import importlib.util
import os
from pathlib import Path
import py_compile
import sys
from edcm.ucns_adapter import (
    UCNSAdapterConstructionError,
    _is_runtime_cache,
    _verify_cached_bytecode,
)

root = Path(sys.argv[1])
source = root / "profile.py"
trusted = b"VALUE = 'trusted'\\n"
altered = b"VALUE = 'altered'\\n"
source.write_bytes(trusted)
cache = Path(importlib.util.cache_from_source(str(source)))
py_compile.compile(str(source), cfile=str(cache), doraise=True)
assert sys.flags.optimize == 3
assert ".opt-3.pyc" in cache.name
assert _is_runtime_cache(cache)
_verify_cached_bytecode(cache, verified_paths={source.resolve()})
source.write_bytes(altered)
py_compile.compile(str(source), cfile=str(cache), doraise=True)
compiled_stat = source.stat()
source.write_bytes(trusted)
os.utime(source, ns=(compiled_stat.st_atime_ns, compiled_stat.st_mtime_ns))
try:
    _verify_cached_bytecode(cache, verified_paths={source.resolve()})
except UCNSAdapterConstructionError:
    pass
else:
    raise AssertionError("altered active opt-3 cache was accepted")
"""
    subprocess.run(
        [sys.executable, "-OOO", "-c", script, str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )


def test_distribution_identity_ignores_foreign_abi_cache(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, bytecode_path = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    cache_tag = sys.implementation.cache_tag
    assert cache_tag is not None
    foreign_cache = bytecode_path.with_name(
        bytecode_path.name.replace(cache_tag, "cpython-999")
    )
    foreign_cache.write_bytes(b"foreign ABI cache is not executable here")
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )

    assert ActualUCNSAdapter(module).status.adapter_active is True


def test_distribution_record_cannot_reanchor_altered_package(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, _ = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )
    assert ActualUCNSAdapter(module).status.adapter_active is True

    altered_payload = b"VALUE = 'altered and reanchored'\n"
    module_path.write_bytes(altered_payload)
    distribution.files = tuple(
        _RecordedPath(str(entry), altered_payload)
        if str(entry) == "ucns/__init__.py"
        else entry
        for entry in distribution.files
    )
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="differs from the pinned producer tree",
    ):
        ActualUCNSAdapter(module)


def test_verified_identity_reloads_stale_ucns_module(
    monkeypatch,
    tmp_path,
):
    package_root = tmp_path / "ucns"
    package_root.mkdir()
    module_path = package_root / "__init__.py"
    module_path.write_text(
        f"UCNS_PRODUCER_COMMIT = '{PINNED_UCNS_COMMIT}'\nVALUE = 'stale'\n",
        encoding="utf-8",
    )
    previous_modules = {
        name: loaded
        for name, loaded in sys.modules.items()
        if name == "ucns" or name.startswith("ucns.")
    }
    for name in previous_modules:
        sys.modules.pop(name, None)
    monkeypatch.syspath_prepend(str(tmp_path))
    importlib.invalidate_caches()
    try:
        stale_module = importlib.import_module("ucns")
        assert stale_module.VALUE == "stale"
        module_path.write_text(
            (
                f"UCNS_PRODUCER_COMMIT = '{PINNED_UCNS_COMMIT}'\n"
                "VALUE = 'verified'\n"
            ),
            encoding="utf-8",
        )
        Path(importlib.util.cache_from_source(str(module_path))).unlink(
            missing_ok=True
        )
        monkeypatch.setattr(
            adapter_module,
            "_distribution_commit",
            lambda module: PINNED_UCNS_COMMIT,
        )

        fresh_module, commit = adapter_module._resolve_ucns_producer(
            stale_module
        )
        assert commit == PINNED_UCNS_COMMIT
        assert fresh_module is not stale_module
        assert fresh_module.VALUE == "verified"
    finally:
        for name in tuple(sys.modules):
            if name == "ucns" or name.startswith("ucns."):
                sys.modules.pop(name, None)
        sys.modules.update(previous_modules)


def test_distribution_raw_record_detects_deleted_file(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, _ = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )
    assert ActualUCNSAdapter(module).status.adapter_active is True

    (module_path.parent / "profile.py").unlink()
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="installed file is missing: ucns/profile.py",
    ):
        ActualUCNSAdapter(module)


def test_distribution_identity_rejects_non_object_direct_url(
    monkeypatch,
    tmp_path,
):
    distribution, module_path, _ = _vcs_distribution(
        monkeypatch,
        tmp_path / "pinned",
        PINNED_UCNS_COMMIT,
    )
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = str(module_path)
    monkeypatch.setattr(distribution, "read_text", lambda name: "[]")
    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        lambda name: distribution,
    )
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="direct_url.json invalid",
    ):
        ActualUCNSAdapter(module)

    def unreadable_direct_url(name):
        raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")

    monkeypatch.setattr(distribution, "read_text", unreadable_direct_url)
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="direct_url.json unreadable",
    ):
        ActualUCNSAdapter(module)


def test_checkout_repository_identity_accepts_renamed_remote(tmp_path):
    checkout = tmp_path / "ucns"
    checkout.mkdir()
    subprocess.run(["git", "init", str(checkout)], check=True, capture_output=True)
    tracked_module = checkout / "src/ucns/__init__.py"
    tracked_module.parent.mkdir(parents=True)
    tracked_module.write_text("VALUE = 'trusted'\n", encoding="utf-8")
    (checkout / ".gitignore").write_text("/ucns/\n", encoding="utf-8")
    (checkout / "tracked.txt").write_text("fixture\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(checkout), "add", "."],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "remote",
            "add",
            "upstream",
            adapter_module.UCNS_SOURCE_REPOSITORY,
        ],
        check=True,
        capture_output=True,
    )
    commit = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert (
        adapter_module._git_checkout_commit(
            checkout,
            module_file=tracked_module,
        )
        == commit
    )

    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "remote",
            "set-url",
            "upstream",
            "ssh://git@github.com/The-Interdependency/ucns.git",
        ],
        check=True,
        capture_output=True,
    )
    assert (
        adapter_module._git_checkout_commit(
            checkout,
            module_file=tracked_module,
        )
        == commit
    )

    original_module = tracked_module.read_bytes()
    tracked_module.write_bytes(original_module.replace(b"trusted", b"altered"))
    subprocess.run(
        ["git", "-C", str(checkout), "add", "src/ucns/__init__.py"],
        check=True,
        capture_output=True,
    )
    replacement_tree = subprocess.run(
        ["git", "-C", str(checkout), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    replacement_commit = subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "-c",
            "user.name=EDCM Test",
            "-c",
            "user.email=edcm-test@example.invalid",
            "commit-tree",
            replacement_tree,
            "-p",
            commit,
            "-m",
            "replacement fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(checkout), "reset", "--hard", commit],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "replace", commit, replacement_commit],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "reset", "--hard", commit],
        check=True,
        capture_output=True,
    )
    assert b"altered" in tracked_module.read_bytes()
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="differs from the pinned tree",
    ):
        adapter_module._git_checkout_commit(
            checkout,
            module_file=tracked_module,
        )
    subprocess.run(
        ["git", "-C", str(checkout), "replace", "-d", commit],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "reset", "--hard", commit],
        check=True,
        capture_output=True,
    )

    malicious_module = original_module.replace(b"trusted", b"altered")
    tracked_module.write_bytes(malicious_module)
    cached_module = Path(importlib.util.cache_from_source(str(tracked_module)))
    py_compile.compile(
        str(tracked_module),
        cfile=str(cached_module),
        doraise=True,
    )
    compiled_stat = tracked_module.stat()
    tracked_module.write_bytes(original_module)
    os.utime(
        tracked_module,
        ns=(compiled_stat.st_atime_ns, compiled_stat.st_mtime_ns),
    )
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="cached bytecode does not match",
    ):
        adapter_module._git_checkout_commit(
            checkout,
            module_file=tracked_module,
        )
    py_compile.compile(
        str(tracked_module),
        cfile=str(cached_module),
        doraise=True,
    )

    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "update-index",
            "--assume-unchanged",
            "--",
            "src/ucns/__init__.py",
        ],
        check=True,
        capture_output=True,
    )
    tracked_module.write_text("# hidden modification\n", encoding="utf-8")
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="differs from the pinned tree",
    ):
        adapter_module._git_checkout_commit(
            checkout,
            module_file=tracked_module,
        )
    tracked_module.write_bytes(original_module)
    subprocess.run(
        [
            "git",
            "-C",
            str(checkout),
            "update-index",
            "--no-assume-unchanged",
            "--",
            "src/ucns/__init__.py",
        ],
        check=True,
        capture_output=True,
    )

    ignored_module = checkout / "ucns/__init__.py"
    ignored_module.parent.mkdir()
    ignored_module.write_text("# fabricated fixture\n", encoding="utf-8")
    with pytest.raises(
        UCNSAdapterConstructionError,
        match="identity unavailable from editable checkout",
    ):
        adapter_module._git_checkout_commit(
            checkout,
            module_file=ignored_module,
        )


def test_explicit_verified_source_checkout_does_not_require_distribution(
    monkeypatch,
):
    module = _exact_identity_module()
    del module.UCNS_PRODUCER_COMMIT
    module.__file__ = "/verified/ucns/src/ucns/__init__.py"
    monkeypatch.setattr(
        adapter_module,
        "_source_checkout_commit",
        lambda candidate: PINNED_UCNS_COMMIT,
    )

    def unrelated_distribution(name):
        raise AssertionError("explicit checkout must not use installed metadata")

    monkeypatch.setattr(
        adapter_module.importlib_metadata,
        "distribution",
        unrelated_distribution,
    )
    assert ActualUCNSAdapter(module).status.adapter_active is True


def test_retired_bridge_object_and_factorization_inputs_fail_closed():
    adapter = ActualUCNSAdapter(_exact_identity_module())
    for key in (
        "ucns_object",
        "ucns_bridge_record",
        "ucns_bridge_record_json",
        "ucns_bridge_record_dict",
        "ucns_factorization_evidence",
    ):
        with pytest.raises(UnsupportedUCNSSchemaError, match="retired"):
            adapter.normalize({key: object()})


def test_flat_transcript_does_not_invent_speaker_turn_boundaries():
    adapter = ActualUCNSAdapter(_exact_identity_module())
    result = adapter.normalize({"transcript": "A: hello\nB: there"})
    assert result["ucns_integration"]["adapter_active"] is True
    assert result["ucns_integration"]["ucns_profile_observation_attached"] is False
    assert "ucns_profile_observation" not in result


def test_live_profile_preserves_full_turn_order_spaces_and_alphabet_failures():
    ucns = pytest.importorskip("ucns")
    adapter = ActualUCNSAdapter(ucns)
    result = adapter.normalize(
        {
            "source_ref": "fixture://exact-turns",
            "ucns_turns": (
                ("A", "word\tgonol\n\u00a0"),
                ("B", "é"),
            ),
        }
    )
    evidence = result["ucns_profile_observation"]
    assert evidence["source_commit"] == PINNED_UCNS_COMMIT
    assert evidence["profile_id"] == "ucns.profile.edcm-word-gonol"
    assert evidence["token_alphabet_size"] == 157
    assert tuple(turn["speaker_id"] for turn in evidence["turns"]) == ("A", "B")
    first = evidence["turns"][0]
    assert first["raw_text"] == "word\tgonol\n\u00a0"
    assert first["unit_support"] == 1.0
    assert first["word_count"] == 2
    assert first["nesting_boundary_count"] == 3
    assert tuple(segment["kind"] for segment in first["segments"]) == (
        "word-gonol",
        "superpositioned-space-boundary",
        "word-gonol",
        "superpositioned-space-boundary",
        "superpositioned-space-boundary",
    )
    boundaries = tuple(
        segment["token"]
        for segment in first["segments"]
        if segment["kind"] == "superpositioned-space-boundary"
    )
    assert tuple(token["source_value"] for token in boundaries) == (
        "\t",
        "\n",
        "\u00a0",
    )
    assert all(token["carrier_token"] == " " for token in boundaries)
    assert all(token["carrier_position"] == 0 for token in boundaries)
    assert all(token["alphabet_position"] == 0 for token in boundaries)
    assert all(token["is_space_manifestation"] is True for token in boundaries)
    assert all(token["has_carrier_assignment"] is True for token in boundaries)
    assert all(token["in_alphabet"] is True for token in boundaries)
    assert all(
        token["is_public_gonol_token"] is False for token in boundaries
    )
    assert first["carrier_unassigned"] == ()
    assert first["out_of_alphabet"] == ()
    assert first["has_complete_carrier_assignment"] is True
    assert first["has_complete_alphabet_coverage"] is True
    assert evidence["source_domain"] == EXPECTED_SOURCE_DOMAIN
    assert evidence["space_assignment_policy"] == EXPECTED_SPACE_ASSIGNMENT_POLICY
    assert evidence["space_code_point_labels"] == EXPECTED_SPACE_CODE_POINT_LABELS
    assert (
        evidence["space_code_points_sha256"]
        == EXPECTED_SPACE_CODE_POINTS_SHA256
    )
    assert evidence["turns"][1]["carrier_unassigned"][0]["value"] == "é"
    assert evidence["turns"][1]["out_of_alphabet"][0]["value"] == "é"
    assert (
        evidence["turns"][1]["out_of_alphabet"][0]["source_value"]
        == "é"
    )
    assert (
        evidence["turns"][1]["out_of_alphabet"][0]["carrier_token"]
        is None
    )
    assert evidence["turns"][1]["has_complete_alphabet_coverage"] is False


def test_live_profile_attaches_observation_without_geometry_or_proof_transfer():
    ucns = pytest.importorskip("ucns")
    result = ActualUCNSAdapter(ucns).normalize(
        {"ucns_turns": (("A", "exact evidence"),)}
    )
    status = result["ucns_integration"]
    evidence = result["ucns_profile_observation"]
    assert status["ucns_profile_observation_attached"] is True
    assert status["ucns_bridge_record_attached"] is False
    assert status["ucns_factorization_evidence_attached"] is False
    assert status["ucns_theorem_status_attached"] is False
    assert evidence["evidence_mode"] == "exact-observation"
    assert evidence["projection_status"] == "not-projected"
    assert evidence["theorem_status_transfer"] is False
    assert evidence["measurement_validity_claim"] is False
    assert "ucns_geometry" not in result
    assert "ucns_factorization_evidence" not in result


def test_invalid_turn_container_fails_closed():
    ucns = pytest.importorskip("ucns")
    adapter = ActualUCNSAdapter(ucns)
    with pytest.raises(TypeError, match="ordered sequence"):
        adapter.normalize({"ucns_turns": iter((("A", "text"),))})
    with pytest.raises(TypeError, match="must be"):
        adapter.normalize({"ucns_turns": [["A", "text"]]})


def test_legacy_schema_identities_and_na_boundary():
    assert "ucns-canonical-json-v1" in REJECTED_LEGACY_SCHEMAS
    assert "ucns.bridge.edcm-metapat-ordered-occurrence" in REJECTED_LEGACY_SCHEMAS
    assert "NA" != 0
    assert "NA" != "0"
