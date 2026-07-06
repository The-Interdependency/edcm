"""Canon-data and parser regression tests for the consolidated measurement package.

Ported from The-Interdependency/edcmbone tests/test_polarity_balance.py and the
backend-parser half of tests/test_affix_residual_validation.py (the
core.operator.matcher half stays upstream — that package was not consolidated).
"""

from __future__ import annotations

import json
from pathlib import Path

from edcm.measurement import CanonLoader
from edcm.measurement.parser.turns_rounds import _BoneClassifier

WORDS_PATH = (
    Path(__file__).resolve().parents[1]
    / "edcm" / "measurement" / "canon" / "data" / "bones_words_v1.json"
)


def _word_tokens():
    data = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    return {e["word"].lower() for e in data["words"]}


# (negative_pole, affirmative_pole) pairs that must both be present.
# Frozen canon principle (bones_words_v1.json _meta.polarity_balance_principle):
# if the negative pole of a category is a bone, the affirmative pole must also
# be a bone, or the instrument carries built-in observer bias.
POLARITY_PAIRS = [
    ("not", "yes"),
    ("never", "always"),
    ("nothing", "something"),
    ("nobody", "somebody"),
    ("nowhere", "somewhere"),
    ("none", "some"),
    ("neither", "either"),
    ("rarely", "often"),
    ("seldom", "frequently"),
    ("hardly", "fully"),
    ("barely", "completely"),
]


def test_polarity_balance_adverbs():
    tokens = _word_tokens()
    for neg, pos in POLARITY_PAIRS:
        assert neg in tokens, f"negative pole missing: {neg!r}"
        assert pos in tokens, f"affirmative pole missing for {neg!r}: {pos!r}"


def test_near_negation_group_has_affirmative_coverage():
    tokens = _word_tokens()
    for neg in ("hardly", "scarcely", "barely"):
        assert neg in tokens, f"near-negation pole missing: {neg!r}"
    for pos in ("fully", "completely"):
        assert pos in tokens, f"affirmative completion pole missing: {pos!r}"


def test_parser_affix_does_not_fire_on_invalid_residuals():
    canon = CanonLoader()
    c = _BoneClassifier(canon)
    toks = ["uncle", "unit", "universe", "under", "unique"]
    out = c.classify_sequence(toks)
    assert all((not hasattr(x, "bone_type") or x.bone_type != "affix") for x in out)


def test_parser_affix_positive_cases_still_emit_for_canon_valid_stems():
    canon = CanonLoader()
    c = _BoneClassifier(canon)

    # Guaranteed by current canon word inventory: "redo" -> residual "do" exists.
    out = c.classify_sequence(["redo"])
    assert [getattr(x, "bone_type", None) for x in out] == ["affix"]


def test_parser_affix_emission_stays_canon_driven():
    canon = CanonLoader()
    c = _BoneClassifier(canon)

    # Morphologically valid English, but backend affix emission depends on the
    # residual stem being present in the canon word index — canon-driven, not
    # heuristic.
    for tok, residual in (("unhappy", "happy"), ("linking", "link")):
        out = c.classify_sequence([tok])[0]
        emits_affix = getattr(out, "bone_type", None) == "affix"
        residual_in_canon = canon.lookup_word(residual) is not None
        assert emits_affix == residual_in_canon
