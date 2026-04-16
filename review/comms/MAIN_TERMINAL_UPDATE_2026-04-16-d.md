---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Phase 0 accepted; launch Phase 1 now
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-16 (d)

## 1. Phase 0 preflight — accepted

All 8 checks resolved acceptably:

- 0.1 test suite: 50 pass / 3 fail — the 3 fails are ANOMALY-A
  on `v2_2_training.csv` (out of scope; known).
- 0.2 `normalise_situation` round-trip: 10/10 clean.
- 0.3 BP JSONL schema preflight: 4/4 pass (Fix 1 holds).
- 0.4 disk 769 GB: fine.
- 0.5 git clean.
- 0.6 `gto_labeller_v3.md` absent: expected (Phase 3
  prerequisite).
- 0.7 `calibration_exam.py` present with `run_calibration`
  entry + `GTO_REVERSAL_HANDS` at line 33: fine.
- 0.8 all 5 generators present with `generate_all()` entries.

Phase 3.5 insertion verified in place (V23_HAND_GENERATION_PLAN
lines 373–504; stop conditions S3.5.1–S3.5.7 landed in §8).

## 2. Launch Phase 1 now

Phase 1 (generation) is independent of Phase 3.5 (labelling
gate). They are sequentially separated. No reason to pause
Phase 1 for a Phase-4-adjacent review.

Execute Phase 1 per plan §1:
- 11 factory buckets via `generate_factory_batch6.py`, 25%
  overshoot, per-bucket JSONL output
- Curated-draw filter surfaces candidates → lands in
  `V23_CURATED_CANDIDATES_2026-04-16.md` for owner spot-check
  (async, non-blocking)
- Solver-sourced cohort waits on owner-led GTO Wizard sessions
  (non-blocking)

Commit cadence per §7: one commit per bucket JSONL.

## 3. Ordering for the next prerequisites (parallel)

Run alongside Phase 1 — these are Phase 3 prerequisites and
should be ready before Phase 3 begins:

### 3.1 `prompts/gto_labeller_v3.md` creation

Copy v2 prompt, apply Scope §3 additions A–D, insert the
Stream B.2 override clause verbatim per
MAIN_TERMINAL_UPDATE_2026-04-16-b §1:

> When villain_checked_back=1, villain_range_capped=1,
> num_opponents≥2, and hero's worse_hand_pct exceeds 0.55,
> prefer BET for value+protection even when OOP or holding a
> medium-strength made hand. The passive line forfeits the
> capped villain's air portion.

Cross-reference comment to MW_MISS_BIAS_ANALYSIS_2026-04-15.md.

Gate: complete before Phase 3 runs.

### 3.2 `calibration_exam.py` update

- Threshold 23/28 (up from 20/24)
- 4 new hard anchors
- Group-D reversal ingestion

Gate: complete before Phase 3 runs.

## 4. Flags from Phase 0 — logged, non-blocking

- **batch4 JSONL absent.** Phase 1 target; not a preflight
  failure. Will be regenerated in Phase 1.
- **v3 prompt absent.** Phase 3 prerequisite; §3.1 above.
- **ANOMALY-A retrain flag.** Retraining on current
  `v2_2_training.csv` needs `--allow-mixed-encoding`. When the
  v2.3 assembly step produces a clean CSV (BP JSONLs from Fix 1
  + d-series), the flag must NOT be needed — the v2.3 preflight
  gate must pass cleanly. Verify at Phase 5 assembly. If the
  clean CSV still fails preflight, STOP — that's a regression
  in the generator fix.

## 5. Agent budget

Phase 1 is the cheap phase (~30-45 min, ~11 bucket-level
programmer calls + filter run). Most of the v2.3 critical path
spend is Phase 4 labelling (~168 agent calls). Phase 3.5 adds
~80 calls to that but saves catastrophic rework if the prompt
is wrong. Good trade.

## 6. Stop-conditions reminder

The plan's stop conditions apply from Phase 1 onward. Specific
to Phase 1:
- Factory yield loss > 25% overshoot → STOP (generator defect
  or predicate too narrow)
- `normalise_situation` round-trip fails on any generated
  JSONL → STOP (Fix 1 regression)
- Schema preflight fails on any bucket output → STOP (encoding
  regression)

## 7. Reporting

Per-bucket results land in
`review/comms/PHASE_1_BUCKET_<name>_2026-04-16.md` (or bundled
in a single `PHASE_1_GENERATION_2026-04-16.md` if builder
prefers — your choice, bundled is fine). Push each commit
immediately.

---

**Launch Phase 1 now. Run §3.1 and §3.2 in parallel. Phase 4
still gates on Phase 3 + Phase 3.5.**
