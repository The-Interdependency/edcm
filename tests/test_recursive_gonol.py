# === CHECKS ===
# id: recursive_uses_closed_gonols_check
#   proves: recursive_uses_closed_gonols
#   call: self::test_recursive_uses_closed_words_without_reopening
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: recursive_relation_is_caller_supplied_check
#   proves: recursive_relation_is_caller_supplied
#   call: self::test_missing_relation_fails_closed
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: recursive_result_may_participate_check
#   proves: recursive_result_may_participate
#   call: self::test_closed_recursive_gonol_may_participate_again
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: recursive_candidate_does_not_select_canon_check
#   proves: recursive_candidate_does_not_select_canon
#   call: self::test_receipt_remains_unimplemented_canon
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import unittest

from edcm.character_word import construct_character_word_gonols
from edcm.definition_gonol import construct_definition_gonol
from edcm.recursive_gonol import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    RecursiveGonolError,
    construct_recursive_gonol,
    replay_recursive_gonol,
)


class RecursiveGonolTest(unittest.TestCase):
    def test_recursive_uses_closed_words_without_reopening(self) -> None:
        words = construct_character_word_gonols("cut divide", source_id="fixture:words")
        receipt = construct_recursive_gonol(
            relation="fixture:ordered-pair",
            participants=words.words,
            source_id="fixture:pair#1",
        )
        self.assertEqual(receipt.recursive.participants, words.words)
        self.assertEqual(receipt.recursive.participants[0].characters, words.words[0].characters)
        self.assertEqual(
            ["".join(word.kind_id) for word in receipt.recursive.participants],
            ["cut", "divide"],
        )

    def test_relation_is_not_inferred_from_adjacency(self) -> None:
        words = construct_character_word_gonols("cut divide", source_id="fixture:words")
        first = construct_recursive_gonol(
            relation="fixture:ordered-pair",
            participants=words.words,
            source_id="fixture:pair#1",
        )
        second = construct_recursive_gonol(
            relation="fixture:contrast",
            participants=words.words,
            source_id="fixture:pair#2",
        )
        self.assertEqual(first.recursive.participants, second.recursive.participants)
        self.assertNotEqual(first.recursive.kind_id, second.recursive.kind_id)
        self.assertNotEqual(first.receipt_digest, second.receipt_digest)

    def test_definition_gonol_may_participate(self) -> None:
        definition = construct_definition_gonol(
            headword="cut",
            definition="to divide",
            source_id="fixture:cut#1",
        )
        other = construct_character_word_gonols("edge", source_id="fixture:edge").words[0]
        receipt = construct_recursive_gonol(
            relation="fixture:uses",
            participants=(definition.definition, other),
            source_id="fixture:uses#1",
        )
        self.assertEqual(receipt.recursive.participants[0], definition.definition)
        self.assertEqual(receipt.recursive.participants[1], other)

    def test_closed_recursive_gonol_may_participate_again(self) -> None:
        words = construct_character_word_gonols("cut divide edge", source_id="fixture:three")
        inner = construct_recursive_gonol(
            relation="fixture:ordered-pair",
            participants=words.words[:2],
            source_id="fixture:inner",
        )
        outer = construct_recursive_gonol(
            relation="fixture:attach",
            participants=(inner.recursive, words.words[2]),
            source_id="fixture:outer",
        )
        self.assertEqual(outer.recursive.participants[0], inner.recursive)
        self.assertEqual(outer.recursive.participants[1], words.words[2])
        self.assertEqual(outer.recursive.kind_id[0], "fixture:attach")

    def test_missing_relation_fails_closed(self) -> None:
        words = construct_character_word_gonols("cut divide", source_id="fixture:words")
        with self.assertRaisesRegex(RecursiveGonolError, "relation must be an exact"):
            construct_recursive_gonol(relation=" ", participants=words.words, source_id="fixture:bad")

    def test_single_participant_fails_closed(self) -> None:
        words = construct_character_word_gonols("cut", source_id="fixture:one")
        with self.assertRaisesRegex(RecursiveGonolError, "at least two closed gonols"):
            construct_recursive_gonol(
                relation="fixture:loop",
                participants=words.words,
                source_id="fixture:loop",
            )

    def test_character_gonol_fails_closed(self) -> None:
        words = construct_character_word_gonols("cut", source_id="fixture:char")
        with self.assertRaisesRegex(RecursiveGonolError, "character gonols are not recursive"):
            construct_recursive_gonol(
                relation="fixture:bad",
                participants=(words.characters[0], words.words[0]),
                source_id="fixture:bad-char",
            )

    def test_replay_matches_byte_identity(self) -> None:
        words = construct_character_word_gonols("cut divide", source_id="fixture:replay")
        kwargs = {
            "relation": "fixture:ordered-pair",
            "participants": words.words,
            "source_id": "fixture:replay#1",
        }
        first = construct_recursive_gonol(**kwargs)
        second = replay_recursive_gonol(**kwargs)
        self.assertEqual(first.receipt_digest, second.receipt_digest)
        self.assertEqual(first.recursive.kind_id, second.recursive.kind_id)

    def test_receipt_remains_unimplemented_canon(self) -> None:
        words = construct_character_word_gonols("cut divide", source_id="fixture:stand")
        receipt = construct_recursive_gonol(
            relation="fixture:ordered-pair",
            participants=words.words,
            source_id="fixture:stand#1",
        )
        self.assertEqual(receipt.constructor_id, CONSTRUCTOR_ID)
        self.assertEqual(receipt.constructor_version, CONSTRUCTOR_VERSION)
        self.assertEqual(receipt.standing, "implemented-candidate")
        self.assertEqual(receipt.selection_effect, "none")
        self.assertIn("not a UCNS geometric coupling law", receipt.nonclaims)
        self.assertIn("UCNS Möbius-carrier affixiation/coupling law", receipt.hmmm)

    def test_identity_is_structure_not_hash(self) -> None:
        words = construct_character_word_gonols("a b", source_id="fixture:id")
        receipt = construct_recursive_gonol(
            relation="r",
            participants=words.words,
            source_id="fixture:id#1",
        )
        self.assertEqual(receipt.recursive.kind_id[0], "r")
        self.assertEqual(receipt.recursive.kind_id[1][0][0], "word")
        self.assertNotEqual(receipt.receipt_digest, receipt.recursive.kind_id)


if __name__ == "__main__":
    unittest.main()
