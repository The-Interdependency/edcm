"""Compatibility contracts for the current METAPAT envelope producer schema."""

from __future__ import annotations

import json
from dataclasses import dataclass
from types import ModuleType

from edcm.metapat_adapter import ActualMetapatAdapter, SUPPORTED_ENVELOPE_SCHEMAS


def _schema_v12_module() -> tuple[ModuleType, type]:
    module = ModuleType("metapat")

    @dataclass(frozen=True)
    class MetapatModuleEnvelope:
        module_id: str = "metapat.root_spine"
        module_kind: str = "canon-module"
        source_statement_refs: tuple[str, ...] = ("AXIOMS.md#root-spine",)
        source_statements: tuple[str, ...] = ("Legible difference is distinction.",)
        constraints: tuple[str, ...] = ("Preserve exact semantic authority.",)
        permitted_interpretations: tuple[str, ...] = ("Use as external provenance.",)
        unresolved_constraints: tuple[str, ...] = ("hmmm: payload meaning remains explicit.",)
        canon_version: str = "metapat-canon-v1"
        canon_digest: str = "a" * 64
        schema_id: str = "metapat.module-envelope"
        schema_version: str = "1.2.0"
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
    module.MODULE_ENVELOPE_SCHEMA_ID = "metapat.module-envelope"
    module.MODULE_ENVELOPE_SCHEMA_VERSION = "1.2.0"
    module.__version__ = "0.3.0"
    return module, MetapatModuleEnvelope


def test_schema_v12_is_explicitly_supported() -> None:
    assert ("metapat.module-envelope", "1.2.0") in SUPPORTED_ENVELOPE_SCHEMAS


def test_schema_v12_roundtrip_preserves_current_producer_fields() -> None:
    module, envelope_type = _schema_v12_module()
    envelope = envelope_type()
    adapter = ActualMetapatAdapter(module)

    live = adapter.normalize({"metapat_envelope": envelope})
    encoded = adapter.normalize({"metapat_envelope_json": json.dumps(envelope.to_dict())})

    assert live["metapat_semantics"] == encoded["metapat_semantics"]
    assert live["metapat_semantics"]["schema_version"] == "1.2.0"
    assert live["metapat_semantics"]["module_kind"] == "canon-module"
    assert live["metapat_semantics"]["theorem_status_transfer"] is False
    assert live["metapat_semantics"]["measurement_validity_claim"] is False
