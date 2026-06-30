from edcm.energy_claims import audit_energy_text, extract_energy_claim_candidates


def codes(report):
    return {flag.code for flag in report.flags}


def test_detects_pressure_claim():
    claims = extract_energy_claim_candidates("Local pressure P = 1.00×10^25 × N_n² × (10^-15 / L_eff)^3.")
    assert claims
    assert claims[0].claimed_quantity
    assert "pressure" in claims[0].claimed_quantity or "P" in claims[0].claimed_quantity


def test_flags_coupling_without_exchange_rule():
    report = audit_energy_text("The intent phase φ_I = +1 modulates coherence and locks stable branches.")
    assert {"E004_COUPLING_WITHOUT_EXCHANGE_RULE", "E003_NO_SOURCE_OR_SINK"} & codes(report)


def test_flags_hard_ceiling_as_boundary():
    report = audit_energy_text("D_f has a hard ceiling at 2.4999 to enforce integer winding.")
    assert "E006_BOUNDARY_WITHOUT_DERIVATION" in codes(report)
    exact_report = audit_energy_text("D_f has a derived exact hard ceiling clamp at 2.4999.")
    assert "E007_CLAMP_PRESENTED_AS_DERIVED" in codes(exact_report)


def test_detects_empirical_target():
    report = audit_energy_text("The theory predicts a CMB power-spectrum excess at multipole l ≈ 10^4.")
    assert "E011_EMPIRICAL_TARGET_PRESENT" in codes(report)
    assert report.claims[0].empirical_target in {"CMB", "multipole"}


def test_exactness_overclaim():
    report = audit_energy_text("The theory exactly reproduces every confirmed gravitational-wave strain with zero free parameters.")
    assert "E009_EXACTNESS_OVERCLAIM" in codes(report)


def test_report_summary_counts():
    report = audit_energy_text(
        "Local pressure P = 1.00×10^25 × N_n² × (10^-15 / L_eff)^3. "
        "D_f has a hard ceiling at 2.4999 to enforce integer winding. "
        "The theory predicts a CMB power-spectrum excess at multipole l ≈ 10^4."
    )
    assert report.summary["claims"] >= 3
    assert report.summary["warning"] >= 1
    assert report.summary["E006_BOUNDARY_WITHOUT_DERIVATION"] >= 1
