"""
edcmbone.metrics.stats
~~~~~~~~~~~~~~~~~~~~~~
Basic text statistics used by the EDCM metric vector.

All functions operate on plain token lists (list of str) or raw strings.
No external dependencies — stdlib only.

Functions
---------
tokenize(text)           -> list[str]
ngrams(tokens, n)        -> list[tuple]
ttr(tokens)              -> float          Type-Token Ratio
repetition_ratio(tokens) -> float          1 - TTR
shannon_entropy(tokens)  -> float          bits
novelty(tokens_b, tokens_a) -> float      fraction of tokens_b not in tokens_a
cosine_sim(tokens_a, tokens_b) -> float   bag-of-words cosine similarity
rep_ngram_density(tokens, n=3) -> float   repeated n-gram density
pattern_density(text, pattern) -> float   occurrences per 1000 chars
jaccard(set_a, set_b)    -> float
correction_fidelity(tokens_a, tokens_b, tokens_c) -> float
clamp(x)                 -> float         max(0, min(1, x))
norm_per_100(x, tokens)  -> float
"""

# === MODULE_BUILD ===
# id: edcmbone_metrics_stats
#   module_name: stats
#   module_kind: engine
#   summary: stdlib-only text statistics (TTR, entropy, novelty, cosine, n-gram density) feeding the EDCM metric vector
#   owner: Erin Spencer
#   public_surface: tokenize, ngrams, ttr, repetition_ratio, shannon_entropy, rep_ngram_density, pattern_density, novelty, cosine_sim, jaccard, correction_fidelity, clamp, norm_per_100
#   internal_surface: _count_vector
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; metric primitives unavailable
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

import re
import math
from collections import Counter


# ---------------------------------------------------------------------------
# Tokenisation
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z''‘’\-]+|\d+|[^\w\s]")


def tokenize(text):
    """Return a list of lowercase tokens from a string."""
    return _WORD_RE.findall(text.lower())


def ngrams(tokens, n):
    """Return a list of n-gram tuples from a token list."""
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


# ---------------------------------------------------------------------------
# Single-sequence statistics
# ---------------------------------------------------------------------------

def ttr(tokens):
    """Type-Token Ratio: |unique tokens| / |total tokens|.

    Returns 0.0 for empty input.
    """
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def repetition_ratio(tokens):
    """1 - TTR."""
    return 1.0 - ttr(tokens)


def shannon_entropy(tokens):
    """Shannon entropy in bits. Returns 0.0 for empty or single-type input."""
    if not tokens:
        return 0.0
    n = len(tokens)
    counts = Counter(tokens)
    entropy = 0.0
    for c in counts.values():
        p = c / n
        entropy -= p * math.log2(p)
    return entropy


def rep_ngram_density(tokens, n=3):
    """Repeated n-gram density.

    Sum of (freq(g) - 1) for all n-grams that appear more than once,
    divided by the total number of n-gram positions.

    Returns 0.0 if fewer than n tokens.
    """
    gs = ngrams(tokens, n)
    if not gs:
        return 0.0
    counts = Counter(gs)
    excess = sum(c - 1 for c in counts.values() if c > 1)
    return excess / len(gs)


def pattern_density(text, pattern):
    """Number of (possibly-overlapping) regex pattern matches per 1000 characters.

    Returns 0.0 for empty text.
    """
    if not text:
        return 0.0
    matches = len(re.findall(pattern, text))
    return matches / len(text) * 1000


# ---------------------------------------------------------------------------
# Two-sequence statistics
# ---------------------------------------------------------------------------

def novelty(tokens_b, tokens_a):
    """Fraction of tokens in B that do not appear in A (as a set).

    Returns 0.0 if B is empty.
    """
    if not tokens_b:
        return 0.0
    set_a = set(tokens_a)
    novel = sum(1 for t in tokens_b if t not in set_a)
    return novel / len(tokens_b)


def _count_vector(tokens_a, tokens_b):
    """Build aligned count vectors over the union vocabulary."""
    vocab = sorted(set(tokens_a) | set(tokens_b))
    ca = Counter(tokens_a)
    cb = Counter(tokens_b)
    va = [ca[w] for w in vocab]
    vb = [cb[w] for w in vocab]
    return va, vb


def cosine_sim(tokens_a, tokens_b):
    """Bag-of-words cosine similarity. Returns 0.0 if either sequence is empty."""
    if not tokens_a or not tokens_b:
        return 0.0
    va, vb = _count_vector(tokens_a, tokens_b)
    dot = sum(a * b for a, b in zip(va, vb))
    mag_a = math.sqrt(sum(a * a for a in va))
    mag_b = math.sqrt(sum(b * b for b in vb))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def jaccard(set_a, set_b):
    """Jaccard similarity between two sets. Returns 0.0 for empty union."""
    set_a, set_b = set(set_a), set(set_b)
    union = set_a | set_b
    if not union:
        return 0.0
    return len(set_a & set_b) / len(union)


def correction_fidelity(tokens_a, tokens_b, tokens_c):
    """Correction fidelity.

    Combines overlap of B with correction C and distance of B from original A:

        Fidelity = 0.5 * J(T_C, T_B) + 0.5 * (1 - cos(c_A, c_B))

    tokens_a : original response A
    tokens_b : new response B
    tokens_c : correction C
    """
    j = jaccard(set(tokens_c), set(tokens_b))
    cos = cosine_sim(tokens_a, tokens_b)
    return 0.5 * j + 0.5 * (1.0 - cos)


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

def clamp(x):
    """Clamp x to [0, 1]."""
    return max(0.0, min(1.0, float(x)))


def norm_per_100(x, tokens):
    """Scale x to a per-100-tokens rate."""
    if not tokens:
        return 0.0
    return float(x) * 100.0 / len(tokens)
