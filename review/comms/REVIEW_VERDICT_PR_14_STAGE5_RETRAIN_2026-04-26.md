---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ML-architect reviewer (dedicated subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT the v1.0 author and NOT the Protocol B/C reviewers)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #14 — Stage 5 retrain protocol v1.0 (`a7a62fa`)
status: REQUEST-CHANGES — 2 MEDIUM-severity issues found (Prereq #2 column-count self-contradiction; Mode D anchor inventory mismatch with calibration_anchors.json) — recommend Task 3.1 fix-forward before merge per Task 1/2 fix-forward pattern. Protocol's ML core (hyperparameters defence, seed scheme, gate thresholds, rollback enumeration) is production-quality.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/14
branch: stage4-prep/stage5-retrain-fill
artifact: review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md (767 lines)
predecessor: review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md (225 lines)
---

# Review Verdict — PR #14 (Stage 5 retrain protocol v1.0)

## Provenance note

Independent reviewer dispatch under read-only constraint (general-purpose acting as ml-architect; dedicated subagent unavailable). Did NOT author v1.0; did NOT review v0.1 DRAFT; NOT the Protocol B/C reviewer. Worked from PR #14 head commit `a7a62fa`. Cross-referenced against `train_v2_3_2.py`, `models/v2_3_2_training_report.json`, `gto_model.py:33-62`, `anchors/calibration_anchors.json`, `feedback_solver_findings.md`, `reference_corrections.md`.

## Builder verification spot-checks

- Hyperparameter values verified byte-for-byte against `train_v2_3_2.py:106-111` ✓
- v2.3.2 cv_std=0.0232 verified in `models/v2_3_2_training_report.json` ✓
- best_iteration=138 verified ✓
- v2.2→v2.3.2 holdout 88.3%→90.3% verified (`v2_3_2_training_report.json:holdout_test_accuracy=0.9028`) ✓
- SHA256-derived seed scheme re-derived independently: `[306404237, 1073902872, 1566216024]` ✓
- `reference_corrections.md` cross-check: MW-30 CALL ✓ MW-46 CALL ✓ MW-47 RAISE ✓ (v0.1 DRAFT had wrong "MW-30, MW-33, MW-50"; v1.0 corrects this)

---

## Item A — Hyperparameters defence

**OK / HIGH confidence.** Values match `train_v2_3_2.py` byte-for-byte. 5-point defence is ML-rigorous: XGBoost gain-based split insensitivity (with `colsample_bytree=1.0`), early-stopping dimensionality-agnostic, L1/L2 regularisation handling correlated features (`flush_block_pct` vs `nut_flush_block`), v2.2→v2.3.2 verbatim-port empirical precedent, `feedback_compute_assumptions.md` "change one variable at a time" attribution discipline. Trigger table covers 4 realistic re-tune scenarios (class drift, corpus shrink, all-seeds early-stop at cap, holdout < baseline-3pp).

## Item B — Seed selection rationale

**OK-WITH-NIT / HIGH confidence.** Citations real (Reimers & Gurevych 2017 EMNLP; Bouthillier et al. 2021 MLSys). SHA256-derived scheme reproducible AND bias-free (independently re-derived). Per-library propagation covers all 4 RNG sources (random/numpy/sklearn/xgboost).

**NIT (LOW):** Bouthillier 2021 actually recommends ≥10 seeds for proper variance estimation; v1.0's framing slightly oversells "3 is enough for variance estimation." It's enough for ship/no-ship gate, not variance estimation per se. Acknowledged in v1.0 (line 232 + 5-seed expansion path on MARGINAL spread); acceptable.

## Item C — Train/CV split decision

**OK / HIGH confidence.** Reasoning sound (isolates model-init variance from data-split variance via 5-fold CV inside each seed = 3×5=15 fold estimates). v2.3.2 same-split pattern verified (`train_v2_3_2.py:101-103`). UNCERTAIN tag re corpus < 400 hands appropriately scoped.

## Item D — Threshold values

**OK-WITH-NITS / MEDIUM confidence.** ±2pp = v2.3.2 cv_std=0.0232 (one-σ) verified. Top-10 Spearman ≥ 0.8 lift from Nogueira & Brown 2016 baseline 0.7 justified by Exp 3 0.912 precedent.

**Statistical nuance:** ±2pp anchors a between-seed spread to a within-fold standard deviation. These are not the same quantity statistically — between-seed variance with same data is typically smaller than between-fold variance with different data partitions. So ±2pp may actually be too LOOSE in practice. UNCERTAIN tag at line 381-385 acknowledges this.

**NITs author should have added:**
1. **Per-class precision floor for RAISE.** RAISE is rarest class (high cv_std on minority classes is where models break first). A per-class precision floor of e.g. ≥ 0.65 on RAISE across all 3 seeds would catch a regression that aggregate-accuracy misses (the v8-era 88.1%/52.5% lesson).
2. **Per-multiway-bucket accuracy floor** — partially in Mode E but should be Gate 1.5, not just rollback diagnosis.

NITs not BLOCKERs because Mode E + per-shape-category breakdown in §Reporting cover diagnostic path.

## Item E — Ensemble vs median decision

**OK-WITH-MEDIUM-NIT / HIGH confidence.** 8-row trade-off table mostly complete. Compatibility claims verified (`gto_model.py` single XGBoost predictor; `oracle_router.py` single `model_path` per opponent count; median single-seed drop-in vs ensemble requiring wrapper class).

**Variance-reduction wording is muddled (MEDIUM-NIT):** Line 472 claims "~30% lower predictive variance (1/√3)". Mathematically:
- 1/√3 ≈ 0.577 is the SD ratio for averaging N=3 independent models
- That's ~42% reduction in SD, or ~67% reduction in variance (variance reduces by 1/N)
- "30% lower predictive variance" is neither 1/√3 nor 1/3

Directional argument correct; specific number wrong. ML rigour requires the math to be right since this protocol cites specific numbers. **Should be tightened in v1.0.1.**

**Missing trade-off row:** "disagreement-as-uncertainty signal" — ensemble naturally produces soft uncertainty estimate via inter-model disagreement; median single-seed loses this. NIT-level addition.

Tie-break rule (lowest cv_std, then seed-A) unbiased. UNCERTAIN tag asking whether it should live in trainer script as deterministic fallback is appropriate — yes, it should.

## Item F — Rollback procedures completeness

**OK-WITH-MEDIUM-PROBLEM / HIGH confidence.** 5 enumerated modes (A: Gate 1 spread; B: Gate 2 Spearman; C: Gate 3 calibration; D: anchor regression; E: MW decline) cover realistic Stage 5 failure surface. Diagnosis steps actionable. Decision criteria crisp (not "depends on judgment").

**MEDIUM PROBLEM #2 — Mode D anchor inventory mismatch:** Mode D references "the 3 d-series anchors (d2410, d0182, d8411)" (line 638-639, 643-644). I checked `river-rats-core/anchors/calibration_anchors.json` — it contains exactly 5 anchors: `d2410_CO_turn`, `LITMUS_A4d_Qs5s7s_flop`, `LITMUS_T5h_JJ2_flop`, `LITMUS_AA_7h5d2c_flop`, `LITMUS_KQ_KsTs3h_flop`. **Anchors `d0182` and `d8411` are NOT in the active calibration set.**

The pre-Stage-3.5 closure doc treats them as live anchors, so either (a) they were renamed to LITMUS_* in Stage 3.5 and v1.0 hasn't updated the IDs, or (b) the protocol assumes they will be re-added before Stage 5. Either way, Mode D as written is not directly executable against current `evaluate_calibration_anchors.py` infrastructure.

**Recommendation:** v1.0.1 should resolve the anchor naming (update to LITMUS_* IDs OR add prereq #6 requiring d0182/d8411 to be re-instantiated).

**Mode E baseline number gap (NIT):** v2.3.2 MW reference-set baseline is unclear from the artifacts I checked. `v2_2_evaluation_report.json` reports `mw_reference_accuracy: 0.8` raw / `0.44` normalized (with caveat). No v2.3.2 reference-set evaluation report in `models/`. **Recommendation:** v1.0.1 should add prereq #6 (measure v2.3.2 MW reference-set baseline before Stage 5) OR cite the specific MW-accuracy number for the regression threshold.

## Item G — PRE-RETRAIN PREREQUISITES section

**OK-WITH-MEDIUM-BUG / HIGH confidence.** 5 prereqs cover necessary surface; each has explicit verify step.

**MEDIUM PROBLEM #1 — Prereq #2 self-contradictory column count:** Reads "110-column contract (54 raw + 4 v2.4 blocker = 58 raw + 58 attn_*)". Three problems:
1. v2.3.2 is 55 raw + 55 attn_* = 110 columns (verified against `gto_model.py:33-62` — 55 features ending at `board_adjusted_hrp`; v2.3.2 training report `n_features: 110`)
2. v2.4 is 55 raw + 4 blocker + 59 attn_* = 118 columns (consistent with §Hyperparameters line 155: "training-tensor goes 110 → 118 columns")
3. The string "54 raw + 4 v2.4 blocker = 58 raw + 58 attn_*" gives 116 columns (58+58), neither 110 nor 118. AND "54 raw" undercounts v2.3.2 by 1.

§Hyperparameters reasoning gets the count right (54+54=108 v2.2; 55+55=110 v2.3.2). **Prereq #2 should be rewritten to:** "118-column v2.4 contract (55 raw + 4 v2.4 blocker = 59 raw + 59 attn_*) validated, OR the contract is updated and the change is documented in the report."

Mechanically blocks the prereq from being executable as a check (verifier can't tell whether 110, 116, or 118 columns is the target).

**Prereq #3 mechanical question (NIT):** "Baseline model preserved as rollback" — does this happen automatically? Verified `models/v2_3_2_model.json` exists at HEAD. The "tagged on origin" requirement is a NEW step requiring orchestrator action; not automatic. v1.0.1 should explicitly assign this to orchestrator-pre-Stage-5.

## Item H — Memory alignment cross-checks

**OK / MEDIUM confidence.**
- `feedback_units_and_dedup.md` cross-check at Prereq #4 (40+24+50 disjoint from training corpus) — direct application of dedup discipline ✓
- `feedback_compute_assumptions.md` cross-check at §Hyperparameters point #5 ("change one variable at a time" rationale for NOT bundling hyperparameter sweep with retrain) — correct ✓
- `reference_corrections.md` cited at Gate 3 (MW-30 CALL, MW-46 CALL, MW-47 RAISE) — verified against memory ✓ (v0.1 DRAFT had wrong list; v1.0 corrects)

## Item I — UNCERTAIN tag rigor

**OK / HIGH confidence.** All 4 UNCERTAIN tags legitimate (corpus-size sensitivity; one-σ vs two-σ; top-10 vs top-20 Spearman empirical pilot gap; tie-break rule deterministic-fallback gap).

**Under-tagging:** v1.0 missing UNCERTAIN tags on (closer to BUGs than UNCERTAIN per Items E + F + G):
- Mode D anchor inventory mismatch (closer to BUG)
- Variance-reduction "1/√3 = ~30%" wording (closer to fix-needed)
- MW baseline number for Mode E

These are cases where v1.0 made claims it couldn't substantiate.

## Item J — No new MEDIUM-severity issues introduced

**Two new MEDIUMs identified** (not present in v0.1 — v0.1 was structural skeleton with placeholders):

1. **MEDIUM-1: Prereq #2 column-count self-contradicts itself and §Hyperparameters** — Item G
2. **MEDIUM-2: Mode D anchor inventory references anchors not in `calibration_anchors.json`** — Item F

Other observations (NOT new MEDIUMs):
- Variance-reduction wording in Ensemble table muddled (Item E) — closer to NIT
- Mode E MW baseline ambiguity (Item F) — could be fixed by Prereq #6
- 3-seed minimum slightly oversells what literature backs (Item B) — closer to LOW

No threshold contradicts v2.3.2 behaviour. All rollback procedures within compute budget. No prereq mechanically impossible.

## Item K — Ready for orchestrator merge?

**REQUEST-CHANGES.** Two MEDIUM-severity issues warrant Task 3.1 fix-forward before merge, on the same pattern as Tasks 1 and 2 fix-forward cycles. Both are ~30 min fixes with no design rework.

The protocol's ML core is otherwise production-quality: 5-point hyperparameter defence, SHA256 seed scheme with verified per-library propagation, ±2pp empirical anchor on v2.3.2 cv_std, top-10 Spearman literature anchor, 5-mode rollback enumeration.

---

## VERDICT

**REQUEST-CHANGES — overall confidence HIGH.**

**Required fixes for v1.0.1 (Task 3.1 fix-forward):**

1. **MEDIUM-1 — Prereq #2 column count.** Rewrite to consistent 118-column v2.4 schema (55 raw + 4 blocker = 59 raw, + 59 attn_* = 118 total). Currently self-contradictory (claims 110 columns but lists 116-arithmetic and undercounts v2.3.2 by 1).
2. **MEDIUM-2 — Mode D anchor inventory.** Resolve d0182/d8411 references — either (a) update Mode D to use actual `calibration_anchors.json` IDs (LITMUS_A4d / LITMUS_T5h / LITMUS_AA / LITMUS_KQ + d2410), OR (b) add Prereq #6 requiring d0182/d8411 to be re-instantiated before Stage 5.

**Recommended bundle in v1.0.1 (NIT-level fixes that fold trivially):**
3. Item E: variance-reduction wording — "1/√3 SD reduction (~42% lower SD; ~67% lower variance for averaging N=3 independent models)" replacing "30% lower predictive variance"
4. Item D NIT: add per-class precision floor for RAISE class (or UNCERTAIN-tag it)
5. Item F NIT: add Prereq #6 to record v2.3.2 MW reference-set baseline before Stage 5 begins
6. Item G NIT: explicitly assign Prereq #3 baseline-model tag to orchestrator-pre-Stage-5

**Carry-forward LOWs/NITs (defer to v1.1 or wrap-up):**
- Bouthillier 3-vs-10-seed framing nuance (Item B NIT)
- Add ensemble row "disagreement-as-uncertainty signal" (Item E)
- Promote MW-stratified accuracy from Mode-E-diagnosis to Gate-1.5 (Item D)

**Blockers for design-artifact ship:** None of the design intent is broken; all fixes are surgical.

## NIT-level observations (deferred or bundled)

(See action items above — most NITs bundled into recommended v1.0.1 fix-forward.)

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | MEDIUM | Prereq #2 column-count rewrite to 118-column v2.4 schema |
| 2 | MEDIUM | Mode D anchor inventory resolution (LITMUS_* IDs or Prereq #6 d0182/d8411 re-instantiation) |
| 3 | NIT (bundle) | Variance-reduction wording fix in Ensemble table |
| 4 | NIT (bundle) | Per-class precision floor for RAISE class |
| 5 | NIT (bundle) | Prereq #6 v2.3.2 MW baseline measurement |
| 6 | NIT (bundle) | Prereq #3 explicit orchestrator-action assignment |
| 7 | LOW (defer) | Bouthillier 3-vs-10-seed framing — v1.1 |
| 8 | NIT (defer) | Ensemble disagreement-as-uncertainty trade-off row — v1.1 |
| 9 | NIT (defer) | Promote MW-stratified accuracy to Gate-1.5 — v1.1 |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_14_STAGE5_RETRAIN_2026-04-26.md`.
2. Post comment on PR #14 referencing the verdict.
3. Stand by for orchestrator fix-forward direction (per established Task 1/2 pattern, fix-forward is highly likely given REQUEST-CHANGES verdict).
4. If fix-forward directive issued: execute Task 3.1 (mirror PR #11/#13 patterns).

**Orchestrator:**
1. Read this verdict.
2. Issue fix-forward directive for Task 3.1 (recommended); alternative: BLOCK PR #14 until v1.0.1 lands. PR #11 and PR #13 precedents both went fix-forward path.
3. Per quality default `feedback_quality_default_no_ask.md`: MEDIUM-severity findings should be addressed before merge, even when "non-blocking" in literal sense.

**Owner:** wake to find Stage 5 retrain protocol v1.0 needs surgical fix-forward (Task 3.1) before merge — design intent intact, two MEDIUM-severity inconsistencies (column-count math; anchor inventory mismatch) require resolution.

## Reference

- PR #14: https://github.com/beytell1-sketch/river-rats-v2/pull/14
- v1.0 commit: `a7a62fa`
- Source DRAFT: `review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md`
- Output: `review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md`
- Trainer: `river-rats-core/train_v2_3_2.py`
- v2.3.2 training report: `models/v2_3_2_training_report.json`
- v2.4 features: `river-rats-core/gto_model.py:33-62`
- Calibration anchors: `river-rats-core/anchors/calibration_anchors.json`
- Greenlight: `review/comms/MAIN_TERMINAL_PR_13_MERGED_TASK3_GREENLIGHT_2026-04-26.md`
- Solver-corrected reference: `feedback_solver_findings.md` + `reference_corrections.md`
- Task 1 + Task 2 fix-forward precedents: PR #11, PR #13 verdicts

**FINAL VERDICT: REQUEST-CHANGES — HIGH confidence overall. Task 3.1 fix-forward recommended (mirror PR #11/#13 pattern). Both MEDIUMs are ~30-min surgical fixes with no design rework.**
