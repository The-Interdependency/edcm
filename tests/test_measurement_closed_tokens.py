"""
Tests for edcm.measurement.ucns.closed_tokens — ported from The-Interdependency/edcmbone tests/test_closed_tokens.py.

Coverage:
  1. All ~250 closed tokens encode without error.
  2. Every encoded token recovers its class via class_of().
  3. Within-class structural similarity: all pronouns share class anchor,
     differ only in payload.
  4. Across-class structural difference: different classes have different
     class anchors.
  5. Pronoun feature recovery: encoding "he" then comparing payloads
     to "she" shows gender difference.
  6. Determiner feature recovery: definite vs indefinite distinguishable.
  7. Pairing chirality: open and close brackets are distinct objects;
     encoding 5 open marks gives 5 distinct objects, same for closes.
  8. Roundtrip: encode → class_of → expected class.
  9. Whitespace varieties distinguishable.
 10. Numeral digit/spelled forms distinguishable.
 11. Full-vocabulary uniqueness: every token in DISPATCH produces a
     UCNS object distinct from every other.
"""

from fractions import Fraction
from edcm.measurement.ucns.ucns_v04 import unit_obj, multiply
from edcm.measurement.ucns.closed_tokens import (
    encode, class_of, feature_payload_of,
    DISPATCH, CLASS_NAMES,
    CLASS_PRONOUN, CLASS_DETERMINER, CLASS_PREPOSITION,
    CLASS_CONJUNCTION, CLASS_AUXILIARY, CLASS_PARTICLE,
    CLASS_INTERJECTION, CLASS_WHITESPACE,
    CLASS_PUNCT_TERMINAL, CLASS_PUNCT_JUNCTURE,
    CLASS_PUNCT_OPEN, CLASS_PUNCT_CLOSE,
    CLASS_PUNCT_AFFIX, CLASS_PUNCT_MODAL, CLASS_NUMERAL,
    PRONOUN_TABLE, DETERMINER_TABLE,
)


def banner(s):
    print("\n" + "=" * 72)
    print(s)
    print("=" * 72)

def ok(cond, label):
    mark = "✓" if cond else "✗"
    print(f"  {mark} {label}")
    if not cond:
        raise AssertionError(label)


def test_all_tokens_encode():
    banner("Test 1 — all closed tokens encode without error")
    failed = []
    for token in DISPATCH:
        obj = encode(token)
        if obj is None:
            failed.append(token)
    ok(not failed, f"all {len(DISPATCH)} closed tokens encode (failures: {failed})")


def test_class_recovery():
    banner("Test 2 — class_of recovers correct class for every token")
    mismatches = []
    for token, (expected_class, _) in DISPATCH.items():
        obj = encode(token)
        recovered = class_of(obj)
        if recovered != expected_class:
            mismatches.append((token, expected_class, recovered))
    if mismatches:
        for token, exp, got in mismatches[:5]:
            print(f"    {token!r}: expected class {exp}, got {got}")
    ok(not mismatches,
       f"all {len(DISPATCH)} tokens roundtrip correctly "
       f"({len(mismatches)} mismatches)")


def test_within_class_share_class_anchor():
    banner("Test 3 — within-class tokens share class anchor")
    pronouns = [encode(w) for w in PRONOUN_TABLE]
    classes = {class_of(p) for p in pronouns}
    ok(classes == {CLASS_PRONOUN},
       f"all pronouns map to class {CLASS_PRONOUN} (got {classes})")

    determiners = [encode(w) for w in DETERMINER_TABLE if w not in PRONOUN_TABLE]
    classes = {class_of(d) for d in determiners}
    ok(classes == {CLASS_DETERMINER},
       f"all determiners map to class {CLASS_DETERMINER} (got {classes})")


def test_across_class_distinguishable():
    banner("Test 4 — different classes produce different objects")
    samples = {
        CLASS_PRONOUN:        encode("i"),
        CLASS_DETERMINER:     encode("the"),
        CLASS_PREPOSITION:    encode("in"),
        CLASS_CONJUNCTION:    encode("and"),
        CLASS_AUXILIARY:      encode("is"),
        CLASS_PARTICLE:       encode("not"),
        CLASS_INTERJECTION:   encode("yes"),
        CLASS_WHITESPACE:     encode(" "),
        CLASS_PUNCT_TERMINAL: encode("."),
        CLASS_PUNCT_JUNCTURE: encode(","),
        CLASS_PUNCT_OPEN:     encode("("),
        CLASS_PUNCT_CLOSE:    encode(")"),
        CLASS_PUNCT_AFFIX:    encode("-"),
        CLASS_PUNCT_MODAL:    encode("..."),
        CLASS_NUMERAL:        encode("3"),
    }
    classes = [class_of(obj) for obj in samples.values()]
    ok(len(set(classes)) == len(samples),
       f"all 15 sampled classes are distinct (got {classes})")


def test_pronoun_feature_difference():
    banner("Test 5 — pronoun gender encoded in payload")
    he = encode("he")
    she = encode("she")
    ok(class_of(he) == class_of(she) == CLASS_PRONOUN,
       "'he' and 'she' both pronouns")
    ok(not he.equivalent(she),
       "'he' ≠ 'she' (gender difference encoded)")
    he_payload = feature_payload_of(he)
    she_payload = feature_payload_of(she)
    ok(he_payload is not None and she_payload is not None,
       "both have non-trivial feature payloads")
    ok(not he_payload.equivalent(she_payload),
       "'he' and 'she' payloads differ")


def test_determiner_feature_difference():
    banner("Test 6 — determiner definiteness encoded")
    the = encode("the")
    a = encode("a")
    ok(class_of(the) == class_of(a) == CLASS_DETERMINER,
       "'the' and 'a' both determiners")
    ok(not the.equivalent(a),
       "'the' ≠ 'a' (definiteness difference)")


def test_pairing_distinct():
    banner("Test 7 — pairing marks: opens distinct from each other and from closes")
    opens = [encode(c) for c in ["(", "[", "{", "“", "‘"]]
    closes = [encode(c) for c in [")", "]", "}", "”", "’"]]
    # All opens are class PUNCT_OPEN.
    open_classes = {class_of(o) for o in opens}
    ok(open_classes == {CLASS_PUNCT_OPEN},
       f"all open marks in PUNCT_OPEN class (got {open_classes})")
    close_classes = {class_of(c) for c in closes}
    ok(close_classes == {CLASS_PUNCT_CLOSE},
       f"all close marks in PUNCT_CLOSE class (got {close_classes})")
    # Within opens, all 5 distinct.
    open_distinct = all(
        not opens[i].equivalent(opens[j])
        for i in range(len(opens)) for j in range(i+1, len(opens))
    )
    ok(open_distinct, "all 5 open marks pairwise distinct")
    close_distinct = all(
        not closes[i].equivalent(closes[j])
        for i in range(len(closes)) for j in range(i+1, len(closes))
    )
    ok(close_distinct, "all 5 close marks pairwise distinct")


def test_whitespace_varieties():
    banner("Test 8 — whitespace kinds distinguishable")
    space = encode(" ")
    tab = encode("\t")
    newline = encode("\n")
    nbsp = encode(" ")
    ok(not space.equivalent(tab), "space ≠ tab")
    ok(not space.equivalent(newline), "space ≠ newline")
    ok(not space.equivalent(nbsp), "space ≠ NBSP")
    ok(not tab.equivalent(newline), "tab ≠ newline")
    ok(class_of(space) == class_of(tab) == class_of(newline) == CLASS_WHITESPACE,
       "all whitespace kinds in WHITESPACE class")


def test_numeral_forms():
    banner("Test 9 — numeral digit and spelled forms distinguishable")
    three_digit = encode("3")
    three_word = encode("three")
    ok(class_of(three_digit) == class_of(three_word) == CLASS_NUMERAL,
       "both numerals")
    ok(not three_digit.equivalent(three_word),
       "'3' ≠ 'three' (form difference)")
    # Different values distinguishable.
    five_digit = encode("5")
    ok(not three_digit.equivalent(five_digit), "'3' ≠ '5'")


def test_full_vocabulary_uniqueness():
    banner("Test 10 — every token (modulo phonetic variants) encodes uniquely")
    # Known phonetic variants — share encoding by design.
    PHONETIC_VARIANTS = {("a", "an"), ("an", "a")}

    seen = []
    duplicates = []
    for token in DISPATCH:
        obj = encode(token)
        found = False
        for prior_token, prior_obj in seen:
            if obj.equivalent(prior_obj):
                pair = tuple(sorted([prior_token, token]))
                # Allow only documented phonetic variants.
                if pair not in PHONETIC_VARIANTS and (pair[0], pair[1]) not in PHONETIC_VARIANTS:
                    if (prior_token, token) not in PHONETIC_VARIANTS:
                        duplicates.append((prior_token, token))
                found = True
                break
        if not found:
            seen.append((token, obj))
    if duplicates:
        for a, b in duplicates[:10]:
            print(f"    {a!r} ≡ {b!r}")
    ok(not duplicates,
       f"all {len(DISPATCH)} tokens encode uniquely (modulo variants); "
       f"{len(duplicates)} unexpected collisions")


def test_unknown_token():
    banner("Test 11 — unknown (open-class) tokens return None")
    ok(encode("dog") is None, "'dog' (open-class noun) returns None")
    ok(encode("running") is None, "'running' (open-class verb) returns None")
    ok(encode("xyzzy") is None, "nonsense token returns None")
    ok(encode("") is None, "empty string returns None")


def test_case_insensitivity_for_words():
    banner("Test 12 — word lookup is case-insensitive")
    ok(encode("THE").equivalent(encode("the")), "'THE' = 'the'")
    ok(encode("The").equivalent(encode("the")), "'The' = 'the'")
    ok(encode("I").equivalent(encode("i")), "'I' = 'i'")


def main():
    test_all_tokens_encode()
    test_class_recovery()
    test_within_class_share_class_anchor()
    test_across_class_distinguishable()
    test_pronoun_feature_difference()
    test_determiner_feature_difference()
    test_pairing_distinct()
    test_whitespace_varieties()
    test_numeral_forms()
    test_full_vocabulary_uniqueness()
    test_unknown_token()
    test_case_insensitivity_for_words()
    print("\n" + "=" * 72)
    print("All edcmbone closed-token tests passed.")
    print("=" * 72)


if __name__ == "__main__":
    main()
