from __future__ import annotations

import json
from dataclasses import dataclass
from types import ModuleType

import pytest

import edcm.metapat_adapter as adapter_module
from edcm.metapat_adapter import (
    ActualMetapatAdapter,
    MetapatAdapterConstructionError,
    UnsupportedMetapatSchemaError,
    select_metapat_adapter,
)


def _fake_metapat(
    *,
    schema_id: str = "metapat.module-envelope",
    schema_version: str = "1.0.0",
) -> tuple[ModuleType, type]:
    module = ModuleType("metapat")

    @dataclass(frozen=True)
    class MetapatModuleEnvelope:
        module_id: str = "metapat.test"
        module_kind: str = "simplex"
        source_statement_refs: tuple[str, ...] = ("AXIOMS.md::ROOT[1]",)
        source_statements: tuple[str, ...] = ("Legible difference is distinction.",)
        constraints: tuple[str, ...] = ("Preserve exact text.",)
        permitted_interpretations: tuple[str, ...] = ("Use as semantic authority.",)
        unresolved_constraints: tuple[str, ...] = ("hmmm: mapping remains unresolved.",)
        canon_version: str = "metapat-canon-v1"
        canon_digest: str = "a" * 64
        schema_id: str = "metapat.module-envelope"
        schema_version: str = "1.0.0"
        provenance_digest: str = "b" * 64

        def to_dict(self):
            return {
                "schema_id": self.schema_id,
                "schema_version": self.schema_version,
                "module_id": self.module_id,
                "module_kind": self.module_kind,
                "canon_version": self.canon_version,
                "canon_digest": self.canon_digest,
                "source_statement_refs": list(self.source_statement_refs),
                "source_statements": list(self.source_statements),
                "constraints": list(self.constraints),
                "permitted_interpretations": list(self.permitted_interpretations),
                "unresolved_constraints": list(self.unresolved_constraints),
                "provenance_digest": self.provenance_digest,
            }

        @classmethod
        def from_dict(cls, data):
            return cls(
                schema_id=data["schema_id"],
                schema_version=data["schema_version"],
                module_id=data["module_id"],
                module_kind=data["module_kind"],
                canon_version=data["canon_version"],
                canon_digest=data["canon_digest"],
                source_statement_refs=tuple(data["source_statement_refs"]),
                source_statements=tuple(data["source_statements"]),
                constraints=tuple(data["constraints"]),
                permitted_interpretations=tuple(data["permitted_interpretations"]),
                unresolved_constraints=tuple(data["unresolved_constraints"]),
                provenance_digest=data["provenance_digest"],
            )

        @classmethod
        def from_json(cls, value):
            return cls.from_dict(json.loads(value))

    module.MetapatModuleEnvelope = MetapatModuleEnvelope
    module.MODULE_ENVELOPE_SCHEMA_ID = schema_id
    module.MODULE_ENVELOPE_SCHEMA_VERSION = schema_version
    module.__version__ = "0.test"
    return module, MetapatModuleEnvelope


def test_direct_metapat_absence_is_typed_unavailable(monkeypatch):
    def missing(name: str):
        raise ModuleNotFoundError("No module named 'metapat'", name="metapat")

    monkeypatch.setattr(adapter_module.importlib, "import_module", missing)
    selection = select_metapat_adapter()
    assert selection.adapter is None
    assert selection.status.metapat_package_available is False
    assert selection.status.metapat_adapter_active is False
    assert selection.status.metapat_envelope_attached is False


def test_transitive_import_failure_is_visible(monkeypatch):
    def broken(name: str):
        raise ModuleNotFoundError("No module named 'metapat_helper'", name="metapat_helper")

    monkeypatch.setattr(adapter_module.importlib, "import_module", broken)
    with pytest.raises(ModuleNotFoundError, match="metapat_helper"):
        select_metapat_adapter()


def test_importable_malformed_metapat_fails_adapter_construction():
    module, _ = _fake_metapat()
    del module.MetapatModuleEnvelope
    with pytest.raises(MetapatAdapterConstructionError, match="MetapatModuleEnvelope"):
        ActualMetapatAdapter(module)


def test_unsupported_metapat_schema_fails_closed():
    module, _ = _fake_metapat(schema_version="99.0.0")
    with pytest.raises(UnsupportedMetapatSchemaError, match="99.0.0"):
        ActualMetapatAdapter(module)


def test_package_and_adapter_do_not_imply_envelope_attachment():
    module, _ = _fake_metapat()
    result = ActualMetapatAdapter(module).normalize({"transcript": "A: hello"})
    status = result["metapat_integration"]
    assert status["metapat_package_available"] is True
    assert status["metapat_adapter_active"] is True
    assert status["metapat_envelope_attached"] is False
    assert status["metapat_canon_identity_attached"] is False
    assert status["metapat_semantic_constraints_attached"] is False
    assert status["metapat_theorem_status_attached"] is False
    assert status["metapat_measurement_values_attached"] is False
    assert "metapat_semantics" not in result


def test_actual_envelope_preserves_semantic_authority_without_measurement_values():
    module, envelope_type = _fake_metapat()
    result = ActualMetapatAdapter(module).normalize(
        {"metapat_envelope": envelope_type()}
    )
    evidence = result["metapat_semantics"]
    status = result["metapat_integration"]

    assert evidence["canon_digest"] == "a" * 64
    assert evidence["provenance_digest"] == "b" * 64
    assert evidence["source_statement_refs"] == ("AXIOMS.md::ROOT[1]",)
    assert evidence["unresolved_constraints"] == (
        "hmmm: mapping remains unresolved.",
    )
    assert evidence["semantic_labels_are_measurements"] is False
    assert evidence["theorem_status_transfer"] is False
    assert evidence["measurement_validity_claim"] is False
    assert status["metapat_envelope_attached"] is True
    assert status["metapat_semantic_constraints_attached"] is True


def test_json_and_mapping_forms_use_producer_constructors():
    module, envelope_type = _fake_metapat()
    envelope = envelope_type()
    adapter = ActualMetapatAdapter(module)

    from_json = adapter.normalize({"metapat_envelope_json": json.dumps(envelope.to_dict())})
    from_dict = adapter.normalize({"metapat_envelope_dict": envelope.to_dict()})
    assert from_json["metapat_semantics"] == from_dict["metapat_semantics"]


def test_multiple_envelope_forms_fail_closed():
    module, envelope_type = _fake_metapat()
    envelope = envelope_type()
    with pytest.raises(ValueError, match="exactly one"):
        ActualMetapatAdapter(module).normalize(
            {
                "metapat_envelope": envelope,
                "metapat_envelope_dict": envelope.to_dict(),
            }
        )


def test_wrong_envelope_object_type_fails_closed():
    module, _ = _fake_metapat()
    with pytest.raises(TypeError, match="actual metapat.MetapatModuleEnvelope"):
        ActualMetapatAdapter(module).normalize({"metapat_envelope": object()})


def test_live_metapat_envelope_roundtrip_when_integration_is_installed():
    metapat = pytest.importorskip("metapat")
    envelope = metapat.root_spine_module_envelope()
    result = ActualMetapatAdapter(metapat).normalize({"metapat_envelope": envelope})

    assert result["metapat_semantics"]["canon_digest"] == envelope.canon_digest
    assert result["metapat_semantics"]["provenance_digest"] == envelope.provenance_digest
    assert result["metapat_semantics"]["source_statements"] == envelope.source_statements
    assert result["metapat_integration"]["metapat_envelope_attached"] is True
    assert result["metapat_integration"]["metapat_theorem_status_attached"] is False
