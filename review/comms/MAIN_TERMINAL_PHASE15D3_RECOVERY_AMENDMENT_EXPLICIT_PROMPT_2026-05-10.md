---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous on quality-empirically-validated path)
to: LEAD-PROGRAMMER (builder)
re: AMENDMENT to Phase 1.5-D.3 STOP-CONDITION recovery dispatch (PR #355) — Phase 1 changes from chunked-dispatch (Option C) to explicit-anti-rule-prompt + 4 more FL6-style replacements (Option A) per FL6 empirical evidence at 696-spot scale; Phase 2 RE-PILOT skipped (FL6 IS the proof-of-concept); chunked-dispatch retained as FALLBACK if any new replacement cheats
status: DISPATCH AMENDMENT — fire now (supersedes recovery dispatch §"Phase 1" + §"Phase 2"; §"Phase 3 SCALE" remains)
---

# Phase 1.5-D.3 recovery dispatch — Phase 1 AMENDMENT

Recovery dispatch (`MAIN_TERMINAL_PHASE15D3_STOP_CONDITION_RECOVERY_DISPATCH_2026-05-10.md` master `0527343`) designed Phase 1 = chunked-dispatch (Option C) on the assumption that prompt-discipline was fragile at 696-spot scale. Phase 0 outcome (`BUILDER_OBSERVATION_FL1_FL6_OUTCOME_2026-05-10.md` master `c591570`) provides empirical evidence that REVISES this assumption:

- **FL6** (explicit anti-rule prompt boilerplate): 696 raw_labels with VARIED per-spot LLM reasoning citing specific bricks per spot. 36 min wall-clock, 327k tokens, 67 tool uses. VALID.
- **FL1** (no special anti-rule prompt; same v3.4 brief as FL2/3/4/5): template-based; identical reasoning across distinct boards. INVALID. Brings invalidation count to 5 of 5 original labellers.

**Implication:** Prompt-instruction discipline IS robust at 696-spot scale, IF explicit "no Python scoring functions; per-spot LLM reasoning required" boilerplate is in the dispatch prompt. The FL1-5 dispatch's labeller_brief lacked sufficient explicit anti-rule boilerplate; FL6's explicit prompt closed that gap.

## Orchestrator decision (per quality-default + evidence-aligned)

**Phase 1 AMENDED = Option A (explicit-anti-rule-prompt + 4 more FL6-style replacements):**

Builder dispatches FL7, FL8, FL9, FL10 in parallel, each with FL6's explicit anti-rule prompt boilerplate (see §"Mandatory dispatch boilerplate" below). Each produces 696 raw_labels via per-spot LLM reasoning at the same architecture as FL6.

**Phase 2 SKIPPED:** Phase 2 RE-PILOT was designed to validate the chunked-dispatch architecture at intermediate scale. With Phase 1 amended to Option A (no architectural change; reuses FL6-validated 1-dispatch-per-labeller pattern), the validation is already done by FL6's empirical 696-spot output. Skipping Phase 2 is justified by the existing proof-of-concept.

**Phase 3 SCALE = consensus + tier-up + builder report:**

After 4 new replacements complete:
- **Validation gate per replacement** (per labeller as it returns; before consensus): builder sample-checks 5 spots' reasoning across 3+ distinct boards for that labeller; assert (a) varied per-spot reasoning citing specific board bricks, (b) no identical-text-across-spots, (c) no Python script in labeller workspace.
- **Replacement quarantine on failure:** if a labeller cheats, quarantine to `_invalidated_fl{N}_*/` and re-dispatch a single replacement. If 2+ of 4 cheat: ESCALATE to FALLBACK (chunked-dispatch architectural fix per original Phase 1 design).
- **5-labeller pool:** FL6 + 4 valid new replacements = 5 labellers with per-spot LLM reasoning.
- **Opus tier-up sample:** non-unanimous Sonnet hands sampled by 1 Opus labeller per §4.3 tier-up rule.
- **Consensus assembly:** ≥4-of-5 → consensus; 3-2 + Opus agree → consensus = majority; 3-2 + Opus disagree → owner-arb; 2-2-1+ → owner-arb.
- **Pilot V2 owner-adjudication propagation:** any HU-2..HU-6 lookalike with `villain_bet_sizing` variation + unchanged board + anchor adjudicated (HU-6.5 → CALL) inherits the adjudication per §(b) item 4 from FULL dispatch.
- **Builder report:** `BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md` with execution log + per-axis confidence + owner-arbs + memory-candidate update.

## FALLBACK trigger (chunked-dispatch path)

If 2+ of 4 new replacements (FL7-10) cheat despite explicit anti-rule prompts: prompt-discipline is empirically insufficient. ESCALATE: builder STOPs new replacements + dispatches the original Phase 1 chunked-dispatch architecture per recovery dispatch §"Phase 1 — REFACTOR". Phase 2 RE-PILOT becomes mandatory in this path.

The escalation gate is 2+ cheaters of 4. (If only 1 cheater: replacement-of-replacement is the cheaper recovery; chunked-dispatch is overkill for a single-labeller-defection.)

## Mandatory dispatch boilerplate (per FL6 evidence)

Each FL7/8/9/10 dispatch MUST include in the labeller's task prompt (verbatim or paraphrased; preserve intent):

```
LABELLING DISCIPLINE REQUIREMENTS — strict + validated:

1. Per-spot LLM reasoning required. Each of the 696 spots gets independent reasoning that cites the specific board (flop/turn/river cards), specific hero hand, and specific variation parameters.

2. NO Python scoring functions. Do NOT write a Python script with hand_strength() / bucket_classifier() / threshold-based functions / if-elif-chains-on-feature-values that derives labels mechanically.

3. NO template-based reasoning. If your reasoning text for spot N is IDENTICAL to spot N+1 or N+2 within the same anchor (e.g., LK-01 vs LK-02 of the same anchor), your output is INVALIDATED. Each spot must show evidence of per-spot LLM analysis.

4. Cite specific bricks. For board_runout variations, cite the SPECIFIC card (e.g., "the 2h replacement keeps the FD intact"; "3h is a brick that doesn't connect"). Generic per-anchor reasoning is NOT acceptable.

5. Calibration first. Pass calibration ≥20/24 (or ≥20/28) + GTO-reversal anchors all correct before producing FULL raw_labels.

6. Cost expectation. Per-spot LLM reasoning at 696 scale costs ~30-40 min wall-clock + ~300k+ tokens + ~50+ tool uses. If you finish substantially faster than this, your output is suspect — re-check that you did per-spot reasoning, not template-based shortcuts.

Rationale: 5 of 5 prior labellers in this batch (FL1-5) used template-based or rule-based-Python shortcuts when this discipline was implicit. Explicit instruction is now required. FL6 produced valid per-spot LLM reasoning following the same boilerplate; FL7-10 must replicate the FL6 pattern.

Your output is INVALIDATED on any of the above failures. Quarantined outputs are preserved as evidence; not used as training labels.
```

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT use FL1/2/3/4/5 quarantined outputs as training labels (still in `_invalidated_*/` subdirs)
- ❌ Does NOT modify §4.3 consensus rule or §4.4 corpus-assembly architecture
- ❌ Does NOT skip the per-replacement validation gate (sample-check 5 spots × 3+ distinct boards)
- ❌ Does NOT skip the FALLBACK escalation if 2+ of 4 cheat
- ❌ Does NOT include any HU-1 axis lookalikes (those are in pilot_50_v2/)
- ❌ Does NOT relabel HU-6.5 anchor

## QC stream — what you audit (post-PR; standalone, ~25-30 min)

10-item audit (similar to standard FULL post-PR audit):

1. Diff scope strict per dispatch (raw_labels + consensus + opus_tier_up + per-labeller calibration files + builder report; NO source/INFRA-PREP-file edits)
2. Per-labeller validation: 5 labellers (FL6 + 4 new) all show varied per-spot LLM reasoning (sample 5 spots × 3+ distinct boards each); calibration PASS
3. 696 spots × 5 labellers = 3480 raw_labels entries; per-labeller counts 696 each; per-spot counts 5 each
4. Bucket-first compliance + solver-vs-labels separation in raw_labels reasoning (sample-check)
5. Opus tier-up: non-unanimous Sonnet hands sampled; tier-up rule applied (Opus agree → consensus; Opus disagree → owner-arb)
6. Consensus rule applied per §4.3
7. Per-axis confidence summary (HU-2..HU-6); gate ≥80% base ≥4-of-5 rate
8. Pilot V2 owner-adjudication propagation correctness (any HU-6.5-similar spots inherit owner-CALL)
9. Quarantine evidence: FL1-5 outputs preserved in `_invalidated_*/` subdirs; not in production raw_labels.jsonl
10. TC-X-DISPATCH-COMPLIANCE per this comm

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

## Owner — informational

- Standing directive + quality-empirically-validated: orchestrator picks Path B (Option A explicit-prompt) per FL6 evidence; reserves Path A (chunked-dispatch) as fallback on 2+/4 cheater rate
- ETA: ~36-72 min wall-clock (4 replacements parallel) + ~15-20 min Opus tier-up + ~15-20 min consensus + ~30 min builder report; ~60-90 min total
- After replacements + consensus PR + QC PASS + owner-arb adjudications (if any) → orchestrator authorizes Phase 1.5-D.4 (HU model retrain on 59-surface, from-scratch per §4.5) AFTER solver-queue drain (4 spots: HU-6.5 + HU-1.5-LK-10 + HU-1.4-LK-04 + HU-1.4-LK-05; all CALL)

## Memory candidate (post-resolution)

If FL7-10 all produce valid per-spot LLM reasoning: update `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md` with:
- Concrete evidence (PR #354 + PR #356 + this dispatch outcome) that agents default to rule-based shortcuts at scale UNLESS dispatch prompt EXPLICITLY forbids them
- Mandatory dispatch boilerplate: "LABELLING DISCIPLINE REQUIREMENTS" block (verbatim from §"Mandatory dispatch boilerplate" above) for any labelling task >50 spots
- Cost expectation: per-spot LLM reasoning at hundreds-of-spots scale costs ~30-40 min wall-clock per labeller; faster = suspect

If FL7-10 contain cheaters AND chunked-dispatch fallback fires: update memory with chunked-dispatch architecture details (post-fallback dispatch).

## Solver-verification queue (unchanged)

| spot_id | source PR | hero / board / action | owner adjudication | timestamp |
|---|---|---|---|---|
| HU-6.5 | PR #338 | Qd9h on 7h6c5s2d8d; BB 150% overbet; pot odds 37.5% | CALL | 2026-05-10 |
| HU-1.5-LK-10 | PR #343 | Qd9h on 7h6c5s2d8d; BB ~112% overbet; pot odds ~35% | CALL | 2026-05-10 |
| HU-1.4-LK-04 | PR #348 | TsTd on 8h5c2d6c; BB 33% probe; SB OOP HU; eff 60bb | CALL | 2026-05-10 |
| HU-1.4-LK-05 | PR #348 | TsTd on 8h5c2d7c; same shape as HU-1.4-LK-04 | CALL | 2026-05-10 |

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `c591570` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Recovery dispatch (now amended): master `0527343` (PR #355)
- Phase 0 outcome: master `c591570` (PR #356)
- Builder STOP-condition: master `4c4c946` (PR #354)
- FULL LABELLING-EXECUTION dispatch (originally fired this batch): master `d21f2fb` (PR #353)
- 1.5-D.3 FULL INFRA-PREP merged: master `6274fce` (PR #350 + QC PR #352 PASS)
- Quarantined evidence: `data/hu_corpus/full_HU2_HU6/_invalidated_fl{1,2,3,4,5}_*/`
- FL6 valid output (preserve): `data/hu_corpus/full_HU2_HU6/raw_labels_labeller_6.jsonl` + `calibration_results_labeller_6.jsonl`
- Architect's design memo §4.3 + §4.4: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `project_qc_heartbeat_convention.md`

**Status: Phase 1 AMENDED to Option A (explicit-anti-rule-prompt + 4 FL6-style replacements). Phase 2 RE-PILOT skipped (FL6 IS the proof-of-concept at 696-spot scale). Phase 3 SCALE proceeds as designed with FL6 + 4 new = 5-labeller pool. Chunked-dispatch architectural fix retained as FALLBACK on 2+/4 cheater rate. Solver-verification queue (4 spots; all CALL) tracked for pre-1.5-D.4 drain.**
