# Plan: v3.1 Clean Rebuild — Final Version

**Date:** 8 April 2026
**Version:** 3 (incorporates Phase 0 results, audit findings, bluff feature research)
**Status:** AWAITING OWNER APPROVAL

---

## Governing Principles

1. Every training label must be reachable by reasoning the model can
   learn from its features. Solver data verifies and researches. It
   never labels. (FEEDBACK_SOLVER_LABELS_DANGER.md)

2. Fix the data before changing the measuring stick. (Reviewer guidance)

3. One variable at a time where possible. (Training protocol)

---

## What happened and why we're rebuilding

- v3 failed Gate 2.4 (31/40, MW-20 regression)
- Root cause 1: Solver-derived KB rules led labelling agents to produce
  RAISE labels the model's features can't support (Phase 0 finding:
  all 7 non-monster RAISEs are NOT DEFENSIBLE from features alone)
- Root cause 2: 52% of factory boards have CRITICAL action sequence
  errors — missing OOP checks, missing intermediate callers. Corrupts
  `num_callers_to_bet` and makes action histories impossible.
- Root cause 3: Model lacks bluff signal — no feature for "where does
  hero's hand sit in hero's own range"

---

## What we KEEP

| Item | Notes |
|------|-------|
| KB v1.2 | Needs v1.3 framing fix but poker knowledge is correct |
| KB v1.3 requirements | 15 changes identified, well-sourced |
| 5 board designs | Poker design good, action sequences are downstream |
| Solver session insights | Research findings — Ace blocker paradox, suit effects, etc. |
| Process Guide | Institutional knowledge from the failure |
| Solver labels danger feedback | Permanent constraint |
| Phase 0 results | All 7 non-monster RAISEs → CALL |
| Phase 1 audit results | 24 CRITICAL, 10 MODERATE, 12 CLEAN boards identified |
| Bluff feature research | 4 agents' findings on hero_range_percentile etc. |
| 200 self-play rows | Clean — game engine enforces correct ordering |

## What we DISCARD

| Item | Why |
|------|-----|
| Factory generation scripts (both) | Systemic action sequence bugs |
| 261 batch 2 labels + 261 reviews | Wrong features + solver contamination |
| v3 model + combined CSV | Trained on corrupted data |

---

## Phase 0 — COMPLETED

All 7 non-monster RAISE labels are NOT DEFENSIBLE from features alone.
RAISE is reserved for is_monster hands only until new bluff features
provide feature-visible signal for non-monster raises.

---

## Phase 1 — COMPLETED (audit)

52% of 46 factory boards have CRITICAL action sequence errors.
Self-play data (200 rows) is clean. Reference evaluator has separate
hand-authored tuple concerns (MW-31, MW-42, MW-46).

---

## Phase 2 — Feature Pipeline Upgrade

**Goal:** Add 4 new features + fix 1 broken feature before regenerating
any data. This ensures the rebuild uses the best possible feature set.

### 2A: New features to add

| # | Feature | Type | How | Effort |
|---|---------|------|-----|--------|
| 49 | `hero_range_percentile` | float 0-1 | Wire existing `get_hand_percentile()` from range_manager.py to feature_extractor.py | Medium |
| 50 | `has_showdown_value` | binary | `int(is_made_hand == 1 and hand_category >= 3)` in add_derived_features() | Trivial |
| 51 | `villain_fold_equity_estimate` | float 0-1 | Derived from villain_top_pair_plus_pct and villain_draw_pct | Trivial |
| 52 | `flush_draw_rank` | int 0-14 | Rank of hero's highest flush-suit card (0 if none) | Low |

### 2B: Bug fix

| Feature | Bug | Fix |
|---------|-----|-----|
| `flush_block_pct` | Returns 0.0 when hero has 2+ flush-suit cards (the draw case). Exactly when it should be most informative. | Compute a meaningful value for hero-has-draw case — e.g., what fraction of villain's flush combos are blocked by hero holding those specific cards |

### 2C: Action sequence validator

Add to `situation_factory.py`: validate that action_history has correct
positional ordering before building any situation. Check:
- First action on each street comes from OOP-most player
- All active players appear in order
- No player acts before a player who should act first

This PREVENTS the Phase 1 bug class from recurring.

### Team

| Agent | Task |
|-------|------|
| Architect | Blueprint for all 5 changes (4 features + 1 fix + validator) |
| Programmer A | Implement features 49-52 |
| Programmer B | Fix flush_block_pct bug |
| Programmer C | Implement action sequence validator |
| Reviewer | Verify all implementations |

### Gate

Owner reviews implemented features. Run 10 test situations through
the updated pipeline and verify:
- hero_range_percentile produces different values for different hands
  on the same board
- has_showdown_value correctly distinguishes paired vs unpaired hands
- villain_fold_equity_estimate is non-zero and varies
- flush_draw_rank correctly identifies hero's flush suit rank
- flush_block_pct returns non-zero when hero has the flush draw
- Action sequence validator catches a known-bad action_history

---

## Phase 3 — Factory Rebuild

**Goal:** Corrected action sequences for all 46 boards. Clean generation.

### 3A: Fix action histories

For each of the 46 boards across both generation scripts:
- Add missing OOP checks before IP bets
- Add missing intermediate caller actions
- Verify positional ordering on every street
- Run through the new action sequence validator

### 3B: Regenerate

Run corrected scripts. All situations now have 52-feature vectors
with correct action sequences.

### 3C: Verify

Re-audit all 46 boards (same checklist as Phase 1). Every board
must be CLEAN. Zero CRITICAL or MODERATE allowed.

### Team

| Agent | Task | Scope |
|-------|------|-------|
| Programmer A | Fix batch 1 action_histories (16 boards) | generate_factory_situations.py |
| Programmer B | Fix batch 2 action_histories (30 boards) | generate_factory_batch2.py |
| Auditor A | Re-audit batch 1 boards | 8 boards |
| Auditor B | Re-audit batch 1 boards | 8 boards |
| Auditor C | Re-audit batch 2 boards | 15 boards |
| Auditor D | Re-audit batch 2 boards | 15 boards |
| Reviewer | Review all fixes and re-audits | All |

### Validation step

Before running at scale: run 10 deals through corrected factory,
manually verify num_callers_to_bet and villain_aggression_count
match the actual action sequence.

### Gate

Owner reviews: all boards CLEAN, validation step passes.

---

## Phase 4 — Relabelling

**Goal:** Fresh labels on clean data with updated labelling rules.

### 4A: Update labelling prompt

Add to the GTO Expert prompt:
- "RAISE is for is_monster hands (sets, nut straights, nut flushes)
  only. Non-monster hands are CALL or FOLD."
- "Your reasoning must be explainable by the feature vector. Do not
  use suit-specific blocker logic."
- "Do not reference solver findings in your reasoning."
- Remove Section 1.7 semi-bluff raise carve-out from the labelling
  context (it teaches feature-invisible logic)

### 4B: Calibration exam

Mandatory with updated prompt. Gate: 20/24 minimum.

### 4C: Relabel all factory situations

Fresh labels on all ~400 factory situations (both batches). The
200 self-play rows retain their existing labels (features unchanged
for self-play data, but hero_range_percentile and new derived
features need to be computed and appended).

### 4D: Review

Independent review of all labels. Same protocol: ≤15 hands per
reviewer, flag disagreements.

### Team

| Agent | Task | Scope |
|-------|------|-------|
| Calibration agent | Blind exam with updated prompt | 24 hands |
| Grader | Score against answer key | Independent |
| Labelling agents | ≤10 hands each | All factory situations |
| Review agents | ≤15 hands each | All labels |

### Gate

Owner reviews: label distribution healthy, no solver contamination,
disagreement rate acceptable.

---

## Phase 5 — Combine + Leakage Check + Train

### 5A: Combine

200 self-play rows (with new features appended) + relabelled factory
rows. Export CSV with 52 features + label.

### 5B: Leakage check (Gate 2.2)

Compare all training situations against 40-hand reference set.
Remove any exact matches.

### 5C: Train v3.1

From-scratch, 52 features, cap 3.0 (same as v3, only data changes
and feature count).

Also train feature-combo variants:
- Model A: 52 features (primary)
- Model B: 48 features (diagnostic — do new features help?)
- Model C: 52 minus flush_block_pct (if still no signal after fix)

### 5D: Gates

- Gate 2.3: feature importance. Check all 4 new features.
  hero_range_percentile should show >1% if the bluff signal works.
- Gate 2.4: reference evaluation. v8, v2.2, v3.1 in same session.
  Ship-it: ≥32/40 raw, no regression vs v2.2.

### Team (Process Guide Section 6)

ML-architect → owner approval → architect → programmer → reviewer
→ owner approval.

---

## Phase 5.5 — Reference Evaluator Audit (parallel)

Verify hand-authored tuples in reference_evaluator.py. Architect B
flagged MW-31, MW-42, MW-46. If miscounts found, correct and re-run
Gate 2.4 for all models.

---

## Decision Points

| # | When | Decision |
|---|------|----------|
| 1 | Now | Approve this plan |
| 2 | After Phase 2 | Approve feature implementations |
| 3 | After Phase 3 | Approve corrected factory + re-audit results |
| 4 | After Phase 4B | Approve calibration with updated prompt |
| 5 | After Phase 4D | Approve labelled dataset |
| 6 | After Phase 5D | Approve or reject v3.1 model |

---

## Estimated effort

| Phase | Hours | Notes |
|-------|-------|-------|
| 2: Feature pipeline | 4-6 | 4 features + 1 fix + validator |
| 3: Factory rebuild | 4-6 | Fix 46 boards + re-audit |
| 4: Relabelling | 6-8 | ~400 situations labelled + reviewed |
| 5: Train + gate | 3-4 | Training + evaluation |
| 5.5: Ref eval audit | 2-3 | Parallel |
| **Total** | **~19-27** | |

---

## What this plan does NOT cover

- KB v1.3 update (downstream — implement after v3.1 ships)
- `nut_draw_bluff_eligible` feature (add in v3.2 after #51 proves useful)
- `bluff_raise_composite_score` (add in v3.2)
- Reference set expansion (only if v3.1 fails Gate 2.4)
- Teaching system updates (gated on 80%+ accuracy)
