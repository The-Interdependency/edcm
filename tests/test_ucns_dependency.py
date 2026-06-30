import shutil

from edcm.energy_claims import audit_energy_text


def test_ucns_dependency_available_when_installed():
    import edcm.ucns_dependency as dep

    report = dep.ucns_dependency_report()
    if report["available"]:
        assert report["available"] is True
    else:
        assert "python -m pip install -e ../ucns" in report["install_hint"]


def test_energy_report_contains_ucns_scope_note():
    report = audit_energy_text("D_f has a hard ceiling at 2.4999.")
    assert hasattr(report, "ucns_dependency")
    assert hasattr(report, "ucns_scope_note")
    assert report.ucns_scope_note


def test_no_ucns_proof_transfer_language():
    report = audit_energy_text("D_f has a hard ceiling at 2.4999.")
    assert "does not validate external physics" in report.capability_statement
    assert "UCNS-A proof status" in report.capability_statement
    assert "empirical truth" in report.capability_statement


def test_no_lean_runtime_dependency_for_python_audit():
    import edcm.energy_claims

    report = edcm.energy_claims.audit_energy_text("The theory predicts a CMB excess.")
    assert report.claims
    assert shutil.which("lake") is None or report.capability_statement
