"""
edcmbone — Closed-Token UCNS Encoder

Maps the closed classes of English (pronouns, determiners, prepositions,
conjunctions, auxiliaries, particles, interjections), whitespace, punctuation,
and small numerals to UCNS objects on a 16-gonal host carrier.

Class partition (host anchor index → class):
   0: pronoun
   1: determiner
   2: preposition
   3: conjunction
   4: auxiliary verb
   5: particle / catch-all
   6: interjection
   7: whitespace
   8: punctuation — sentence terminal
   9: punctuation — internal juncture
  10: punctuation — pairing open
  11: punctuation — pairing close
  12: punctuation — quote (smart open/close handled in pairing classes)
  13: punctuation — affix / connective
  14: punctuation — modal (ellipsis)
  15: numeral

Each token encodes as a UCNSObject with:
  - host length 1 (a single anchor at the class's position on the 16-gonal lattice)
  - payload encoding the per-class features (person/number/case for pronouns, etc.)
  - face bit unused at the host level (set to 0)

The pairing-mark rule: smart open quote and curly open brackets go in class 10;
their close counterparts in class 11. The disk-flip of an open-mark UCNS
object equals the close-mark object (verified by test).
"""

# === MODULE_BUILD ===
# id: edcmbone_ucns_closed_tokens
#   module_name: closed_tokens
#   module_kind: adapter
#   summary: encodes English closed-class tokens, whitespace, punctuation, and small numerals to UCNS objects on a 16-gon host carrier
#   owner: Erin Spencer
#   public_surface: encode, class_of, feature_payload_of
#   internal_surface: _class_anchor, _wrap_with_class, _feature_payload, _build_dispatch_table
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_closed_tokens
#   rollout: default_enabled
#   rollback: remove module; closed-token UCNS encoding unavailable
#   requires: edcmbone_ucns_v04
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

from .ucns_v04 import (
    UCNSObject, AnchorPayload,
    unit_obj, multiply,
)


# ---------- class indices ----------

CLASS_PRONOUN     = 0
CLASS_DETERMINER  = 1
CLASS_PREPOSITION = 2
CLASS_CONJUNCTION = 3
CLASS_AUXILIARY   = 4
CLASS_PARTICLE    = 5
CLASS_INTERJECTION = 6
CLASS_WHITESPACE  = 7
CLASS_PUNCT_TERMINAL = 8
CLASS_PUNCT_JUNCTURE = 9
CLASS_PUNCT_OPEN     = 10
CLASS_PUNCT_CLOSE    = 11
CLASS_PUNCT_QUOTE    = 12   # reserved; quote glyphs are routed to OPEN/CLOSE
CLASS_PUNCT_AFFIX    = 13
CLASS_PUNCT_MODAL    = 14
CLASS_NUMERAL        = 15

CLASS_NAMES = {
    0:  "pronoun", 1:  "determiner", 2:  "preposition", 3:  "conjunction",
    4:  "auxiliary", 5:  "particle", 6:  "interjection", 7:  "whitespace",
    8:  "punct.terminal", 9:  "punct.juncture", 10: "punct.open",
    11: "punct.close", 12: "punct.quote", 13: "punct.affix",
    14: "punct.modal", 15: "numeral",
}

HOST_CARRIER = 16  # 16-gonal lattice for the host class anchor


# ---------- helpers ----------

def _class_anchor(class_idx: int) -> Fraction:
    """Anchor position on the 16-gonal lattice (in turns)."""
    return Fraction(class_idx, HOST_CARRIER)


def _wrap_with_class(class_idx: int, payload: Optional[UCNSObject]) -> UCNSObject:
    """
    Encode class and feature payload as a 2-anchor object on a 32-gonal lattice.

    Anchor 0: at position 0 (structural marker, no payload).
    Anchor 1: at position (class_idx + 1) / 32, carrying the feature payload.

    After normalize, the first anchor stays at 0 (it's already there), and
    the second stays at (class_idx + 1) / 32 — a relative offset that
    encodes the class index uniquely for class_idx ∈ {0..15}.
    """
    class_offset = Fraction(class_idx + 1, 32)
    return UCNSObject(
        n_dec=32,
        n_min=1,  # normalize will recompute
        anchors_pos=(
            AnchorPayload(Fraction(0), None),
            AnchorPayload(class_offset, payload),
        ),
        faces_pos=(0, 0),
    ).normalize()


def _feature_payload(feature_dict: Dict[str, Tuple[int, int]]) -> Optional[UCNSObject]:
    """
    Build a feature payload from a dict of {feature_name: (value_index, modulus)}.

    Encoding: features sorted lexicographically. Each feature contributes one
    anchor at position (value_idx + 1) / (modulus + 1) on the payload's host
    carrier — the +1 offset prevents value_idx=0 from landing at position 0,
    which would collapse to the unit object under normalization.

    Plus one structural marker anchor at position 0 so the relative anchor
    positions survive normalization unchanged.

    For empty feature dicts, return None (the unit/no-payload).
    """
    if not feature_dict:
        return None

    from math import gcd
    def _lcm(a, b):
        return a * b // gcd(a, b) if a and b else max(a, b)
    moduli = [m + 1 for _, m in feature_dict.values()]  # +1 to host the offset
    carrier = 1
    for m in moduli:
        carrier = _lcm(carrier, m)

    names_sorted = sorted(feature_dict.keys())
    # First anchor: structural marker at 0.
    anchors = [AnchorPayload(Fraction(0), None)]
    # Subsequent anchors: one per feature, at (value_idx + 1) / (modulus + 1).
    for name in names_sorted:
        value_idx, modulus = feature_dict[name]
        anchor = Fraction(value_idx + 1, modulus + 1)
        anchors.append(AnchorPayload(anchor, None))

    return UCNSObject(
        n_dec=carrier,
        n_min=1,
        anchors_pos=tuple(anchors),
        faces_pos=tuple([0] * len(anchors)),
    ).normalize()


# ---------- pronoun encoding ----------

# Person: 1=first, 2=second, 3=third  (modulus 3)
# Number: singular=0, plural=1        (modulus 2)
# Case:   sub=0, obj=1, poss_det=2, poss_pro=3, refl=4   (modulus 5)
# Gender: m=0, f=1, n=2, na=3         (modulus 4)

PRONOUN_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {
    # First person
    "i":        {"person": (0,3), "number": (0,2), "case": (0,5), "gender": (3,4)},
    "me":       {"person": (0,3), "number": (0,2), "case": (1,5), "gender": (3,4)},
    "my":       {"person": (0,3), "number": (0,2), "case": (2,5), "gender": (3,4)},
    "mine":     {"person": (0,3), "number": (0,2), "case": (3,5), "gender": (3,4)},
    "myself":   {"person": (0,3), "number": (0,2), "case": (4,5), "gender": (3,4)},
    "we":       {"person": (0,3), "number": (1,2), "case": (0,5), "gender": (3,4)},
    "us":       {"person": (0,3), "number": (1,2), "case": (1,5), "gender": (3,4)},
    "our":      {"person": (0,3), "number": (1,2), "case": (2,5), "gender": (3,4)},
    "ours":     {"person": (0,3), "number": (1,2), "case": (3,5), "gender": (3,4)},
    "ourselves":{"person": (0,3), "number": (1,2), "case": (4,5), "gender": (3,4)},
    # Second person (no English number distinction)
    "you":      {"person": (1,3), "number": (0,2), "case": (0,5), "gender": (3,4)},
    "your":     {"person": (1,3), "number": (0,2), "case": (2,5), "gender": (3,4)},
    "yours":    {"person": (1,3), "number": (0,2), "case": (3,5), "gender": (3,4)},
    "yourself": {"person": (1,3), "number": (0,2), "case": (4,5), "gender": (3,4)},
    "yourselves":{"person": (1,3), "number": (1,2), "case": (4,5), "gender": (3,4)},
    # Third person
    "he":       {"person": (2,3), "number": (0,2), "case": (0,5), "gender": (0,4)},
    "him":      {"person": (2,3), "number": (0,2), "case": (1,5), "gender": (0,4)},
    "his":      {"person": (2,3), "number": (0,2), "case": (2,5), "gender": (0,4)},
    "himself":  {"person": (2,3), "number": (0,2), "case": (4,5), "gender": (0,4)},
    "she":      {"person": (2,3), "number": (0,2), "case": (0,5), "gender": (1,4)},
    "her":      {"person": (2,3), "number": (0,2), "case": (1,5), "gender": (1,4)},
    "hers":     {"person": (2,3), "number": (0,2), "case": (3,5), "gender": (1,4)},
    "herself":  {"person": (2,3), "number": (0,2), "case": (4,5), "gender": (1,4)},
    "it":       {"person": (2,3), "number": (0,2), "case": (0,5), "gender": (2,4)},
    "its":      {"person": (2,3), "number": (0,2), "case": (2,5), "gender": (2,4)},
    "itself":   {"person": (2,3), "number": (0,2), "case": (4,5), "gender": (2,4)},
    "they":     {"person": (2,3), "number": (1,2), "case": (0,5), "gender": (3,4)},
    "them":     {"person": (2,3), "number": (1,2), "case": (1,5), "gender": (3,4)},
    "their":    {"person": (2,3), "number": (1,2), "case": (2,5), "gender": (3,4)},
    "theirs":   {"person": (2,3), "number": (1,2), "case": (3,5), "gender": (3,4)},
    "themselves":{"person": (2,3),"number": (1,2), "case": (4,5), "gender": (3,4)},
}


# ---------- determiner encoding ----------

# Definiteness: def=0, indef=1, demo=2, poss=3, quant=4, neg=5  (modulus 6)
# Number:       sg=0, pl=1, mass=2, both=3                       (modulus 4)
# Distance:     prox=0, distal=1, neutral=2                      (modulus 3)

DETERMINER_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {
    "the":   {"definiteness": (0,6), "number": (3,4), "distance": (2,3)},
    "a":     {"definiteness": (1,6), "number": (0,4), "distance": (2,3)},
    "an":    {"definiteness": (1,6), "number": (0,4), "distance": (2,3)},
    "some":  {"definiteness": (4,6), "number": (3,4), "distance": (2,3)},
    "any":   {"definiteness": (4,6), "number": (3,4), "distance": (2,3)},
    "no":    {"definiteness": (5,6), "number": (3,4), "distance": (2,3)},
    "every": {"definiteness": (4,6), "number": (0,4), "distance": (2,3)},
    "each":  {"definiteness": (4,6), "number": (0,4), "distance": (2,3)},
    "all":   {"definiteness": (4,6), "number": (3,4), "distance": (2,3)},
    "both":  {"definiteness": (4,6), "number": (1,4), "distance": (2,3)},
    "either":{"definiteness": (4,6), "number": (0,4), "distance": (2,3)},
    "neither":{"definiteness":(5,6), "number": (0,4), "distance": (2,3)},
    "few":   {"definiteness": (4,6), "number": (1,4), "distance": (2,3)},
    "several":{"definiteness":(4,6), "number": (1,4), "distance": (2,3)},
    "many":  {"definiteness": (4,6), "number": (1,4), "distance": (2,3)},
    "much":  {"definiteness": (4,6), "number": (2,4), "distance": (2,3)},
    "more":  {"definiteness": (4,6), "number": (3,4), "distance": (2,3)},
    "most":  {"definiteness": (4,6), "number": (3,4), "distance": (2,3)},
    "less":  {"definiteness": (4,6), "number": (2,4), "distance": (2,3)},
    "this":  {"definiteness": (2,6), "number": (0,4), "distance": (0,3)},
    "that":  {"definiteness": (2,6), "number": (0,4), "distance": (1,3)},
    "these": {"definiteness": (2,6), "number": (1,4), "distance": (0,3)},
    "those": {"definiteness": (2,6), "number": (1,4), "distance": (1,3)},
}


# ---------- preposition encoding ----------

# Domain: spatial=0, temporal=1, logical=2, other=3      (modulus 4)
# Direction: toward=0, away=1, neutral=2                  (modulus 3)
# Containment (for spatial): inside=0, outside=1, surface=2, edge=3, none=4 (modulus 5)

PREPOSITION_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {
    # Spatial
    "in":      {"domain": (0,4), "direction": (2,3), "containment": (0,5)},
    "on":      {"domain": (0,4), "direction": (2,3), "containment": (2,5)},
    "at":      {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    "to":      {"domain": (0,4), "direction": (0,3), "containment": (4,5)},
    "from":    {"domain": (0,4), "direction": (1,3), "containment": (4,5)},
    "into":    {"domain": (0,4), "direction": (0,3), "containment": (0,5)},
    "onto":    {"domain": (0,4), "direction": (0,3), "containment": (2,5)},
    "out":     {"domain": (0,4), "direction": (1,3), "containment": (1,5)},
    "of":      {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "by":      {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    "with":    {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "without": {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "for":     {"domain": (2,4), "direction": (0,3), "containment": (4,5)},
    "above":   {"domain": (0,4), "direction": (2,3), "containment": (1,5)},
    "below":   {"domain": (0,4), "direction": (2,3), "containment": (1,5)},
    "under":   {"domain": (0,4), "direction": (2,3), "containment": (1,5)},
    "over":    {"domain": (0,4), "direction": (2,3), "containment": (1,5)},
    "between": {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    "through": {"domain": (0,4), "direction": (0,3), "containment": (0,5)},
    "across":  {"domain": (0,4), "direction": (0,3), "containment": (2,5)},
    "against": {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    "around":  {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    "near":    {"domain": (0,4), "direction": (2,3), "containment": (3,5)},
    # Temporal
    "before":  {"domain": (1,4), "direction": (1,3), "containment": (4,5)},
    "after":   {"domain": (1,4), "direction": (0,3), "containment": (4,5)},
    "during":  {"domain": (1,4), "direction": (2,3), "containment": (0,5)},
    "since":   {"domain": (1,4), "direction": (1,3), "containment": (4,5)},
    "until":   {"domain": (1,4), "direction": (0,3), "containment": (4,5)},
    # Logical
    "about":   {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "as":      {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "than":    {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "like":    {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
    "despite": {"domain": (2,4), "direction": (2,3), "containment": (4,5)},
}


# ---------- conjunction encoding ----------

# Type: coord=0, sub=1, correl=2, other=3                  (modulus 4)
# Polarity: pos=0, neg=1, neutral=2                        (modulus 3)
# Relation: addition=0, contrast=1, cause=2, condition=3, time=4, choice=5, neutral=6 (modulus 7)

CONJUNCTION_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {
    # Coordinating
    "and":      {"type": (0,4), "polarity": (0,3), "relation": (0,7)},
    "or":       {"type": (0,4), "polarity": (2,3), "relation": (5,7)},
    "but":      {"type": (0,4), "polarity": (1,3), "relation": (1,7)},
    "nor":      {"type": (0,4), "polarity": (1,3), "relation": (5,7)},
    "so":       {"type": (0,4), "polarity": (0,3), "relation": (2,7)},
    "yet":      {"type": (0,4), "polarity": (1,3), "relation": (1,7)},
    # Subordinating
    "because":  {"type": (1,4), "polarity": (0,3), "relation": (2,7)},
    "since":    {"type": (1,4), "polarity": (0,3), "relation": (2,7)},
    "although": {"type": (1,4), "polarity": (1,3), "relation": (1,7)},
    "though":   {"type": (1,4), "polarity": (1,3), "relation": (1,7)},
    "while":    {"type": (1,4), "polarity": (2,3), "relation": (4,7)},
    "when":     {"type": (1,4), "polarity": (2,3), "relation": (4,7)},
    "if":       {"type": (1,4), "polarity": (0,3), "relation": (3,7)},
    "unless":   {"type": (1,4), "polarity": (1,3), "relation": (3,7)},
    "whether":  {"type": (1,4), "polarity": (2,3), "relation": (5,7)},
    "until":    {"type": (1,4), "polarity": (2,3), "relation": (4,7)},
    "as":       {"type": (1,4), "polarity": (2,3), "relation": (4,7)},
    "that":     {"type": (1,4), "polarity": (2,3), "relation": (6,7)},
}


# ---------- auxiliary encoding ----------

# Tense: pres=0, past=1, fut=2, base=3                                  (modulus 4)
# Number: sg=0, pl=1, both=2                                            (modulus 3)
# Modality: ind=0, modal_pos=1, modal_oblig=2, modal_perm=3, modal_cond=4, perfective=5, progressive=6 (modulus 7)

AUXILIARY_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {
    "be":      {"tense": (3,4), "number": (2,3), "modality": (0,7)},
    "am":      {"tense": (0,4), "number": (0,3), "modality": (0,7)},
    "is":      {"tense": (0,4), "number": (0,3), "modality": (0,7)},
    "are":     {"tense": (0,4), "number": (1,3), "modality": (0,7)},
    "was":     {"tense": (1,4), "number": (0,3), "modality": (0,7)},
    "were":    {"tense": (1,4), "number": (1,3), "modality": (0,7)},
    "been":    {"tense": (1,4), "number": (2,3), "modality": (5,7)},
    "being":   {"tense": (0,4), "number": (2,3), "modality": (6,7)},
    "have":    {"tense": (0,4), "number": (2,3), "modality": (5,7)},
    "has":     {"tense": (0,4), "number": (0,3), "modality": (5,7)},
    "had":     {"tense": (1,4), "number": (2,3), "modality": (5,7)},
    "having":  {"tense": (0,4), "number": (2,3), "modality": (5,7)},
    "do":      {"tense": (0,4), "number": (1,3), "modality": (0,7)},
    "does":    {"tense": (0,4), "number": (0,3), "modality": (0,7)},
    "did":     {"tense": (1,4), "number": (2,3), "modality": (0,7)},
    "will":    {"tense": (2,4), "number": (2,3), "modality": (1,7)},
    "would":   {"tense": (1,4), "number": (2,3), "modality": (4,7)},
    "shall":   {"tense": (2,4), "number": (2,3), "modality": (1,7)},
    "should":  {"tense": (1,4), "number": (2,3), "modality": (2,7)},
    "can":     {"tense": (0,4), "number": (2,3), "modality": (3,7)},
    "could":   {"tense": (1,4), "number": (2,3), "modality": (4,7)},
    "may":     {"tense": (0,4), "number": (2,3), "modality": (3,7)},
    "might":   {"tense": (1,4), "number": (2,3), "modality": (4,7)},
    "must":    {"tense": (0,4), "number": (2,3), "modality": (2,7)},
    "ought":   {"tense": (0,4), "number": (2,3), "modality": (2,7)},
}


# ---------- particle, interjection ----------
# Stored as bare class anchors with a small distinguishing index payload.

PARTICLE_LIST = [
    "not", "to", "up", "down", "off", "out", "in", "on", "over", "back",
    "away", "around", "along", "apart", "together", "across",
]

INTERJECTION_LIST = [
    "yes", "no", "oh", "ah", "ouch", "wow", "hi", "hello", "hey", "bye",
    "okay", "ok", "well", "please", "thanks",
]


# ---------- whitespace, punctuation, numerals ----------

# Whitespace: kind 0=space, 1=tab, 2=newline, 3=double-newline, 4=non-breaking
WHITESPACE_TABLE = {
    " ":   {"kind": (0, 5), "breaking": (0, 2)},
    "\t":  {"kind": (1, 5), "breaking": (0, 2)},
    "\n":  {"kind": (2, 5), "breaking": (0, 2)},
    "\n\n":{"kind": (3, 5), "breaking": (0, 2)},
    " ": {"kind": (4, 5), "breaking": (1, 2)},  # NBSP
}

# Sentence terminals (modality)
TERMINAL_TABLE = {
    ".": {"modality": (0, 3)},   # declarative
    "?": {"modality": (1, 3)},   # interrogative
    "!": {"modality": (2, 3)},   # exclamatory
}

# Internal junctures (binding strength)
JUNCTURE_TABLE = {
    ",": {"binding": (0, 3)},    # weakest
    ";": {"binding": (1, 3)},    # medium
    ":": {"binding": (2, 3)},    # strongest internal
}

# Pairing marks. Smart quotes use Unicode left/right curly forms.
# Each gets a "shape" feature (paren=0, square=1, curly=2, dquote=3, squote=4)
PAIR_OPEN_TABLE = {
    "(": {"shape": (0, 5)},
    "[": {"shape": (1, 5)},
    "{": {"shape": (2, 5)},
    "“": {"shape": (3, 5)},  # "
    "‘": {"shape": (4, 5)},  # '
}
PAIR_CLOSE_TABLE = {
    ")": {"shape": (0, 5)},
    "]": {"shape": (1, 5)},
    "}": {"shape": (2, 5)},
    "”": {"shape": (3, 5)},  # "
    "’": {"shape": (4, 5)},  # '
}

# Affix and connective marks
AFFIX_TABLE = {
    "'": {"kind": (0, 4)},   # ASCII apostrophe (possessive/contraction)
    "-": {"kind": (1, 4)},   # hyphen
    "–": {"kind": (2, 4)},  # en-dash
    "—": {"kind": (3, 4)},  # em-dash
}

# Modal punctuation
MODAL_PUNCT_TABLE = {
    "...": {"kind": (0, 2)},
    "…": {"kind": (0, 2)},  # ellipsis char
}

# Numerals: digits 0-9 and small spelled forms.
NUMERAL_TABLE: Dict[str, Dict[str, Tuple[int, int]]] = {}
for i, digit in enumerate("0123456789"):
    NUMERAL_TABLE[digit] = {"value": (i, 10), "form": (0, 2)}  # digit form
SPELLED_NUMERALS = ["zero", "one", "two", "three", "four", "five",
                    "six", "seven", "eight", "nine"]
for i, word in enumerate(SPELLED_NUMERALS):
    NUMERAL_TABLE[word] = {"value": (i, 10), "form": (1, 2)}  # spelled form


# ---------- master encode / decode ----------

def _build_dispatch_table():
    """Build the master {token: (class_idx, feature_dict)} table.

    For tokens that share identical feature dicts (e.g. 'every' and 'each'),
    we add a 'lemma_id' feature to keep their UCNS encodings distinct.

    Phonetic variants ('a' / 'an') are canonically merged: both produce the
    same UCNS object since they differ only in surface phonology.
    """
    PHONETIC_VARIANTS = {"an": "a"}  # an → a as canonical encoding

    out: Dict[str, Tuple[int, Dict[str, Tuple[int, int]]]] = {}

    def add(token, class_idx, feats):
        if token in PHONETIC_VARIANTS:
            # Skip — variant will be aliased after the canonical is in place.
            return
        if token in out:
            return  # earlier class entry wins
        out[token] = (class_idx, feats)

    for w, feats in PRONOUN_TABLE.items():
        add(w, CLASS_PRONOUN, feats)
    for w, feats in DETERMINER_TABLE.items():
        add(w, CLASS_DETERMINER, feats)
    for w, feats in PREPOSITION_TABLE.items():
        add(w, CLASS_PREPOSITION, feats)
    for w, feats in CONJUNCTION_TABLE.items():
        add(w, CLASS_CONJUNCTION, feats)
    for w, feats in AUXILIARY_TABLE.items():
        add(w, CLASS_AUXILIARY, feats)
    for i, w in enumerate(PARTICLE_LIST):
        add(w, CLASS_PARTICLE, {"idx": (i, max(len(PARTICLE_LIST), 1))})
    for i, w in enumerate(INTERJECTION_LIST):
        add(w, CLASS_INTERJECTION, {"idx": (i, max(len(INTERJECTION_LIST), 1))})
    for w, feats in WHITESPACE_TABLE.items():
        add(w, CLASS_WHITESPACE, feats)
    for w, feats in TERMINAL_TABLE.items():
        add(w, CLASS_PUNCT_TERMINAL, feats)
    for w, feats in JUNCTURE_TABLE.items():
        add(w, CLASS_PUNCT_JUNCTURE, feats)
    for w, feats in PAIR_OPEN_TABLE.items():
        add(w, CLASS_PUNCT_OPEN, feats)
    for w, feats in PAIR_CLOSE_TABLE.items():
        add(w, CLASS_PUNCT_CLOSE, feats)
    for w, feats in AFFIX_TABLE.items():
        add(w, CLASS_PUNCT_AFFIX, feats)
    for w, feats in MODAL_PUNCT_TABLE.items():
        add(w, CLASS_PUNCT_MODAL, feats)
    for w, feats in NUMERAL_TABLE.items():
        add(w, CLASS_NUMERAL, feats)

    # Add lemma_id disambiguator for structurally-duplicate tokens.
    # Group tokens by (class_idx, frozenset(feats.items())) and assign
    # lemma_id = 0, 1, 2... within each duplicate group.
    from collections import defaultdict
    groups = defaultdict(list)
    for token, (class_idx, feats) in out.items():
        key = (class_idx, frozenset(feats.items()))
        groups[key].append(token)

    for key, tokens in groups.items():
        if len(tokens) > 1:
            # Assign lemma_id based on alphabetical order for determinism.
            tokens_sorted = sorted(tokens)
            for lemma_id, token in enumerate(tokens_sorted):
                class_idx, feats = out[token]
                new_feats = dict(feats)
                new_feats["lemma_id"] = (lemma_id, max(len(tokens), 2))
                out[token] = (class_idx, new_feats)

    # Phonetic variants alias to canonical.
    for variant, canonical in PHONETIC_VARIANTS.items():
        if canonical in out:
            out[variant] = out[canonical]

    return out


DISPATCH: Dict[str, Tuple[int, Dict[str, Tuple[int, int]]]] = _build_dispatch_table()


def encode(token: str) -> Optional[UCNSObject]:
    """
    Encode a closed-class token into a UCNS object. Returns None if the
    token is not in any closed class (caller should treat as open-class).
    Lookup is case-insensitive for words; punctuation is case-preserving.
    """
    if not token:
        return None

    # Case-insensitive lookup for word tokens; case-sensitive for punctuation.
    key = token if not token.isalpha() else token.lower()
    entry = DISPATCH.get(key)
    if entry is None:
        return None

    class_idx, features = entry
    payload = _feature_payload(features)
    return _wrap_with_class(class_idx, payload)


def class_of(obj: UCNSObject) -> Optional[int]:
    """
    Return the class index of an encoded token, or None if the object
    doesn't fit the closed-token encoding shape.
    """
    obj = obj.normalize()
    if len(obj.anchors_pos) != 2:
        return None
    if obj.anchors_pos[0].theta != 0:
        return None
    if obj.anchors_pos[0].payload is not None:
        return None
    # Second anchor's theta is (class_idx + 1) / 32 by construction.
    second_theta = obj.anchors_pos[1].theta
    expected_denominator_factor = 32
    # Reconstruct class_idx: theta * 32 - 1.
    # Use exact rational arithmetic: theta = (k+1)/32 → k = theta*32 - 1.
    candidate = second_theta * expected_denominator_factor - 1
    if candidate.denominator != 1:
        return None
    class_idx = int(candidate.numerator)
    if 0 <= class_idx < HOST_CARRIER:
        return class_idx
    return None


def feature_payload_of(obj: UCNSObject) -> Optional[UCNSObject]:
    """Return the feature payload (the second anchor's payload), or None."""
    obj = obj.normalize()
    if len(obj.anchors_pos) != 2:
        return None
    return obj.anchors_pos[1].payload
