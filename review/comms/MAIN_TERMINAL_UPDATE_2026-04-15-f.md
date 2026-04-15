---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Post-Round-3 directives — Track 2 closes, Track 6 launches, Stream C opens
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-15 (f)

Round 3 accepted (`REVIEW_ROUND3_2026-04-15.md`). Execute the
following.

## 1. Close Track 2

Canonical numbers:
- FB-40: 72.5% (29/40) on live `v2_2_model.json`
- MW-50: **84.0% (42/50)** on live `v2_2_model.json`,
  d2920-IN / d4534-IN (not d4534-OUT)

Update `V22_TRAINER_PORT_2026-04-15.md` §4 with:
- 84% adopted as canonical; 80% reclassified as
  recovered-eval shadow-model measurement, preserved in
  `review/recovered/` for reference
- Track 2 status: CLOSED

Commit + push.

## 2. Launch Track 6 (architect)

Single architect call. Apply to
`review/comms/PLAN_V23_SCOPE_2026-04-15.md` in place:

### 2.1 BET delta reconciliation

Allocation table says +166 BET; narrative says +155 + 31
protection. Pick one accounting. If protection BETs are a
subset of total BET (likely), narrative says "+166 BET (of
which ~31 are protection)". If they are additive, allocation
table becomes +186. One number, consistent everywhere.

### 2.2 Section 2 bias signature — replace wording

Drop entire `hero_range_percentile = 0.00` and "bucket-first
CHECK bias" framing. Replace with the Stream B.2 adopted
wording (verbatim block below, then expand into a Section 2
that references the preconditions as measurable predicates):

> **Defensive multiway-checked-through CHECK bias.** The v2.2
> model underbets in multiway pots where villain(s) have
> checked the previous street, villain ranges are capped, hero
> sits at or above median range strength with worse_hand_pct
> ≥ 0.55, and SPR is low (≤ 2). The model reads mutual
> passivity plus villain_top_pair_plus density as
> range-vs-range standoff and defaults to pot-control CHECK,
> overriding the value+protection case that the passive
> villain line actually enables. The v2.3 supplement should
> target this bucket specifically; a uniform "bet more often"
> correction would overshoot.

Precondition predicate for supplement targeting:
`facing_bet=False ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
 villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧
 equity_vs_range≥0.35 ∧ SPR≤2.0`

Also add the secondary fix — Pass 1 prompt override clause:
> When villain_checked_back=1, villain_range_capped=1,
> num_opponents≤2 (or specifically ≥2 in MW context), and
> hero's worse_hand_pct exceeds 0.55, prefer BET for
> value+protection even when OOP or holding a medium-strength
> made hand. The passive line forfeits the capped villain's
> air portion.

Both fixes are committed in scope; supplement sizing pending
Stream C (§3).

### 2.3 Explicit calibration gate

Add a gate section stating: "v2.3 training must pass the
calibration exam (23/28 minimum, scaled from v2.2's 20/24) +
all reversal hands correct, before any v2.3 production
labelling begins. Any failure returns to panel redesign."

### 2.4 Track E amendments

Apply to `PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md` in
place:

1. Absolute accuracy floor on Groups A+B: 70% minimum in
   absolute terms, not just 5pp improvement over v2.2.
2. Group D regression fallback: if v2.3 regresses on Group D
   reversal accuracy by >1 hand vs v2.2, stop and investigate
   before ship.

### Deliverable

Updated scope docs in place. Commit message lists the
amendments applied. Push.

## 3. Launch Stream C — training CSV label spot-check

Single programmer call. Analysis only, no code changes.

### 3.1 Scope

Query `training-data/v2_2_training.csv` for rows matching:
`facing_bet=0 ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
 villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧
 equity_vs_range≥0.35 ∧ spr≤2.0`

(Note: mixed-encoding CSV — use the CAT_MAPS path from the
ported trainer. Load via `--allow-mixed-encoding` equivalent.)

Report:
- Total rows matching the bucket
- Action-label distribution: % CHECK / BET / CALL / RAISE / FOLD
- Median `hero_range_percentile`, `equity_vs_range`,
  `worse_hand_pct` in the bucket
- Any rows stamped `label_source=panel_reversal` or similar
  override metadata, counted separately

### 3.2 Verdict logic

- If > 30% CHECK in the bucket → label conservatism compounds
  the model bias. v2.3 supplement sizing targets the upper
  end (800 hands).
- If ≤ 30% CHECK → label signal is healthy; model failed to
  learn despite correct labels. Supplement sizing targets the
  lower end (400 hands).
- If bucket has < 20 rows total → training-data sparsity in
  this precondition shape IS the root cause. Supplement
  sizing critical; flag for architect adjustment of scope.

### 3.3 Deliverable

`review/comms/STREAM_C_TRAINING_BUCKET_ANALYSIS_2026-04-15.md`
with the table, verdict, and supplement-size recommendation.

Feeds into Track 6 amendment §2.2. Architect may need to
re-enter after this lands to finalize supplement sizing.
Acceptable for Track 6 to ship in two commits (initial +
sizing update) rather than wait.

## 4. Forensic verification (low priority)

Run `review/recovered/eval_MW_with_legal_action_masking.py`
as-is, unmodified, from its recovered location. Confirm it
reproduces:
- MW-50 = 80.0% (40/50)
- Hand swap: d2920-IN / d4534-OUT

If yes, attach a one-line confirmation to
`V22_TRAINER_PORT_2026-04-15.md`. Shadow-model finding closes
cleanly.

If no, report the discrepancy — there may be another
difference beyond the shadow-model retrain.

Single programmer call. Not blocking anything.

## 5. Stream A artifacts — already accepted

No further work needed on:
- `river-rats-core/train_model_v2_2.py`
- `river-rats-core/evaluate_v2_2.py`
- `review/recovered/` (preserved)
- CLAUDE.md §6 addendum

## 6. Still held / gated

- v2.3 hand generation: gated on Track 6 approval + owner
  signoff
- Clean-CSV retrain: deferred (PLAN_CONSOLIDATED §4)
- v3.0 action distributions: backlog
- Gate 7 ship/iterate: owner call (criterion-pass clears
  the numeric case)

## 7. Protocols

- Test-first on Stream C analysis script if you write one.
- Commit per deliverable, push immediately.
- Any STOP-condition during Track 6 amendment: pause and
  report rather than improvise the scope decision.
