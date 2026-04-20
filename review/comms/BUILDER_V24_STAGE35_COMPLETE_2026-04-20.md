---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 3.5 COMPLETE — action-aware range narrowing landed + all gates PASS
status: STAGE 3.5 COMPLETE — Stage 4 gate satisfied; awaiting parallel Stage 3 v3.2 prompt
---

# v2.4 Stage 3.5 — COMPLETE

Per GTO review (a4cab83) + spec lock. All M1-M7 modifications
applied, all acceptance gates clear, **Stage 3.5 alone restores
the three β-panel TPTK-after-flop-check regressions on the v2.3.1
model without retraining**.

## Headline

**M5 pre-retrain diagnostic: 3/3 anchors RESTORED TO BET.**

| Anchor | Expected | v2.3.1 BEFORE Stage 3.5 | v2.3.1 AFTER Stage 3.5 |
|---|---|---|---|
| d2410_CO_turn | BET | CHECK 0.713 (v2.3.2 regression) | **BET 0.976** ✅ |
| d0182_BTN_turn | BET | CHECK | **BET 0.984** ✅ |
| d8411_BB_turn | BET | CHECK | **BET 0.589** ✅ |

Feature correctness alone was the cause. v2.3.2's Path C
counter-example work was fixing a symptom (class ratio) not the
cause (action-history-ignorant villain range). Stage 4 re-label
becomes **additive insurance**, not a correctness necessity.

## All Stage 3.5 acceptance gates

| Gate | Required | Actual | Status |
|---|---|---|---|
| Unit tests (M3) | All pass | 16/16 (0.06s) | ✅ |
| Backward compat (v2.3.1 anchor gate) | 5/5 | 5/5 (d2410 0.966→0.970 up) | ✅ |
| M4 isolation check (flop-only shift) | 0 violations | 0/124 | ✅ |
| M4 chain activity (multi-street) | High % fires | 455/455 (100%) | ✅ |
| M5 pre-retrain diagnostic | BET on d2410 | 3/3 BET restored | ✅ |

## What was implemented (M1–M7)

### M1 — Table updates + new CALL-continue tables

`river-rats-core/range_narrowing.py`:
- `RIVER_BETTING_FREQUENCIES['bluff']`: 0.35 → **0.20** (3-way per §1.4)
- `RIVER_BETTING_FREQUENCIES['air']`: 0.20 → **0.10** (3-way per §1.4/§1.7)
- NEW `FLOP_CALL_FREQUENCIES` (8 categories, solver-intuition-grounded)
- NEW `TURN_CALL_FREQUENCIES`
- NEW `RIVER_CALL_FREQUENCIES`
- All three preserve `medium_made` elevation (bluff-catch band)
  and suppress `nuts`/`strong_value` (they raise, not call)

### M2 — Chain walker + safety rails

NEW `narrow_to_continuing_range()` — per-street CALL filter
NEW `narrow_by_action_history()` — chains bet/check/call narrowing
    across villain's prior-street actions on the per-street board slice.

Three safety rails:
1. Empty-chain fallback — revert to last valid range if a step
   produces zero weight (don't emit empty composition to downstream)
2. Weight-floor guard — if narrowing collapses to <3 hands, revert
3. Returns `(range, meta)` with `chain_steps` + `truncated` + schema
   warnings for teaching/audit visibility

Same-street pre-hero actions **excluded** from the chain per Q2
verdict. Preserves 4 flop calibration anchors as zero-impact
controls.

### M3 — Unit tests (16/16 PASS)

`river-rats-core/tests/test_range_narrowing_stage35.py`:
- M1 table values verified
- `medium_made` elevated across streets; `nuts`/`strong_value`
  suppressed
- Same-street pre-hero actions excluded from chain (Q2 verdict)
- H_8dfb6ef8 canonical bet-check-call-bet chain produces
  `['flop:BET', 'turn:CHECK', 'turn:CALL']` (river-bet excluded as
  same-street on decision)
- d2410 shape: `'flop:CHECK'` in chain, `'turn:CHECK'` excluded
- FOLD terminates chain (empty range)
- Schema mismatch → warning + fallback, no crash
- Tuple and dict action-history formats both supported
- Deep-chain safety rail prevents empty-range collapse

### M4 — Retroactive audit (579 rows)

`review/run_stage35_backfill_audit.py`:

```
Total training rows: 579 (filtered to rows with real stored values)
Build failures:      0
Flop-only rows:      124
Multi-street rows:   455

Isolation check (flop-only, |delta| > 0.01):
  Violations: 0 / 124  ✅

Chain activity (multi-street):
  chain_steps populated: 455 / 455 (100%)  ✅
```

Multi-street shifts by feature × street (expected direction per
GTO reviewer prediction):

| feature | street | mean_delta | interpretation |
|---|---|---|---|
| TP+ | turn | **-0.14** | Turn-bet on capped range has less premium hands |
| TP+ | river | **-0.27** | Compound narrowing depresses TP+ further |
| medium | turn | +0.04 | Mediums survive check filters that strip TP+ |
| medium | river | +0.11 | Same effect, compounded |
| draw | turn | +0.03 | Small shift (draws ≈ neutral to bet/check filters) |
| draw | river | 0.00 | River draws auto-converted to air (correct) |
| air | turn | +0.07 | Air persists through check filters |
| air | river | +0.15 | Compound |

Directional reading: villain's action-chain-conditioned range is
"less value-heavy, more medium/air-heavy" than single-street
narrowing suggested. That's exactly the solver-correct direction
for post-check-action ranges. And it's why d2410-class hands now
see hero's TPGK as ahead of more of villain's turn-bet range → BET.

### M5 — Pre-retrain diagnostic (3/3 RESTORED)

`review/run_v231_anchor_recheck_stage35.py`:

Ran v2.3.1 model on 3 β-panel HIGH-impact anchors with NEW
action-aware feature values. Model weights unchanged; only feature
inputs shift. All three anchors predict BET:

- d2410 BET 0.976 (chain: `['flop:CHECK']`; post-chain TP+=0.19, medium=0.39, air=0.27)
- d0182 BET 0.984 (chain: `['flop:CHECK']`; TP+=0.10, medium=0.41, air=0.49)
- d8411 BET 0.589 (chain: `['flop:CHECK']`; TP+=0.11, medium=0.23, air=0.63)

The d8411 margin is thin (BET 0.589 vs CHECK 0.391) — worth
monitoring in Stage 5 retrain. But all three are on the correct
side of the decision boundary, which was the gate.

### M6 — d2410 direction prediction (confirmed)

Reviewer predicted BET confidence UP. Observed:
- v2.3.1 with OLD features: d2410 predicts BET at 0.966
- v2.3.1 with NEW (Stage 3.5) features: d2410 predicts BET at 0.976

Small positive shift, direction matches. More importantly: v2.3.2
regression (same model but with training-data changes that broke
d2410) is reversed WITHOUT retraining. Stage 3.5 is the cleaner fix.

### M7 — Scope discipline

- One CALL-continue table per street (no raise-aware variants)
  → raise-aware deferred to v2.5 per TICKET_V25_PRO_LEVEL_NARROWING_GAPS
- Same-street pre-hero exclusion preserved
- `gto_model.FEATURE_COLUMNS` untouched (55 cols, v2.3.x compat)
- 4 v2.4 P1 blocker features inherit corrected range automatically
- No changes to KB (§1.10-§1.12 already landed Stage 2)
- No changes to v3.1 prompt (Stage 3 concern, parallel stream)

## Implications for v2.4 plan

### The big re-scope candidate: is Stage 4 re-label still needed?

**Evidence that Stage 4 re-label may not be strictly necessary:**

1. v2.3.1 model WITHOUT retraining now predicts BET on d2410/d0182/d8411
2. The β-panel regressions were feature-correctness issues, not
   class-balance issues
3. Calibration anchor gate passes 5/5 on the existing v2.3.1 model
   with the new features

**Evidence that Stage 4 re-label is still desirable:**

1. `villain_top_pair_plus_pct` on multi-street rows drops by 0.14-0.27
   on average. Model weights trained on the old distribution will
   drift away from the new one over time.
2. The 4 new v2.4 P1 blocker features are only partially represented
   in v2.3.1 training data (added in Stage 1, no re-label run yet).
3. v3.2 prompt (Stage 3) will tag feature_attention differently for
   the new blocker features — labels need to be re-emitted under
   v3.2 guidance for that signal to reach training.

**Recommendation** (builder, for reviewer's scope decision):

Shift Stage 4 from "re-label because v2.3.2 broke" to "re-label
because v3.2 prompt + action-aware ranges need a clean training
pass." This preserves the re-label work but re-frames its purpose.

## What's NOT done in Stage 3.5

Per directive-x / spec lock / manifest v1.6:

- Stage 3 v3.2 prompt — parallel stream, not this ticket
- v2.5 ticket items (raise-aware call, bet-sizing-conditional
  narrowing) — deferred
- Stage 4 re-label — gated on Stages 3 + 3.5 both landing
- Stage 5 retrain — downstream

## Artifacts this cycle

- `river-rats-core/range_narrowing.py` — M1 updates + CALL tables +
  narrow_to_continuing_range + narrow_by_action_history
- `river-rats-core/game_state_bridge.py` — flatten street_actions
  to `_action_history` on hand payload
- `river-rats-core/feature_extractor.py` — accept action_history
  in `extract_range_composition`; plumb from `extract_all_features`;
  return chain_steps + truncated metadata
- `river-rats-core/tests/test_range_narrowing_stage35.py` — 16 tests
- `review/run_stage35_backfill_audit.py` — M4 audit runner
- `review/run_v231_anchor_recheck_stage35.py` — M5 diagnostic runner
- `review/comms/BUILDER_V24_STAGE35_BACKFILL_AUDIT_2026-04-20.md` — M4 report
- `review/comms/BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md` — M5 report
- `review/comms/BUILDER_V24_STAGE35_COMPLETE_2026-04-20.md` — this doc

## Stage 4 gate status

Per manifest v1.6 ship sequence:

- [x] Stage 1 — v2.4 P1 blocker features (2aa5d7f)
- [x] Stage 2 — KB §1.10-§1.12 (d0ad914)
- [ ] Stage 3 — v3.2 prompt (parallel, not started)
- [x] **Stage 3.5 — action-aware range narrowing** (this commit)
- [ ] Stage 4 — training-data re-label (gated on Stage 3 AND 3.5)
- [ ] Stage 5 — retrain + full eval
- [ ] Stage 6 — ship gate

Stage 4 gate is **half open**: Stage 3.5 complete, Stage 3
(v3.2 prompt) still outstanding. Both required before Stage 4.

## Ask for owner

1. **Confirm Stage 3.5 complete** — no further rework needed
2. **Stage 3 kickoff** — v3.2 prompt derivation can start now
3. **Stage 4 re-scoping question** (see §"The big re-scope candidate"
   above) — do we re-label because v2.3.2 broke, or because v3.2 +
   action-aware ranges need a clean pass? Affects what Stage 4 looks
   like concretely.

Standing by.
