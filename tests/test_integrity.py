from __future__ import annotations

from importlib.resources import files

from edcm.integrity import (
    EXPECTED_MEASUREMENT_AUTHORITY,
    FROZEN_CANON_GIT_BLOBS,
    git_blob_sha1,
    run_integrity_gate,
    verify_frozen_canon,
    verify_measurement_authority,
    verify_orthogonality_alias,
)


def _copy_frozen_canon(destination) -> None:
    source = files("edcm.measurement.canon").joinpath("data")
    for name in FROZEN_CANON_GIT_BLOBS:
        destination.joinpath(name).write_bytes(source.joinpath(name).read_bytes())


def test_git_blob_sha1_matches_known_empty_blob_identity() -> None:
    assert git_blob_sha1(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def test_current_installed_integrity_gate_passes() -> None:
    report = run_integrity_gate()
    assert report.passed is True
    assert report.findings
    assert all(finding.passed for finding in report.findings)


def test_frozen_canon_exact_file_set_and_bytes_pass(tmp_path) -> None:
    _copy_frozen_canon(tmp_path)
    findings = verify_frozen_canon(tmp_path)
    assert findings[0].check == "frozen_canon_file_set"
    assert all(finding.passed for finding in findings)


def test_frozen_canon_byte_change_fails_closed(tmp_path) -> None:
    _copy_frozen_canon(tmp_path)
    target = tmp_path / "markers_v1.json"
    target.write_bytes(target.read_bytes() + b"\n")

    findings = verify_frozen_canon(tmp_path)
    changed = next(
        finding
        for finding in findings
        if finding.check == "frozen_canon_blob:markers_v1.json"
    )
    assert changed.passed is False
    assert changed.expected != changed.observed


def test_frozen_canon_added_or_missing_file_fails_set_gate(tmp_path) -> None:
    _copy_frozen_canon(tmp_path)
    (tmp_path / "invented_v1.json").write_text("{}", encoding="utf-8")
    with_extra = verify_frozen_canon(tmp_path)[0]
    assert with_extra.passed is False
    assert "invented_v1.json" in with_extra.observed

    (tmp_path / "invented_v1.json").unlink()
    (tmp_path / "bones_words_v1.json").unlink()
    with_missing = verify_frozen_canon(tmp_path)[0]
    assert with_missing.passed is False
    assert "bones_words_v1.json" not in with_missing.observed


def test_measurement_authority_exact_policy_passes() -> None:
    finding = verify_measurement_authority(EXPECTED_MEASUREMENT_AUTHORITY)
    assert finding.passed is True


def test_measurement_authority_runtime_override_or_source_change_fails() -> None:
    changed = dict(EXPECTED_MEASUREMENT_AUTHORITY)
    changed["runtime_override_by_edcmbone"] = True
    finding = verify_measurement_authority(changed)
    assert finding.passed is False

    changed = dict(EXPECTED_MEASUREMENT_AUTHORITY)
    changed["source_of_truth"] = "The-Interdependency/edcmbone"
    finding = verify_measurement_authority(changed)
    assert finding.passed is False


def test_orthogonality_surface_is_one_canonical_alias() -> None:
    finding = verify_orthogonality_alias()
    assert finding.passed is True
    assert all(finding.observed.values())
