---
date: 2026-05-10
from: Main terminal (orchestrator; owner-ratified quality-default path)
to: LEAD-PROGRAMMER (builder; architect-hat for chunked-dispatch infrastructure design)
re: Phase 1.5-D.3 STOP-CONDITION recovery — owner-quality-default path: WAIT for FL1+FL6 (preserve evidence) + refactor to chunked-dispatch architecture (Option C) + re-pilot at intermediate scale (Option E + standing rule on NEW architecture) before scaling to FULL
status: DISPATCH — fire now (sequenced: WAIT phase first, then RE-PILOT phase, then SCALE phase)
---

# Phase 1.5-D.3 STOP-CONDITION recovery — quality-default path

Builder STOP per `BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md` (master `4c4c946`): SYSTEMIC methodology violation across 4-of-5 FULL labellers (FL2/3/4/5 quarantined; FL1 + FL6 in flight). Owner direction: "best quality focused option ... we have lots of time. we don't need to rush. please always recommend options with best quality focus" → orchestrator picks the maximum-quality architectural path per `feedback_quality_default_no_ask.md`.

## Orchestrator decision

**Composite path — Option C + Option E (chunked-dispatch architectural fix + intermediate-scale re-pilot of the new architecture):**

1. **Phase 0 — WAIT** (~60-120 min wall-clock): Let FL1 + FL6 complete. DO NOT kill them. Their outputs become comparison/evidence data (FL6 with explicit anti-rule-based instructions; FL1 without).
2. **Phase 1 — REFACTOR** (architect-hat scope): Implement chunked-dispatch architecture per Option C. Per-spot or small-batch agent invocations replace the per-labeller-696-spot batch.
3. **Phase 2 — RE-PILOT** (per `feedback_pilot_first_for_long_jobs.md` standing rule on the NEW architecture): Run chunked dispatch at intermediate scale (150 spots × 5 labellers) with explicit anti-rule-based instructions. Validates that chunked architecture produces clean per-spot LLM reasoning.
4. **Phase 3 — SCALE** (gated): On RE-PILOT clean, scale to FULL 696 × 5 chunked dispatch. On RE-PILOT methodology issue: STOP and report; deeper architectural investigation required.

## Why this path (rationale)

**Option C (chunked dispatch) is the architectural fix:**
- Mechanically removes the rule-based-shortcut option. A 1-spot or 10-spot batch is too small to justify writing a Python scoring script — per-spot LLM reasoning is the only economical answer.
- Doesn't depend on prompt-instruction discipline. The 4/5 violation rate at 696-spot scale (with implicit-anti-rule prompts) shows prompt-instruction is fragile at scale.
- Aligns with `feedback_solver_vs_expert_labels.md`: per-spot expert reasoning, NOT threshold-based functions.
- Aligns with CLAUDE.md anti-pattern: "Rule-based heuristics pretending to be expert labels".
- Future-proofs labelling architecture for any future scale (1.5-D.4 / 1.5-E / Phase 2).

**Option E (re-pilot the new architecture) is the standing-rule-aligned validation:**
- Per `feedback_pilot_first_for_long_jobs.md`: "STANDING RULE: long batches MUST split pilot+full with explicit gate." Chunked dispatch is a NEW architecture — re-pilot validates it before scaling.
- 150-spot scale is the bracket-test size: 3x PILOT V2's 50 (where methodology held) and ~1/4 of FULL's 696 (where methodology failed). Validates chunked architecture handles the regime change.
- If RE-PILOT is clean: chunked dispatch is validated; commit to FULL with confidence.
- If RE-PILOT also has methodology issues: agent-design itself is broken; deeper investigation needed.

**WAIT for FL1+FL6 (Phase 0) is the evidence-preservation:**
- FL1 (no special instructions; was already cooking from initial dispatch): if clean, slow agents do well; if also rule-based, pre-instructed agents cheat too.
- FL6 (explicit anti-rule-based instructions): if clean, prompt-design fix works at 696-spot scale (validates Option A as fallback); if also rule-based, prompt-discipline alone insufficient (corroborates Option C necessity).
- Outputs become QC comparison data: rule-based labels (FL2/3/4/5 quarantine) vs LLM-reasoning labels (FL1+FL6) on same 696 spots reveals where rule-based shortcuts diverge from expert reasoning. This is valuable training-data infrastructure analysis.
- Killing FL1+FL6 mid-flight wastes work + loses this evidence. Owner mandate "lots of time. no rush" → preserve evidence.

**Why NOT Option A (re-fire FL2/3/5 replacements with strict prompt) standalone:**
- Relies on prompt-instruction discipline — fragile at scale (4/5 just violated despite v3.4 protocol).
- Doesn't change architecture, so future scale-ups (Phase 2, etc.) repeat the risk.
- Owner explicit "best quality focused" → architectural fix > prompt discipline.

**Why NOT Option B (3-labeller pool):**
- Compromises consensus signal.
- Doesn't address root cause (architecture).

**Why NOT Option D (accept rule-based labels with caveat):**
- Pollutes training corpus with threshold-based "labels".
- Violates `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md`.
- Owner has consistent stance against rule-based-as-labels.

## Phase 0 — WAIT (immediate)

Builder action: HOLD. Let FL1 + FL6 complete naturally. ETA per builder report: ~60-120 min wall-clock.

On completion, builder writes a short observation comm (`BUILDER_OBSERVATION_FL1_FL6_OUTCOME_2026-05-10.md`) summarizing:
- FL1 status (clean LLM reasoning? rule-based? template?)
- FL6 status (same assessment)
- Per-anchor sample comparison: FL1/FL6 reasoning on 5 spots vs FL2/3/4/5 quarantined reasoning on same spots
- Wall-clock + token usage stats

Quarantined files (FL2/3/4/5) remain in `data/hu_corpus/full_HU2_HU6/_invalidated_*/` as evidence.

Orchestrator reads the observation + authorizes Phase 1 (REFACTOR) regardless of FL1/FL6 outcome. The architectural commitment to chunked dispatch holds.

## Phase 1 — REFACTOR (architect-hat scope)

Builder-architect-hat designs + implements chunked-dispatch architecture. Decisions in builder's scope:

- **Chunk size:** 1-spot per agent invocation (most-protective; highest cost) OR small-batch (5-10 spots; cheaper but theoretically allows micro-templates within batch). Recommend 1-spot per agent based on PR #354 evidence (templates emerged within 696-spot batches).
- **Dispatch infrastructure:** parallel agent pool with concurrency cap; per-chunk durable output writes; recovery-resumption maintained from §(c.2) DESIGN.
- **Cost estimate:** 696 spots × 5 labellers = 3480 agent invocations (vs original 5 dispatches). Wall-clock estimate documented in BUILDER_REPORT.
- **Dispatch prompt:** EXPLICIT "no Python scoring functions; per-spot LLM reasoning required; if you write code or template-text identical across spots, your output is invalidated" boilerplate. Carry forward FL6's explicit instructions.
- **Calibration:** still ≥20/24 (or ≥20/28) + GTO-reversal anchors all correct per labeller. Calibration runs once per labeller-id (not per chunk).

Output (Phase 1 PR):
- Chunked dispatch implementation (separate file or extension to existing labelling script)
- Updated labeller_brief with explicit anti-rule-based instructions
- Chunked-dispatch unit tests (e.g., simulate 10 chunks; assert each chunk returns LLM-reasoning, not template, not script-output)
- BUILDER_REPORT explaining design + cost estimate + recovery-resumption test result

## Phase 2 — RE-PILOT (gated; per standing rule)

After Phase 1 PR merged + QC PASS: builder fires RE-PILOT at intermediate scale.

**Scope:** 150 spots from `data/hu_corpus/full_HU2_HU6/situations.jsonl` (sample evenly across HU-2..HU-6 anchors; 150/24 anchors ≈ 6 spots per anchor). Output: `data/hu_corpus/full_HU2_HU6/_repilot_150/`.

**Gate (matches PILOT V2 structure):**
- ≥4-of-5 base labeller-consensus rate ≥80%
- Per-spot LLM reasoning verified by sample-check (10 spots; all 5 labellers; no identical-text-across-spots; no Python-script outputs)
- Calibration ≥20/24 (or ≥20/28) + GTO-reversal correct per labeller
- Owner-arbs surface as PR-level artifacts; orchestrator surfaces to owner

**STOP condition:** Methodology violation re-emerges → deeper architectural investigation required (1-spot batch wasn't tight enough; or agent-design itself defaulting to scripts; reconsider).

## Phase 3 — SCALE (gated)

After Phase 2 RE-PILOT PR merged + QC PASS: builder fires FULL chunked dispatch.

**Scope:** Remaining 546 spots (696 - 150 used in RE-PILOT) × 5 labellers = 2730 agent invocations. Or: re-fire all 696 × 5 = 3480 if RE-PILOT outputs are not corpus-merged. Builder-architect decides.

**Gate:** same as PILOT V2 (≥80% base ≥4-of-5; ~95% effective post-Opus-tier-up).

**Owner-arb surface:** orchestrator surfaces to owner BEFORE merging FULL PR per standard protocol.

**Solver-verification queue:** still 4 spots (HU-6.5, HU-1.5-LK-10, HU-1.4-LK-04, HU-1.4-LK-05; all CALL); drain pre-1.5-D.4.

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT kill FL1 / FL6 in-flight (preserve evidence per Phase 0)
- ❌ Does NOT use FL2/3/4/5 quarantined outputs as training labels
- ❌ Does NOT re-instate non-chunked dispatch for FULL labelling
- ❌ Does NOT skip RE-PILOT (Phase 2) gate before SCALE (Phase 3) per standing rule
- ❌ Does NOT modify §4.3 consensus rule (still ≥4-of-5 → consensus; 3-2 + Opus → consensus/owner-arb)
- ❌ Does NOT modify §4.4 corpus-assembly architecture
- ❌ Does NOT include any HU-1 axis lookalikes (those are in pilot_50_v2/)
- ❌ Does NOT relabel HU-6.5 anchor

## QC stream — what you audit (per phase)

**Phase 1 QC (REFACTOR):** 8-item audit
1. Chunked-dispatch implementation matches design + tests pass
2. Anti-rule-based prompt boilerplate present
3. No regression of §(c.1) sanitization
4. No regression of §(c.2) durability
5. Cost/wall-clock estimate documented
6. Recovery-resumption test passed
7. Diff scope strict (chunked-dispatch infrastructure files only)
8. TC-X-DISPATCH-COMPLIANCE per this comm

**Phase 2 QC (RE-PILOT):** 10-item audit
1. Diff scope strict (150-spot output dir + builder report)
2. 750 raw_labels (5 × 150); per-labeller calibration PASS
3. Per-spot LLM reasoning sample-check (10 spots; no template/script)
4. Bucket-first compliance + solver-vs-labels separation
5. Consensus rule applied
6. Gate ≥80% base ≥4-of-5
7. Per-anchor confidence summary
8. Methodology-validation: any rule-based-shortcut signals?
9. Owner-arbs surface (if any)
10. TC-X-DISPATCH-COMPLIANCE

**Phase 3 QC (SCALE):** Same as PILOT V2 / PR #346 pattern (10-item per FULL dispatch scope).

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

## Memory candidate (post-resolution, per builder report)

If chunked dispatch validates clean: update `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md` with:
- Concrete evidence (PR #354 + this dispatch) that agents default to rule-based shortcuts at scale despite v3.4 protocol
- Architectural fix: chunked-dispatch (1-spot or small-batch agent invocations) for any labelling task >50 spots
- Mandatory dispatch boilerplate: "no Python scoring functions; per-spot LLM reasoning required; identical text across distinct spots → invalidated"

This memory candidate is fired after Phase 3 PASS.

## Solver-verification queue (unchanged)

| spot_id | source PR | hero / board / action | owner adjudication | timestamp |
|---|---|---|---|---|
| HU-6.5 | PR #338 | Qd9h on 7h6c5s2d8d; BB 150% overbet; pot odds 37.5% | CALL | 2026-05-10 |
| HU-1.5-LK-10 | PR #343 | Qd9h on 7h6c5s2d8d; BB ~112% overbet; pot odds ~35% | CALL | 2026-05-10 |
| HU-1.4-LK-04 | PR #348 | TsTd on 8h5c2d6c; BB 33% probe; SB OOP HU; eff 60bb | CALL | 2026-05-10 |
| HU-1.4-LK-05 | PR #348 | TsTd on 8h5c2d7c; same shape as HU-1.4-LK-04 | CALL | 2026-05-10 |

## Owner — informational

- Quality-default path per owner mandate: WAIT (preserve evidence) + REFACTOR (architectural fix Option C) + RE-PILOT (validate per standing rule Option E) + SCALE (gated).
- ETA: Phase 0 ~60-120 min; Phase 1 ~30-60 min builder + ~15-20 min QC; Phase 2 ~varies (chunked dispatch wall-clock TBD by builder estimate) + ~15-20 min QC; Phase 3 same.
- Total path is significantly longer than the original FULL dispatch but maximizes quality.
- Standing directive: orchestrator merges all 3 phase PRs + QC verdicts autonomously per quality-default (post-owner-adjudication on any new owner-arbs that surface).

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `4c4c946` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Builder STOP-condition observation: master `4c4c946` (PR #354)
- 1.5-D.3 FULL LABELLING-EXECUTION dispatch (now superseded by this 3-phase recovery): master `d21f2fb` (PR #353)
- 1.5-D.3 FULL INFRA-PREP merged: master `6274fce` (PR #350 + QC PR #352 PASS)
- 1.5-D.3 FULL dispatch: master `bfebd13` (PR #348)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict: master `b790524` (PR #346; PASS · 0/0/0)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- Architect's design memo §4.3 + §4.4: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Quarantined evidence: `data/hu_corpus/full_HU2_HU6/_invalidated_fl4_rule_based/`, `_invalidated_fl{2,3,5}_template_based/`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `project_qc_heartbeat_convention.md`
- CLAUDE.md anti-pattern reference: "Rule-based heuristics pretending to be expert labels"

**Status: 3-phase recovery dispatched. Phase 0 WAIT in progress (FL1 + FL6 cooking). Builder authorized to begin Phase 1 REFACTOR design once FL1+FL6 complete + observation comm written. Standing-directive autonomous on Phase 1/2/3 PR cycles + QC verdicts. Owner gate only on novel owner-arbs surfaced in RE-PILOT or SCALE outputs. Solver-verification queue (4 spots; all CALL) tracked for pre-1.5-D.4 drain.**
