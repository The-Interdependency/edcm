# === CHECKS ===
# id: character_admission_is_unicode_scalar_check
#   proves: character_admission_is_unicode_scalar
#   call: self::test_every_unicode_scalar_is_a_character_gonol
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: word_closure_uses_declared_whitespace_check
#   proves: word_closure_uses_declared_whitespace
#   call: self::test_whitespace_closes_words_and_keeps_boundaries
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: closed_words_preserve_constituents_check
#   proves: closed_words_preserve_constituents
#   call: self::test_closed_word_keeps_apostrophe_and_constituents
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
# id: candidate_does_not_select_canon_check
#   proves: candidate_does_not_select_canon
#   call: self::test_receipt_remains_unimplemented_canon
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from types import SimpleNamespace
import unittest
from unittest.mock import patch

from edcm.character_word import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    PINNED_PUBLIC_GONOL_SHA256,
    CharacterWordError,
    construct_character_word_gonols,
    replay_character_word_gonols,
)


class CharacterWordGonolTest(unittest.TestCase):
    def test_every_unicode_scalar_is_a_character_gonol(self) -> None:
        receipt = construct_character_word_gonols("Aé ", source_id="fixture-scalars")
        self.assertEqual([item.scalar for item in receipt.characters], ["A", "é", " "])
        self.assertEqual([item.occurrence for item in receipt.characters], [0, 1, 2])
        self.assertEqual(receipt.characters[0].carrier_index, 1)
        self.assertIsNone(receipt.characters[1].carrier_index)
        self.assertEqual(receipt.characters[2].carrier_index, 0)
        self.assertEqual(receipt.carrier_digest, PINNED_PUBLIC_GONOL_SHA256)

    def test_whitespace_closes_words_and_keeps_boundaries(self) -> None:
        receipt = construct_character_word_gonols("  word  gonol\n", source_id="fixture-space")
        self.assertEqual(["".join(word.kind_id) for word in receipt.words], ["word", "gonol"])
        self.assertEqual([item.scalar for item in receipt.boundaries], [" ", " ", " ", " ", "\n"])
        self.assertEqual(receipt.words[0].source_start, 2)
        self.assertEqual(receipt.words[0].source_end, 6)
        self.assertEqual(receipt.words[1].source_start, 8)
        self.assertEqual(receipt.words[1].source_end, 13)

    def test_closed_word_keeps_apostrophe_and_constituents(self) -> None:
        receipt = construct_character_word_gonols("don't cut.", source_id="fixture-dont")
        self.assertEqual(len(receipt.words), 2)
        dont = receipt.words[0]
        self.assertEqual(dont.kind_id, ("d", "o", "n", "'", "t"))
        self.assertEqual([item.role for item in dont.characters], ["word-member"] * 5)
        self.assertEqual(dont.characters[3].scalar, "'")
        self.assertIsNotNone(dont.characters[3].carrier_index)
        cut = receipt.words[1]
        self.assertEqual(cut.kind_id, ("c", "u", "t", "."))
        self.assertEqual(receipt.boundaries[0].scalar, " ")

    def test_empty_source_is_complete_and_empty(self) -> None:
        receipt = construct_character_word_gonols("", source_id="fixture-empty")
        self.assertEqual(receipt.source_length, 0)
        self.assertEqual(receipt.characters, ())
        self.assertEqual(receipt.words, ())
        self.assertEqual(receipt.boundaries, ())

    def test_replay_matches_byte_identity(self) -> None:
        source = "don't cut."
        first = construct_character_word_gonols(source, source_id="fixture-replay")
        second = replay_character_word_gonols(source, source_id="fixture-replay")
        self.assertEqual(first.receipt_digest, second.receipt_digest)
        self.assertEqual(
            [item.scalar for item in first.characters],
            [item.scalar for item in second.characters],
        )
        self.assertEqual(
            [word.kind_id for word in first.words],
            [word.kind_id for word in second.words],
        )

    def test_receipt_remains_unimplemented_canon(self) -> None:
        receipt = construct_character_word_gonols("a", source_id="fixture-standing")
        self.assertEqual(receipt.constructor_id, CONSTRUCTOR_ID)
        self.assertEqual(receipt.constructor_version, CONSTRUCTOR_VERSION)
        self.assertEqual(receipt.standing, "implemented-candidate")
        self.assertEqual(receipt.selection_effect, "none")
        self.assertIn("not selected canon", receipt.nonclaims)
        self.assertIn("not EDCM measurement validity", receipt.nonclaims)
        self.assertIn("definition gonol constructor", receipt.hmmm)

    def test_identity_is_structure_not_hash(self) -> None:
        receipt = construct_character_word_gonols("aa", source_id="fixture-identity")
        self.assertEqual(receipt.characters[0].kind_id, "a")
        self.assertEqual(receipt.characters[1].kind_id, "a")
        self.assertNotEqual(receipt.characters[0].occurrence, receipt.characters[1].occurrence)
        self.assertEqual(receipt.words[0].kind_id, ("a", "a"))
        self.assertNotEqual(receipt.receipt_digest, receipt.words[0].kind_id)

    def test_digest_mismatch_fails_closed(self) -> None:
        fake = SimpleNamespace(
            PUBLIC_GONOL_SHA256="0" * 64,
            public_gonol_position=lambda _glyph: 0,
        )
        with patch("edcm.character_word.importlib.import_module", return_value=fake):
            with self.assertRaisesRegex(CharacterWordError, "digest mismatch"):
                construct_character_word_gonols("a", source_id="fixture-mismatch")

    def test_surrogate_fails_closed(self) -> None:
        with self.assertRaisesRegex(CharacterWordError, "surrogate"):
            construct_character_word_gonols("\ud800", source_id="fixture-surrogate")


if __name__ == "__main__":
    unittest.main()
