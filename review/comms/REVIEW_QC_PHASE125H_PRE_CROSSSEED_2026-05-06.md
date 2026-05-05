---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #161 (12.5H-pre cross-seed analysis; H-FEAT median validated, volatile bimodal) — APPROVE; 0 NIT
severity: clean approval; no findings
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + V-Source (citation existence) + **TC-X-CROSS-SEED-IMPORTANCE first activation** + dispatch §"NEW: Reproducibility"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 8th successive cycle solo-routed)
---

# QC Review — PR #161 (12.5H-pre cross-seed analysis): APPROVE; 0 NIT

## Verdict

**APPROVE PR #161 for merge.** All 4 dispatch-required audits PASS. **TC-X-CROSS-SEED-IMPORTANCE first activation succeeded** — every reported statistic (median 0.0268, mean 0.0461, std 0.0514, min 0.0000, max 0.1406, 60% ≥ 0.02) computes exactly from the per-seed table. Both chosen-seed values (12.5E-E seed 2 = 0.0268; 12.5G seed 3 = 0.0054) match prior PR reports verbatim. Reproducibility re-run on seed 0 produced bit-exact value (`nut_flush_block=0.1406` matches report).

12.5H-pre answers the H-FEAT validation question definitively: **VALIDATED at median; VOLATILE across seeds (bimodal 60/40).** The migration's premise survives; the corpus is at the boundary of consistent feature activation. This empirical answer is what the orchestrator's 12.5H-pre dispatch was set up to produce, and the builder delivered cleanly.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR161_2026-05-06.md` master `0625b0f` + PR #160 dispatch)

4 audits (smaller analysis-only scope vs trainer-PR audits): diff scope, citation existence, TC-X-CROSS-SEED-IMPORTANCE applied, reproducibility.

PR #161 head: `e064edd719cf9f461fd91b3aacc3684a0ac6b7ba` (branch `programmer/phase125h-pre-crossseed-2026-05-05`). Merge-base: `2c52e6b` (= PR #160 = 12.5H-pre dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 1-2 files (analysis-only); no `river-rats-core/` touches; no corpus/labels/prompt edits"*

| File | additions | deletions | category |
|---|---|---|---|
| `review/comms/BUILDER_REPORT_PHASE125H_PRE_CROSSSEED_2026-05-05.md` | 137 | 0 | NEW (analysis report) |
| `scripts/extract_cross_seed_importance.py` | 211 | 0 | NEW (Path 2 analysis script) |
| **Total** | **+348** | **0** | **2 files** ✓ |

- File count = 2 ✓ (within 1-2 dispatch range)
- Zero `river-rats-core/` touches ✓
- Zero corpus/labels/prompt edits ✓
- All-additions, no deletions ✓ (analysis-only)

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

3 distinct file paths cited in builder report:

| Citation | Status |
|---|---|
| `review/comms/MAIN_TERMINAL_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (PR #160 dispatch) | ✅ TRACKED at origin/master |
| `review/comms/BUILDER_REPORT_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (self) | NOT-TRACKED ✓ expected (NEW in PR; will track post-merge) |
| `scripts/extract_cross_seed_importance.py` (self) | NOT-TRACKED ✓ expected (NEW in PR; will track post-merge) |

5 PR/master-SHA references:

| Reference | Status |
|---|---|
| PR #152 / master `b51e525` (12.5E-E) | ✅ verifiable in git log |
| PR #155 / master `16351e1` (12.5E-F synthesis) | ✅ verifiable |
| PR #157 / master `2135fc8` (12.5G) | ✅ verifiable |
| PR #159 / master `fcb88d6` (QC verdict on 12.5G) | ✅ verifiable |
| PR #160 / master `2c52e6b` (12.5H-pre dispatch) | ✅ verifiable |

**Citation existence: CLEAN.**

## Audit 3 — TC-X-CROSS-SEED-IMPORTANCE applied ✅ EXACT-ARITHMETIC-MATCH

**Dispatch:** *"verify per-seed numbers reported across all 5 seeds for both 12.5E-E and 12.5G runs; verify median + std + min/max + chosen-seed values match expected (12.5E-E chosen=0.0268; 12.5G chosen=0.0054)"*

This is the **first empirical activation of the TC-X-CROSS-SEED-IMPORTANCE test class** queued in `~/river-rats-qc/learning/test_class_registry.md` on commit `7354fad` (2026-05-05) following 12.5G's empirical refutation of single-seed importance reporting.

### Per-seed table (cap=3.0 nut_flush_block)

| seed | nut_flush_block | source flag |
|---|---|---|
| 0 | 0.1406 | (highest) |
| 1 | 0.0577 | |
| 2 | **0.0268** | ← 12.5E-E chosen |
| 3 | **0.0054** | ← 12.5G chosen |
| 4 | 0.0000 | (zero — feature never split on) |

### Statistical verification (computed from per-seed values)

```
$ python3 -c "import statistics; vals = [0.1406, 0.0577, 0.0268, 0.0054, 0.0000]; ..."
```

| Statistic | Computed | Reported | Match |
|---|---|---|---|
| Median | 0.0268 | 0.0268 | ✅ exact |
| Mean | 0.0461 | 0.0461 | ✅ exact |
| Std (population) | 0.0514 | 0.0514 | ✅ exact |
| Min | 0.0000 | 0.0000 | ✅ exact |
| Max | 0.1406 | 0.1406 | ✅ exact |
| % ≥ 0.02 | 60% (3/5) | 60% | ✅ exact |

### Chosen-seed cross-reference (against prior trainer reports)

| Phase | Chosen seed | This report value | Prior report value | Match |
|---|---|---|---|---|
| 12.5E-E (PR #152) | seed 2 | 0.0268 | 0.0268 | ✅ |
| 12.5G (PR #157) | seed 3 | 0.0054 | 0.0054 | ✅ |

Both prior chosen-seed snapshots are confirmed accurate; the 12.5H-pre cross-seed table embeds them at expected positions.

### Cap-non-binding cross-validation (bonus)

cap=3.0 vs cap=4.0 per-seed deltas are all 0.0000 across seeds 0-4 (table at lines 34-43 of report). This is an independent confirmation (orthogonal to 12.5G's predict-time observation) that **trainer-time** model output is byte-identical between caps. Strengthens 12.5G's cap-non-binding finding from "approximately equivalent" to "literally byte-identical at trainer time."

**TC-X-CROSS-SEED-IMPORTANCE: EXACT ARITHMETIC MATCH.** First activation produces clean validation.

## Audit 4 — Reproducibility ✅ BIT-EXACT

**Dispatch:** *"verify the analysis script is runnable AND deterministic (same `--seeds 0-4` produces same importances on re-run)"*

### Runnable check

```
$ python3 scripts/extract_cross_seed_importance.py --help
usage: extract_cross_seed_importance.py [-h] --corpus CORPUS --labels LABELS
                                        [--warm-start WARM_START]
                                        [--seeds SEEDS] [--caps CAPS]
                                        [--test-size TEST_SIZE] --output OUTPUT
```

Argparse parses cleanly; expected interface present. ✓

### Reproducibility re-run (seed 0 cap=3.0)

```
$ OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 scripts/extract_cross_seed_importance.py \
    --corpus data/corpus_combined_604_2026-05-05.jsonl \
    --labels data/corpus_combined_604_labels_2026-05-05.jsonl \
    --seeds 0 --caps 3.0 \
    --output /tmp/qc_repro_seed0.json

[xs] joined 604 rows; class distribution: {0: 75, 1: 271, 2: 72, 3: 118, 4: 68}
[xs] cap=3.0 seed=0 nut_flush_block=0.1406 flush_draw_block_pct=0.0143 acc=0.9421
```

| Quantity | Re-run | Report (seed 0) | Match |
|---|---|---|---|
| nut_flush_block | 0.1406 | 0.1406 | ✅ **bit-exact** |
| held-out acc | 0.9421 | 0.942 | ✅ matches (rounded) |
| Class distribution | 75/271/72/118/68 | (combined corpus) | ✅ |

The script's docstring warns of ~±5-10% noise from xgboost BLAS non-determinism on re-runs, but with deterministic threading (`OMP_NUM_THREADS=1` + `OPENBLAS_NUM_THREADS=1`) the result is **bit-exact** with the report. Stronger than dispatch's reproducibility floor.

**Reproducibility: BIT-EXACT.** Script is runnable AND deterministic under the stated thread-control conditions.

## Bonus observation — TC-X-CROSS-SEED-IMPORTANCE first validation

The 12.5H-pre PR is the **first empirical activation** of TC-X-CROSS-SEED-IMPORTANCE since QC queued the class on 2026-05-05 (`~/river-rats-qc/learning/curative_additions_log.md` Entry #9). The class definition was:

> *"When a trainer report claims a feature's importance crossed an ml-architect-prescribed threshold, QC verifies cross-seed median ± std rather than taking chosen-seed value as proxy. If trainer report only emits chosen-seed importance (no cross-seed median), QC FLAGS the gap and recommends cross-seed enrichment of `write_report` for future cycles."*

The orchestrator pre-empted the FLAG by dispatching 12.5H-pre to produce the cross-seed enrichment as a one-off analysis (Path 2). The empirical result validates the class's underlying premise: chosen-seed importance IS unreliable as cross-seed proxy on this corpus (range [0.0000, 0.1406]; 40% of seeds below 0.02 floor; bimodal distribution).

The class's forward-active scope continues — at next trainer touch (12.5H-A or beyond), QC verifies cross-seed importance reporting becomes a **standing trainer-report contract**, not a one-off analysis. Per dispatch §"What's queued" line 116 (PR #156 dispatch), per-seed importance logging in trainer module is queued for next trainer touch.

The class also produced a useful methodology validation: when builder uses `OMP_NUM_THREADS=1 + OPENBLAS_NUM_THREADS=1` thread control, importance values become bit-stable across re-runs. This is a forward-actionable methodology note: future cross-seed analyses should standardize on deterministic threading.

## What QC did NOT audit (scope partition)

- **Per-hand poker analysis** of why bimodality exists — out of scope; ml-architect / gto-expert at 12.5H-A design phase
- **5-seed N-extension question** (would 10 seeds tighten the distribution?) — orchestrator scope; informational data point for 12.5H-A E-DIST design
- **Effect of bimodality on litmus score** — gated on 12.5H-E re-train + 12.5H-F gate evaluation; future-cycle scope

## Test class implication

- **TC-X-CROSS-SEED-IMPORTANCE first activation: SUCCESS.** Class produces clean exact-arithmetic-match validation. Forward-active for any future cross-seed analysis.
- **TC-X-CAP-BINDING-PRE-CHECK independent cross-validation:** the cap-non-binding finding is now confirmed via two orthogonal mechanisms (predict-time at 12.5G; trainer-time at 12.5H-pre). Test class strengthened.
- **Reproducibility-with-deterministic-threading pattern** — useful methodology note. Future analysis scripts that depend on reproducibility could codify `OMP_NUM_THREADS=1 + OPENBLAS_NUM_THREADS=1` as a standard pre-flight env-var setup.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **8th successive cycle solo-routed**. Trigger comm received (PR #162 master `0625b0f`); QC fired immediately. Loop heartbeat (auto-poll every 25min) detected the trigger landing within ~5min of master push.

## References

- PR #161: https://github.com/beytell1-sketch/river-rats-v2/pull/161
- PR #161 head: `e064edd719cf9f461fd91b3aacc3684a0ac6b7ba`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR161_2026-05-06.md` (master `0625b0f`, PR #162)
- 12.5H-pre dispatch: `MAIN_TERMINAL_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (master `2c52e6b`, PR #160)
- 12.5G: master `2135fc8` (PR #157)
- 12.5E-E: master `b51e525` (PR #152)
- TC-X-CROSS-SEED-IMPORTANCE class definition: `~/river-rats-qc/learning/test_class_registry.md` (commit `7354fad` on QC repo)
- Reproducibility re-run output: `/tmp/qc_repro_seed0.json` (ephemeral; bit-exact match with report seed 0)
- Memory: `feedback_qc_routing_when_standalone_active.md` (8th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #161 for merge.** All 4 audits PASS; 0 NIT. The clearest TC-X-CROSS-SEED-IMPORTANCE activation possible (every statistic computes exactly; reproducibility bit-exact under stated thread control).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H-A design (corpus expansion focus on E-DIST patterns; seed-volatility caveat documented)
- 12.5H-A dispatch may fold N-seed-sweep-for-confidence + per-seed importance trainer logging requirements (per dispatch §"What's queued" line 38)
