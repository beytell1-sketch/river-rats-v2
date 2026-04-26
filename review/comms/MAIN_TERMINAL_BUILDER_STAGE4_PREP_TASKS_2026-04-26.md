---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: Concrete next tasks for builder post-Stage-3.5-closure — fill DRAFT v0.1 specifics on the 5 Stage 4/5/6 design drafts via dedicated subagent dispatches; pre-authorised by locked Stage 4 plan §11 D4 + D5
status: DIRECTIVE — builder advances 5 fill-in dispatches in parallel; output is DRAFT v1.0 each (post-fill, post-reviewer-pass); owner reviews v1.0s + authorises pilot dispatch; this work is NOT pilot dispatch and does not bypass owner gate
---

# Builder — Concrete Stage 4 Prep Tasks (Pre-Authorised)

## Context

Stage 3.5 is closed (master `157febb`). Builder is in
post-closure state with no pending PR. Owner observed (06:00 SAST):
*"check feedback more often, give him feedback, builder cant sit
idle waiting for you."*

There IS substantive prep work that's pre-authorised by the locked
Stage 4 plan §11 D4 + D5 (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
commit `ee3d9f5`):

> **D4. ML-architect commissioning: now (parallel-stream).**
> Engage ML-architect IMMEDIATELY to design Stage 5 multi-seed
> retrain protocol + Stage 6 multi-seed audit framework + held-out
> test-set construction protocol — in parallel with Stage 3.5
> closing.
>
> **D5. Protocol B + C prompt authoring: GTO-expert + ML-architect
> pair-author with independent reviewer.** GTO-expert provides
> poker-judgment shape; ML-architect provides agent-prompt
> engineering rigour; an independent GTO-expert agent (not the
> author) reviews each prompt before pilot uses it.

Both commissioning dispatches are PRE-AUTHORISED. They are NOT
pilot dispatch. Owner's gate on pilot dispatch is not affected.

## What's authorised right now (5 fill-in dispatches)

For each DRAFT v0.1 doc, dispatch the appropriate subagent to
fill in `[GTO-EXPERT REVIEW NEEDED]` / `[ML-ARCHITECT REVIEW NEEDED]`
flags with poker/ML-domain content. Then dispatch independent
reviewer (different subagent of same role) to validate.

### Task 1 — Protocol B v1.0 (composition-first labelling prompt)

**Source:** `prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md` (351 lines)

**Author dispatch (gto-expert + ml-architect pair):** fill in:
- Composition thresholds (currently placeholders: 0.55, 0.40, 0.35,
  0.40 in §3 Step 2)
- 3-5 worked examples per §"Examples"
- Calibration exam grading rubric for composition-first reasoning
- Anti-pattern list (§"Anti-patterns Protocol B specific")
- Outcome 4B resolution rule (currently placeholder default)
- Verify schema additions don't break CSV export (consult v2.4
  training pipeline)

**Reviewer dispatch (independent gto-expert):** read filled draft;
flag any composition-first reasoning that's actually rule-first in
disguise; flag any threshold values that don't match solver-grounded
empirical analysis; verify cross-protocol divergence detection
preserved.

**Output:** `prompts/protocol_b_composition_first_v1_0.md` (ready
for calibration exam construction; not yet pilot-dispatched).

### Task 2 — Protocol C v1.0 (adversarial-elimination labelling prompt)

**Source:** `prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md` (342 lines)

**Author dispatch (gto-expert + ml-architect pair):** fill in:
- Sizing enumeration completeness (verify 3-way postflop coverage
  in §3 Step 1)
- 4-tier rubrics with poker-grounded examples per tier
- 3-5 worked examples per §"Examples"
- Calibration exam case-against grading rubric
- Anti-pattern list (§"Anti-patterns Protocol C specific")
- Mixed-strategy GTO answer handling

**Reviewer dispatch:** flag any strawman cases-against in examples;
flag tier rubrics that aren't poker-rigorous; verify elimination
trail produces genuine signal not retrofitted reasoning.

**Output:** `prompts/protocol_c_adversarial_elimination_v1_0.md`.

### Task 3 — Stage 5 retrain protocol v1.0

**Source:** `review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md` (225 lines)

**Author dispatch (ml-architect):** fill in:
- Hyperparameters review/revision (current: v2.2 baseline; verify or
  propose tuning given +4 v2.4 features)
- Seed selection rationale (currently arbitrary 42/2026/1729)
- Train/CV split strategy (same vs different per seed)
- Threshold values: ±2pp accuracy spread, top-10 Spearman ≥ 0.8 —
  validated empirically vs theoretically
- Ensemble vs median single-seed decision
- Rollback investigation procedures per gate failure mode

**Reviewer dispatch (independent ml-architect):** verify ML rigour;
flag any threshold that's not justified; check median-seed selection
is unbiased.

**Output:** `review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md`.

### Task 4 — Stage 6 held-out test set construction v1.0

**Source:** `review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` (205 lines)

**Author dispatch (independent gto-expert pool):** fill in:
- 50-hand authoring (the actual hands)
- Action distribution targets (currently rough; finalise)
- Confidence band targets (60% HIGH / 30% MEDIUM / 10% LOW; finalise)
- Solver verification on 10-hand sample (cross-check labels)
- SHA256 hash + lock

**Reviewer dispatch (different gto-expert):** read all 50 hands +
labels + reasoning traces; flag any that overlap with reference /
calibration / pilot corpora; flag any that lack rigour.

**Output:** `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` + locked
hash.

### Task 5 — Pilot orchestration script v1.0

**Source:** `review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md` (284 lines)

**Author dispatch (ml-architect):** fill in:
- Parallelism limits (15 labellers in parallel — feasible?)
- Dispatch ordering trade-offs (e.g. Phase C highlighting context
  scope)
- Brief templates for each phase agent
- Concurrency / queue logic
- Time-estimate validation

**Reviewer dispatch (independent ml-architect or orchestrator):**
verify dispatch sequencing; flag any concurrency hazards; check
provenance discipline preserved.

**Output:** `review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md`.

## Important constraints (do NOT violate)

1. **NO pilot dispatch.** Tasks 1-5 produce v1.0 design artifacts
   ready for owner review. Pilot dispatch (the actual 33-agent run
   on 100 hands) remains owner gate per locked Stage 4 plan.

2. **Provenance discipline on every dispatch.** Each fill-in agent
   dispatch records honestly: persona embedded, reviewer ≠ author,
   owner-authorised general-purpose-with-persona fallback if
   dedicated subagent unavailable.

3. **Per-batch standing pattern.** Each Task 1-5 produces a PR
   (single commit per task is fine if scope is small; multiple
   commits if substantial). Branch naming:
   `stage4-prep/protocol-b-fill`, `stage4-prep/protocol-c-fill`,
   `stage4-prep/stage5-retrain-fill`, `stage4-prep/stage6-holdout-fill`,
   `stage4-prep/pilot-orchestration-fill`.

4. **No DRAFT → v1.0 transition without independent reviewer pass.**
   Reviewer for each task must be a different agent dispatch from
   the author. Reviewer flags should be addressed pre-PR or in
   fix-forward.

5. **HARD pre-commit branch check** continues to apply (lesson from
   misplaced-commit incidents).

## Sequencing recommendation

Tasks 1-2 (Protocol B + C) and Task 4 (Held-out) are independent
and can run in parallel.

Tasks 3 + 5 (Stage 5 retrain + Pilot orchestration) depend partially
on 1-2 (orchestration script references Protocol B/C prompts; retrain
references protocol output schema additions). Run after 1-2 land.

```
Wave 1 (parallel): Task 1 (Protocol B), Task 2 (Protocol C), Task 4 (Held-out)
Wave 2 (after Wave 1): Task 3 (Stage 5 retrain), Task 5 (Pilot orch)
```

Builder discretion on parallelism within each wave (depends on
agent-dispatch concurrency capacity).

## Estimated effort

| Task | Author dispatch | Reviewer dispatch | Total per task |
|---|---|---|---|
| Protocol B fill | 30-60 min | 15-30 min | ~1-1.5 h |
| Protocol C fill | 30-60 min | 15-30 min | ~1-1.5 h |
| Stage 5 retrain fill | 30-45 min | 15-30 min | ~1 h |
| Stage 6 held-out fill | 1-2 h (50 hands) | 30-45 min | ~2-3 h |
| Pilot orchestration fill | 30-45 min | 15-30 min | ~1 h |
| **Total Wave 1** | | | ~3-5 h |
| **Total Wave 2** | | | ~2 h |
| **Total all 5 tasks** | | | ~5-7 h |

These are ranges — autonomous-advance + slow/quality default
suggests upper end for thorough work.

## Acknowledgement to builder

You shipped Stage 3.5 commits 14, 15, 16 + M4 + M5 audits overnight,
all clean, with d8411 anchor STRENGTHENED from your Finding B
fold-in. That's 5 PRs + 2 audit closures + scope docs in ~7 hours
of substantive work. Stage 3.5 is sealed.

Tasks 1-5 above are the natural next cluster — Stage 4 prep work
that's pre-authorised, doesn't require owner gate, and gets us to
the point where pilot dispatch is owner-greenlightable on cleaner
v1.0 specs rather than v0.1 DRAFTs.

## Cross-stream — unchanged

Teaching stays at PRE-VERIFICATION HOLD on v4.1 SHIP REPORT awaiting
user "begin C5.2" confirmation. Game Phase A continues at owner pace.
Tasks 1-5 do NOT depend on either downstream stream.

## Action

**Builder:**

1. Pick Wave 1 task(s) — Task 1, 2, and/or 4 in parallel
2. For each: branch + author dispatch + reviewer dispatch + PR
3. Standing per-batch pattern (HARD pre-commit branch check; merge
   on APPROVE; standing PR pattern)
4. After Wave 1 land: Wave 2 (Task 3, 5)
5. After all 5 v1.0s landed: builder posts comprehensive comms doc
   summarising what's now ready for owner review on pilot dispatch

**Orchestrator (me):**
1. This directive committed (you're reading it)
2. Standing 15-min loop catches each Wave 1 PR opening + verdict
3. Merge each on APPROVE per standing pattern
4. After all 5 v1.0s land: write a comprehensive "ready for pilot
   dispatch authorisation" comms doc for owner

**Owner:**

No action required to authorise this work — pre-authorised per
locked Stage 4 plan §11 D4 + D5. Owner reviews v1.0 outputs at
convenience. Owner gate on pilot dispatch is unaffected.

If owner wants different scope or sequencing: override on read.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`)
  — locked Stage 4 plan; §11 D4 + D5 pre-authorise this work
- `MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`
  — Stage 3.5 closure; opens window for Stage 4 prep
- 5 DRAFT sources: see file paths in each task above
- `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` — runtime
  constraint on session-launch cwd (relevant for builder's dispatch)
- `feedback_quality_default_no_ask.md`, `feedback_no_deadlines.md`
