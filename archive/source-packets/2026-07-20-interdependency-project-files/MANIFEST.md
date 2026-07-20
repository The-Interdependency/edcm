# EDCM packet manifest

Source packet: `interdependency_project_files.zip`  
Review date: 2026-07-20  
EDCM-classified files: 12

Hashes are SHA-256 over the uploaded bytes.

| Uploaded filename | Bytes | SHA-256 | Placement status |
|---|---:|---|---|
| `EDCM__260125_181916.txt` | 28,607 | `f66aab2c507f331020989bae550dde1ee85f87c400f52497de1c605ffac83334` | historical engine narrative |
| `EDCM_metrics.txt` | 31,953 | `ae735bf8d1286d9760a9823c32cc6f99f24281bcf4dafdeaf7974a5beb1194f0` | historical alternate metric system |
| `canon_definitions_invariants.md` | 10,932 | `01fbb4ab3fec6c2f52e285135055fd840712756419d5f43d9d32ff307a519cb6` | earlier cross-project aggregator |
| `canon_definitions_invariants-1.md` | 12,417 | `ddf2542d4404aac4c14fd56db9ef5ea840171967cf8de71d417bbe7ad82c9af4` | later cross-project aggregator |
| `canon_definitions_invariants-2.md` | 12,417 | `ddf2542d4404aac4c14fd56db9ef5ea840171967cf8de71d417bbe7ad82c9af4` | exact duplicate of `-1` |
| `core_thresholds_Version3.md` | 4,315 | `6fc6c2349e43619ccfe901dd09a5966804a1ccc297f51380c837d384b62ee722` | unvalidated threshold/state design |
| `edcmbone_pivot.txt` | 11,550 | `56bd82bb9b3365a16cb03468014161820a091215738bd3d1f0b6eea5109c7a2c` | historical repository architecture |
| `edcmbone_v1.txt` | 23,557 | `a109fe28f47cbafd6ae54dc4afc565803c992e080c80004fab7018715bbf8fc5` | historical functional canon draft |
| `closed_tokens.py` | 24,487 | `c89b973f117f81ca721ab5272d5f586a4566584cc3a62029c95b9fd03ea15adc` | pre-reset UCNS encoder lineage |
| `test_closed_tokens.py` | 9,583 | `93b047de02543ff6ceac3aa1487aa9f5742ce3d018b782924d107da3db198bc18` | passing legacy encoder tests |
| `pipeline_py.py` | 7,842 | `a49cc09662e43e67fb2f142a383cc058e7228b39764ec03b649cf388742cc07d` | historical scaffold |
| `lexicon_pv_v1.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty placeholder; no payload |

## Review notes

- `canon_definitions_invariants-1.md` and `-2.md` are byte-identical.
- The later canon aggregator changes PCNA/PCTA meanings and adds PTCA, proving
  that the packet itself contains moving cross-project doctrine rather than one
  immutable EDCM authority.
- The closed-token test suite passes all 196 listed tokens against its legacy
  16-gon model. This validates determinism within that model, not conformity to
  current UCNS canon.
- All Python files in the full packet compile.

## Exclusions

No private business-record filename, address, payment fragment, or document hash
is published in this manifest. Other-project files were routed or withheld as
stated in the review README.

## hmmm

This manifest establishes provenance for review without freezing any alternate
metric formula or pre-reset geometry into active EDCM canon.