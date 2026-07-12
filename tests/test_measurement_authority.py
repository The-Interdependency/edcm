from __future__ import annotations

from types import ModuleType

import edcm.layers as layers_module
from edcm.layers import ConsolidatedMeasurementLayer
from edcm.measurement import (
    CONSOLIDATION_SOURCE_COMMIT,
    MEASUREMENT_AUTHORITY,
    MEASUREMENT_COMPATIBILITY_POLICY,
    MEASUREMENT_SOURCE_OF_TRUTH,
)
from edcm.ucns_adapter import UCNSAdapterSelection, missing_ucns_status


def test_measurement_authority_is_machine_readable():
    assert MEASUREMENT_AUTHORITY["canonical"] is True
    assert MEASUREMENT_AUTHORITY["source_of_truth"] == MEASUREMENT_SOURCE_OF_TRUTH
    assert MEASUREMENT_AUTHORITY["compatibility_policy"] == MEASUREMENT_COMPATIBILITY_POLICY
    assert MEASUREMENT_AUTHORITY["consolidation_source_commit"] == CONSOLIDATION_SOURCE_COMMIT
    assert MEASUREMENT_AUTHORITY["runtime_override_by_edcmbone"] is False
    assert MEASUREMENT_AUTHORITY["ucns_theorem_status_transfer"] is False


def test_importable_edcmbone_does_not_change_layer_selection(monkeypatch):
    monkeypatch.setitem(__import__("sys").modules, "edcmbone", ModuleType("edcmbone"))
    status = missing_ucns_status()
    monkeypatch.setattr(
        layers_module,
        "select_ucns_adapter",
        lambda: UCNSAdapterSelection(adapter=None, status=status),
    )

    layers = layers_module.build_default_layers()
    assert isinstance(layers.measurement, ConsolidatedMeasurementLayer)
    result = layers.run({"input": "authority check"})
    assert result["measurement"] == "edcm.measurement"
    assert result["layer_provenance"]["measurement"]["canonical"] is True
