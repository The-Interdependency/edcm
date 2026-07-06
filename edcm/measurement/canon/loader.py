"""
edcmbone.canon.loader
~~~~~~~~~~~~~~~~~~~~~
Loads and exposes the v1 canon data files:
  - bones_words_v1.json       free word bones (PKQTS families)
  - bones_affixes_v1.json     bound bone affixes
  - bones_punct_v1.json       punctuation bones
  - markers_v1.json           behavioral-layer markers (9-metric vector)
"""

# === MODULE_BUILD ===
# id: edcmbone_canon_loader
#   module_name: loader
#   module_kind: adapter
#   summary: loads the v1 canon data files (bones/affixes/punct/markers) and exposes a lookup API
#   owner: Erin Spencer
#   public_surface: CanonLoader
#   internal_surface: _load
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: hmmm
#   rollout: default_enabled
#   rollback: remove module; parser falls back to no embedded canon
#   requires: none
#   since: 2026-06-02
#   unresolved: dedicated canon-loader test module not located in tracked tests/
# === END MODULE_BUILD ===


import json
import pathlib

_DATA_DIR = pathlib.Path(__file__).parent / "data"


def _load(filename):
    return json.loads((_DATA_DIR / filename).read_text(encoding="utf-8"))


class CanonLoader:
    """Provides lookup access to all v1 canon data.

    Usage::

        from edcm.measurement.canon import CanonLoader

        canon = CanonLoader()

        # Bone lookups
        canon.lookup_word("not")          # -> {"word": "not", "primary": "P", ...}
        canon.lookup_affix("un-")         # -> {"affix": "un-", "primary": "P", ...}
        canon.lookup_punct("?")           # -> {"mark": "?", "primary": "Q", ...}

        # Marker lookups
        canon.metric_names()              # -> ["C", "R", "D", "N", "L", "O", "F", "E", "I"]
        canon.metric_info("R")            # -> {metric, formula, computable_from_markers, ...}
        canon.marker_phrases("R", "refusal_markers")  # -> ["no", "won't", ...]
    """

    def __init__(self):
        self._words_data = _load("bones_words_v1.json")
        self._affixes_data = _load("bones_affixes_v1.json")
        self._punct_data = _load("bones_punct_v1.json")
        self._markers_data = _load("markers_v1.json")

        # Build lookup indexes
        self._word_index = {
            entry["word"].lower(): entry
            for entry in self._words_data["words"]
        }
        self._multiword_index = {
            entry["joined"].lower(): entry
            for entry in self._words_data.get("multiword_joins", [])
        }

        self._affix_index = {}
        for section in ("inflectional", "derivational_prefixes", "derivational_suffixes"):
            for entry in self._affixes_data[section]["affixes"]:
                self._affix_index[entry["affix"].lower()] = entry

        self._punct_index = {
            entry["mark"]: entry
            for entry in self._punct_data["punctuation"]
        }

    # ------------------------------------------------------------------
    # Bone lookups
    # ------------------------------------------------------------------

    def lookup_word(self, word):
        """Return the bone entry for a free word, or None if not in canon.

        Checks multiword joins first (using the joined/normalised form),
        then single-word entries.
        """
        key = word.lower().replace(" ", "")
        result = self._multiword_index.get(key)
        if result is None:
            result = self._word_index.get(word.lower())
        return result

    def lookup_affix(self, affix):
        """Return the bone entry for an affix (e.g. 'un-', '-ness'), or None."""
        return self._affix_index.get(affix.lower())

    def lookup_punct(self, mark):
        """Return the bone entry for a punctuation mark, or None."""
        return self._punct_index.get(mark)

    def all_words(self):
        """Return all free-word bone entries."""
        return list(self._words_data["words"])

    def all_multiword_joins(self):
        """Return all multiword-join entries."""
        return list(self._words_data.get("multiword_joins", []))

    def all_affixes(self):
        """Return all affix bone entries across all sections."""
        return list(self._affix_index.values())

    def all_punct(self):
        """Return all punctuation bone entries."""
        return list(self._punct_data["punctuation"])

    # ------------------------------------------------------------------
    # Marker lookups
    # ------------------------------------------------------------------

    def metric_names(self):
        """Return the ordered list of behavioral metric keys."""
        return [k for k in self._markers_data if k != "_meta"]

    def metric_info(self, metric):
        """Return the full metric dict for a given key (e.g. 'C', 'R').

        Keys include: metric, formula, computable_from_markers,
        requires_embeddings, explanation, markers.
        """
        if metric not in self._markers_data:
            raise KeyError("Unknown metric {!r}. Available: {}".format(
                metric, self.metric_names()
            ))
        return self._markers_data[metric]

    def marker_phrases(self, metric, category):
        """Return the phrase list for a marker category within a metric.

        Args:
            metric:   e.g. "R"
            category: e.g. "refusal_markers" (a key inside metric["markers"])

        Returns:
            list of strings
        """
        info = self.metric_info(metric)
        markers = info.get("markers", {})
        if category not in markers:
            raise KeyError("Unknown category {!r} for metric {!r}. Available: {}".format(
                category, metric, list(markers.keys())
            ))
        return list(markers[category])

    def all_marker_phrases(self, metric):
        """Return a flat list of all marker phrases across all categories for a metric."""
        info = self.metric_info(metric)
        phrases = []
        for phrases_list in info.get("markers", {}).values():
            if isinstance(phrases_list, list):
                phrases.extend(phrases_list)
        return phrases

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    def meta(self, dataset):
        """Return the _meta block for a dataset.

        Args:
            dataset: one of "words", "affixes", "punct", "markers"
        """
        mapping = {
            "words": self._words_data,
            "affixes": self._affixes_data,
            "punct": self._punct_data,
            "markers": self._markers_data,
        }
        if dataset not in mapping:
            raise KeyError("Unknown dataset {!r}. Choose from: {}".format(
                dataset, list(mapping.keys())
            ))
        return mapping[dataset].get("_meta", {})
