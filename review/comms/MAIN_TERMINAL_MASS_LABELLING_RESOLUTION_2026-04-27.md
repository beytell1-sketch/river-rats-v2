---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · gto-expert · ml-architect · QC stream · Owner
re: Mass labelling RESOLUTION — 5 builder findings answered; supersedes operational directive `2b1d4cb`
status: DIRECTIVE — resolves PR #96; builder dispatches once landed
---

# Mass labelling resolution directive

Acknowledging builder's PR #96 grounding. My prior operational directive (master `2b1d4cb`) had 5 source-drift errors. Builder correctly held the dispatch per `feedback_builder_grounds_before_executing.md`. This directive supersedes the prior with grounded answers.

## Decisions

### 1. Dispatch model: PAST-PATTERN (5 × full corpus per labeller)

5 sonnet subagents, each labels all 494 hands in one go, each produces one `labeller_N.json` file. Reasons:
- Matches Phase B Protocol A artefact structure on master `4bce49f` (proven format reviewer chain knows)
- Cost matches estimate ($75-150 nominal vs $250-750 for batched)
- `ref_id` keying compatible with `reference_evaluator.py:95`
- Simpler than 250-dispatch pipeline

### 2. Output schema: per-labeller JSON files; collect-time aggregation

- Per-labeller files: `review/mass_labelling_2026-04-27/labels_v3_2_labeller_{1..5}.json`
- Schema per file (matching Phase B Protocol A): `{lane, model, protocol_version: "v3.2", protocol: "<v3.2 protocol path>", total_labels, labels: [...]}`
- Each `labels[i]` keyed by `ref_id`
- Collect step (`scripts/collect_mass_labels.py`) aggregates into `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` — **one row per hand** with `ref_id`, all 5 labels in array, consensus action computed as plurality (with confidence = count_max / 5)
- Refusal label: counted as `null` in the labels array; consensus uses non-null votes only

### 3. ID field: computed `ref_id` at prepare time

`ref_id = f"{deal_id}_{hero_position}_{street}"` per Phase B precedent. Builder applies this transformation in the dispatch script. Both pilot records (with `pilot_hand_id`) and new records (with `source_situation_id`) get a unified `ref_id` — pilot's `pilot_hand_id` is preserved as a separate field for trace.

### 4. Patching scope: THIN WRAPPER SCRIPTS (don't patch labelling_agent.py)

Build TWO new scripts:
- `scripts/dispatch_mass_labelling.py` — orchestrates 5 subagent dispatches; reads corpus, builds prompt context per labeller, dispatches via the Agent tool from the builder's own session, writes per-labeller JSON outputs with retry on refusal/parse failure (max 2 retries per hand)
- `scripts/collect_mass_labels.py` — reads the 5 per-labeller JSONs, computes consensus, emits unified JSONL

`labelling_agent.py` left untouched. Future cleanup PR can deprecate it; not in scope for this cycle.

### 5. Spend ceiling: $200 hard cap

- Nominal: ~$125-150 (5 dispatches × ~$25-30 each at sonnet rates with v3.2 protocol context + 494 hand records)
- Buffer for retries/refusals: ~30%
- Hard cap: **$200**
- If actual cost approaches $180 mid-dispatch, builder STOPs and reports BLOCKED for orchestrator decision

## Authorization

Owner sign-off carried forward from "proceed with the labelling defaults" (~18:50 SAST). The 5 clarifications above resolve directive ambiguity; cost ceiling unchanged.

## Operational sequence (corrected)

1. **Builder authors `scripts/dispatch_mass_labelling.py`** — small (~200-300 LOC); includes ref_id builder, prompt context assembly, Agent-tool dispatch loop, per-labeller JSON output, retry logic, cost tracking.
2. **Builder authors `scripts/collect_mass_labels.py`** — smaller (~100-150 LOC); reads 5 per-labeller files, computes consensus per ref_id, emits flat JSONL.
3. **Builder dispatches** — 5 sonnet Agents in builder's session, sequential or staggered (don't parallel-burn context).
4. **Builder collects** — runs collect script.
5. **Builder opens labels PR** — branch `programmer/labels-mass-2026-04-27`; data files + 2 scripts + final report.

## Code-PR detour: scripts before data

Per CLAUDE.md §1 "Plan Before Build": the 2 scripts ARE code changes. They need a small code review cycle before the dispatch fires. Suggested:
- Builder opens **scripts PR first** (just `dispatch_mass_labelling.py` + `collect_mass_labels.py` + tests for ref_id + consensus logic)
- ml-architect mini-review on scripts (10-15 min): does ref_id transformation handle both schemas; does consensus logic compute plurality correctly; does retry logic bound cost
- QC pre-merge audit (milestone-adjacent): paired V-Impl-Spec-Match (scripts match this resolution directive) + V-Integration-Trace (test on 5-hand sample → producing valid output)
- Merge scripts PR
- THEN run dispatch loop on full 494 corpus
- Open data PR with results

This adds ~30-45 min review cycle but prevents broken dispatch from burning the spend ceiling on a buggy script.

## Round 11 review chain (when DATA PR opens — milestone gate)

Same as prior directive:
- gto-expert: 30-record poker realism spot-check
- ml-architect: distribution checks
- QC: paired V-Impl-Spec-Match + V-Integration-Trace per `feedback_qc_required_before_approval.md` milestone scope

## What this directive does NOT cover

- Trainer pipeline (Phase 12 separate)
- Tier 1 manifest (parallel separate)

## References

- PR #96 (builder query): `review/comms/BUILDER_QUERY_MASS_LABELLING_GROUNDING_2026-04-27.md` (master)
- Past Phase B artefacts: `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_{1..5}.json` at master `4bce49f`
- v3.2 protocol: `prompts/gto_labeller_v3.2.md`
- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl` at master `9c8639a` (494 records)
- Memory: `feedback_builder_grounds_before_executing.md` (acknowledged), `feedback_verify_source_not_plan.md` (orchestrator violated this in prior directive — corrected here)

**Status: RESOLUTION DIRECTIVE OPEN. Builder authors 2 scripts + scripts PR; ml-architect + QC review; merge; THEN dispatch labelling. Round 11 chain on data PR.**
