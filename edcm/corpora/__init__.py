"""Full-corpus, source-native evidence adapters.

Usage guidance
--------------
Corpus runners are explicit commands. They require a locally held source
artifact whose bytes match an admitted manifest; raw corpora are never package
data. See :mod:`edcm.corpora.multiwoz21` for the first admitted runner.
"""

# === MODULE_BUILD ===
# id: edcm_corpora_package
#   module_name: corpora
#   module_kind: adapter
#   summary: source-native full-corpus execution surfaces with admission, reconciliation, and completion or incompletion receipts
#   owner: Erin Spencer
#   public_surface: load_multiwoz21_admission, run_multiwoz21_archive
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: caller-selected aggregate reports, receipts, and checkpoints only; raw corpora remain external
#   network_boundary: none
#   user_data_boundary: source evidence is read locally and only non-text aggregates and cryptographic identities are emitted
#   admin_only: false
#   tests: tests.test_multiwoz21_corpus
#   rollout: explicit per-corpus command after admission-manifest verification
#   rollback: remove the corpus package and generated aggregate evidence; frozen measurement and historical experiments remain unchanged
#   requires: edcm_ucns_adapter
#   since: 2026-07-28
#   unresolved: admission and adapter design for the six queued corpora after MultiWOZ 2.1
# === END MODULE_BUILD ===

from importlib import import_module
from typing import Any


def __getattr__(name: str) -> Any:
    """Load corpus surfaces lazily so ``python -m`` runs without re-import."""

    aliases = {
        "load_multiwoz21_admission": "load_admission_manifest",
        "run_multiwoz21_archive": "run_archive",
    }
    if name in {"AdmissionManifest", "CorpusRunError", *aliases}:
        module = import_module(".multiwoz21", __name__)
        return getattr(module, aliases.get(name, name))
    raise AttributeError(name)

__all__ = [
    "AdmissionManifest",
    "CorpusRunError",
    "load_multiwoz21_admission",
    "run_multiwoz21_archive",
]
