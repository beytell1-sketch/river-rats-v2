---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 self-play diagnostic — STOP CONDITION triggered (3 anomalies)
status: BLOCKED — v2.3.1 does NOT ship as-is; reporting per discipline
---

# v2.3.1 Self-Play Diagnostic — STOP

The reviewer-directed pre-ship validation caught a real regression.
Applying stop-and-report discipline — no workaround, no ship.

## Config

- Model: `river-rats-core/models/v2_3_1_model.json`
- Deals: 2000 (× 6 positions × 1 variant = 12,000 games)
- Seed: 42
- Runtime: ~34 min wall / ~97 min CPU (vs v2.3's ~5 min — see "why slow" below)
- Raw: `review/v231_selfplay_raw.json`
- Script: `review/run_v231_selfplay_diagnostic.py` (committed separately at `e5d85bf`)

## Headline comparison table

| Metric | v2.2 | v2.3 | **v2.3.1** | Watch status |
|---|---|---|---|---|
| Facing-bet 3-way+ count | ~0 | 1,269 | **145** | **COLLAPSE** (-88.6%) |
| Check-to-hero BET prob < 0.05 | 63.0% | 0.0% | **48.8%** | **RESURGENT** (+48.8pp) |
| 3-way+ postflop yield | 3.7% | 5.7% | **4.1%** | regression |
| Total postflop decisions | — | 2,772 | **17,478** | 6.3× inflation (more CHECKs → longer hands) |
| BET prob median (check-to-hero) | — | 0.729 | **0.063** | collapsed |
| BET prob mean (check-to-hero) | — | 0.697 | **0.319** | halved |
| Postflop CHECK share | — | ~10% | **36.2%** | **SPIKE** (> 25% threshold) |
| Postflop BET share | — | ~44% | **30.9%** | reduced |

## The three anomalies (triggered by the watch script)

```
**ANOMALIES DETECTED** — stop-and-report discipline:
  - Facing-bet count collapsed: 145 < 0.7×1269 = 888
  - CHECK share spike at postflop: 36.2% > 25% threshold
  - Check-to-hero low-BET spots resurgent: 48.8% > 5%
```

## What happened

**v2.3.1 has over-corrected.** The Layer 2 air-CHECK counter-
examples pushed the model from v2.3's BET-heavy stance past the
target point and into CHECK-heavy territory. Half of 3-way
checked-to spots (48.8%) now produce near-zero BET probability —
the original passive-loop signature we fought to eliminate in v2.3.

Mechanically:
- Model bets less in checked-to spots → fewer bets happen → hands
  continue with more checks → 6.3× more postflop decisions per
  deal (17,478 vs 2,772)
- Fewer bets means fewer facing-bet situations → 145 vs 1,269
  (89% collapse toward v2.2's ~0)
- Postflop CHECK share jumped from ~10% to 36% — the over-
  correction signal the reviewer flagged as a watch condition

## Targeted litmus results were clean — why did self-play fail?

This is important context. The earlier gates all passed:
- FB-40 77.5%, MW-50 84.0% (standard holdouts)
- 2/2 flop litmus (A4d/Qs5s7s CHECK 93.5%; T5h/JJ2 CHECK 98.3%)
- Broader sweep 18/19 = 94.7% CHECK on curated air-on-hostile
  flop cases

Those gates measure: **given an air-in-hostile-flop spot, does
the model say CHECK?** Answer: yes. The fix works for the target
class.

Self-play measures a different thing: **across dynamic play, does
the model bet at a reasonable overall frequency?** Answer: no.
The model has learned "CHECK" more generally than just the air
class — over-applying the pattern to spots where a BET would be
GTO-correct (value bets, semi-bluffs with legitimate equity,
protection bets).

Two gates passed; one gate failed. The earlier gates validated
the symptom fix; self-play validates the systemic balance. Both
matter.

## Diagnostic detail

### Per-position action breakdown (signal of over-correction)

```
pos    FOLD     CHECK    CALL     BET      RAISE
BB    11.7%    40.4%    13.4%    33.9%     0.6%    ← BB checking too much
SB     8.2%    36.9%    11.0%    43.5%     0.3%
BTN   14.6%    27.2%    36.3%    18.8%     3.0%    ← BTN IP betting too little
CO     8.7%    35.2%    24.5%    28.8%     2.8%
HJ     9.3%    33.3%    26.4%    29.6%     1.4%
UTG    6.5%    37.5%    22.3%    30.6%     3.2%
```

BTN c-bet frequency at 18.8% is well below the KB-cited 30-45%
target for 3-way IP c-bets. SB/BB CHECK share near 37-40% reflects
positional appropriateness but the totals still skew CHECK.

### `board_adjusted_hrp` distribution (hero postflop)

```
n=2902  mean=0.248  p25=0.053  p50=0.162  p75=0.373  p90=0.635  max=0.999
non-zero: 2819/2902 (97.1%)
```

Distribution looks reasonable (mean 0.25, p50 0.16, no degeneracy,
97% non-zero coverage). The feature is doing what it's designed
to do — suppressing HRP when equity is low. The problem isn't
this feature; it's the Layer 2 training signal weight.

### Why the run took ~34 min

v2.3's 5-minute baseline assumed short hands (many preflop folds,
quick flop resolutions via bets). v2.3.1's CHECK-heavy output
makes hands PLAY OUT — 6.3× more postflop decisions per deal.
Runtime scales with decision count, not deal count. Same reason
facing-bet collapsed: fewer bets initiated means fewer turns
where the facing-bet branch fires.

## What this means for Layer 2

The 40 air-CHECK counter-examples (26% of post-assembly CHECK
rows, 5.9% of all training rows) appear to have carried more
decision-boundary weight than expected. The model generalized the
air-CHECK signal across a broader class than intended.

Contributing factors to explore:
1. **Class distribution shift.** Assembled CSV CHECK share went
   from 23.7% (v2.3-clean) to 26.1% (v2.3.1 with +40 air-CHECK).
   Small shift but on small dataset (637 → 677 rows) it's
   structurally amplified.
2. **No class weighting.** v2.3-clean used no weights and was
   fine. But adding 40 similar-shape CHECKs in a small training
   set concentrates the signal.
3. **Layer 2 hands are tightly clustered** on 7 unique 3-way
   boards (earlier flagged in yield stats). High within-class
   redundancy may have over-emphasized the specific air-feature
   pattern.
4. **Potential interaction with Layer 1.** `board_adjusted_hrp`
   + air-CHECK pattern may stack — the feature and the training
   examples both point "CHECK" in overlapping spots.

## Paths forward (reviewer to scope)

### Path A — Rebalance Layer 2 weighting

Retrain with `sample_weight` reducing air-CHECK rows to ~0.5
effective weight. Keeps data, tones down signal. 15-min retrain.

Risk: may break the target fix (flop litmuses). Gates must re-run.

### Path B — Prune Layer 2 rows to a smaller set

Take top-15 most-representative air-CHECK rows (one per unique
board × position archetype) instead of all 40. 15-min
re-assemble + retrain.

Risk: weaker target fix; litmus margin reduces but should still pass.

### Path C — Add balancing BET/RAISE counter-examples

Generate ~40 hands where hero has VALUE in checked-through-looking
spots (sets, two-pair, TPTK on dry boards) and label BET. Rebalances
the signal. 1-2 hour generation + relabel.

Risk: slower path; broader scope creep.

### Path D — Targeted self-play data source for v2.4

Use v2.3 self-play output (the 1,269 facing-bet spots) as a
diagnostic / training source. Relabel via v3.1, add to training.
Larger refactor; v2.4 scope.

**Builder recommendation:** **Path A first** — fastest, minimal
risk, evidence-based. If Path A's post-retrain self-play still
shows collapse, escalate to B/C.

## Ship-block status

**v2.3.1 DOES NOT SHIP** until:
- Self-play diagnostic's anomalies resolve (facing-bet count ≥
  ~900, CHECK share < 25%, check-to-hero low-BET ≤ 5%)
- Previous gates (FB-40/MW-50/flop litmus/sweep) re-run and
  confirm no regression from the rebalance

Game stays on v2.2. Teaching terminal's Path B and Layer 3 work
remain independent; no coupling to the logic regression.

## Artifacts this commit

- `review/v231_selfplay_raw.json` — full diagnostic output
- `review/comms/BUILDER_V231_SELFPLAY_STOP_2026-04-18.md` — this
  doc

No model / training-data changes. v2.3.1 model artifact stays in
place as-is pending reviewer decision on Path A/B/C/D.

## Builder self-assessment

The earlier gates were sound for the target class but incomplete
for systemic balance. Self-play diagnostic was the right gate to
catch this — the reviewer's insistence on "not optional" prevented
a bad ship. Discipline over speed.

The architectural finding is real and worth capturing: a 40-hand
targeted counter-example injection into a 637-row dataset CAN
shift the decision boundary more than intended. Future Layer-2-
style counter-example work should:
- Pre-check self-play impact at smaller sample sizes (e.g.,
  include a 500-deal sanity check between labelling and ship
  gates)
- Consider sample-weight discipline upfront rather than relying
  on raw row count
- Monitor broader action distributions, not just target-class
  accuracy

Standing by for scope direction.
