"""English surface rendering over the scale-neutral gonol composition.

Rendering is evidence, not permission. Every affix/root composition exists before
English orthography chooses a familiar spelling. Consequently every renderer
returns the literal concatenation as well as all codified conventional variants.
"""

# === MODULE_BUILD ===
# id: edcm_language_rendering
#   module_name: rendering
#   module_kind: engine
#   summary: codifies reversible English orthographic and compounding transformations without using them as composition gates
#   owner: Erin Spencer
#   public_surface: TransformationRule, transformation_inventory, render_affix_candidates, inverse_affix_candidates, compound_candidates, normalize_lemma
#   internal_surface: _is_cvc, _ordered_unique
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_full_run
#   rollout: default_enabled
#   rollback: restore the prior renderer version and regenerate all molecular artifacts
#   requires: edcm_language_affixes
#   since: 2026-07-13
#   unresolved: pronunciation rendering remains outside this first complete written-English run
# === END MODULE_BUILD ===

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
import unicodedata
from typing import Iterable

from .affixes import AffixRecord


@dataclass(frozen=True, slots=True)
class TransformationRule:
    rule_id: str
    name: str
    direction: str
    description: str
    universal_validity: bool = True


_RULES = (
    TransformationRule(
        "literal-concatenation",
        "literal concatenation",
        "bidirectional",
        "Affix and base surfaces are joined without rejecting any combination.",
    ),
    TransformationRule(
        "prefix-hyphen-optional",
        "prefix hyphen optionality",
        "bidirectional",
        "A prefix may render joined or hyphenated; convention selects among valid surfaces.",
    ),
    TransformationRule(
        "suffix-hyphen-optional",
        "suffix hyphen optionality",
        "bidirectional",
        "A suffix may render joined or hyphenated; convention selects among valid surfaces.",
    ),
    TransformationRule(
        "silent-e-deletion",
        "silent e deletion",
        "bidirectional",
        "Final e may be deleted before a vowel-initial suffix.",
    ),
    TransformationRule(
        "y-to-i",
        "final y to i",
        "bidirectional",
        "Consonant+y may become i before a suffix other than -ing.",
    ),
    TransformationRule(
        "ie-to-y-before-ing",
        "final ie to y before ing",
        "bidirectional",
        "Final ie may become y before -ing.",
    ),
    TransformationRule(
        "final-consonant-doubling",
        "final consonant doubling",
        "bidirectional",
        "A final consonant in a CVC base may double before a vowel-initial suffix.",
    ),
    TransformationRule(
        "f-fe-to-v",
        "f or fe to v",
        "bidirectional",
        "Final f or fe may become v before plural or related suffixes.",
    ),
    TransformationRule(
        "sibilant-es",
        "sibilant es realization",
        "bidirectional",
        "Plural or third-person s may surface as es after a sibilant ending.",
    ),
    TransformationRule(
        "apostrophe-clitic",
        "apostrophe clitic attachment",
        "bidirectional",
        "Contraction morphemes attach to the host while retaining their apostrophe.",
    ),
    TransformationRule(
        "compound-spacing",
        "compound spacing",
        "bidirectional",
        "Constituents may render with a space, hyphen, or closed adjacency.",
    ),
    TransformationRule(
        "case-fold",
        "Unicode normalization and case fold",
        "input-normalization",
        "Dictionary matching uses NFC Unicode and casefold while original surfaces remain metadata.",
    ),
)

_VOWELS = frozenset("aeiou")
_SIBILANT_ENDINGS = ("s", "x", "z", "ch", "sh", "o")


def transformation_inventory() -> dict[str, object]:
    return {
        "schema": "edcm.english-rendering-transformations",
        "version": "1.0.0",
        "composition_restrictions": False,
        "rules": [asdict(rule) for rule in _RULES],
    }


def normalize_lemma(value: str) -> str:
    """Canonical dictionary matching surface, not an intrinsic gonol label."""

    return unicodedata.normalize("NFC", value).replace("_", " ").strip().casefold()


def _ordered_unique(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = normalize_lemma(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            out.append(normalized)
    return tuple(out)


def _is_cvc(base: str) -> bool:
    letters = re.sub(r"[^a-z]", "", base)
    if len(letters) < 3:
        return False
    a, b, c = letters[-3:]
    return a not in _VOWELS and b in _VOWELS and c not in _VOWELS and c not in "wxy"


def render_affix_candidates(base: str, affix: AffixRecord) -> tuple[str, ...]:
    """Return every codified rendering, always including literal composition."""

    base = normalize_lemma(base)
    token = normalize_lemma(affix.bare)
    values: list[str] = []

    if affix.kind == "prefix":
        values.extend((token + base, token + "-" + base))
    elif affix.kind == "suffix":
        values.extend((base + token, base + "-" + token))
        vowel_initial = bool(token) and token[0] in _VOWELS
        if base.endswith("e") and vowel_initial:
            values.append(base[:-1] + token)
        if base.endswith("ie") and token == "ing":
            values.append(base[:-2] + "y" + token)
        if len(base) > 1 and base.endswith("y") and base[-2] not in _VOWELS and token != "ing":
            values.append(base[:-1] + "i" + token)
        if vowel_initial and _is_cvc(base):
            values.append(base + base[-1] + token)
        if token in {"s", "es"}:
            if base.endswith(_SIBILANT_ENDINGS):
                values.append(base + "es")
            if base.endswith("y") and len(base) > 1 and base[-2] not in _VOWELS:
                values.append(base[:-1] + "ies")
            if base.endswith("fe"):
                values.append(base[:-2] + "ves")
            elif base.endswith("f"):
                values.append(base[:-1] + "ves")
        if token == "ed" and base.endswith("y") and len(base) > 1 and base[-2] not in _VOWELS:
            values.append(base[:-1] + "ied")
    elif affix.kind == "contraction":
        values.append(base + token)
    else:
        values.extend((base + token, token + base))

    return _ordered_unique(values)


def inverse_affix_candidates(surface: str, affix: AffixRecord) -> tuple[str, ...]:
    """Return every base that could render as ``surface`` with ``affix``.

    Candidates are intentionally over-complete. Dictionary membership and later
    evidence determine soundness; this function never declares a composition
    invalid.
    """

    surface = normalize_lemma(surface)
    token = normalize_lemma(affix.bare)
    values: list[str] = []

    if affix.kind == "prefix":
        for prefix in (token, token + "-"):
            if token and surface.startswith(prefix) and len(surface) > len(prefix):
                values.append(surface[len(prefix) :])
    elif affix.kind == "suffix":
        for suffix in (token, "-" + token):
            if token and surface.endswith(suffix) and len(surface) > len(suffix):
                values.append(surface[: -len(suffix)])
        if token and surface.endswith(token):
            stem = surface[: -len(token)]
            if token[0] in _VOWELS:
                values.append(stem + "e")
                if len(stem) >= 2 and stem[-1:] == stem[-2:-1] and stem[-1] not in _VOWELS:
                    values.append(stem[:-1])
            if stem.endswith("i") and token != "ing":
                values.append(stem[:-1] + "y")
        if token == "ing" and surface.endswith("ying"):
            values.append(surface[:-4] + "ie")
        if token in {"s", "es"}:
            if surface.endswith("ies"):
                values.append(surface[:-3] + "y")
            if surface.endswith("ves"):
                values.extend((surface[:-3] + "f", surface[:-3] + "fe"))
            if surface.endswith("es"):
                values.append(surface[:-2])
        if token == "ed" and surface.endswith("ied"):
            values.append(surface[:-3] + "y")
    elif affix.kind == "contraction":
        if token and surface.endswith(token) and len(surface) > len(token):
            values.append(surface[: -len(token)])

    return _ordered_unique(values)


def compound_candidates(parts: Iterable[str]) -> tuple[str, ...]:
    """Render one ordered constituent sequence at the same composition scale."""

    normalized = tuple(normalize_lemma(part) for part in parts if normalize_lemma(part))
    if not normalized:
        return ()
    return _ordered_unique((" ".join(normalized), "-".join(normalized), "".join(normalized)))


__all__ = [
    "TransformationRule",
    "compound_candidates",
    "inverse_affix_candidates",
    "normalize_lemma",
    "render_affix_candidates",
    "transformation_inventory",
]
