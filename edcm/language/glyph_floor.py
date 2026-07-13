"""Public 157-vertex glyph floor migrated from a0-betatest."""

# === MODULE_BUILD ===
# id: edcm_language_glyph_floor
#   module_name: glyph_floor
#   module_kind: canon
#   summary: reproduces and validates the exact public 157-vertex glyph arrangement selected from a0-betatest for this English embedding run
#   owner: Erin Spencer
#   public_surface: PUBLIC_GLYPH_FLOOR_157, build_public_glyph_floor_157, validate_public_glyph_floor, glyph_floor_sha256
#   internal_surface: _UPPERCASE, _LOWERCASE, _DIGITS_ODD, _DIGITS_EVEN, _PAIRED_OPEN, _PAIRED_CLOSE, _UNPAIRED_ASCII, _UNPAIRED_OPS
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_language_embeddings
#   rollout: default_enabled
#   rollback: restore the prior a0-betatest source as the only authority and remove this migrated copy
#   requires: edcm_language_manifest
#   since: 2026-07-13
#   unresolved: private per-agent phase and permutation remain outside this public embedding artifact
# === END MODULE_BUILD ===

from __future__ import annotations

import hashlib
import string

from .manifest import PUBLIC_GLYPH_FLOOR_SHA256

_UPPERCASE = tuple(string.ascii_uppercase)
_LOWERCASE = tuple(string.ascii_lowercase)
_DIGITS_ODD = ("1", "3", "5", "7", "9")
_DIGITS_EVEN = ("2", "4", "6", "8", "0")
_PAIRED_OPEN = ("(", "[", "{", "<", "‘", "“", "«")
_PAIRED_CLOSE = (")", "]", "}", ">", "’", "”", "»")
_UNPAIRED_ASCII = tuple(
    chr(index)
    for index in range(33, 127)
    if chr(index)
    not in (
        set(_UPPERCASE)
        | set(_LOWERCASE)
        | set(string.digits)
        | set(_PAIRED_OPEN)
        | set(_PAIRED_CLOSE)
        | {" "}
    )
)
_UNPAIRED_OPS = (
    "…", "—", "–", "·", "°", "±", "×", "÷", "√", "∂", "∫", "∑", "∏", "∇", "∞",
    "≈", "≠", "≤", "≥", "→", "←", "↑", "↓", "↔", "⊕", "⊗", "⊙", "⊘", "∈", "∉",
    "⊂", "⊃", "⊆", "⊇", "∩", "∪", "∧", "∨", "¬", "∀", "∃", "⊢", "⊨", "∴", "∵",
    "≡", "ψ", "φ", "ω", "α", "β", "γ", "δ", "λ", "π", "σ", "τ", "θ", "∅", "ℕ", "ℤ",
    "ℚ", "ℝ", "ℂ", "ℵ",
)


def build_public_glyph_floor_157() -> tuple[str, ...]:
    """Reproduce a0-betatest ``EXAMPLE_157`` exactly and deterministically."""

    size = 157
    slots = [""] * size
    slots[0] = " "
    upper_arc = list(range(1, (size // 2) + 1))
    lower_arc = list(range((size // 2) + 1, size))

    upper_letters = list(range(1, upper_arc[-1], 3))[:26]
    lower_letters = list(range(lower_arc[1], lower_arc[-1], 3))[:26]
    for index, glyph in enumerate(_UPPERCASE):
        slots[upper_letters[index]] = glyph
    for index, glyph in enumerate(_LOWERCASE):
        slots[lower_letters[index]] = glyph

    upper_gaps = [position for position in upper_arc if slots[position] == ""]
    upper_step = max(1, len(upper_gaps) // (len(_DIGITS_ODD) + 1))
    for index, glyph in enumerate(_DIGITS_ODD):
        target = upper_step * (index + 1)
        if target < len(upper_gaps):
            slots[upper_gaps[target]] = glyph

    lower_gaps = [position for position in lower_arc if slots[position] == ""]
    lower_step = max(1, len(lower_gaps) // (len(_DIGITS_EVEN) + 1))
    for index, glyph in enumerate(_DIGITS_EVEN):
        target = lower_step * (index + 1)
        if target < len(lower_gaps):
            slots[lower_gaps[target]] = glyph

    upper_remaining = [position for position in upper_arc if slots[position] == ""]
    lower_remaining = [position for position in lower_arc if slots[position] == ""]
    open_step = max(1, len(upper_remaining) // (len(_PAIRED_OPEN) + 1))
    close_step = max(1, len(lower_remaining) // (len(_PAIRED_CLOSE) + 1))
    for index, glyph in enumerate(_PAIRED_OPEN):
        target = open_step * (index + 1)
        if target < len(upper_remaining):
            slots[upper_remaining[target]] = glyph
    for index, glyph in enumerate(_PAIRED_CLOSE):
        target = close_step * (index + 1)
        if target < len(lower_remaining):
            slots[lower_remaining[target]] = glyph

    unpaired = _UNPAIRED_ASCII + _UNPAIRED_OPS
    fill_positions = [position for position in range(size) if slots[position] == ""]
    if len(fill_positions) > len(unpaired):
        raise ValueError("the declared public glyph inventory does not fill 157 vertices")
    for index, position in enumerate(fill_positions):
        slots[position] = unpaired[index]

    result = tuple(slots)
    validate_public_glyph_floor(result)
    return result


def glyph_floor_sha256(glyphs: tuple[str, ...]) -> str:
    """Hash the one-glyph-per-line canonical floor representation."""

    return hashlib.sha256(("\n".join(glyphs) + "\n").encode("utf-8")).hexdigest()


def validate_public_glyph_floor(glyphs: tuple[str, ...]) -> None:
    if len(glyphs) != 157:
        raise ValueError("public glyph floor must contain exactly 157 vertices")
    if glyphs[0] != " ":
        raise ValueError("vertex zero must remain the literal-space seam")
    if len(set(glyphs)) != len(glyphs):
        raise ValueError("public glyph floor must be bijective")
    if any(not glyph or glyph.startswith("\x00") for glyph in glyphs):
        raise ValueError("every public vertex must contain one explicit non-NUL glyph")
    digest = glyph_floor_sha256(glyphs)
    if digest != PUBLIC_GLYPH_FLOOR_SHA256:
        raise ValueError(f"public glyph floor drift: expected {PUBLIC_GLYPH_FLOOR_SHA256}, got {digest}")


PUBLIC_GLYPH_FLOOR_157 = build_public_glyph_floor_157()


__all__ = [
    "PUBLIC_GLYPH_FLOOR_157",
    "build_public_glyph_floor_157",
    "glyph_floor_sha256",
    "validate_public_glyph_floor",
]
