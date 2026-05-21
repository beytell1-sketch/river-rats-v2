# Corpus Audit — Top Findings Summary

Generated 2026-05-13. Source: 337 consensus rows across batches 001-007.
Ordered by impact on Phase 2-F (final retrain / A1 quotas / v3.5 amendment).

## Finding 1: Action class imbalance — RAISE and FOLD are sparse

- **Evidence:** BET 34%, CHECK 20%, CALL 20%, RAISE 17%, FOLD 9%.
- Actions <10%: FOLD.
- **Implication:** Training classifier on raw distribution will under-learn RAISE/FOLD. v3.5 amendment should (a) apply class weights inversely proportional to frequency, or (b) raise A1 quota minimums for RAISE/FOLD-heavy spot-buckets. Failure-direction reports per feedback_failure_direction_classification will likely surface under-aggress (missed RAISE) and over-call (missed FOLD) skews.

## Finding 2: Hero position over-represents BTN

- **Evidence:** BTN = 90/337 (27%); next: CO=74 (22%), SB=43 (13%), MP=39 (12%), BB=32 (9%).
- **Implication:** Position-conditional generalization will be weak for under-represented seats. v3.5 amendment for A1 quotas should require minimum n per position (e.g. ≥40 per position over 700-corpus target).

## Finding 3: Board-texture skew

- **Evidence:** rainbow_dry = 104/337 (31%); paired/monotone undersampled.
- Textures <10%: rainbow, paired, monotone.
- **Implication:** Paired/monotone boards are texturally distinct (different draw structure, different value class shapes). Under-sampling means weak generalization to these textures. A1 should target ≥10% per texture.

## Finding 4: `predicted_sizing_pct` has dual semantics — RAISE labels mix pct-of-pot and raise-to-bb

- **Evidence:** 18.4% of BET/RAISE sizing labels fall outside the canonical pct-of-pot grid (25/33/66/75/150).
- Top 6 buckets: ~66%-pot=446, raise-to-9bb? (semantic mismatch)=119, ~25%-pot=114, ~33%-pot=67, ~75%-pot=62, oversized-300% (likely bb-not-pct)=21.
- The RAISE-only cluster at value=9 (n=119, 44% of RAISE labels) maps coherently to raise-to-9bb on spots like 4WF-MULTIWAY-147 (`to_call_bb=2.5, pot_bb=13.5`) where 9% pct-of-pot would be an impossible (sub-min) raise.
- Additional outliers at 300/360/720 likely encode raise-to-bb when stacks are deep, or raise-as-pct-of-original-bet.
- BET sizings are clean: 77% at ~66%-pot, 13% at ~25%-pot, 10% at ~33%-pot — no semantic mixing.
- **Implication (HIGH for Phase 2-F):** Training-data export currently treats `predicted_sizing_pct` as a single numeric field. If passed to the trainer as-is, RAISE-sizing targets are corrupted (mixing dimensionless ratios with absolute bb amounts). v3.5 amendment MUST:
  - (a) split into two fields (`sizing_pct_of_pot`, `raise_to_bb`) at the labelling-prompt level, OR
  - (b) add a deterministic normalizer at the training-export boundary (convert raise-to-bb → pct-of-pot using `pot_bb`+`to_call_bb` from 50hand context).
- This is upstream of A1 quota questions and should be resolved before retraining.

## Finding 5: Per-batch action-mix is severely heterogeneous — all 7 batches exceed 10pp drift from corpus mean

- **Evidence:** Batches 1-3 are BET-heavy (+15 to +26pp ΔBET), batches 5-6 are CALL/RAISE-heavy (ΔBET = -19/-27pp; ΔCALL = +18 to +23pp). Max |Δ| ranges 12-27pp across batches. Agreement rates also stratify: B1=0.99 / B6=0.98 (highest) vs B7=0.95 (lowest).
- The pattern strongly implies the seed-spot generator changed primary-axis distribution between batches (B1-3 = opener/cbet spots; B4-7 = closing/multiway/turn-decision spots) rather than randomly sampling from a unified spec.
- **Implication (HIGH for Phase 2-F):** A model trained on all 7 batches sees non-stationary action distributions. If the eval split is sampled differently from train, calibration metrics will be unreliable. v3.5 must (a) stratify train/eval splits on (batch × action), or (b) verify seed-spot generator emits a stable mix per batch, or (c) treat the 7 batches as 2-3 mini-corpora and report metrics per-stratum. Without this, the standard random-split eval will hide direction-specific failures.

## Finding 6 (informational): Agreement asymmetry — RAISE is the disagreement sink

- **Evidence:** agreement-rate by action: RAISE=0.91 (only 57% unanimous, n=58) vs BET=0.98 (91% unanimous, n=113). FOLD=0.97/90% unanimous despite n=31.
- BB position has lowest agreement (0.93 / 69% unanimous, n=32) — likely OOP multiway defending decisions.
- Overall non-unanimous: 17.8% (below 40% threshold).
- **Implication:** RAISE labels are the noisiest reference target. Combined with Finding 4 (sizing semantics) and Finding 1 (RAISE under-represented at 17%), RAISE prediction is triple-jeopardized. Solver-verify queue should prioritize the 4-1 / 3-2 RAISE spots in §11 of the audit (4WF-CLOSING-214, -216, -240; 4WF-MULTIWAY-162).

## Additional flags (informational)

- **Empty strata confirmed:** facing-raise = 0/337, river = 0/337 (per pilot-agent note).
- **Street distribution:** flop=238 (71%), preflop=72 (21%), turn=27 (8%). Turn is materially under-sampled.
- **Postflop board-texture (excluding 74 preflop):** rainbow_dry 40%, two_tone 39%, rainbow 11%, paired 8%, monotone 2%.
- **Confidence:** 90% HIGH, 10% MEDIUM across all 1750 raw labels — labellers are not flagging uncertainty heavily even where consensus disagrees.
