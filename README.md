# edcm

This repository is the consolidation of:

- [`The-Interdependency/edcmbone`](https://github.com/The-Interdependency/edcmbone)
- [`erinepshovel-code/EDCM`](https://github.com/erinepshovel-code/EDCM)

It is intended to bring the structural measurement work from **edcmbone**
together with the application work from **EDCM** in one place.

## Four-layer bootstrap

A minimal executable four-layer bootstrap now exists in `edcm/layers.py`.

- **Semantics layer**: tries to import from `ucns` and falls back to a local default.
- **Measurement layer**: tries to import from `edcmbone` and falls back to a local default.
- **Composition layer**: local orchestration default.
- **Delivery layer**: local output default.

### Usage

```python
from edcm import build_default_layers

layers = build_default_layers()
result = layers.run({"input": "example"})
print(result)
```

This allows the repository to run today even before upstream package wiring is fully settled.
