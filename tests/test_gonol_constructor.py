# === CHECKS ===
# id: single_constructor_uses_scale_option_sets_check
#   proves: single_constructor_uses_scale_option_sets
#   call: self::test_constructor_uses_declared_scale_option_set
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: closed_gonol_atomic_at_any_scale_check
#   proves: closed_gonol_atomic_at_any_scale
#   call: self::test_closed_gonols_participate_directly_without_ladder
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: suffix_exception_carried_by_suffix_gonol_check
#   proves: suffix_exception_carried_by_suffix_gonol
#   call: self::test_suffix_coupling_exception_is_carried_by_closed_suffix
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: construction_survives_absent_ucns_geometry_check
#   proves: construction_survives_absent_ucns_geometry
#   call: self::test_base_construction_survives_absent_ucns_without_sys_path_mutation_or_ambient_import
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: geometry_mismatch_fails_closed_check
#   proves: geometry_mismatch_fails_closed
#   call: self::test_digest_mismatch_fails_closed
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: unified_candidate_does_not_select_canon_check
#   proves: unified_candidate_does_not_select_canon
#   call: self::test_receipt_remains_candidate
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from edcm.gonol import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    SCALE_OPTION_SETS,
    GonolConstructionError,
    construct_gonol,
    replay_gonol,
)


def _fake_public_gonol_authority() -> tuple[str, SimpleNamespace]:
    carrier = (" ", "A") + tuple(chr(0xE000 + index) for index in range(155))
    digest = sha256(
        json.dumps(tuple(carrier), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    index_by_glyph = {glyph: index for index, glyph in enumerate(carrier)}
    return digest, SimpleNamespace(
        PUBLIC_GONOL_157=carrier,
        PUBLIC_GONOL_SHA256=digest,
        public_gonol_position=lambda glyph: index_by_glyph.get(glyph),
    )


class GonolConstructorTest(unittest.TestCase):
    def test_constructor_uses_declared_scale_option_set(self) -> None:
        receipt = construct_gonol(scale="word", source="cut", source_id="fixture:cut")
        self.assertEqual(receipt.constructor_id, CONSTRUCTOR_ID)
        self.assertEqual(receipt.constructor_version, CONSTRUCTOR_VERSION)
        self.assertEqual(receipt.option_set, SCALE_OPTION_SETS["word"])
        self.assertEqual(receipt.gonol.scale, "word")
        self.assertEqual(receipt.gonol.source_units, ("c", "u", "t"))
        self.assertEqual([item.scale for item in receipt.gonol.source_characters], ["character", "character", "character"])
        self.assertEqual([item.source_units for item in receipt.gonol.source_characters], [("c",), ("u",), ("t",)])
        self.assertEqual(receipt.gonol.relation, "word-closure")
        self.assertEqual(receipt.gonol.receipt_digest, receipt.receipt_digest)

    def test_base_construction_survives_absent_ucns_without_sys_path_mutation_or_ambient_import(self) -> None:
        before = tuple(sys.path)
        receipt = construct_gonol(scale="word", source="cut", source_id="fixture:no-ucns")
        self.assertEqual(tuple(sys.path), before)
        self.assertEqual(receipt.geometry["state"], "hmmm")
        self.assertEqual(receipt.geometry["authority_binding"], "not-supplied")
        self.assertEqual(receipt.geometry["reason"], "UCNS Public Gonol authority not supplied")
        self.assertEqual(receipt.gonol.kind_id[0], "word")

    def test_explicit_geometry_is_observed_without_operation_claim(self) -> None:
        digest, fake = _fake_public_gonol_authority()
        with patch("edcm.gonol.PINNED_PUBLIC_GONOL_SHA256", digest):
            receipt = construct_gonol(
                scale="character",
                source="A",
                source_id="fixture:A",
                geometry_authority=fake,
            )
        self.assertEqual(receipt.geometry["state"], "observed")
        self.assertEqual(receipt.geometry["authority_binding"], "explicit")
        self.assertEqual(receipt.geometry["positions"], (1,))
        self.assertIn("not a UCNS geometric function operation", receipt.nonclaims)
        self.assertIn("exact UCNS geometric operation", receipt.hmmm[0])
        with self.assertRaises(TypeError):
            receipt.geometry["carrier_digest"] = "changed"  # type: ignore[index]

    def test_digest_mismatch_fails_closed(self) -> None:
        _digest, fake = _fake_public_gonol_authority()
        fake = SimpleNamespace(
            PUBLIC_GONOL_157=fake.PUBLIC_GONOL_157,
            PUBLIC_GONOL_SHA256="0" * 64,
            public_gonol_position=fake.public_gonol_position,
        )
        with self.assertRaisesRegex(GonolConstructionError, "digest mismatch"):
            construct_gonol(
                scale="character",
                source="A",
                source_id="fixture:mismatch",
                geometry_authority=fake,
            )

    def test_closed_gonols_participate_directly_without_ladder(self) -> None:
        character = construct_gonol(scale="character", source="c", source_id="fixture:c")
        word = construct_gonol(scale="word", source="cut", source_id="fixture:cut")
        definition = construct_gonol(
            scale="definition",
            relation="fixture:defines-directly",
            participants=(character.gonol, word.gonol),
            source="direct cross-scale evidence",
            source_id="fixture:def",
        )
        self.assertEqual(definition.gonol.participants, (character.gonol, word.gonol))
        self.assertEqual([item.scale for item in definition.gonol.participants], ["character", "word"])
        self.assertNotIn("mandatory character-word-definition-recursive ladder", definition.receipt_digest)
        self.assertIn("not a mandatory character-word-definition-recursive ladder", definition.nonclaims)

    def test_suffix_coupling_exception_is_carried_by_closed_suffix(self) -> None:
        base = construct_gonol(scale="word", source="try", source_id="fixture:try")
        ing = construct_gonol(
            scale="suffix",
            source="ing",
            source_id="fixture:ing",
            carried_options=(("suffix-coupling.final-y-after-consonant", "preserve-y"),),
        )
        coupling = construct_gonol(
            scale="suffix-coupling",
            participants=(base.gonol, ing.gonol),
            source_id="fixture:trying",
        )

        self.assertEqual(coupling.option_set, SCALE_OPTION_SETS["suffix-coupling"])
        self.assertEqual(coupling.gonol.relation, "suffix-coupling")
        self.assertEqual(coupling.gonol.participants, (base.gonol, ing.gonol))
        self.assertEqual(
            coupling.gonol.participants[1].carried_options,
            (("suffix-coupling.final-y-after-consonant", "preserve-y"),),
        )
        self.assertEqual(coupling.gonol.carried_options, ())
        self.assertIn(("carried_option", "suffix-coupling.final-y-after-consonant=preserve-y"), ing.gonol.provenance)
        self.assertNotIn("final-y-after-consonant", repr(SCALE_OPTION_SETS["suffix-coupling"]))
        self.assertNotIn("preserve-y", repr(SCALE_OPTION_SETS["suffix-coupling"]))

        replay = replay_gonol(receipt=coupling)
        self.assertEqual(coupling.receipt_digest, replay.receipt_digest)

    def test_suffix_carried_options_are_part_of_identity_and_fail_closed(self) -> None:
        base = construct_gonol(scale="word", source="try", source_id="fixture:try")
        ing_preserve = construct_gonol(
            scale="suffix",
            source="ing",
            source_id="fixture:ing",
            carried_options=(("suffix-coupling.final-y-after-consonant", "preserve-y"),),
        )
        ing_change = construct_gonol(
            scale="suffix",
            source="ing",
            source_id="fixture:ing",
            carried_options=(("suffix-coupling.final-y-after-consonant", "change-y-to-i"),),
        )
        self.assertNotEqual(ing_preserve.gonol.atomic_id, ing_change.gonol.atomic_id)

        preserved = construct_gonol(
            scale="suffix-coupling",
            participants=(base.gonol, ing_preserve.gonol),
            source_id="fixture:trying",
        )
        changed = construct_gonol(
            scale="suffix-coupling",
            participants=(base.gonol, ing_change.gonol),
            source_id="fixture:trying",
        )
        self.assertNotEqual(preserved.gonol.atomic_id, changed.gonol.atomic_id)

        with self.assertRaisesRegex(GonolConstructionError, "carried by a closed suffix gonol"):
            construct_gonol(
                scale="suffix-coupling",
                participants=(base.gonol, ing_preserve.gonol),
                carried_options=(("suffix-coupling.final-y-after-consonant", "preserve-y"),),
                source_id="fixture:bad-carrier",
            )

        with self.assertRaisesRegex(GonolConstructionError, "carried by a closed suffix gonol"):
            construct_gonol(
                scale="word",
                source="try",
                source_id="fixture:bad-word-carrier",
                carried_options=(("suffix-coupling.final-y-after-consonant", "preserve-y"),),
            )

        with self.assertRaisesRegex(GonolConstructionError, "closed base and closed suffix"):
            construct_gonol(
                scale="suffix-coupling",
                participants=(ing_preserve.gonol, base.gonol),
                source_id="fixture:bad-order",
            )

    def test_recursive_requires_relation_and_two_closed_participants(self) -> None:
        word = construct_gonol(scale="word", source="cut", source_id="fixture:one")
        self.assertEqual(SCALE_OPTION_SETS["recursive"].arity_policy, "minimum-two-closed-participants")
        with self.assertRaisesRegex(GonolConstructionError, "relation must be exact"):
            construct_gonol(scale="recursive", participants=(word.gonol, word.gonol), source_id="bad")
        with self.assertRaisesRegex(GonolConstructionError, "at least two closed participants"):
            construct_gonol(
                scale="recursive",
                relation="fixture:loop",
                participants=(word.gonol,),
                source_id="bad-one",
            )

    def test_order_and_multiplicity_are_preserved_in_atomic_identity(self) -> None:
        a = construct_gonol(scale="character", source="a", source_id="fixture:a")
        b = construct_gonol(scale="character", source="b", source_id="fixture:b")
        first = construct_gonol(
            scale="recursive",
            relation="fixture:sequence",
            participants=(a.gonol, a.gonol, b.gonol),
            source_id="fixture:seq-aab",
        )
        second = construct_gonol(
            scale="recursive",
            relation="fixture:sequence",
            participants=(a.gonol, b.gonol, a.gonol),
            source_id="fixture:seq-aba",
        )
        self.assertNotEqual(first.gonol.atomic_id, second.gonol.atomic_id)
        self.assertEqual(first.gonol.participants[0], first.gonol.participants[1])
        self.assertEqual([item.source_id for item in first.gonol.participants], ["fixture:a", "fixture:a", "fixture:b"])

    def test_replay_matches_byte_identity(self) -> None:
        word = construct_gonol(scale="word", source="cut", source_id="fixture:replay-word")
        kwargs = {
            "scale": "recursive",
            "relation": "fixture:pair",
            "participants": (word.gonol, word.gonol),
            "source_id": "fixture:replay",
        }
        first = construct_gonol(**kwargs)
        second = replay_gonol(receipt=first)
        self.assertEqual(first.receipt_digest, second.receipt_digest)
        self.assertEqual(first.gonol.atomic_id, second.gonol.atomic_id)
        tampered = replace(first, geometry={"state": "hmmm", "positions": ()})
        with self.assertRaisesRegex(GonolConstructionError, "geometry digest"):
            replay_gonol(receipt=tampered)

    def test_character_and_word_validation_fail_closed(self) -> None:
        with self.assertRaisesRegex(GonolConstructionError, "exactly one Unicode scalar"):
            construct_gonol(scale="character", source="ab", source_id="fixture:bad-char")
        with self.assertRaisesRegex(GonolConstructionError, "surrogate"):
            construct_gonol(scale="character", source="\ud800", source_id="fixture:bad-surrogate")
        with self.assertRaisesRegex(GonolConstructionError, "source_id contains a surrogate"):
            construct_gonol(scale="word", source="bad", source_id="fixture:\ud800")
        with self.assertRaisesRegex(GonolConstructionError, "relation contains a surrogate"):
            construct_gonol(scale="definition", source="bad", relation="fixture:\ud800", source_id="fixture:bad")
        with self.assertRaisesRegex(GonolConstructionError, "whitespace-delimited"):
            construct_gonol(scale="word", source="two words", source_id="fixture:bad-word")

    def test_declared_default_relation_and_registry_are_frozen(self) -> None:
        with self.assertRaisesRegex(GonolConstructionError, "declared default"):
            construct_gonol(
                scale="character",
                source="A",
                source_id="fixture:bad-relation",
                relation="fixture:custom-character",
            )
        with self.assertRaises(TypeError):
            SCALE_OPTION_SETS["character"] = SCALE_OPTION_SETS["word"]  # type: ignore[index]

    def test_participant_receipt_identity_is_bound_into_parent_closure(self) -> None:
        digest, fake = _fake_public_gonol_authority()
        absent = construct_gonol(scale="word", source="A", source_id="fixture:A")
        with patch("edcm.gonol.PINNED_PUBLIC_GONOL_SHA256", digest):
            observed = construct_gonol(
                scale="word",
                source="A",
                source_id="fixture:A",
                geometry_authority=fake,
            )
        self.assertEqual(absent.gonol.source_units, observed.gonol.source_units)
        self.assertNotEqual(absent.gonol.geometry_digest, observed.gonol.geometry_digest)
        self.assertNotEqual(absent.receipt_digest, observed.receipt_digest)
        first = construct_gonol(
            scale="recursive",
            relation="fixture:geometry-sensitive",
            participants=(absent.gonol, absent.gonol),
            source_id="fixture:parent",
        )
        second = construct_gonol(
            scale="recursive",
            relation="fixture:geometry-sensitive",
            participants=(observed.gonol, observed.gonol),
            source_id="fixture:parent",
        )
        self.assertNotEqual(first.receipt_digest, second.receipt_digest)

    def test_tampered_closed_participants_fail_before_parent_hashing(self) -> None:
        word = construct_gonol(scale="word", source="cut", source_id="fixture:cut")
        tampered = replace(word.gonol, source_units=("X",))
        with self.assertRaisesRegex(GonolConstructionError, "source character gonol count"):
            construct_gonol(
                scale="recursive",
                relation="fixture:tampered",
                participants=(tampered, word.gonol),
                source_id="fixture:tampered-parent",
            )

    def test_receipt_remains_candidate(self) -> None:
        receipt = construct_gonol(scale="word", source="cut", source_id="fixture:standing")
        self.assertEqual(receipt.standing, "implemented-candidate")
        self.assertEqual(receipt.selection_effect, "none")
        self.assertIn("not selected canon", receipt.nonclaims)
        self.assertIn("not EDCM measurement validity", receipt.nonclaims)
        self.assertIn("which scales and relations, if any, are later selected", receipt.hmmm)


if __name__ == "__main__":
    unittest.main()
