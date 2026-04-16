---
date: 2026-04-16
from: Owner (Rupert) via remote-control
to: Builder + Main terminal + Teaching team
re: Gate 7 ship/iterate decision + v2.3 scope approval + solver deferral
status: DECISION — actionable
---

# v2.2 Ship Decision + v2.3 Scope Approval

## 1. v2.2 SHIPS as production

**Gate 7 verdict: SHIP.**

Numeric case is clear on the live `v2_2_model.json`:
- FB-40: 72.5% (29/40) — passes the 70.0% target
- MW-50: 84.0% (42/50) — passes the 82.5% target

Both gates clear. No criterion is failing.

### Rationale

1. **Bias is narrow and scoped.** "Defensive multiway-checked-through
   CHECK bias" is a precondition-locked shape (per Stream B.2 +
   Stream C). Predicate: `facing_bet=False ∧ num_opponents≥2 ∧
   villain_checked_back=1 ∧ villain_range_capped=1 ∧
   worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35 ∧ SPR≤2.0`. The v2.2
   model handles the other 92%+ of spots correctly.
2. **v2.3 supplement targets the bias directly.** 400-hand bucket
   already scoped, sized, and queued (per Track 6 sizing commit
   `166d393`). The fix is in motion.
3. **Not shipping = weeks of teaching-team idle.** Teaching has the
   v2.2 export (Track D handoff). Shipping releases downstream work;
   v2.3 swaps in when it clears its own gates. This is the quality
   path — not "rush v2.3," but "don't stall downstream work for a
   fix that's already queued."

### What "ship" means

- v2.2 (`v2_2_model.json`) is the **production artifact** as of
  2026-04-16.
- Teaching team is unblocked for full Phase 2 work using the v2.2
  export.
- v2.2 stays production **until v2.3 clears its own gates**, at
  which point v2.3 swaps in.
- No code or model file moves; the designation is documentary.
  Pinning happens via `models/PRODUCTION.md` if/when teaching needs
  a canonical pointer.

## 2. v2.3 scope APPROVED

`review/comms/PLAN_V23_SCOPE_2026-04-15.md` is approved as of
2026-04-16, after the cleanup commit `b723d72` resolved the four
stale Open Questions.

Approved substance (per Round 3 + Round 4 reviews):
- BET delta: +186 BET / 48.2% (additive interpretation)
- Section 2: "Defensive multiway-checked-through CHECK bias" with
  formal predicate and Pass 1 prompt override clause
- Supplement sizing: 400 hands (per Stream C, label signal healthy
  at 79.2% BET + bucket-size sparsity caveat)
- Calibration gate: 23/28 minimum + all reversal hands correct
  before any production labelling
- Diagnostic test set: 70% absolute floor on Groups A+B; >1-hand
  Group D regression = STOP before ship

Companion doc `PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md` also
approved with the Track E amendments.

## 3. Solver — deferred to v2.3 validation

The 8 remaining MW misses (after 2 BP-pattern resolutions) will be
solver-verified during v2.3 validation, not v2.2 ship gate.

Rationale: running solver on the same 8 hands now confirms a bias
already established robustly across 10 hands by Stream B.2 + Stream
C — low marginal value. Running solver on those same 8 hands after
v2.3 retrains measures whether the bias correction actually worked
on the exact spots that originally failed — high marginal value.
Same solver budget, much better ROI.

## 4. Builder next actions

1. ✅ Mark `PLAN_V23_SCOPE_2026-04-15.md` header as APPROVED (commit
   following this artifact).
2. Architect produces v2.3 hand generation BUILD PLAN per CLAUDE.md
   §1 (plan-before-build): per-bucket generator commands, yield
   targets and overshoot strategy, calibration-gate sequencing,
   checkpoint commits, stop conditions. Deliverable:
   `review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md`.
3. Owner reviews build plan; on approval, generation begins.
4. Solver runs as part of v2.3 validation pass (post-training).

## 5. Standing items

- v3.0 action distributions: backlog, post-v2.3
- Clean-CSV retrain of v2.2: deferred (consolidated plan §4); not
  on critical path
- Pre-existing 11 test failures (`test_oracle_router` missing model
  artefacts): separate cleanup track, not blocking

— Recorded by Builder, 2026-04-16
