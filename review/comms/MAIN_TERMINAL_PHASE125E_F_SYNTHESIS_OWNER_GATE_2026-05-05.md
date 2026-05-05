---
date: 2026-05-05
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-F gate evaluation — Opus second-tier evaluation; owner WHAT decision (A / B / C / D / B-then-C)
status: SYNTHESIS — owner gate
---

# Phase 12.5E-F — gate evaluation synthesis

12.5E-E merged at master `b51e525`. Median solver-corrected 32/40, +1 vs 12.5D' baseline of 31. Primary gate threshold (≥33) NOT cleared. Migration's H-FEAT premise validated at feature layer (`nut_flush_block` importance 0.0000 → 0.0268, above ml-architect Q4's ≥0.02 prediction).

Orchestrator ran Opus second-tier gate evaluation per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule (training-data outputs / model artifacts require higher-rigor-tier verification before promotion). Full analysis: `ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (in this PR).

## Headline empirical reconciliation

| Quantity | 12.5D' | 12.5E | Δ | Predicted (ml-architect Q4) |
|---|---|---|---|---|
| Median solver-corrected | 31 | 32 | +1 | 35-37 |
| Mean solver-corrected | 30.6 | 32.2 | +1.6 | — |
| Std solver-corrected | 0.49 | 0.40 | -0.09 | — |
| `nut_flush_block` importance | 0.0000 | **0.0268** | +0.0268 | ≥0.02 ✓ |
| 7 shared-cause hands flipped | 1/7 | 1/7 (MW-42 new; MW-24 unchanged from 12.5D') | net 0 | 7/7 |
| Newly broken | — | MW-20 (RAISE over-aggression) | — | — |

H-FEAT premise: **validated at feature layer; partial at gate-score layer.** The 35-37 median prediction over-estimated transfer because 5 of 7 shared-cause hands are dominantly E-DIST (corpus-distribution issue), not H-FEAT-primary. ml-architect's structural error: treated all 7 shared-cause hands as approximately equally H-FEAT-responsive; gto-expert's twice-confirmed per-hand classification shows realistic flip-yield from H-FEAT alone was always 1-2 hands.

## Per-hand diagnosis on 5 stay-wrong (Opus second-tier read)

- **3 pure E-DIST** (MW-25, MW-40, MW-45) — corpus didn't target these patterns; H-FEAT activation provides ZERO leverage. Only further corpus expansion targeting these specific templates can move them.
- **1 E-FEATURE primary** (MW-17) — discriminating signal is implied-odds + nut-blocker reasoning outside 59-feature surface; H-FEAT activation provides marginal leverage only.
- **1 compound** (MW-47) — feature now active, closer corpus exemplars exist, **may flip under cap=4.0** retuning.
- **MW-20 newly-broken** is over-aggression downstream of corpus RAISE-class shift; held-out CHECK recall dropped 0.939 → 0.815 confirms slight over-rotation.

## Owner WHAT decision space (A / B / C / D / B-then-C)

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator presents; owner picks.

### A — PROMOTE at 32/40
- Probability of "right call": **10-15%**
- FOR: H-FEAT platform validation; mean improved (30.6→32.2); std tightened (0.49→0.40); RAISE class doubled (5.9%→11.26%)
- AGAINST: −1 vs baseline 33/40; MW-20 newly-broken; held-out CHECK regression
- HOW (if picked): ship with documented regression in model card; v9-3way-v2.2 stays as 45-feat fallback; ~1 builder day

### B — 12.5G cap retuning sweep
- Probability of clearing ≥33: **10-15%** (revised UP from ml-architect Q5's 5% prior; H-FEAT now active gives cap a new lever specifically on MW-47)
- HOW (if picked): cap=4.0 sweep on combined corpus (cap=2.0/2.5 likely regress; only cap=4.0 is informative). 1 builder day, ~$5-10. Targets MW-47 specifically.

### C — Corpus expansion 110 → 160-200
- Probability of clearing ≥33: **50-60%** (revised down from gto-expert's 50-70% prior due to empirical lower-than-predicted marginal yield)
- HOW (if picked): 50-90 new hands targeting E-DIST stay-wrong patterns:
  - T8' (monotone-multiway-checked-through, MW-25 family expansion)
  - T9' (PFR-checks-back-Ax-multiway, MW-40 family)
  - T10' (slowplay-set-turn-lead, MW-45 family expansion)
  - T7-extension (NFD-CALL implied-odds, MW-17 family)
- 2-3 weeks corpus + retrain. ~$80-150 labelling spend.

### D — Abandon migration; v9-3way-v2.2 stays canonical
- Probability of "right call given evidence": **20-30%** (revised DOWN from prior because H-FEAT just validated — abandoning would discard a validated platform)
- HOW (if picked): ml-architect Variant 3a — keep trainer + tests + corpus on master as research artefact with abandoned-banner; ~10-line PR; v9-3way-v2.2 stays canonical

### B-then-C — compound (Opus highest-EV recommendation)
- 1-day cap=4.0 sweep first (~30% chance MW-47 flips for median 33)
- If clear: PROMOTE at median 33+
- If not clear: fold cap=4.0 evidence into C corpus design (informs which templates to expand)
- Extracts maximum signal from H-FEAT validation moment without committing 3 weeks upfront

## Orchestrator structural read (per slow-quality default; owner picks WHAT)

Honest reads given empirical evidence + Opus second-tier evaluation:

- **A** is structurally weak (regression; MW-20 newly broken; held-out regress)
- **B alone** has limited expected value (~10-15% gap close; cap orthogonal to E-DIST root cause for 3 of 5 stay-wrong)
- **C** is highest individual EV (~50-60%); only direction acting on E-DIST root cause; targets the empirical residual
- **D** is structurally weakened post-H-FEAT validation (we just proved the platform; abandoning discards it)
- **B-then-C** is the slow-quality compound: 1-day cheap empirical bet on cap=4.0; falls into C if no clear; extracts maximum information

**Owner standing instruction is "slow quality, no asking, recommend the quality path."** The slow-quality path here is **B-then-C**: run cap=4.0 sweep first (1 day, $5-10), use the result to inform C design (whether to also adjust cap in retrain or just expand corpus). Worst case: cap=4.0 doesn't help, we've spent 1 day + $10 and informed the C corpus design. Best case: cap=4.0 closes MW-47, median 33, PROMOTE.

If owner disagrees with B-then-C and prefers C alone, that's also defensible (~50-60% gap close, slightly slower path to ship). If owner prefers A or D, that's a legitimately different read on the trade-offs.

## What does NOT happen at this gate

- No 12.5+1 / 12.5G / 12.5H dispatch until owner picks
- No model promotion at median 32 without owner explicit APPROVE
- No source-surface edits beyond what each path implicitly requires
- v9-3way-v2.2 stays canonical until promotion happens

## On owner decision

| Owner picks | Next orchestrator action |
|---|---|
| A | Author "12.5E-ship at 32/40" directive; v9-3way-v2.2 stays as 45-feat fallback; QC + ml-architect re-review the ship-a-regression decision |
| B | Author "12.5G cap=4.0 retune" directive (1 builder day, ~$10); fire trainer with cap=4.0 only on combined corpus; gate at median 33 |
| C | Author "12.5H corpus expansion 110→160-200" directive; ml-architect-hat designs new templates; multi-week scope |
| D | Author "12.5 abandon close-out" directive; Variant 3a annotation; v9-3way-v2.2 stays canonical |
| B-then-C | Author "12.5G cap=4.0 retune" directive with explicit "if median <33 → 12.5H corpus expansion" follow-on; orchestrator gates between |

## What's blocked / what's queued

**Blocked:**
- All forward dispatch options on owner WHAT decision

**Queued (independent of WHAT pick):**
- T1 outcome assessment (per PR #144 deferral): MW-25 still wrong → T1 expansion likely needed if owner picks C
- T8 schema gap (PR #150 NEW NIT): encode `design_action` per T8 hand in future situation factory runs
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations) → builder formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5E-E merged: master `b51e525` (PR #152)
- 12.5E-E QC APPROVE: master `00fe4ab` (PR #154)
- 12.5E-D APPROVE: master `4070a11` (PR #150)
- Opus second-tier evaluation: `ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (in this PR)
- ml-architect 12.5D' findings (Q4 H-FEAT prediction): `/tmp/ml_architect_125d_prime_findings.md`
- gto-expert 12.5D' findings (per-hand classification): `/tmp/gto_expert_125d_prime_findings.md`
- 12.5C blueprint: master `1e4e47e` (PR #122)
- Memory: `feedback_quality_default_no_ask.md` (slow-quality), `feedback_pilot_first_for_long_jobs.md` (tier-up verification on training-data outputs), `feedback_orchestrator_decides_not_recommends.md`, `feedback_failure_direction_classification.md`, `feedback_river_rats_team_structure.md`

**Status: 12.5E-F SYNTHESIS COMPLETE. Owner gate ready: A / B / C / D / B-then-C. Orchestrator structural read = B-then-C as slow-quality compound. Awaiting owner WHAT decision.**
