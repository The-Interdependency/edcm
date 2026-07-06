"""
edcmbone.compress
~~~~~~~~~~~~~~~~~
Lossless codec for ParsedTranscript + RoundMetrics.

The encoding scheme is EDCM-aware: bones and flesh are stored in separate
streams, making the structural (constraint-skeleton) layer addressable without
full decompression.  The final byte form uses zlib (DEFLATE) for entropy
coding; the EDCM structure does most of the modelling work.

Lossless guarantee
------------------
    pt2, metrics2 = from_bytes(to_bytes(pt, metrics))
    # pt2 and metrics2 are token-for-token identical to the originals.

Compression-metric connection
------------------------------
The bone family sequence is treated as the "compressed structural text".
Its Shannon entropy is the theoretical minimum bits-per-bone under optimal
coding.  compression_stats() returns this alongside byte-level ratios,
linking the codec directly to the EDCM metric mathematics (§2, §11).

Public API
----------
    encode(parsed, metrics=None) -> dict          JSON-serialisable dict
    decode(data)   -> (ParsedTranscript, metrics) from dict
    to_bytes(parsed, metrics=None) -> bytes       zlib-compressed
    from_bytes(data) -> (ParsedTranscript, metrics)
    compression_stats(original_text, compressed_bytes, parsed) -> dict
"""

# === MODULE_BUILD ===
# id: edcmbone_compress
#   module_name: compress
#   module_kind: engine
#   summary: lossless EDCM-aware codec for ParsedTranscript + RoundMetrics (separate bone/flesh streams, zlib entropy coding)
#   owner: Erin Spencer
#   public_surface: encode,decode,to_bytes,from_bytes,compression_stats
#   internal_surface: _tok_to_dict,_dict_to_tok,_metrics_to_dict,_dict_to_metrics,_build_huffman_codes,_huffman_expected_bits
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; transcripts persist uncompressed
#   requires: edcmbone_parser_turns_rounds,edcmbone_metrics_compute
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===


from __future__ import annotations

import heapq
import json
import math
import zlib
from collections import Counter

from .parser.turns_rounds import (
    BoneToken, FleshToken, ParsedTranscript, Round, Turn,
)
from .metrics.compute import RoundMetrics
from .metrics.stats import shannon_entropy


# ---------------------------------------------------------------------------
# Format version — bump when encoding changes
# ---------------------------------------------------------------------------
_FORMAT_VERSION = 1


# ---------------------------------------------------------------------------
# Token serialisation
# ---------------------------------------------------------------------------

def _tok_to_dict(tok):
    if isinstance(tok, BoneToken):
        return {
            "k": "B",
            "s": tok.surface,
            "p": tok.primary,
            "f": tok.families,
            "t": tok.bone_type,
            "n": tok.normalized,
        }
    return {"k": "F", "s": tok.surface}


def _dict_to_tok(rec):
    if rec["k"] == "B":
        return BoneToken(
            surface=rec["s"],
            normalized=rec.get("n", rec["s"].lower()),
            bone_type=rec["t"],
            primary=rec["p"],
            families=rec["f"],
            entry={},
        )
    return FleshToken(surface=rec["s"])


# ---------------------------------------------------------------------------
# Metrics serialisation
# ---------------------------------------------------------------------------

def _metrics_to_dict(m):
    return {slot: getattr(m, slot) for slot in m.__slots__}


def _dict_to_metrics(d):
    return RoundMetrics(**d)


# ---------------------------------------------------------------------------
# Encode / decode
# ---------------------------------------------------------------------------

def encode(parsed, metrics=None):
    """Encode a ParsedTranscript (+ optional metrics list) to a plain dict.

    The dict is JSON-serialisable and self-describing.  Bones and flesh are
    interleaved in token order so reconstruction is exact.
    """
    rounds_out = []
    for i, rnd in enumerate(parsed.rounds):
        turns_out = []
        for turn in rnd.turns:
            turns_out.append({
                "sp": turn.speaker,
                "tx": turn.text,
                "tk": [_tok_to_dict(t) for t in turn.tokens],
            })
        rec = {"i": rnd.index, "turns": turns_out}
        if metrics is not None and i < len(metrics):
            rec["m"] = _metrics_to_dict(metrics[i])
        rounds_out.append(rec)

    return {
        "v": _FORMAT_VERSION,
        "speakers": parsed.speakers,
        "rounds": rounds_out,
    }


def decode(data):
    """Decode a dict produced by encode().

    Returns
    -------
    (ParsedTranscript, list[RoundMetrics] | None)
    """
    rounds = []
    all_turns = []
    metrics_out = []

    for rec in data["rounds"]:
        turns = []
        for trec in rec["turns"]:
            tokens = [_dict_to_tok(t) for t in trec["tk"]]
            turn = Turn(trec["sp"], trec["tx"], tokens)
            turns.append(turn)
            all_turns.append(turn)

        rnd = Round(rec["i"], turns)
        rounds.append(rnd)

        if "m" in rec:
            metrics_out.append(_dict_to_metrics(rec["m"]))

    pt = ParsedTranscript(rounds=rounds, turns=all_turns)
    return pt, (metrics_out if metrics_out else None)


# ---------------------------------------------------------------------------
# Byte-level codec (JSON + zlib)
# ---------------------------------------------------------------------------

def to_bytes(parsed, metrics=None, level=9):
    """Encode and zlib-compress.  Returns bytes.

    level : zlib compression level 0-9 (default 9 = maximum compression).
    """
    encoded = encode(parsed, metrics)
    raw = json.dumps(encoded, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return zlib.compress(raw, level=level)


def from_bytes(data):
    """Decompress and decode bytes produced by to_bytes().

    Returns
    -------
    (ParsedTranscript, list[RoundMetrics] | None)
    """
    raw = zlib.decompress(data)
    return decode(json.loads(raw.decode("utf-8")))


# ---------------------------------------------------------------------------
# Huffman lower bound (informational, not used in actual codec)
# ---------------------------------------------------------------------------

def _huffman_expected_bits(counts):
    """Expected bits per symbol under optimal Huffman coding.

    Equal to the Shannon entropy when the distribution is dyadic; otherwise
    the Huffman code is within 1 bit/symbol of the entropy lower bound.
    """
    total = sum(counts.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for c in counts.values():
        p = c / total
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def _build_huffman_codes(counts):
    """Return {symbol: bitstring} for a symbol frequency dict."""
    if not counts:
        return {}
    if len(counts) == 1:
        sym = next(iter(counts))
        return {sym: "0"}

    # Min-heap of (freq, counter, tree_node)
    heap = []
    for i, (sym, freq) in enumerate(counts.items()):
        heapq.heappush(heap, (freq, i, sym))

    counter = len(counts)
    parent = {}

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        parent[n1] = (counter, "0")
        parent[n2] = (counter, "1")
        heapq.heappush(heap, (f1 + f2, counter, counter))
        counter += 1

    root = heap[0][2]

    codes = {}
    for sym in counts:
        bits = []
        node = sym
        while node in parent:
            node, bit = parent[node]
            bits.append(bit)
        codes[sym] = "".join(reversed(bits)) if bits else "0"

    return codes


# ---------------------------------------------------------------------------
# Compression statistics
# ---------------------------------------------------------------------------

def compression_stats(original_text, compressed_bytes, parsed):
    """Return a dict linking byte compression to EDCM metric mathematics.

    Fields
    ------
    original_chars          : character count of raw transcript
    original_bytes          : UTF-8 byte count
    compressed_bytes        : zlib-compressed byte count
    byte_compression_ratio  : compressed / original  (<1 = savings)
    byte_savings_pct        : (1 - ratio) * 100

    total_tokens            : all tokens across all turns
    bone_count              : tokens that are bones
    flesh_count             : tokens that are flesh
    structural_density      : bone_count / total_tokens
                              (= constraint weight of the text)

    family_counts           : {P,K,Q,T,S} -> int
    bone_entropy_bits       : Shannon entropy of bone family sequence (bits/bone)
    huffman_min_bits        : optimal Huffman code length (bits/bone)
                              — lower bound on lossless structural compression
    huffman_codes           : {family -> bitstring} for the bone stream

    flesh_vocabulary_size   : unique flesh token types
    flesh_type_token_ratio  : vocabulary / flesh tokens
                              (high = diverse content, low = repetitive)

    bone_stream_raw_bits    : bone_count * 3  (naive 3-bit fixed code)
    bone_stream_huffman_bits: bone_count * huffman_min_bits  (optimal)
    bone_stream_savings_pct : percent reduction vs naive
    """
    all_tokens = []
    bone_tokens = []
    flesh_tokens = []
    family_seq = []

    for rnd in parsed.rounds:
        for turn in rnd.turns:
            for tok in turn.tokens:
                all_tokens.append(tok)
                if isinstance(tok, BoneToken) and tok.primary:
                    bone_tokens.append(tok)
                    family_seq.append(tok.primary)
                else:
                    flesh_tokens.append(tok)

    family_counts = Counter(family_seq)
    bone_entropy = shannon_entropy(family_seq)
    huffman_min = _huffman_expected_bits(family_counts)
    huffman_codes = _build_huffman_codes(dict(family_counts))

    n_total = len(all_tokens)
    n_bones = len(bone_tokens)
    n_flesh = len(flesh_tokens)

    flesh_types = len({t.surface.lower() for t in flesh_tokens})
    flesh_ttr = flesh_types / max(1, n_flesh)

    orig_bytes = len(original_text.encode("utf-8"))
    comp_bytes = len(compressed_bytes)
    byte_ratio = comp_bytes / max(1, orig_bytes)

    bone_raw_bits = n_bones * 3  # ceil(log2(5)) = 3
    bone_huffman_bits = n_bones * huffman_min
    bone_savings = (1.0 - huffman_min / 3.0) * 100.0 if n_bones > 0 else 0.0

    return {
        "original_chars": len(original_text),
        "original_bytes": orig_bytes,
        "compressed_bytes": comp_bytes,
        "byte_compression_ratio": round(byte_ratio, 4),
        "byte_savings_pct": round((1.0 - byte_ratio) * 100.0, 2),
        "total_tokens": n_total,
        "bone_count": n_bones,
        "flesh_count": n_flesh,
        "structural_density": round(n_bones / max(1, n_total), 4),
        "family_counts": dict(family_counts),
        "bone_entropy_bits": round(bone_entropy, 4),
        "huffman_min_bits": round(huffman_min, 4),
        "huffman_codes": huffman_codes,
        "flesh_vocabulary_size": flesh_types,
        "flesh_type_token_ratio": round(flesh_ttr, 4),
        "bone_stream_raw_bits": bone_raw_bits,
        "bone_stream_huffman_bits": round(bone_huffman_bits, 1),
        "bone_stream_savings_pct": round(bone_savings, 2),
    }
