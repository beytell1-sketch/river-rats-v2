---
date: 2026-04-19
from: Builder
to: Main terminal / Owner
re: v2.4 P0 — calibration-anchor pre-flight gate LANDED + retroactive audit
status: P0 COMPLETE — gate validated against v2.2/v2.3.1/v2.3.2
---

# v2.4 P0 — Calibration-Anchor Pre-Flight Gate (Landed)

Per directive-x: 5 seed anchors, Tier 0 pre-flight, catches distribution-
shift in seconds.

## Artifacts committed

- `river-rats-core/anchors/calibration_anchors.json` — fixture (5 seeds)
- `river-rats-core/evaluate_calibration_anchors.py` — runner (CLI + import)
- This report

## Runner contract

**Standalone CLI:**
```
python3 river-rats-core/evaluate_calibration_anchors.py \\
    --model river-rats-core/models/<model>.json \\
    --csv training-data/<csv>.csv \\
    [--json]  [--strict-exit]
```

**Import (for future train-script trailers):**
```python
from evaluate_calibration_anchors import run_anchor_gate
results = run_anchor_gate(model_path, csv_path)
failed = [r for r in results if not r.passed and not r.skip_reason]
```

No training-script wiring yet per directive-x ("Do NOT yet: start model
training"). When the next retrain fires (after P1 plans complete), the
trailer hook is a 3-line addition.

## Seed anchors (5)

| anchor_id | expected | rationale |
|---|---|---|
| `d2410_CO_turn` | BET | Calibration anchor from v3.1 Notes. TPGK on J-high turn, compressed SPR ~1.25, worse_pct 0.82. The exact anchor v2.3.2 regressed on. |
| `LITMUS_A4d_Qs5s7s_flop` | CHECK | v2.3.1 playtest fix. Air on 3-spade flop, checked-to BTN. v2.3 predicted BET 98.6% — Layer 1 + Layer 2 fixed to CHECK 93%. |
| `LITMUS_T5h_JJ2_flop` | CHECK | v2.3.1 playtest fix. 10-high on paired JJ2, checked-to BTN. v2.3 predicted BET 72% — fixed to CHECK 98%. |
| `LITMUS_AA_7h5d2c_flop` | BET | v2.3.2 Path C value litmus. Overpair on dry board — solver value bet. |
| `LITMUS_KQ_KsTs3h_flop` | BET | v2.3.2 Path C value litmus. TPGK on two-tone — solver value-and-protect bet. |

Tolerance: all 5 are `strict` (top-1 legal-masked action must equal expected).

## Retroactive audit

| Model | d2410 | A4d/Qs5s7s | T5h/JJ2 | AA/7h5d2c | KQ/KsTs3h | Pass |
|---|---|---|---|---|---|---|
| **v2.2** (production) | BET 0.263 | CHECK 0.397 | CHECK 0.427 | BET 0.686 | BET 0.688 | **5/5** |
| **v2.3.1** (iter baseline) | BET 0.973 | CHECK 0.935 | CHECK 0.983 | BET 0.950 | BET 0.993 | **5/5** |
| **v2.3.2** (shelved) | **CHECK 0.287** | CHECK 0.958 | CHECK 0.984 | BET 0.995 | BET 0.992 | **4/5** — d2410 fails |

v2.3.2's d2410 failure: model probability for the expected BET is only
0.287 (legal-masked CHECK wins at 0.713). The gate catches this exactly
as predicted by the β panel re-label work.

**Speed:** end-to-end gate runs in ~2 seconds vs 45 min of self-play.
Target metric achieved.

## Observations from the audit

Three points worth flagging, none blocking P0:

1. **v2.2 margins are thin.** Air litmuses pass with only 0.397 / 0.427
   probability on CHECK — these are essentially coin-flips on v2.2.
   Layer 1 (`board_adjusted_hrp`) + Layer 2 (air-CHECK counter-examples)
   in v2.3.1 push these to 0.935 / 0.983. The gate will pass v2.2 but
   future retrains should clear the margin comfortably. Not a false
   positive risk, but worth monitoring.

2. **d2410 margin is narrow on v2.2 too.** v2.2 passes d2410 with only
   0.263 probability on BET (legal-masked CHECK would only need to cross
   0.263 to flip). This is a "barely passes" case on the production
   baseline. One interpretation: d2410 has always been close; v2.3.2
   pushed it across the line.

3. **The "FAILURE detail" output currently shows `p(expected)` but not
   `p(predicted)`.** If reviewer wants, I can add the competing action's
   probability to the failure report. Minor formatting tweak.

## What P0 provides for v2.4

- Every future `train_v2_N_M.py` can add a trailer:
  ```python
  from evaluate_calibration_anchors import run_anchor_gate, render_report
  results = run_anchor_gate(out_model, csv_path)
  logger.info(render_report(results))
  if any(not r.passed for r in results):
      logger.error("CALIBRATION ANCHOR FAIL — see above. Do not accept.")
  ```
- P1b Path C rescope work gets this gate for free on every iteration.
- Regression bisecting: given two models, diff anchor results to localize
  which class broke.

## Future work (deferred per directive-x)

Not in P0 scope:

- Train-script trailer wiring — deferred until next retrain fires
- Expand seed set from 5 to ~15-20 (MW-30, MW-33, MW-50 reversal anchors
  from v3.1 Calibration Notes; d8886, d8963, d3178) — add as P1 lands
  and gates prove out
- Mixed-tolerance anchors (d8886, d8963 are solver 50/50 spots — need
  tolerance=`mixed` path well-tested; current 5 seeds are all strict)
- `--anchors-bisect` CLI mode: given two model paths, diff which anchors
  differ — convenience tooling for future regression hunts

## Next action

Moving to P1 parallel stream now: three plan docs for the new blocker
features (`nut_flush_block`, `draw_block_pct`, `nut_made_block_pct`),
each expert-reviewed by GTO reviewer subagent before any code.

No training fires until P1 plans are approved.
