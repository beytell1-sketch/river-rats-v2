---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #14 (Task 3 Stage 5 retrain protocol v1.0) — REQUEST-CHANGES verdict; fix-forward to v1.0.1 required (column-count self-contradiction + anchor inventory mismatch + variance-math)
status: DIRECTIVE — 2 MEDIUMs + 1 MEDIUM-NIT to address; same pattern as Tasks 1.1 + 2.1; fix-forward branch stage4-prep/stage5-retrain-fill-3-1
---

# PR #14 Fix-Forward Required — Stage 5 Retrain Protocol v1.0.1

## Reviewer verdict summary

PR #14 verdict at `463e718`: **REQUEST-CHANGES** — stronger than
APPROVE-WITH-NITS. Reviewer explicitly recommends Task 3.1 fix-forward
before merge. Status:

> "REQUEST-CHANGES — 2 MEDIUM-severity issues found... recommend
> Task 3.1 fix-forward before merge per Task 1/2 fix-forward
> pattern. Protocol's ML core (hyperparameters defence, seed scheme,
> gate thresholds, rollback enumeration) is production-quality."

Per memory `feedback_quality_default_no_ask.md`: standing pattern
applies. PR #14 held pending fix-forward.

## The 2 MEDIUM findings + 1 MEDIUM-NIT

### MEDIUM #1 — Prereq #2 column-count self-contradiction (Item G)

Protocol §Prereq #2 reads: *"110-column contract (54 raw + 4 v2.4
blocker = 58 raw + 58 attn_*)"*

**Three problems:**
1. **v2.3.2 is 55 raw + 55 attn_* = 110 columns** (verified against
   `gto_model.py:33-62` — 55 features ending at `board_adjusted_hrp`;
   v2.3.2 training report `n_features: 110`)
2. **v2.4 is 55 raw + 4 blocker + 59 attn_* = 118 columns** (consistent
   with §Hyperparameters line 155: "training-tensor goes 110 → 118
   columns")
3. **The string "54 raw + 4 v2.4 blocker = 58 raw + 58 attn_*" gives
   116 columns** (58+58), neither 110 nor 118. AND "54 raw" undercounts
   v2.3.2 by 1.

§Hyperparameters reasoning gets the count right (54+54=108 v2.2;
55+55=110 v2.3.2; 55+59=118 v2.4). Internally inconsistent.

**Fix-forward action:** rewrite Prereq #2 to:

> "118-column v2.4 contract (55 raw + 4 v2.4 blocker = 59 raw +
> 59 attn_*) validated, OR the contract is updated and the change
> is documented in the report."

Mechanically blocks the prereq from being executable as a check until
fixed (verifier can't tell whether 110, 116, or 118 columns is the
target).

### MEDIUM #2 — Mode D anchor inventory mismatch (Item F)

Mode D references *"the 3 d-series anchors (d2410, d0182, d8411)"*
(lines 638-639, 643-644).

**Reality:** `river-rats-core/anchors/calibration_anchors.json` contains
exactly 5 anchors:
- `d2410_CO_turn`
- `LITMUS_A4d_Qs5s7s_flop`
- `LITMUS_T5h_JJ2_flop`
- `LITMUS_AA_7h5d2c_flop`
- `LITMUS_KQ_KsTs3h_flop`

**Anchors `d0182` and `d8411` are NOT in the active calibration set.**

The pre-Stage-3.5 closure doc (`MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`)
treats them as live anchors. Either (a) they were renamed to LITMUS_*
in Stage 3.5 and v1.0 hasn't updated the IDs, or (b) the protocol
assumes they will be re-added before Stage 5.

Either way, Mode D as written is not directly executable against
current `evaluate_calibration_anchors.py` infrastructure.

**Fix-forward action:** v1.0.1 must resolve the anchor naming. Two
options:
- (a) Update Mode D to use LITMUS_* IDs (if d0182/d8411 were renamed
  in Stage 3.5)
- (b) Add Prereq #6 requiring d0182/d8411 to be re-instantiated in
  `calibration_anchors.json` before Stage 5 begins

Builder discretion on (a) vs (b) — depends on the actual Stage 3.5
rename status. Verify against the current `calibration_anchors.json`
content + Stage 3.5 commit history.

### MEDIUM-NIT — Variance-reduction math (Item E)

§Ensemble vs median table line 472 claims *"~30% lower predictive
variance (1/√3)"*.

**Mathematically wrong:**
- 1/√3 ≈ 0.577 is the **SD ratio** for averaging N=3 independent models
- That's **~42% reduction in SD**, or **~67% reduction in variance**
  (variance reduces by 1/N)
- "30% lower predictive variance" is neither 1/√3 nor 1/3

Directional argument correct; specific number wrong. ML rigour
requires the math to be right since this protocol cites specific
numbers.

**Fix-forward action:** rewrite as one of:
- "~42% lower predictive SD (1/√3 ≈ 0.577 ratio)"
- "~67% lower predictive variance (1/N ratio for N=3)"

Pick whichever framing is most natural for the surrounding context.

## NITs that defer (not fix-forward blockers)

Reviewer flagged several LOW NITs:

- **3-seed minimum framing** (Item B): Bouthillier 2021 actually
  recommends ≥10 seeds for variance estimation; v1.0 oversells "3
  is enough for variance estimation." Acknowledged in v1.0 (line 232
  + 5-seed expansion path on MARGINAL spread); acceptable but could
  tighten language.
- **±2pp vs cv_std statistical nuance** (Item D): between-seed
  variance with same data ≠ within-fold standard deviation. ±2pp may
  be too LOOSE in practice. UNCERTAIN tag at line 381-385 acknowledges
  this; acceptable.
- **Prereq #3 auto-rollback tagging** (Item G): "Baseline model
  preserved as rollback" — not automatic. v1.0.1 could explicitly
  assign this to orchestrator-pre-Stage-5 step.
- **Mode E MW baseline number gap** (Item F): v2.3.2 MW reference-set
  baseline is unclear from artifacts. Could be addressed by Prereq #6
  (measure v2.3.2 MW reference-set baseline before Stage 5) OR cite
  specific MW-accuracy number.

These are LOW-severity. Fold into Task 3.1 if ergonomic OR Task 5
wrap-up commit.

## Fix-forward workflow (mirror Task 1.1/2.1 pattern)

1. **New branch:** `stage4-prep/stage5-retrain-fill-3-1`
2. **Author dispatch:** address MEDIUM #1 (column-count rewrite),
   MEDIUM #2 (anchor inventory resolution), MEDIUM-NIT (variance math)
3. **Reviewer dispatch (different agent):** verify all 3 MEDIUMs
   addressed; verify no new MEDIUMs introduced; check anchor IDs
   against current `calibration_anchors.json` empirically
4. **Open PR #15** with title "Stage 4 prep Task 3.1: Stage 5 retrain
   protocol v1.0.1 (REQUEST-CHANGES fix-forward)"
5. **Standing PR pattern:** 4-checkpoint state protocol, verdict on
   PR thread, builder writes verdict comms, orchestrator merges on
   APPROVE
6. **PR #14 disposition:** orchestrator merges PR #15 (which contains
   PR #14's content as ancestor) — same auto-resolution pattern as
   PR #10 → #11 and PR #12 → #13

## Estimated fix-forward effort

~30-45 min for the 2 MEDIUMs + 1 MEDIUM-NIT (text-only changes,
straightforward to verify against existing infrastructure). Plus
reviewer dispatch ~15-30 min. Total ~1 hour.

## Cross-stream — unchanged

Task 4 (Stage 6 held-out) and Task 5 (Pilot orchestration) sequencing
unchanged. Builder may run Task 3.1 in parallel with Task 4 OR
sequential per their plan.

## Action

**Builder:**
1. Pick path: stay sequential (Task 3.1 first, then Task 4) OR
   parallel
2. Author dispatch on `stage4-prep/stage5-retrain-fill-3-1`
3. Reviewer dispatch (independent)
4. PR #15 per standing pattern
5. After PR #15 APPROVE: orchestrator merges (auto-resolves PR #14)

**Orchestrator (me):**
1. PR #14 held pending fix-forward
2. PR #15 (Task 3.1) merge per standing pattern after APPROVE
3. Loop continues at 15-min cadence

## Reference

- `MAIN_TERMINAL_PR_12_FIX_FORWARD_REQUIRED_2026-04-26.md` (`31aa43c`)
  — Task 2.1 fix-forward precedent
- `MAIN_TERMINAL_PR_13_MERGED_TASK3_GREENLIGHT_2026-04-26.md` (`0d9bdfb`)
  — Task 2 closure pattern
- `463e718` — PR #14 reviewer verdict (REQUEST-CHANGES)
- `feedback_quality_default_no_ask.md` — "MEDIUM/non-blocking →
  still address; don't defer"
