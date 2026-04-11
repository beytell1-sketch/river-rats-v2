# Plan: v3 Data Integrity — Updated with Audit Findings

**Date:** 8 April 2026
**Version:** 2 (incorporates completed Phase 1 audit results)
**Status:** AWAITING OWNER APPROVAL

---

## Governing Principle

Every training label must be reachable by reasoning the model can learn
from its 48 features. Solver data verifies and researches. It never labels.

See: review/FEEDBACK_SOLVER_LABELS_DANGER.md

---

## What the audit found (Phase 1 — COMPLETED)

**52% of factory boards have CRITICAL action sequence errors.**

| Category | Boards | % |
|----------|--------|---|
| CLEAN | 12 | 26% |
| MODERATE | 10 | 22% |
| CRITICAL | 24 | 52% |

**Root cause:** When an OOP player checks before an IP player bets,
the check is missing from action_history. This is systemic across
both batch 1 and batch 2 factory scripts.

**Corrupted feature:** `num_callers_to_bet` reads 0 when it should
read 1+ on boards where an intermediate player called but that call
is missing from the history. Other action-derived features
(`villain_checked_back`, `villain_aggression_count`) may also be
affected on multi-street situations.

**Self-play data (200 rows) is CLEAN.** Game engine enforces correct
ordering by construction.

**Reference evaluator:** Separate bug class — hand-authored tuples
with possible miscounts on MW-31, MW-42, MW-46. Needs its own audit.

**Full audit reports available from 7 agents:**
- Architect A: factory code analysis (situation_factory.py → features)
- Architect B: reference evaluator code analysis
- Auditors A-D: board-by-board findings across both batches + self-play

---

## What we KEEP from this session

| Item | Status |
|------|--------|
| KB v1.2 | KEEP — correct poker, needs v1.3 framing fix |
| KB v1.3 requirements | KEEP — 15 changes identified |
| 5 board designs | KEEP — poker design is good, only action sequences wrong |
| Solver session insights | KEEP — research findings, not data artifacts |
| Feature analysis of solver hands | KEEP as reference |
| Process Guide additions | KEEP |
| Solver labels danger feedback | KEEP — permanent constraint |
| Calibration exam results | KEEP — diagnostic value |
| Audit findings (Phase 1) | KEEP — already complete |

## What we DISCARD

| Item | Why |
|------|-----|
| Factory generation scripts (both) | Root cause — rebuild with correct action sequences |
| 261 batch 2 labels | Based on wrong features + solver contamination |
| 261 batch 2 reviews | Validated contaminated labels |
| v3 model | Trained on corrupted data |
| Combined CSV | Structurally wrong at feature level |

---

## Revised Phase Sequence

### Phase 0 — RAISE Label Policy (NOT YET STARTED)

**Goal:** Before rebuilding anything, establish which RAISE labels are
defensible from feature-visible logic alone. This determines the
labelling rules for the rebuild.

**Why first:** If we rebuild the factory, regenerate, and relabel
without resolving this, we'll get the same solver contamination again.

**Team:**

| Agent | Task | Scope |
|-------|------|-------|
| GTO Analyst A | For each of the 8 flagged RAISE hands from the analyst review, write the case for RAISE using ONLY the 48 features. No blocker logic unless flush_block_pct captures it. | 4 hands |
| GTO Analyst B | Same. | 4 hands |
| Independent Reviewer | Check both analysts' reasoning. Flag any feature-invisible logic. | All 8 |

**Deliverable:** A table of verdicts (DEFENSIBLE / NOT DEFENSIBLE)
with feature-only reasoning.

**Gate:** Owner reviews and approves verdicts. This establishes the
RAISE labelling policy for the rebuild.

---

### Phase 1 — COMPLETED (audit findings above)

No further work needed. Results feed into Phase 2.

---

### Phase 2 — Factory Rebuild + Action Sequence Validator

**Goal:** Produce clean factory generation scripts with correct action
sequences and a validator that prevents recurrence.

**Scope (informed by audit):**

The audit found that the CLEAN boards all share a pattern: either
hero is OOP acting first with no prior actions (lead decisions), or
the OOP player IS the bettor (donk-bets), or the checks are
explicitly included. The fix is mechanical: add missing OOP checks
and intermediate caller actions to every affected board spec.

**Team:**

| Agent | Task | Scope |
|-------|------|-------|
| Architect | Design the action-ordering validator for situation_factory.py. Spec: for each street, verify first action comes from OOP-most player, all players act in position order, no player is missing. | Code spec |
| Programmer A | Implement the validator | situation_factory.py |
| Programmer B | Rebuild batch 1 action_histories (16 boards) with correct sequences | generate_factory_situations.py |
| Programmer C | Rebuild batch 2 action_histories (30 boards) with correct sequences | generate_factory_batch2.py |
| Auditor A | Re-audit batch 1 boards (verify fixes) | 16 boards |
| Auditor B | Re-audit batch 2 boards 1-15 (verify fixes) | 15 boards |
| Auditor C | Re-audit batch 2 boards 16-30 (verify fixes) | 15 boards |
| Independent Reviewer | Review all fixes and re-audit results | All |

**Validation step:** Before running at scale, run 10 deals through
the corrected factory and manually verify that `num_callers_to_bet`
and `villain_aggression_count` values match the actual hand history.

**Deliverable:** Two corrected generation scripts + action-ordering
validator in situation_factory.py. All 46 boards pass the validator.

**Gate:** Owner reviews corrected scripts before generation runs.

---

### Phase 3 — Regenerate + Diff + Relabel

**Goal:** Generate clean feature vectors, identify what changed, and
relabel only the situations where features changed.

**Team:**

| Agent | Task |
|-------|------|
| Programmer A | Run corrected factory scripts, generate new JSONL files |
| Programmer B | Diff old vs new feature vectors — flag every row where num_callers_to_bet, villain_checked_back, or villain_aggression_count changed |
| Programmer C | Combine: 200 clean self-play rows + regenerated factory rows. Export CSV. |

**The diff determines relabelling scope:**
- Rows where NO features changed → keep existing label (if it passes
  Phase 0 RAISE policy)
- Rows where features changed → relabel with corrected feature context
- All RAISE labels → must pass Phase 0 policy regardless

**Relabelling team (after diff):**

| Agent | Task | Scope |
|-------|------|-------|
| GTO labelling agents | Relabel changed rows. Labelling prompt UPDATED with feature-only reasoning rule. | ≤10 hands each |
| GTO review agents | Independent review of relabelled hands. | ≤15 hands each |

**Additional constraints for relabelling:**
- Labelling prompt must include: "Your reasoning must be explainable
  by the 48-feature vector. Do not use suit-specific blocker logic
  unless flush_block_pct captures the effect."
- No solver-derived rules in the labelling context
- Calibration exam with updated labelling prompt before dispatching

**Gate:** Owner reviews relabelled dataset before training.

---

### Phase 4 — Retrain v3.1

Same as original plan Phase 3. From-scratch, 48 features, cap 3.0.
Only the data changes — one variable at a time.

**Team:** ML-architect → owner approval → architect → programmer →
reviewer → owner approval.

**Gates:**
- Gate 2.2: leakage check on final dataset
- Gate 2.3: feature importance
- Gate 2.4: reference evaluation (v8, v2.2, v3.1 in same session)
- Ship-it: ≥32/40 raw with no regression vs v2.2

---

### Phase 4.5 — Reference Evaluator Audit (can run in parallel)

**Goal:** Verify the hand-authored action tuples in reference_evaluator.py.
Architect B flagged possible miscounts on MW-31, MW-42, MW-46.

**Team:**

| Agent | Task |
|-------|------|
| Auditor | Check all 40 hand tuples against the prose in BATCH2_8_HAND_DESIGNS.md |
| Independent Reviewer | Verify |

**If miscounts found:** Correct the tuples, re-run Gate 2.4 for all
historical models (v2.2, v3.1). This may change the baseline scores.

---

## Decision Points

| # | When | Decision |
|---|------|----------|
| 1 | Now | Approve this plan |
| 2 | After Phase 0 | Approve RAISE verdicts and labelling policy |
| 3 | After Phase 2 | Approve corrected factory scripts |
| 4 | After Phase 3 diff | Approve relabelling scope |
| 5 | After Phase 3 relabelling | Approve clean dataset |
| 6 | After Phase 4 training | Approve or reject v3.1 model |

---

## Estimated effort

| Phase | Hours | Parallelizable? |
|-------|-------|----------------|
| 0: RAISE policy | 2-3 | Yes (2 analysts + reviewer) |
| 2: Factory rebuild | 4-6 | Partially (programmer + auditor in sequence) |
| 3: Regen + relabel | 4-6 | Yes (diff is fast, relabelling parallelizes) |
| 4: Retrain | 2-3 | Sequential |
| 4.5: Ref eval audit | 2-3 | Parallel with Phase 2-4 |
| **Total** | **~14-21** | |

---

## What this plan does NOT cover

- KB v1.3 update (downstream of Phase 0 — which rules need rewriting)
- Labelling prompt update details (downstream of Phase 0)
- Process Guide Section 5.4 (implement after plan completes)
- Reference set expansion (only if v3.1 fails Gate 2.4)
- New features (flush_draw_rank, etc.) — backlog for v4
