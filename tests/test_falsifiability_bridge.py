from edcm.falsifiability_bridge import (
    EDCMBONE_FAILURE_TAXONOMY,
    audit_falsifiability_preservation,
)


def test_bridge_counts_falsifiability_preservation_loss():
    result = audit_falsifiability_preservation(
        "The theory predicts a CMB power-spectrum excess at multipole l ≈ 10^4.",
        "The theory is elegant and coherent.",
    )

    assert result["input_falsifiable_count"] == 1
    assert result["output_falsifiable_count"] == 0
    assert result["possible_falsifiability_loss"] is True
    assert "F1" in result["edcmbone_failure_codes"]


def test_bridge_preserves_boundary_language():
    result = audit_falsifiability_preservation(
        "The theory predicts a CMB power-spectrum excess at multipole l ≈ 10^4.",
        "It predicts a CMB excess at multipole l ≈ 10^4.",
    )

    assert result["possible_falsifiability_loss"] is False
    assert "does not validate external physics" in result["boundary_note"]
    assert "UCNS-A proof status" in result["boundary_note"]
    assert "empirical truth" in result["boundary_note"]


def test_bridge_exposes_edcmbone_failure_taxonomy():
    result = audit_falsifiability_preservation("CMB prediction is testable.", "CMB prediction is testable.")

    assert result["edcmbone_failure_taxonomy"] == EDCMBONE_FAILURE_TAXONOMY
    assert "Deletion" in result["edcmbone_failure_taxonomy"]["F1"]
    assert "Decorative preservation" in result["edcmbone_failure_taxonomy"]["F6"]
