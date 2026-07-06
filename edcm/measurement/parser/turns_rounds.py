"""
edcmbone.parser.turns_rounds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Embedded-model transcript parser.

The canon data (via CanonLoader) is the model — no external ML dependencies.
Classification is fully rule-based: multiword-join lookup → single-word
lookup → affix stripping → punctuation lookup → flesh.

Public API
----------
parse_transcript(text, round_strategy="cycle") -> ParsedTranscript

Data classes (all plain Python, no dataclasses module for 3.8 compat)
----------------------------------------------------------------------
BoneToken, FleshToken, Turn, Round, ParsedTranscript
"""

# === MODULE_BUILD ===
# id: edcmbone_parser_turns_rounds
#   module_name: turns_rounds
#   module_kind: engine
#   summary: embedded rule-based transcript parser (canon-driven, no ML deps) producing bones/flesh tokens, turns, and rounds
#   owner: Erin Spencer
#   public_surface: parse_transcript, BoneToken, FleshToken, Turn, Round, ParsedTranscript
#   internal_surface: _BoneClassifier, _split_turns, _group_into_rounds, _raw_tokens, _ordered_unique
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_apostrophe_normalization_and_tokenization
#   rollout: default_enabled
#   rollback: remove module; transcripts cannot be parsed into the EDCM structure
#   requires: edcmbone_canon_loader
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

import re
import math
from collections import Counter

from ..canon import CanonLoader

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class BoneToken:
    """A single token that matched the bone canon."""

    __slots__ = ("surface", "normalized", "bone_type", "primary", "families", "entry")

    def __init__(self, surface, normalized, bone_type, primary, families, entry):
        self.surface = surface          # original text as it appeared
        self.normalized = normalized    # key used for lookup
        self.bone_type = bone_type      # "word" | "multiword" | "affix" | "punct"
        self.primary = primary          # dominant PKQTS letter
        self.families = families        # full family list, e.g. ["P", "K"]
        self.entry = entry              # raw canon dict

    def __repr__(self):
        return "BoneToken({!r}, {})".format(self.surface, self.primary)


class FleshToken:
    """A token that did not match any bone canon entry."""

    __slots__ = ("surface",)

    def __init__(self, surface):
        self.surface = surface

    def __repr__(self):
        return "FleshToken({!r})".format(self.surface)


class Turn:
    """One speaker utterance."""

    def __init__(self, speaker, text, tokens):
        self.speaker = speaker
        self.text = text
        self.tokens = tokens            # list of BoneToken | FleshToken

        self.bone_tokens = [t for t in tokens if isinstance(t, BoneToken)]
        self.flesh_tokens = [t for t in tokens if isinstance(t, FleshToken)]

        # family counts for this turn
        self.family_counts = Counter()
        for t in self.bone_tokens:
            self.family_counts[t.primary] += 1

        self.bone_count = len(self.bone_tokens)
        self.token_count = len(self.tokens)

    def __repr__(self):
        return "Turn({!r}, bones={})".format(self.speaker, self.bone_count)


class Round:
    """A group of turns forming one exchange cycle."""

    def __init__(self, index, turns):
        self.index = index
        self.turns = turns

        # aggregate across turns
        self.all_tokens = []
        self.bone_tokens = []
        self.family_counts = Counter()
        for t in turns:
            self.all_tokens.extend(t.tokens)
            self.bone_tokens.extend(t.bone_tokens)
            for fam, cnt in t.family_counts.items():
                self.family_counts[fam] += cnt

        self.bone_count = len(self.bone_tokens)
        self.token_count = len(self.all_tokens)
        self.speakers = [t.speaker for t in turns]

    def __repr__(self):
        return "Round(index={}, turns={}, bones={})".format(
            self.index, len(self.turns), self.bone_count
        )


class ParsedTranscript:
    """Full parse result."""

    def __init__(self, rounds, turns):
        self.rounds = rounds
        self.turns = turns
        self.speakers = _ordered_unique(t.speaker for t in turns)

    # convenience -------------------------------------------------------

    def bone_count(self):
        return sum(t.bone_count for t in self.turns)

    def family_counts(self):
        total = Counter()
        for t in self.turns:
            total.update(t.family_counts)
        return dict(total)

    def __repr__(self):
        return "ParsedTranscript(rounds={}, turns={}, speakers={})".format(
            len(self.rounds), len(self.turns), self.speakers
        )


# ---------------------------------------------------------------------------
# Turn splitter — detects speaker prefixes in common transcript formats
# ---------------------------------------------------------------------------

# Patterns tried in order; each must have a named group "speaker" and "text".
_TURN_PATTERNS = [
    # **Speaker**: text   (markdown bold)
    re.compile(r"^\*\*(?P<speaker>[^*]+)\*\*\s*:\s*(?P<text>.+)$", re.MULTILINE),
    # [Speaker]: text
    re.compile(r"^\[(?P<speaker>[^\]]+)\]\s*:\s*(?P<text>.+)$", re.MULTILINE),
    # Speaker (role): text
    re.compile(r"^(?P<speaker>[A-Za-z][A-Za-z0-9 _\-]{0,30})\s*\([^)]*\)\s*:\s*(?P<text>.+)$", re.MULTILINE),
    # Speaker: text  (plain label — shortest reliable last)
    re.compile(r"^(?P<speaker>[A-Za-z][A-Za-z0-9 _\-]{0,30})\s*:\s*(?P<text>.+)$", re.MULTILINE),
]


def _split_turns(text):
    """Return list of (speaker, text) pairs from a raw transcript string."""
    for pattern in _TURN_PATTERNS:
        matches = list(pattern.finditer(text))
        if len(matches) >= 2:
            return [(m.group("speaker").strip(), m.group("text").strip()) for m in matches]

    # Fallback: treat the whole transcript as one anonymous turn
    stripped = text.strip()
    if stripped:
        return [("SPEAKER", stripped)]
    return []


# ---------------------------------------------------------------------------
# Round grouper
# ---------------------------------------------------------------------------

def _group_into_rounds(turns, strategy="cycle"):
    """Group Turn objects into Round objects.

    strategy="cycle"  — a new round starts each time the first-seen
                        speaker takes the floor again after at least one
                        other speaker has spoken.  Works for N speakers.
    strategy="pairs"  — every consecutive pair of turns is one round
                        (ignores speaker identity).
    """
    if not turns:
        return []

    if strategy == "pairs":
        rounds = []
        for i in range(0, len(turns), 2):
            rounds.append(Round(len(rounds), turns[i: i + 2]))
        return rounds

    # strategy == "cycle"
    anchor = turns[0].speaker
    rounds = []
    current = []
    seen_others = False

    for turn in turns:
        if turn.speaker == anchor and seen_others and current:
            rounds.append(Round(len(rounds), current))
            current = [turn]
            seen_others = False
        else:
            if turn.speaker != anchor:
                seen_others = True
            current.append(turn)

    if current:
        rounds.append(Round(len(rounds), current))

    return rounds


# ---------------------------------------------------------------------------
# Tokenizer — word + punctuation split
# ---------------------------------------------------------------------------

# Split into word-runs and individual punctuation characters.
# Preserve hyphenated compounds as one token before punctuation handling.
_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+|[A-Za-z]+(?:'[A-Za-z]+)*|[0-9]+|[^\w\s]")


def _raw_tokens(text):
    """Return list of raw token strings from utterance text."""
    text = (text or '').replace('’', "'").replace('‘', "'")
    return _WORD_RE.findall(text)


# ---------------------------------------------------------------------------
# Bone classifier — the embedded model
# ---------------------------------------------------------------------------

class _BoneClassifier:
    """Classifies token sequences using CanonLoader as its model."""

    def __init__(self, canon: CanonLoader):
        self._canon = canon

        # Pre-sort prefixes/suffixes longest-first so greedy matching works
        self._prefixes = sorted(
            [a["affix"].rstrip("-") for a in canon.all_affixes()
             if a.get("type") == "prefix"],
            key=len, reverse=True
        )
        self._suffixes = sorted(
            [a["affix"].lstrip("-") for a in canon.all_affixes()
             if a.get("type") == "suffix"],
            key=len, reverse=True
        )

        # Build word → entry map for quick lookup (already in canon._word_index,
        # but we access via the public API for correctness)
        self._word_cache = {}
        self._affix_cache = {}
        self._valid_stems = {
            entry["word"].lower()
            for entry in canon.all_words()
            if entry.get("primary") != "S"
        }

    def _make_bone(self, surface, normalized, bone_type, entry):
        return BoneToken(
            surface=surface,
            normalized=normalized,
            bone_type=bone_type,
            primary=entry["primary"],
            families=entry.get("families", [entry["primary"]]),
            entry=entry,
        )

    def classify_sequence(self, raw_tokens):
        """Classify a flat list of raw token strings into BoneToken/FleshToken.

        Tries (in order) for each position:
          1. Multiword join (2-gram)
          2. Single word lookup
          3. Affix strip (prefix then suffix)
          4. Punctuation lookup
          5. Flesh
        """
        result = []
        i = 0
        n = len(raw_tokens)
        while i < n:
            tok = raw_tokens[i]

            # 1. Try 2-gram multiword join
            if i + 1 < n:
                bigram = (tok + raw_tokens[i + 1]).lower().replace(" ", "")
                entry = self._canon.lookup_word(bigram)
                if entry and entry.get("joined"):
                    result.append(self._make_bone(
                        tok + " " + raw_tokens[i + 1], bigram, "multiword", entry
                    ))
                    i += 2
                    continue

            # 2. Single word lookup
            entry = self._canon.lookup_word(tok)
            if entry:
                result.append(self._make_bone(tok, tok.lower(), "word", entry))
                i += 1
                continue

            # 3. Affix strip — prefix
            lower = tok.lower()
            matched_affix = False
            for pre in self._prefixes:
                if lower.startswith(pre) and len(lower) - len(pre) >= 2:
                    residual = lower[len(pre):]
                    if residual not in self._valid_stems:
                        continue
                    affix_key = pre + "-"
                    if affix_key not in self._affix_cache:
                        self._affix_cache[affix_key] = self._canon.lookup_affix(affix_key)
                    entry = self._affix_cache[affix_key]
                    if entry:
                        result.append(self._make_bone(tok, affix_key, "affix", entry))
                        matched_affix = True
                        break
            if matched_affix:
                i += 1
                continue

            # 3b. Affix strip — suffix
            for suf in self._suffixes:
                if lower.endswith(suf) and len(lower) - len(suf) >= 2:
                    residual = lower[:-len(suf)]
                    if residual not in self._valid_stems:
                        continue
                    affix_key = "-" + suf
                    if affix_key not in self._affix_cache:
                        self._affix_cache[affix_key] = self._canon.lookup_affix(affix_key)
                    entry = self._affix_cache[affix_key]
                    if entry:
                        result.append(self._make_bone(tok, affix_key, "affix", entry))
                        matched_affix = True
                        break
            if matched_affix:
                i += 1
                continue

            # 4. Punctuation — only count entries that actually emit tokens
            entry = self._canon.lookup_punct(tok)
            if entry and entry.get("tokens_emitted", 0) > 0:
                result.append(self._make_bone(tok, tok, "punct", entry))
                i += 1
                continue

            # 5. Flesh
            result.append(FleshToken(tok))
            i += 1

        return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_transcript(transcript, round_strategy="cycle", canon=None):
    """Parse a raw transcript string into a ParsedTranscript.

    Parameters
    ----------
    transcript : str
        Raw text. Speaker turns must be prefixed with a label followed by
        a colon, e.g. ``A: hello`` or ``**User**: hello``. Multiple
        recognised formats are tried automatically.
    round_strategy : "cycle" | "pairs"
        How to group turns into rounds.
        "cycle" (default) — a round ends when the anchor speaker (first
        speaker seen) regains the floor after at least one other speaker
        has spoken.
        "pairs" — every consecutive pair of turns is one round.
    canon : CanonLoader | None
        Pass an existing CanonLoader instance to avoid reloading data.
        If None, a fresh instance is created.

    Returns
    -------
    ParsedTranscript
    """
    if canon is None:
        canon = CanonLoader()

    classifier = _BoneClassifier(canon)

    raw_turns = _split_turns(transcript)
    turns = []
    for speaker, text in raw_turns:
        raw_toks = _raw_tokens(text)
        classified = classifier.classify_sequence(raw_toks)
        turns.append(Turn(speaker, text, classified))

    rounds = _group_into_rounds(turns, strategy=round_strategy)
    return ParsedTranscript(rounds=rounds, turns=turns)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ordered_unique(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
