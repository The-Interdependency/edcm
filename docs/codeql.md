# CodeQL source-size configuration

The repository-owned `.github/workflows/codeql.yml` scans Python, GitHub Actions
and JavaScript/TypeScript with the existing `security-extended` suite. It runs on
main pushes, pull requests, merge groups, weekly Wednesday scans and manual runs.

The previous JavaScript extractor skips `edcm_msdmd.ts` because its 13.4 MB size
exceeds the default 10 MB source-file cutoff. The supported override is
`CODEQL_EXTRACTOR_JAVASCRIPT_MAX_FILE_SIZE`, expressed in decimal megabytes.

The JavaScript job computes the largest tracked file's size at each checkout and
rounds up to whole megabytes before initializing CodeQL. Its allowance therefore
tracks the actual source instead of imposing another fixed ceiling. The metadata
collection remains the exact canonical output.

Upstream implementation: [AutoBuild's source-size check](https://github.com/github/codeql/blob/main/javascript/extractor/src/com/semmle/js/extractor/AutoBuild.java)
and [the environment-variable reader](https://github.com/github/codeql/blob/main/javascript/extractor/src/com/semmle/js/extractor/EnvironmentVariables.java).

## Activation and verification

The repository currently uses GitHub's automatic default setup. Applying the
workflow requires switching CodeQL to advanced setup in repository Settings,
Advanced Security. GitHub's default setup controls its own environment and blocks
advanced-workflow result uploads while it remains enabled. See [setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types).

After switching, run the `CodeQL` workflow and inspect `Analyze
(javascript-typescript)`. The sizing step must report an allowance covering the
largest source, and the extraction log must report successful extraction of
`edcm_msdmd.ts`. Require successful analysis and result publication for all three
languages. A completed sizing step alone does not establish scanner coverage.

If extraction exceeds runner capacity, retain the actual error and choose a
suitable runner before restarting it. To roll back, restore the preceding scan
configuration; its original 10 MB failure remains an explicit limitation.

hmmm: advanced-setup activation and successful hosted extraction/publication are
required before this change can be called active.

GPT generated; context, prompt Erin Spencer.
