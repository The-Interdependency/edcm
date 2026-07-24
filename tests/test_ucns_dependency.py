import shutil

from edcm.energy_claims import audit_energy_text


EXPLICIT_UCNS_FIELDS = {
    "ucns_package_available",
    "ucns_adapter_active",
    "ucns_object_attached",
    "ucns_bridge_record_attached",
    "ucns_scope_metadata_attached",
    "ucns_factorization_evidence_attached",
    "ucns_negative_certification_attached",
    "ucns_theorem_status_attached",
}


def test_ucns_dependency_report_separates_package_from_evidence():
    import edcm.ucns_dependency as dep

    report = dep.ucns_dependency_report()
    assert EXPLICIT_UCNS_FIELDS.issubset(report)
    assert report["ucns_object_attached"] is False
    assert report["ucns_bridge_record_attached"] is False
    assert report["ucns_scope_metadata_attached"] is False
    assert report["ucns_factorization_evidence_attached"] is False
    assert report["ucns_negative_certification_attached"] is False
    assert report["ucns_theorem_status_attached"] is False
    assert report["install_hint"] is None

    if report["ucns_package_available"]:
        assert report["available"] is True
        assert report["dependency"] in {"available", "failed"}
        if report["dependency"] == "available":
            assert report["ucns_adapter_active"] is True
    else:
        assert report["dependency"] == "missing"
        assert report["ucns_adapter_active"] is False


def test_energy_report_does_not_convert_import_into_scope_attachment():
    report = audit_energy_text("D_f has a hard ceiling at 2.4999.")
    assert EXPLICIT_UCNS_FIELDS.issubset(report.ucns_dependency)
    assert report.ucns_dependency["ucns_object_attached"] is False
    assert report.ucns_dependency["ucns_bridge_record_attached"] is False
    assert report.ucns_dependency["ucns_scope_metadata_attached"] is False
    assert report.ucns_dependency["ucns_factorization_evidence_attached"] is False
    assert "attached no UCNS" in report.ucns_scope_note or "no UCNS object" in report.ucns_scope_note


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
