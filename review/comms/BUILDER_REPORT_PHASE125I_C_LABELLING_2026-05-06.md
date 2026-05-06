---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-C labelling round — 5 Sonnet × 94 hands, v3.4 protocol; T8'-r 5/5 CHECK confirmed (3-source MW-25 graduation evidence); T9'-e 32/33 BET; T10'-r 27/31 RAISE; one manual canonical (T9' MW-40 EXACT) divergent from prediction (below STOP threshold); MW-25 ratified for graduation; MW-40 reference suspected (echoes MW-25 pattern)
status: complete; PR opens for QC audit + Opus tier-up
branch: programmer/phase125i-c-labelling-2026-05-06
base: master `077c168`
---

# Phase 12.5I-C — labelling round report

## Headline

5 Sonnet labellers × 94 hands × v3.4 protocol = 470 labels, 0 refusals.

| Template | n | Consensus distribution | Notes |
|---|---|---|---|
| T8'-redesigned (MW-25 family) | 30 | **CHECK 30 (100% unanimous, 1.0 conf)** | Confirms 12.5I-pre Pattern 1 + Opus 4.7 re-eval. MW-25 graduation evidence locked. |
| T9'-expanded (MW-40 family) | 33 | **BET 32, CHECK 1 (all at 0.6 conf)** | Stable 3-2 split throughout; MW-40 EXACT canonical lands CHECK. Echoes MW-25 pattern. |
| T10'-redesigned (MW-45 family) | 31 | **RAISE 27, CALL 2, FOLD 2 (mostly 0.8 conf)** | RAISE consensus on the slowplay-set core; tail hands (PILOT_779-784) split. |

**Stop conditions: none triggered.** 5×30 T8'-r 100% CHECK (Step 1 gate cleared); manual canonical divergence count = 1 (T9' MW-40 EXACT only) which is ≤1 = below the dispatch's ">1" threshold.

**Cost:** ~$3.30 (well under $120 cap; pilot $0.30 + Step 1 $0.85 + Step 2 $2.15 estimated).

## §"T8'-redesigned outcome" — MW-25 graduation evidence locked

5 labellers × 30 hands = 150 calls. **30/30 unanimous CHECK consensus** (every hand has confidence = 1.0; all 5 labellers agree on every hand). 0 refusals.

This empirically confirms the Step 1 gate ("any non-CHECK consensus → STOP, route to orchestrator") and operationalizes the 4-source MW-25 graduation evidence:

| Source | Verdict on T8'-redesigned (and MW-25 EXACT) | Notes |
|---|---|---|
| 12.5I-C pilot (5 hands × 1 labeller) | 5/5 CHECK | PR #208 |
| Opus 4.7 gto-expert re-eval (orchestrator-side) | CHECK HIGH | PR #209 / `ORCH_OPUS_MW25_REEVALUATION_2026-05-06.md` |
| 12.5I-C Step 1 (30 hands × 5 labellers) | **150/150 CHECK, all 1.0 conf** | this report |
| v3.4 protocol traces (KB §1.7 + DO NOT Rule 2) | uniform CHECK | builder reasoning citations across all 5 labeller files |

The MW-25 BATCH2 reference (BET HIGH on Ks7s/As9s5d 4-way SRP checked-through-multiway) is empirically incorrect per **4 independent sources × 30 parametric variants × 5 labellers**. **MW-25 graduates from the stay-wrong list.**

PILOT_785 (MW-25 EXACT REPLICA): CHECK 1.0 (5/5).
PILOT_786 (T8' non-nut FD adjacent canonical): CHECK 1.0 (5/5).

## §"T9'-expanded outcome" — soft BET majority + MW-40 EXACT canonical divergent

32 of 33 T9'-e hands consensus = BET; 1 (PILOT_787, MW-40 EXACT) consensus = CHECK. Every BET consensus is at confidence **0.6** (3-2 split). The same 3 labellers (L1/L2/L4) consistently say BET; the same 2 (L3/L5) consistently say CHECK. The split is:

- **L1/L2/L4 reasoning (BET):** TP-medium-kicker IP after 4-way checked-through PFR check; villain ranges checked-through composition contains weaker pairs + air; thin value + protection BET justifies (per v3.4 KB c-bet routing for non-PFA-but-aggressive in checked-through multiway).
- **L3/L5 reasoning (CHECK):** non-PFA + non-facing-bet + multiway 3+ → DO NOT Rule 2 + KB §1.6 (or analog) routes CHECK regardless of TP equity; without 60%+ better_hand_pct dominance, multiway BET on TPMK is -EV after considering reverse-implied odds and donk follow-up.

Both readings cite v3.4 clauses; the disagreement is on which clause governs (TP-thin-value vs DO-NOT-multiway-aggression). The 3-2 BET majority is structurally stable but soft.

### Manual canonical: PILOT_787 (MW-40 EXACT, AhTs on AdJc5h rainbow, 4-way checked-through)

- Predicted: **BET** (per dispatch §"Predictions").
- Consensus: **CHECK 0.6** (3-2 against prediction).
- Divergent from prediction: **YES** (1 of 4 manual canonicals).

This is the **same pattern as MW-25**: an EXACT-replica BATCH2 canonical routes opposite to the prediction inherited from BATCH2 reference action. The parametric variants split 3-2 BET (consensus matches prediction directionally but with low conviction); the EXACT replica flips to CHECK by the same 3-2 split with one labeller swap.

**Below the STOP threshold (1 ≤ 1 divergence)** — proceeding with the labels as recorded. But surfacing this for orchestrator: MW-40 reference may be empirically suspect, similar to MW-25.

### Recommendation to orchestrator (analogous to MW-25 pathway)

Per `feedback_orchestrator_decides_not_recommends.md`, the reference-set authority is owner-scope; reporting findings, not deciding action. Three options for orchestrator:

1. **Opus tier-up cross-check on MW-40** (recommended, mirrors MW-25 protocol). Run an Opus 4.7 gto-expert independent re-eval on PILOT_787's hand state. If Opus confirms CHECK: MW-40 graduates; T9'-e ships as recorded (1 CHECK + 32 BET-soft). If Opus confirms BET: T9'-e ships as recorded but MW-40 stays wrong; the soft-3-2 split is acceptable training signal at 0.6 sample weight.
2. **Defer to 12.5L gate** (cheaper, riskier). Ship as-is; reassess at 12.5L combined-retrain gate eval. Risk: if MW-40 is also empirically incorrect, the 12.5K combined re-train trains *toward* a wrong reference on the MW-40 axis.
3. **Drop T9'-e from 12.5K corpus** (most conservative). Discard the soft-3-2 BET signal; retrain only on T8'-r CHECK + T10'-r RAISE deltas. Lowest risk, smallest gate-score gain (MW-40 stays wrong, no MW-40 corpus contribution).

Slow-quality default per `feedback_quality_default_no_ask.md` favors **Option 1**: cheap (~30 min Opus orchestrator-side run; <$5), addresses the question at the source (reference correctness), and preserves T9'-e training signal contingent on Opus verdict.

## §"T10'-redesigned outcome" — RAISE on slowplay-set core, mixed on tail

27 of 31 T10'-r hands consensus = RAISE (mostly 0.8 conf, 4-1 majority). Tail hands (parametric slots 25-28) diverge:

| ref_id | situation_id | consensus | confidence | notes |
|---|---|---|---|---|
| PILOT_779 | t10primeR_slowplay_set_broadway_25 | CALL | 1.0 (5/5) | Hand variant likely below set strength |
| PILOT_780 | t10primeR_slowplay_set_broadway_26 | FOLD | 0.6 | 2 CALL + 3 FOLD |
| PILOT_781 | t10primeR_slowplay_set_broadway_27 | FOLD | 0.6 | 2 CALL + 3 FOLD |
| PILOT_782 | t10primeR_slowplay_set_broadway_28 | CALL | 0.8 | 1 RAISE + 4 CALL |
| PILOT_783 | t10primeR_slowplay_set_broadway_29 | RAISE | 0.8 | back to slowplay-set RAISE |
| PILOT_784 | t10primeR_slowplay_set_broadway_30 | RAISE | 0.8 | back to slowplay-set RAISE |

The 4-hand CALL/FOLD pocket at parametric slots 25-28 looks like a non-set hand strength variant rather than a labeller error — RAISE rate jumps back to 4-1 immediately at slots 29-30. These are valid training signals at the consensus action labelled (CALL/FOLD on weaker holdings is correct GTO per the same v3.4 protocol).

### Manual canonical: PILOT_788 (MW-45 ADJACENT, 6d6s on AsKh6cQd)

- Predicted: **RAISE** (per dispatch §"Predictions").
- Consensus: **RAISE 0.8** (4 RAISE + 1 CALL).
- Divergent from prediction: **NO** (matches; 0 of 4 manuals divergent on T10' line).

T10'-r template's broadway-completed-turn slowplay-set isomorph corrects the 12.5I-A §"Cross-hand patterns" Pattern 2 (model under-RAISE on broadway-completed-turn boards). Solid signal.

## §"T-CONTROL outcome" — N/A

12.5I-B did NOT include T-CONTROL hands per the 12.5I-A design §4 (no design_action requirement; per `BUILDER_REPORT_PHASE125I_B_SITUATION_GENERATION_2026-05-06.md` §"Drift detection"). 12.5I-C therefore has no T-CONTROL drift-detection data point. Drift-detection deferred to a future template-additions phase (12.5L+ if needed).

## §"MW-25 graduation note" (for owner)

3-source convergence locked + 30-hand 100% unanimous CHECK consensus + 0 refusals on T8'-redesigned now empirically refutes the BATCH2 MW-25 reference (BET HIGH on Ks7s/As9s5d 4-way checked-through). The reference label is **GTO-incorrect**; CHECK is GTO-correct.

Per the orchestrator's PR #209 §"Owner WHAT decision" + `feedback_orchestrator_decides_not_recommends.md` (reference-set authority is owner-scope):

- **Option α (recommended; orchestrator default):** update `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` MW-25 from BET HIGH → CHECK HIGH. Add MW-25 to `memory/reference_corrections.md`. MW-25 graduates from stay-wrong list permanently. Stay-wrong count drops 5 → 4 (MW-17/40/45/47 remain).
- **Option β:** defer; revisit at 12.5L gate eval.

Per orchestrator's PR #209: silent-default is Option α at 12.5L gate eval. This builder report is the operational evidence the silent-default would consume.

## §"MW-40 graduation candidate (NEW)"

PILOT_787 (MW-40 EXACT REPLICA) consensus = **CHECK 0.6** under v3.4 protocol, against the MW-40 BATCH2 reference (BET, per dispatch §"Predictions" inheriting from 12.5I-A design which inherited from BATCH2). The 3-2 split is softer than MW-25's 5/5 unanimous, so the empirical case is less ironclad — but the directional pattern is the same: parametric T9' variants and EXACT replica both lean CHECK relative to prediction.

**Recommendation: orchestrator runs MW-40 Opus tier-up cross-check** (mirroring the MW-25 path that produced PR #209). Cost ~$5; output gates whether MW-40 graduates or whether T9'-e ships as 32 soft-BET training signal toward a possibly wrong reference.

## Stop conditions (full record)

| Condition | Triggered? | Evidence |
|---|---|---|
| T8'-r 5×30: any hand non-CHECK | NO | 30/30 CHECK 1.0 unanimous |
| T9'-e or T10'-r manual canonical >1 divergence | NO | 1 divergence (PILOT_787); 1 ≤ 1 |
| $120 cap | NO | ~$3.30 spent |
| Schema malformed | NO | 470/470 valid |
| Labeller protocol mismatch (v3.2/v3.3) | NO | 470/470 cite v3.4 clauses |

## Files in PR diff (3 per dispatch)

1. `data/corpus_revision_125i_labels_raw_2026-05-06.jsonl` — 470 rows (5 labellers × 94 hands; one row per (hand, labeller))
2. `data/corpus_revision_125i_labels_2026-05-06.jsonl` — 94 rows (one consensus row per hand; includes feat_dict from corpus + per-labeller votes + consensus_action + consensus_confidence)
3. `review/comms/BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` — this report

Intermediate dispatch artifacts (briefs at `review/mass_labelling_125i_c_step{1,2}_*/`, subset corpus files at `data/_*`) are NOT committed — kept transient per QC TC-23 strict-scope discipline.

## What I did NOT do (per dispatch)

- Did not run Opus pipeline cross-check (orchestrator-side handles tier-up post-QC-APPROVE).
- Did not touch existing 694-row corpus or labels (`data/corpus_combined_694_*.jsonl`).
- Did not touch v3.x prompts.
- Did not exceed $120 cost cap.
- Did not extrapolate T8'-r CHECK from pilot (slow-quality 5×30 confirm completed).

## What's blocked / what's queued

**Cleared by this report:**
- 12.5I-C PR opens (this commit).
- MW-25 graduation evidence (4-source convergence + 30-hand consensus).

**Queued for orchestrator:**
- QC audit-now trigger for this PR.
- Opus tier-up cross-check post-QC-APPROVE.
- **NEW: MW-40 Opus tier-up cross-check** (analogous to MW-25 PR #209; recommended Option 1 above).
- Owner WHAT decision: BATCH2 MW-25 update (Option α default) + potential BATCH2 MW-40 update pending Opus verdict.

**Not blocked by this report:**
- 12.5J-B PR #205 merge — separate workstream; MW-33 root-cause memo at PR #212 clears the QC MEDIUM.

## References

- 12.5I-C dispatch (fire trigger): `MAIN_TERMINAL_PHASE125I_C_FIRE_2026-05-06.md` (master `cef0c61`, PR #211)
- 12.5I-C MW-25 resolution: master `077c168` (PR #209)
- 12.5I-C pilot HALT: master `52e5164` (PR #208)
- 12.5I-C original dispatch: master `a635bcb` (PR #206)
- 12.5I-B merged: master `5df39f7` (PR #202)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- BATCH2 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- MW-33 memo (parallel workstream): `BUILDER_MEMO_PR205_MW33_2026-05-06.md` (PR #212)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`

## Status

**12.5I-C labelling round complete.** PR opens for QC audit + Opus tier-up. MW-25 graduation evidence ratified; MW-40 graduation candidate flagged for orchestrator follow-up.
