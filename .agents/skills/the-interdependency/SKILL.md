---
name: the-interdependency
description: Protocol and workflow for all tasks involving The Interdependency organization, its repositories, The Interdependent Way projects, EDCMBONE transcript analysis, code building, research, GitHub maintenance and updates. Load this whenever the task or context touches The-Interdependency assets, or on phrases like "assemble edcmbone transcripts for analysis", "write code that...", or any GitHub/research/build work on org projects.
---

# the-interdependency — Workflow Protocol for The Interdependency Projects

`the-interdependency` is a procedural skill that enforces consistent, high-fidelity, structure-preserving practices when working inside The Interdependency ecosystem (org repos, The Interdependent Way artifacts, skill-lib, edcmbone, ucns, pcea, a0, aimmh, etc.). It ensures EDCMBONE analysis follows framework conventions, code and docs always carry usage guidance, GitHub ops respect org standards, and neurodivergence-compatible structure is preserved.

## Load this when

- Any task, research, code, or context mentions The-Interdependency, The Interdependent Way, interdependentway.org, Harrison Hovel, or any repository under the The-Interdependency GitHub organization.
- User requests include: "assemble edcmbone transcripts for analysis", "write code that..." (or similar), GitHub maintenance, updates, pushes, repo hygiene, or cross-project work.
- Building, editing, reviewing, or shipping code, specs, documentation, or analysis artifacts destined for or affecting The-Interdependency projects.
- Performing GitHub operations on org repositories (commits, branches, PRs, issues, propagation, drift checks).
- Working with skill-lib itself, canon, msdmd blocks, or propagating skills to target repos.

## Core Doctrine

- **Structure preservation first**: Before any summarization, compression, decision, or output, preserve the complete relational structure, variables, topology, epistemic status (declared / implemented / inferred / hmmm), distinct layers (lived experience vs formal claims vs emotional), and explicitly mark all unresolveds. This follows the org's neurodivergence-preserving interaction principles.
- **EDCMBONE transcript assembly & analysis**: When the task involves assembling or analyzing transcripts (e.g. for EDCMBONE / Energy Dissonance Circuit Model Bound Operator Numerical Evaluation), apply the established EDCMBONE lens: map energy flows and dissonance circuits, compute/report F-loss metrics (fidelity, deletion, inversion, collapse detection), tag F1–F6 failure modes, segment for cognitive accessibility (especially neurodivergent readers), and preserve transcript topology. Do not improvise assembly; extend or adhere to patterns from the edcmbone repository.
- **Code writing standards**: When writing or modifying code that touches The-Interdependency:
  - Use msdmd self-declaration blocks (`# === BLOCK_NAME ===` ... `# === END BLOCK_NAME ===`) wherever the module fits an existing or new metadata skill.
  - **Always include prominent usage guidance**: runnable examples, invocation patterns, integration notes, edge cases, limitations, and how the code participates in larger workflows (e.g. a0p/AIMMH orchestration, EDCMBONE analysis pipelines).
  - Respect ratios, test contracts, dependency declarations, ownership, and risk boundaries per the relevant skills.
  - For new modules, begin with `meta-module-build` patterns.
- **GitHub maintenance & updates**: 
  - Follow org conventions in `ORG_DISTRIBUTION.md` (install paths `.agents/skills/`, propagation rules).
  - Before/after changes, run available drift checkers and update machine-readable indexes (`skills.json`, README tables, AGENTS.md pointers).
  - Use clear commit messages that reference affected skills or the change class.
  - When propagating skill-lib changes, prefer the canonical `tools/propagate_skills.py` (or equivalent) with `--apply` only after dry-run validation.
- **Usage guidance requirement**: Every code file, SKILL.md update, README change, research summary, or artifact produced under this skill **must contain clear, actionable usage guidance**. This is non-negotiable for accessibility, onboarding, and reducing signal loss.
- **Research & canon alignment**: Ground all claims in source-backed canon (cross-load `canon` skill). Use `char-compress` for context handoff. Leave genuine uncertainty as `hmmm`.

## Workflow

1. **Trigger detection**: Activate on any The-Interdependency context or the example trigger phrases listed in the description.
2. **Context assembly**: For transcript work, explicitly structure output using EDCMBONE energy-dissonance mapping, F-metrics, failure-mode tags, and accessibility annotations. Preserve full original relations.
3. **Artifact production**: Write code/docs with msdmd blocks (if applicable) + dedicated "Usage Guidance" section or equivalent. Include examples that can be copy-pasted.
4. **GitHub hygiene**: Check drift, update indexes, propagate only after validation. Reference this skill in commit messages where relevant.
5. **Output packaging**: Structure responses with:
   - Preserved structure / epistemic layers first.
   - EDCMBONE-mapped analysis where transcripts are involved.
   - Usage guidance and examples.
   - `hmmm` boundaries clearly marked.
   - Smallest next patch or action.

## Anti-patterns

- Flattening, dropping variables, or losing topology/relations before acting or summarizing (directly conflicts with neurodivergence preservation).
- Producing code, docs, or analysis without explicit usage guidance and examples.
- Assembling or analyzing EDCMBONE transcripts without applying the framework's energy circuit, F-loss, and failure-mode model.
- Performing GitHub or org maintenance without drift checks or index updates.
- Canonizing inferred patterns without source backing (pair with `canon` skill).
- Omitting `hmmm` when uncertainty or missing source exists.
- Treating repo-local copies as canonical source of truth.

## Output Rubric (active whenever this skill is loaded)

- Lead with preserved relational structure and epistemic status.
- Transcript tasks → EDCMBONE-structured output (energy maps, F1–F6 tags, accessibility notes, full topology).
- Code / docs → msdmd blocks where fitting + prominent, copy-pasteable "Usage Guidance" with examples and integration notes.
- GitHub / research → Drift status noted, index updates performed, relevant skills cross-referenced.
- Always close with actionable next steps and any open `hmmm` items.

hmmm
- Precise auto-detection triggers or harness integration for automatic loading of this skill (currently relies on description match in agent harness).
- Whether a companion metadata-block skill (e.g. `# === TIW_WORKFLOW ===` or `# === INTERDEPENDENCY ===`) should be added for self-declaring modules inside The-Interdependency repos.
- Deeper integration with a0p-instancing / agent-instantiation so that TIW-context automatically loads this skill for sub-agents.
- Exact canonical reference for the full EDCMBONE transcript assembly protocol — should the detailed steps live in this skill or be expanded inside the edcmbone repo's own skill definitions?
