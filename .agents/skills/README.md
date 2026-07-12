# Repo-local skill-lib subset

These directories are vendored consumers of the canonical organization skill library:

```text
repository: The-Interdependency/skill-lib
source commit: d0036c6c3a449f5a1213e3289dceb1c43263cb52
```

Installed subset:

```text
meta-module-build/
the-interdependency/
```

The subset is intentionally bounded:

- `the-interdependency` governs all organization repository, code, research, and GitHub work;
- `meta-module-build` governs metadata-first creation and maintenance of EDCM-native modules.

The full canonical skill library is not copied here. CI checks out the pinned source commit and uses its unmodified:

```text
tools/check_consumer_drift.py
msdmd/collect.py
msdmd/parsers/
```

Validation:

```bash
# With skill-lib checked out beside this repository at the pinned commit:
python ../skill-lib/tools/check_consumer_drift.py . \
  --sha d0036c6c3a449f5a1213e3289dceb1c43263cb52 \
  --strict-sha \
  --require-vendored

PYTHONPATH=../skill-lib python ../skill-lib/msdmd/collect.py \
  --root . \
  --repo The-Interdependency/edcm \
  --out edcm_msdmd.ts
```

Repo-local copies are never the authority. Edit skills in `The-Interdependency/skill-lib` first, then propagate and update this source commit.

## hmmm

Whether EDCM should later vendor additional metadata-block skill specifications rather than loading them from the canonical checkout during compliance work.
