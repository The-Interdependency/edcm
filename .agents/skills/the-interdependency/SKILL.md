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
- **Resource-run preflight and completion**: Resource scarcity requires contemplation **before** a compute run begins. Before launch, inspect or estimate whether available time under real external constraints, CPU, memory, disk, battery/power, network, quotas, API/tool usage limits, and session/process durability are sufficient for the run to reach its natural terminal condition. If there is material doubt that it can finish, do not start it: reduce, stage/checkpoint, relocate, acquire resources, or leave it `hmmm`. Once a healthy run begins, let it finish to completion or deterministic computational failure unless the user explicitly cancels it or an unforeseen real resource/safety emergency requires interruption. Do **not** invent or enforce a wall-clock cutoff merely to make work bounded, falsifiable, or convenient. Runtime/resource ceilings are stopping criteria only when the quantity is itself load-bearing to the hypothesis or acceptance criterion, an authorized safety boundary, or a real externally imposed hard limit, and they must be justified before launch.
- **METAPAT consultation gate**: Consult current `The-Interdependency/metapat` before committing a conceptual choice when the task must decide which distinctions, relations, boundaries, transformations, scales, or cross-domain correspondences should organize downstream work. METAPAT consultation is also required when an unresolved conceptual choice would constrain architecture, semantics, measurement, ontology, or later falsifiable claims. Do not consult METAPAT merely to execute an already-fixed implementation, run tests, repair syntax, move data, or apply a relation whose meaning and boundary are already established. METAPAT is the source of truth for its own doctrine; skill-lib routes to it and must not duplicate a frozen theory snapshot.
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

## METAPAT consultation test

Ask one question before conceptual or architectural commitment:

> Am I deciding **what relation/boundary/transformation should exist or matter**, or merely implementing one already established?

Consult METAPAT for the first case. Continue locally for the second.

Strong consultation triggers:

- choosing or revising an architecture-level distinction;
- deciding whether a boundary deserves independent status;
- comparing similarly shaped transformations across different domains;
- importing a domain term, metaphor, formula, or ontology into another layer;
- deciding what remains invariant across scale or representation change;
- a design choice is being mistaken for an empirical or mathematical claim, or vice versa;
- an unexplained but productive discovery path is at risk of being removed only because its mechanism is not yet known;
- two repos disagree because they encode different conceptions of the same relation rather than because of an implementation bug.

Non-triggers:

- routine refactors under fixed contracts;
- dependency/version updates;
- deterministic data ingestion;
- tests whose expected relation is already declared;
- formatting, documentation, packaging, CI, deployment, or syntax repair;
- independent recovery of a result after the discovery result and comparison criterion are already frozen.

When consultation triggers, inspect the current METAPAT repository state before deciding. At minimum resolve the relevant current axioms, postulates, domain-restraint rules, and any directly applicable theory/implementation boundary. Do not import historical skill-lib `meta` wording as authority over current METAPAT.

## Workflow

1. **Trigger detection**: Activate on any The-Interdependency context or the example trigger phrases listed in the description.
2. **Resource preflight**: Before starting any compute run, decide whether the available resources can sustain it to its natural terminal condition. If not, do not launch it. Do not substitute an arbitrary timeout for preflight judgment.
3. **METAPAT gate**: Before conceptual or architectural commitment, run the consultation test above. If triggered, inspect current METAPAT before selecting the relation, boundary, transformation, or cross-domain mapping.
4. **Context assembly**: For transcript work, explicitly structure output using EDCMBONE energy-dissonance mapping, F-metrics, failure-mode tags, and accessibility annotations. Preserve full original relations.
5. **Artifact production**: Write code/docs with msdmd blocks (if applicable) + dedicated "Usage Guidance" section or equivalent. Include examples that can be copy-pasted.
6. **GitHub hygiene**: Check drift, update indexes, propagate only after validation. Reference this skill in commit messages where relevant.
7. **Output packaging**: Structure responses with:
   - Preserved structure / epistemic layers first.
   - EDCMBONE-mapped analysis where transcripts are involved.
   - Usage guidance and examples.
   - `hmmm` boundaries clearly marked.
   - Smallest next patch or action.

## Anti-patterns

- Flattening, dropping variables, or losing topology/relations before acting or summarizing (directly conflicts with neurodivergence preservation).
- Starting a compute run when available resources have not been considered sufficiently to expect completion.
- Terminating a healthy compute run because of an arbitrary wall-clock limit that was not actually load-bearing to the claim, safety boundary, or external resource limit.
- Producing code, docs, or analysis without explicit usage guidance and examples.
- Assembling or analyzing EDCMBONE transcripts without applying the framework's energy circuit, F-loss, and failure-mode model.
- Performing GitHub or org maintenance without drift checks or index updates.
- Canonizing inferred patterns without source backing (pair with `canon` skill).
- Omitting `hmmm` when uncertainty or missing source exists.
- Treating repo-local copies as canonical source of truth.
- Using METAPAT to decorate a routine implementation decision.
- Making a conceptual architecture choice that crosses the METAPAT gate without consulting current METAPAT.
- Copying METAPAT doctrine into skill-lib and allowing the copy to become a competing authority.

## Output Rubric (active whenever this skill is loaded)

- Lead with preserved relational structure and epistemic status.
- Transcript tasks → EDCMBONE-structured output (energy maps, F1–F6 tags, accessibility notes, full topology).
- Code / docs → msdmd blocks where fitting + prominent, copy-pasteable "Usage Guidance" with examples and integration notes.
- GitHub / research → Drift status noted, index updates performed, relevant skills cross-referenced.
- If the METAPAT gate triggered, state what conceptual boundary required consultation and preserve any remaining `hmmm`.
- Always close with actionable next steps and any open `hmmm` items.

hmmm
- Precise harness integration for automatically fetching current METAPAT after this gate triggers; the skill currently defines the decision rule and source-of-truth boundary, while the consuming agent uses its available GitHub/local-repo access.
- Whether the historical `meta` skill should remain as a compatibility router or be removed after all consumers propagate this gate.
- Whether a companion metadata-block skill (e.g. `# === TIW_WORKFLOW ===` or `# === INTERDEPENDENCY ===`) should be added for self-declaring modules inside The-Interdependency repos.
- Deeper integration with a0p-instancing / agent-instantiation so that TIW-context automatically loads this skill for sub-agents.
- Exact canonical reference for the full EDCMBONE transcript assembly protocol — should the detailed steps live in this skill or be expanded inside the edcmbone repo's own skill definitions?
