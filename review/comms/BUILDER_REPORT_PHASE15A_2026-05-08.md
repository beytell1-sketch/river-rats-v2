---
date: 2026-05-08 (rev 1) · 2026-05-09 (rev 2 amendment per QC PR #311 SHOULD_FIX-1)
from: LEAD-PROGRAMMER (architect-hat; builder)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase 1.5-A — unified-59-surface design memo (single committed path; design only)
status: BUILDER REPORT — rev 2 amendment authored per owner direction Path A+; awaiting QC re-audit + owner-merge gate
---

# Phase 1.5-A — builder report

## Rev 2 amendment summary (2026-05-09 per QC PR #311 SHOULD_FIX-1 + NIT-1)

Owner directed Path A+ on 2026-05-09: fix in PR #307 (do not fix-forward in 1.5-B). Auto mode authorized; architect-hat executed methodology amendments while surfacing newly-discovered cost data (v8-HU-38 = 11.7 MB × 2 = 23 MB, ~38% growth on current 61 MB `.git`) for owner-scope decision before 1.5-D.1 fires.

Single commit on `programmer/phase15a-unified-surface-design-2026-05-08`:

- **§1.2 re-attestation (SHOULD_FIX-1 fix):** replaced `ls`/disk-existence prose with git-tracked verification (`git ls-files <path>`) for all 19 cited paths. Result: 17 GREEN / 2 RED. The 2 RED are `gto_model_v8_hu.json` + `gto_model_v8_38feat.json` — on disk (11.7 MB each) but never git-tracked due to `.gitignore` line 3 (`*.json`). New attestation explicitly labels each path GREEN/RED; exposes the root cause + production-runtime status.
- **§4.2 cascade fix:** added ⚠️ owner-scope decision for close-hand-anchor model (Path α commit-v8 ~23 MB vs Path β re-anchor on v9-3way-on-59). Architect-hat recommendation per `docs/PROCESS_GUIDE.md:59-77` HOW-not-WHETHER scope: Path β (no repo-size cost; v9-3way handles HU via `num_opponents=1` feature; structural). Owner directs.
- **§4.5 cascade fix:** reframed v8-HU-38 "lineage anchor" as "production-runtime-anchor without git provenance" — accurate to current state. From-scratch HU retrain commitment unaffected.
- **§4.6 cascade fix:** reframed "REPLACED in production" as "filename-pointer change at `oracle_router.py:34`" with explicit commitment that the new HU model file is force-added to git at 1.5-E (avoiding the same git-tracking gap recurring).
- **§7 owner-scope items:** added 4th item (close-hand-anchor model decision) — does NOT block Phase 1.5-A merge; fires in 1.5-D.1 dispatch sequencing.
- **NIT-1 fix:** §1.3.3 trainer-asserts prose corrected — pre-drop `_V24_P1_BLOCKERS` indices `-6:-2` of 61-list become indices `-4:` of post-drop 59-list (the J-B drop frees the tail; v2.4 P1 blockers occupy the final 4 positions).

Diff scope still 2 files. New owner-scope item is informational + decision-surfaced; does NOT change the substantive design path of the memo.

## Dispatch compliance

Authored per `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306). Architect-hat fire-now received via owner+orchestrator comm; explicit action trigger: "LEAD-PROGRAMMER architect-hat is authorized to fire on next tick" + acknowledgement that PR #306 dispatch is in master.

Pre-execution grounding (per `feedback_builder_grounds_before_executing.md` + `feedback_verify_source_not_plan.md`):

- Read `feature_extractor.py:FEATURE_COLUMNS` (1569-1620) — confirmed 61 features; both J-B drops at lines 1618-1619.
- Read `feature_keys.py` (full file, 117 lines) — confirmed `F.NUT_BLOCKER_OVERCARD_COUNT` and `F.BET_CALL_MULTIWAY_OOP_RAISE_PRESSURE_INDEX` at lines 100-101.
- Read `train_model_v9_student.py:1-220` — confirmed surface assertions, `_N_FEATURES_STUDENT = 61`, pre-pad mechanism.
- Read `gto_model.py` and `coaching/gto_model.py` — confirmed production routing FEATURE_COLUMNS at 55 (different surface from experimental student's 61); auto-detect 38/45 logic.
- Read `oracle_router.py` — confirmed HU slot at line 34, legacy fallback line 41.
- Verified all model artifacts (`v8_hu`, `v8_38feat`, `v9_3way_v2.2`, `125k_c_e/v9_3way_125k_c_e`).
- Verified 988-corpus structure (988 rows, `feat_dict` keys=61, both J-B features present).
- Verified `docs/PROCESS_GUIDE.md` sections cited by the dispatch (§1.1, §1.2, §1.4, §2.1).
- Verified the 40-hand multiway reference design pattern at `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`.
- `grep`-verified J-B feature touch-points across `training-data/`, `prompts/`, `river-rats-core/`, `scripts/` — confirmed 0 matches in attention vocab and labelling prompts (which is the §1.3.2 finding the memo flags).

## Path corrections logged

Per `feedback_verify_source_not_plan.md`, the dispatch's references to `assemble_v23.py`, `train_v2_3_clean.py`, `check_leakage.py` are legacy v2.3 paths at REPO ROOT (not `river-rats-core/`); the canonical 988-corpus assembly is `scripts/assemble_125k_c_e_988.py` (lineage `scripts/assemble_125i_d_788.py`). The memo cites the actual canonical paths and flags the discrepancy in §1.2 explicitly.

## Memo scope confirmation

5 design areas covered as committed paths (no menus):

1. **59-surface canonical** — full enumeration with line refs, axis-of-targeting, chosen-seed importance; TC-23 EXISTENCE attestation; lock-step touch-points inventory (incl. the 12.5J-B attention-layer gap finding).
2. **Drop-2-J-B-features migration** — re-extract from raw (committed; reasoning in §2.1); deterministic bit-equality verification command (§2.3); output artifact spec (§2.4); invariant-tests scope adjudication (§2.5).
3. **3-way verification at 59** — 5-seed pre-pad warm-start from v9-3way-v2.2 (§3.3); PASS/STOP/HALT gate matrix (§3.4); failure-direction classification format (§3.4); 1-seed smoke pilot (§3.5).
4. **HU re-train cascade** — 30-hand 6-axis HU reference set (§4.2); 5-labeller v3.4 + Opus tier-up labelling (§4.3); ~750-situation HU corpus (§4.4); from-scratch HU retrain with reasoning (§4.5); 28/30 ship gate with reasoning (§4.6); sub-sub-phase decomposition (§4.7).
5. **Cost/time forecast** — per-sub-phase $$/wall-clock/binding-pilot-gate/HALT-condition table (§5.1); critical path (§5.2); off-ramps (§5.3).

7 falsifiable predictions registered for TC-X-DISPATCH-PREDICTION-VERIFICATION (§6) — exceeds the dispatch's "≥ 3" requirement.

3 genuine owner-scope items surfaced explicitly (§7) — HU corpus size, Phase 1.5 ship boundary, Phase 2 D5 entry — none of which are technical-decision menus.

## Methodology compliance

- **Single committed path** per `feedback_quality_default_no_ask.md`: every technical choice committed with reasoning (re-extract over column-drop §2.1; pre-pad warm-start §3.3; from-scratch HU §4.5; 28/30 HU ship gate §4.6; 30-hand 6-axis HU reference §4.2; 750 HU corpus §4.4). Owner-scope flags only on genuine trade-offs (§7).
- **Pilot-first** per `feedback_pilot_first_for_long_jobs.md`: every long batch has explicit pilot+full split with binding gate — HU reference set design (5/25 split §4.2), HU labelling (5/25 split §4.3), HU corpus (50/700 split §4.4), HU retrain (1-seed smoke + 5-seed full §4.5), 3-way verification at 59 (1-seed smoke + 5-seed full §3.5).
- **Tier-up sub-rule** per `feedback_pilot_first_for_long_jobs.md`: HU labelling specifies Sonnet → Opus cross-check on non-unanimous-Sonnet sample (§4.3).
- **Solver-aligned bet sizes** per `feedback_solver_aligned_sizing.md`: HU spot specs adopt flop 25%/66%, turn 33%/75%, river 33%/75%/150% (§4.2).
- **Terminology compliance** per `feedback_terminology_raise_vs_bet.md`: explicit raise/bet/open definition adoption in HU spot specs (§4.2).
- **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: solver verifies disagreements only; never used as training labels (§4.3).
- **Bucket-first** per `feedback_bucket_first_labelling.md`: no equity thresholds in labelling prompt; thresholds in `coaching/spot_classifier.py` (§4.3).
- **Postflop strength composition** per `feedback_preflop_geometry_vs_postflop_composition.md`: HU axis design uses TP+/draws/air composition (§4.2).
- **Close-hand selection** per `feedback_close_hand_selection.md`: 3-of-5 close hands per axis driven by v8-HU-38 model uncertainty + poker difficulty (§4.2).
- **Failure-direction classification** per `feedback_failure_direction_classification.md`: under-aggress / over-aggress / class-collapse format committed for both 3-way verification and HU retrain reports (§3.4).
- **Attention/prompt/capture/trainer lock-step** per `feedback_attention_flags_when_features_change.md`: 1.3 inventory enumerates every touch-point; 1.3.2 documents the 12.5J-B attention-layer gap.
- **No deadlines** per `feedback_no_deadlines.md`: §5.1 estimates labelled "rough" / "estimate" with explicit caveat; quality path beats schedule.
- **TC-23 EXISTENCE + CONTENT** per `feedback_spec_vs_infrastructure_code_drift.md`: §1.2 explicit attestation list at master `e66e2e6`.

## Negative scope (mandatory)

- ❌ No source / data / model / prompt edits in this branch.
- ❌ No execution of any feature drop, corpus re-extract, retrain, or HU labelling.
- ❌ No modification of `feature_extractor.py` / `feature_keys.py` / any river-rats-core source.
- ❌ No modification of v3.x prompts / BATCH2 / 988-corpus / model files / 40-hand reference set.
- ❌ No execution of D5.
- ❌ No "open technical questions" in the memo (architect commits with reasoning per `feedback_quality_default_no_ask.md`); only genuine owner-scope trade-offs flagged.

PR diff scope: 2 files only — this report + the design memo. No other changes.

## What gates this PR

1. **QC stream audit** (~15-20 min, standalone, ~/river-rats-qc/) per `feedback_qc_routing_when_standalone_active.md`. 7-item audit per dispatch §"QC stream — what you audit". QC writes `~/river-rats-qc/findings/2026-05-08-pr<N>-phase15a-design.md` + cross-posts `review/comms/REVIEW_QC_PHASE15A_DESIGN_2026-05-08.md`. Updates heartbeat per `project_qc_heartbeat_convention.md`.
2. **Owner-merge gate** per `feedback_explicit_action_trigger.md` and `feedback_qc_required_before_approval.md` (milestone-class PR — design lock for the entire 1.5 workstream). Orchestrator does NOT merge milestone PRs without explicit owner `fire now`.

## What fires after this PR merges

- Orchestrator dispatches Phase 1.5-B (feature-prune mechanical execution) per architect's committed sequencing in §4.7.
- Owner ratifies 1.5-B fire authorization.
- Owner-scope items (§7) may be surfaced earlier if any become blocking; otherwise discussed at 1.5-D.3 dispatch (HU corpus size) and Phase 1.5 SHIP comm (ship boundary, D5 entry).

## References

(See memo §8 for complete reference list.)

Key dispatch and lineage references:

- Phase 1.5-A dispatch: `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (PR #306, master `5863f13`).
- 12.5L SHIP-A QC PASS (most recent merged milestone): master `e66e2e6` (PR #305).
- This branch: `programmer/phase15a-unified-surface-design-2026-05-08`.

---

**Status: 2 files in PR diff (this report + design memo). Single committed path across 5 design areas. 7 falsifiable predictions for QC retro-verification. 3 owner-scope items surfaced. Awaits QC + owner-merge gate.**
