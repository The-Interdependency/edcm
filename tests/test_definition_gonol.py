# === CHECKS ===
# id: definition_uses_closed_word_gonols_check
#   proves: definition_uses_closed_word_gonols
#   call: self::test_definition_uses_closed_word_gonols_without_reopening
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: definition_requires_exact_source_evidence_check
#   proves: definition_requires_exact_source_evidence
#   call: self::test_empty_definition_fails_closed
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: definition_relation_is_intrinsic_check
#   proves: definition_relation_is_intrinsic
#   call: self::test_definition_relation_binds_headword_and_body_words
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: definition_candidate_does_not_select_canon_check
#   proves: definition_candidate_does_not_select_canon
#   call: self::test_receipt_remains_unimplemented_canon
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import unittest

from edcm.character_word import construct_character_word_gonols
from edcm.definition_gonol import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    RELATION,
    DefinitionGonolError,
    construct_definition_gonol,
    replay_definition_gonol,
)


class DefinitionGonolTest(unittest.TestCase):
    def test_definition_uses_closed_word_gonols_without_reopening(self) -> None:
        receipt = construct_definition_gonol(
            headword="don't",
            definition="do not",
            source_id="fixture:dont#1",
        )
        independent = construct_character_word_gonols("don't", source_id="fixture:dont#1#headword")
        self.assertEqual(len(receipt.definition.headword_words), 1)
        self.assertEqual(receipt.definition.headword_words[0].kind_id, independent.words[0].kind_id)
        self.assertEqual(
            receipt.definition.headword_words[0].characters,
            independent.words[0].characters,
        )
        self.assertEqual(receipt.headword_receipt.receipt_digest, independent.receipt_digest)
        self.assertEqual(
            ["".join(word.kind_id) for word in receipt.definition.body_words],
            ["do", "not"],
        )

    def test_definition_relation_binds_headword_and_body_words(self) -> None:
        receipt = construct_definition_gonol(
            headword="ice cream",
            definition="a frozen dessert",
            source_id="fixture:ice-cream#1",
        )
        self.assertEqual(receipt.definition.relation, RELATION)
        self.assertEqual(
            ["".join(word.kind_id) for word in receipt.definition.headword_words],
            ["ice", "cream"],
        )
        self.assertEqual(
            ["".join(word.kind_id) for word in receipt.definition.body_words],
            ["a", "frozen", "dessert"],
        )
        self.assertEqual(
            receipt.definition.kind_id,
            (
                (("i", "c", "e"), ("c", "r", "e", "a", "m")),
                (
                    ("a",),
                    ("f", "r", "o", "z", "e", "n"),
                    ("d", "e", "s", "s", "e", "r", "t"),
                ),
            ),
        )

    def test_empty_definition_fails_closed(self) -> None:
        with self.assertRaisesRegex(DefinitionGonolError, "definition produced no closed word"):
            construct_definition_gonol(
                headword="cut",
                definition="   ",
                source_id="fixture:cut#empty",
            )

    def test_empty_headword_fails_closed(self) -> None:
        with self.assertRaisesRegex(DefinitionGonolError, "headword produced no closed word"):
            construct_definition_gonol(
                headword="\n",
                definition="to divide",
                source_id="fixture:cut#no-head",
            )

    def test_missing_source_id_fails_closed(self) -> None:
        with self.assertRaisesRegex(DefinitionGonolError, "source_id"):
            construct_definition_gonol(headword="cut", definition="to divide", source_id="")

    def test_senses_remain_separate_gonols(self) -> None:
        first = construct_definition_gonol(
            headword="cut",
            definition="to divide with a sharp edge",
            source_id="fixture:cut#1",
        )
        second = construct_definition_gonol(
            headword="cut",
            definition="to reduce",
            source_id="fixture:cut#2",
        )
        self.assertEqual(first.definition.headword_words[0].kind_id, second.definition.headword_words[0].kind_id)
        self.assertNotEqual(first.definition.kind_id, second.definition.kind_id)
        self.assertNotEqual(first.receipt_digest, second.receipt_digest)

    def test_replay_matches_byte_identity(self) -> None:
        kwargs = {
            "headword": "cut",
            "definition": "to divide with a sharp edge",
            "source_id": "fixture:cut#replay",
        }
        first = construct_definition_gonol(**kwargs)
        second = replay_definition_gonol(**kwargs)
        self.assertEqual(first.receipt_digest, second.receipt_digest)
        self.assertEqual(first.definition.kind_id, second.definition.kind_id)

    def test_receipt_remains_unimplemented_canon(self) -> None:
        receipt = construct_definition_gonol(
            headword="cut",
            definition="to divide",
            source_id="fixture:cut#standing",
        )
        self.assertEqual(receipt.constructor_id, CONSTRUCTOR_ID)
        self.assertEqual(receipt.constructor_version, CONSTRUCTOR_VERSION)
        self.assertEqual(receipt.standing, "implemented-candidate")
        self.assertEqual(receipt.selection_effect, "none")
        self.assertIn("not a dictionary or sense inventory", receipt.nonclaims)
        self.assertIn("not OEWN or lexical-floor revival", receipt.nonclaims)
        self.assertIn("which recursive relations, if any, are later selected", receipt.hmmm)

    def test_identity_is_structure_not_hash(self) -> None:
        receipt = construct_definition_gonol(
            headword="a",
            definition="b",
            source_id="fixture:id",
        )
        self.assertEqual(receipt.definition.kind_id, ((("a",),), (("b",),)))
        self.assertNotEqual(receipt.receipt_digest, receipt.definition.kind_id)


if __name__ == "__main__":
    unittest.main()
