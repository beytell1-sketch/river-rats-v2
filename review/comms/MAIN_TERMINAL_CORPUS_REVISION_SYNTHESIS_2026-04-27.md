---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · architect / gto-expert / ml-architect (audits complete) · QC stream
re: Synthesis of three specialist corpus audits — convergent recommendation: rebuild via supplement (preserve 100 existing + generate 300-500 new). Source-pool generation infrastructure needs revision, not just sampling strategy.
status: SYNTHESIS — three audits converge on rebuild+supplement; differences in target size (400 vs 500-600) reconciled below; next blocker is corpus-generation pipeline design (architect Phase 2)
---

# Corpus revision synthesis — three specialist audits reconciled

## Context

Per `MAIN_TERMINAL_RANGE_LOGIC_RESEARCH_DECISION_2026-04-26.md` (master `0f66298`, PR #51), corpus revision is the next blocker before Phase B labelling resumes. Three specialist audits dispatched in parallel returned in this session.

Audits committed alongside this synthesis:
- `AUDIT_ARCHITECT_CORPUS_DESIGN_2026-04-27.md` — rule-trigger taxonomy + coverage matrix
- `AUDIT_GTO_EXPERT_ACTION_DISTRIBUTION_2026-04-27.md` — poker-pattern coverage
- `AUDIT_ML_ARCHITECT_CORPUS_SIZING_2026-04-27.md` — Tier 2 size + architecture audit

## Convergent findings (all three agree)

### 1. The 100-hand corpus is structurally inadequate

Hard structural deficits documented across all three audits:
- **97/100 hands have `facing_bet=0`** — opener decisions only
- **0/100 hands have `is_preflop_aggressor=1`** — c-bet decisions entirely absent (architect Q2; gto-expert Q2)
- **94/100 hands have SPR=exactly 1.25** — single SPR depth tested; no standard (4-8) or deep SPR (architect Q2; gto-expert Q2)
- **24% IP** vs ~40-50% in real play (gto-expert Q2)
- **0/100 hands have `board_favour > 0.2`** — hero is never range-advantaged (gto-expert Q2)

### 2. The 100 existing labels can't produce RAISE predictions architecturally

ml-architect Q2 confirmed: 0 RAISE + 1 CALL across 500 labels means XGBoost cannot form leaves for these classes (`min_child_weight=5` blocks zero-instance leaves). Sample weighting (current `RAISE_WEIGHT_CAP=3.0`) is irrelevant when count=0. **The fix is corpus redesign, not hyperparameter tuning.**

### 3. v3.2 rule-trigger coverage has 9 zero-instance patterns

Per architect Q4, these v3.2 rules have **zero examples** in the corpus:
- KB §1.7 RAISE (nut FD semi-bluff RAISE)
- KB §1.7 OVERRIDE → CALL (the carve-out v3.2 was specifically built for, MW-39 pattern)
- MW-30 CALL (facing initial bet + callers)
- MW-33 RAISE (set value vs pot-control)
- MW-50 FOLD (action-history range-narrowing)
- Rule 4 (PFA c-bet)
- Multi-street aggression fold
- Standard SPR (4-8)
- Deep SPR (>8)

Per gto-expert Q3, 4 critical poker patterns have zero coverage:
- Bet-and-call sequences (3-way fold-pressure dynamic)
- Free-card protection (sets on draw-heavy boards)
- Multi-street equity realisation (linked decisions across streets)
- Nut-blocker RAISE facing bet (MW-39 structural pattern)

### 4. The source pool itself is structurally limited

Critical finding from architect Q6: the source pool `3way_situations_10k.jsonl` (962 hands) has:
- 0% `is_preflop_aggressor=1`
- 0% `villain_aggression_count≥2`
- 0% SPR>2.0
- 0% `num_callers_to_bet≥1`

**Resampling the current pool cannot close the 9 critical gaps.** New generation infrastructure required.

This is the single most important finding for execution — it changes the work from "sample better" to "generate hands with corrected structural parameters."

### 5. Hard single-action labels remain correct format

ml-architect Q5 + Q7 confirmed soft-label / mixed-strategy format is not viable at scale (labellers can't produce reliable frequency tiers without solver). Architecture stays single-task XGBoost with hard labels. Validates today's research conclusion.

### 6. Feature signal mostly sufficient

ml-architect Q6: the 59-feature contract carries the signal v3.2's rules need. Three features cover hero range positioning (`hero_range_percentile`, `board_adjusted_hrp`, `is_preflop_aggressor`). Two moderate gaps: no direct `hero_range_is_capped` feature; `villain_checked_back` is not street-specific. Both addressable via corpus design (sufficient paired-board + river hands); feature additions optional.

## Divergence (where audits differ — and reconciliation)

### Total corpus size: architect says 400, ml-architect/gto-expert say 500-600

- **architect Q5/Q6:** 400 hands target = 100 existing + 300 new. Rationale: preserve the 500-label investment at `4bce49f`, hit minimum 20 instances per trigger pattern, hit minimum action class balance.
- **ml-architect Q3/Q8:** 500-600 hands target. Rationale: warm-start theory with v8 baseline already trained on 45-feature PokerBench means new corpus only teaches v3.2 pattern delta (~288 cells); 500-600 sits in rapid-improvement zone, diminishing returns by 800-1200.
- **gto-expert Q7:** 500-600 hands target. Rationale: matches ml-architect on warm-start theory; adds explicit Tier-A/B/C spot type allocations.

**Reconciliation:**
- The **lower bound** (400) is the architect's "minimum to cover all 9 zero-instance patterns + boundary cases."
- The **practical bound** (500-600) is the ml-architect/gto-expert "rapid-improvement zone for warm-start delta learning."

I'd take the practical bound: **target 500 hands** = 100 existing + 400 new generated. This is within both architect's "minimum threshold met" AND ml-architect's "rapid-improvement zone." Gives buffer for stratification slack.

### Action distribution targets

- ml-architect: CHECK 25% / BET 25% / FOLD 15% / CALL 20% / RAISE 15%
- gto-expert: CHECK 35% / BET 30% / CALL 12% / FOLD 10% / RAISE 13%
- architect: 40-50 BET/CHECK, 30-40 CALL, 20-30 RAISE, 20-30 FOLD (out of ~300, so ~13-17%/13-17%/10-13%/7-10%/7-10% per class)

**Reconciliation:**
The three targets fall in similar bands:
- CHECK: 25-35% — settle at **30%**
- BET: 25-30% — settle at **27%**
- CALL: 12-20% — settle at **17%**
- RAISE: 13-15% — settle at **14%**
- FOLD: 10-15% — settle at **12%**

Total = 100%. Roughly 50% facing-bet (CALL + RAISE + FOLD = 43%; the other 7% accounts for FOLD on opener decisions which can occur on river-checked-to spots or strong-rage check-folds).

For 500 total hands: ~150 CHECK / ~135 BET / ~85 CALL / ~70 RAISE / ~60 FOLD.

### Calibration set sizing

- ml-architect: 33 → 45-50 hands
- architect: didn't specify a number but recommended adding boundary cases for thresholds
- gto-expert: didn't specify a number

**Adoption:** ml-architect's 45-50 hands. Specifically: add 5-8 facing-bet reversals + 2-4 FOLD reversals to the existing 33. **Tier 1 target: 45 hands.**

### Whether to preserve existing 100 hands

- architect: preserve (recommends keep + 300 new)
- ml-architect/gto-expert: rebuild from scratch favoured

**Reconciliation:**
The 100 existing labels at `4bce49f` are valid labels on a narrow corpus. They cover CHECK/BET on opener decisions reasonably (the 5 labellers showed strong inter-labeller agreement on those). Discarding them throws away ~$15-25 of accurate work.

**Adoption: preserve the 100 existing hands** as the "opener decisions stratum" of the new 500-hand corpus. Generate 400 new hands targeting the gap patterns. Net: 100 existing + 400 new = 500 total.

This costs ~$30-50 for the additional 400 labels (vs ~$75 for a full 500 rebuild). Saves the existing investment without compromising coverage.

## Unified corpus revision plan

### Tier 1 (calibration set)

- **Target: 45 hands** (current 33 + 12 additions)
- Additions: 5-8 facing-bet reversals (KB §1.7 OVERRIDE pattern, MW-30 CALL pattern, MW-33 RAISE pattern, multi-street fold patterns) + 2-4 FOLD reversals (over-fold-bias diagnostic spots) + 1-3 c-bet pattern hands (PFA Rule 4)
- Solver verification on ALL Tier 1 hands (current process) — no protocol-derived labels for Tier 1

### Tier 2 (training corpus)

- **Target: 500 hands** (100 existing + 400 generated new)
- Stratification:
  - Action distribution: CHECK 30% / BET 27% / CALL 17% / RAISE 14% / FOLD 12%
  - facing_bet=1: ≥25% (≥125 hands)
  - is_preflop_aggressor=1: ≥30% (≥150 hands)
  - SPR≥4: ≥25% (≥125 hands) — covers standard + deep SPR
  - SPR 2-4: ≥20% (≥100 hands) — covers medium SPR (currently zero)
  - SPR≤2: ≤55% — current narrow band kept proportional
  - OOP/IP balance: 55-65% OOP / 35-45% IP
  - Each of the 9 zero-instance v3.2 rules: ≥20 instances, with ≥5 boundary cases per threshold rule
  - Each of the 4 zero-coverage poker patterns (bet-and-call, free-card protection, multi-street equity realisation, nut-blocker RAISE): ≥15 instances each

### Tier 3 (holdout)

- Untouched at hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- Disjointness must be re-verified after corpus expansion

### Architecture changes

- **No XGBoost changes required** (per ml-architect Q1, Q7)
- **No feature additions required** for v3.0 launch (per ml-architect Q6) — `hero_range_is_capped` and `villain_checked_back_turn` are optional improvements if model fails reference gate
- Training: warm-start from v8 base via `xgb_model` parameter (per ml-architect Q3)
- Validation: gate against the 24 three-way reference hands directly, not random 20% split (per ml-architect Q7)

## Cost estimate (revised)

| Step | Cost | Wall-time |
|------|------|-----------|
| 1. Corpus-generation pipeline design (architect Phase 2) | ~$15 | 1-2 hours |
| 2. Source-pool expansion (new hands generation) | ~$10-20 | 1-2 days |
| 3. Tier 1 calibration set expansion (33 → 45) | depends on solver | days (manual solver work) |
| 4. v3.2 protocol QC against expanded Tier 1 (may surface v3.3 needs) | ~$10 | hours |
| 5. Tier 2 mass labelling (400 new hands × 5 labellers Protocol A) | ~$60-100 | hours |
| 6. (Optional) Protocol B + C for Tier 2 | ~$120-200 | hours |
| 7. Student model training (warm-start) | ~$10-20 | hours |
| 8. Reference-gate evaluation + diagnostic | ~$10 | hours |
| 9. Holdout evaluation (Stage 6) | ~$5 | hour |

**Revised total: ~$240-380 (Protocol A only) or ~$360-580 (all 3 protocols).**

Substantially less than my earlier ~$400-1000 estimate, primarily because the warm-start delta corpus is 500 hands not 2000-5000.

Cumulative pilot spend after this work: ~$260-415 (Protocol A only) or ~$380-625 (all protocols), all within the original $700 envelope per the pilot spec.

## Execution sequencing

### Step 1 (now): Synthesis + audits committed
- This document + 3 audit files PR'd to master

### Step 2 (next): Architect Phase 2 — corpus-generation pipeline design
- Specialist agent designs how to generate hands satisfying the missing structural conditions (preflop_aggressor=1, multi-street aggression, varied SPR, etc.)
- Output: source-pool expansion plan + sampling strategy for 400 new hands
- This is the single most important next-step deliverable

### Step 3: Source-pool generation
- Execute the architect Phase 2 plan
- Generate ~2000+ candidate hands satisfying the structural targets
- Sample 400 stratified hands meeting the Tier 2 distribution targets

### Step 4: Tier 1 expansion
- gto-expert + solver curate 12 additional calibration hands
- v3.2 protocol QC: do existing rules cover the new patterns? Do we need v3.3?

### Step 5: Tier 2 mass labelling (Protocol A first)
- 5 sonnet labellers × 400 new hands = 2000 new labels
- Combined with existing 500 = 2500 total Protocol A labels (the 5x labeller redundancy carries through)
- PR + merge

### Step 6: Protocol B + C (optional, owner decision)
- Composition-first + adversarial-elimination protocols on revised corpus
- Cost-deferral candidate if Protocol A on revised corpus produces good model

### Step 7: Student model training + evaluation
- Warm-start XGBoost from v8 base
- Reference-gate validation
- Stage 6 holdout evaluation

### Step 8: Iteration
- If model fails reference gate: feature additions per ml-architect Q6
- If calibration surfaces gaps: v3.3 protocol revision
- If corpus distribution is off: rebalance and re-sample

## Decisions for owner

1. **Adopt the unified plan (target 500 hands, preserve existing 100, add 400 new)?**
   Or alternative: full rebuild (no preservation) — costs ~$25 more, moderate benefit
   Or alternative: minimum-viable supplement (target 400, architect's lower bound) — saves ~$30, more risk on rapid-improvement zone

2. **Authorize architect Phase 2 dispatch?** (corpus-generation pipeline design)
   This is the next concrete step. ~$15, 1-2 hours.

3. **Solver bandwidth for Tier 1 expansion** — is the 12-hand expansion (33→45) feasible in the existing manual solver pipeline, or do we need different tooling?

4. **Protocol B/C on revised corpus** — proceed when Tier 2 is built, or defer until model validation shows Protocol A is sufficient?

5. **Timeline expectation** — owner okay with 1-2 weeks for full revision + relabel + train cycle, or want shorter scope?

## Risks flagged

- **Source-pool generation may surface v3.2 rule gaps.** When the corpus contains spots v3.2 doesn't have rules for, the protocol may need a v3.3 revision before mass labelling. This adds wall-time but improves quality.
- **Tier 1 expansion depends on solver bandwidth.** If solver curation is bottlenecked, the full plan stalls at Tier 1 step. Worth verifying solver workflow before committing.
- **Action distribution targets are estimates.** Rebalancing during corpus build is expected; final distribution may shift ±3pp per class.
- **Existing 100-hand labels' integration** — using opener-decision labels alongside facing-bet decision labels may introduce stratum imbalance the model learns spuriously. Mitigation: balanced sampling at training time.

## What is NOT changing

- v3.2 protocol unchanged (may revise to v3.3 if Tier 1 expansion surfaces gaps)
- Phase B Protocol A labels at master `4bce49f` preserved (form the opener-decisions stratum)
- v3.2 GO at `903c5c9` and Phase A.7 conclusion stand
- XGBoost architecture unchanged

## What IS changing

- Corpus design: 100 → 500 hands with new stratification
- Tier 1 calibration: 33 → 45 hands
- Source-pool generation pipeline: needs architect Phase 2 design + new generation
- Phase B Protocol B/C dispatch: held until corpus revision complete

## References

- Range-logic research decision: `MAIN_TERMINAL_RANGE_LOGIC_RESEARCH_DECISION_2026-04-26.md` (master `0f66298`, PR #51)
- v3.2 protocol seal: `42cace2` (PR #47)
- A.7 GO: `903c5c9`
- Phase B Protocol A labels: `4bce49f` (PR #50, preserved)
- audit files: `AUDIT_ARCHITECT_CORPUS_DESIGN_2026-04-27.md`, `AUDIT_GTO_EXPERT_ACTION_DISTRIBUTION_2026-04-27.md`, `AUDIT_ML_ARCHITECT_CORPUS_SIZING_2026-04-27.md` (this PR)

**Status: SYNTHESIS COMPLETE. CORPUS REVISION PLAN READY FOR OWNER REVIEW. NEXT BLOCKER: ARCHITECT PHASE 2 DISPATCH FOR CORPUS-GENERATION PIPELINE DESIGN.**
