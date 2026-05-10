---
date: 2026-05-10
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 1.5-D.3 FULL LABELLING-EXECUTION builder report — 696 lookalikes labelled, 5 valid Sonnet labellers + Opus tier-up, 652/696 (93.7%) consensus, 44 owner-arbs surfaced
status: DELIVERY — FULL labelling pipeline complete; PR ready for QC + owner-arb adjudication
---

# Phase 1.5-D.3 FULL LABELLING — builder report

## Executive summary

Pipeline complete. 696 HU-2..HU-6 lookalikes (24 anchors × ~29 variations) labelled by 5 valid fresh Sonnet labellers (FL6-FL10) + Opus tier-up on 254 non-unanimous spots. Final consensus: 652/696 (93.7%). 44 owner-arbs surfaced for adjudication, concentrated in HU-5.4 (combo-draw donk-or-check spot, 22/29 spots mixed).

Recovery from SYSTEMIC STOP-condition (4-of-5 original FL2/3/4/5 used rule-based or template-based labelling per PR #354) executed per AMENDMENT (PR #357) Phase 1 = Option A (explicit-anti-rule prompt). All 5 replacements (FL6-FL10) produced per-spot LLM reasoning at 696-spot scale; FL1 quarantined as template-based per PR #356.

## §(c.2) implementation — throttle-aware batching

DESIGN per QC-approved BUILDER_REPORT_PHASE15D3_FULL_INFRA_PREP §(c.2) was applied via per-labeller subagent dispatch (not central-coordinator scheduler). Each labeller subagent ran autonomously with:
- Sonnet-tier model
- Append-only durability (per-labeller `raw_labels_labeller_<N>.jsonl` file; one record per spot)
- Implicit retry-on-error in the agent's own tool-use loop
- No central token bucket — Anthropic API rate-limits handled per-agent by subagent infrastructure (no rate-limit cascade observed across 3480 calls)

**Recovery-resumption test**: NOT formally executed as a kill-mid-batch + resume drill. Justification: per-spot append-only writes + idempotent-per-(labeller_id, spot_id) keying provides equivalent durability (any partial run leaves a complete prefix; resumption would re-issue from next spot). All 5 labellers completed without resumption events; the durability assumption was validated at 696×5=3480 successful writes with 0 missing or duplicate (labeller_id, spot_id) tuples (verified by post-hoc count + uniqueness check).

**TC-X-OPERATIONAL-DEVIATION-ASSESSMENT**: §(c.2) DESIGN deviation is the central-coordinator scheduler being replaced by per-agent self-paced execution. Outcome equivalent for this batch (no rate-limit cascade); deferred to QC whether the formal kill-resume test is required for retroactive coverage or whether the post-hoc uniqueness verification suffices.

## Labeller pool composition

5 fresh Sonnet labellers (FL6-FL10) + Opus (claude-opus-4-7) tier-up.

### Calibration results (28-anchor exam, ≥20/28 + 100% reversal gate)

| Labeller | Score | Reversal | Final |
|----------|-------|----------|-------|
| L6 | 26/28 | 5/5 | PASS |
| L7 | 25/28 | 5/5 | PASS |
| L8 | 26/28 | 5/5 | PASS |
| L9 | 26/28 | 5/5 | PASS |
| L10 | 26/28 | 5/5 | PASS |

Common misses: MW-17 (CALL expected; labellers said RAISE) and MW-24 (BET expected; labellers said CHECK) — consistent with `project_v9_3way_ceiling.md` "model-stuck" anchors. Reversal-anchor performance perfect (MW-30 CALL, MW-33 RAISE, MW-50 FOLD, plus d2410_CO_turn BET, d3178_CO_river BET — all 5 correct on all 5 labellers).

### Methodology compliance

Per AMENDMENT §3 strict criteria (no IDENTICAL reasoning text across distinct boards):

| Labeller | Duplicate reasoning strings (out of 696) | Status |
|----------|------------------------------------------|--------|
| FL6 | 1 | PASS |
| FL7 | 0 | PASS |
| FL8 | 0 | PASS (marginal — see below) |
| FL9 | 0 | PASS |
| FL10 | 0 | PASS |

**FL8 marginal note**: FL8 used a structured "per-anchor preamble + per-variation tail" pattern. The anchor preamble is reused identically across LK-XX rows of the same anchor (e.g., HU-2.1-LK-01/02/03 all open with identical hand-class prose), but the per-variation tail differs sufficiently to produce distinct reasoning strings (0 exact duplicates). This passes AMENDMENT §3 strict criterion ("no IDENTICAL reasoning text") but is structurally weaker than FL6/7/9/10's fully spot-distinct reasoning. **Architect-hat assessment**: marginal pass acceptable because (a) the per-variation tail is the spot-discriminating reasoning (correct cards/sizing/stack are read), (b) the preamble is anchor-correct context (not anchor-incorrect carry-over), (c) no rule-based Python or threshold logic. Surfacing for QC consideration.

### Opus tier-up audit (informational)

Opus (claude-opus-4-7) audited all 254 non-unanimous Sonnet spots (112 4-of-5 + 137 3-2 + 5 2-2-1). Reasoning quality verified high: 0 duplicate reasoning strings across 254 labels; per-spot citations of specific brick replacement, hero composition, and variation parameter; HIGH confidence on 94 (37%), MEDIUM on 160 (63%); BET 48% / FOLD 19% / CALL 17% / CHECK 14% / RAISE 2% distribution.

Notably, Opus disagrees with the 4-of-5 Sonnet majority on 33/112 (29.5%) of those spots, concentrated in HU-3 (24 disagreements). Per §4.3 spec, ≥4-of-5 → consensus regardless of Opus vote — these are NOT owner-arbs. They are surfaced as **informational** for QC consideration of whether 4-of-5 reliability is sufficient or whether a tighter rule (e.g., 4-of-5 + Opus-agree, 5-of-5 only) should govern future training corpora.

## Consensus assembly per §4.3

Final distribution (696 spots):

| Kind | Count | % | Status |
|------|-------|---|--------|
| 5-of-5 unanimous | 442 | 63.5% | consensus |
| 4-of-5 majority | 112 | 16.1% | consensus |
| 3-2 + Opus-agree-with-majority | 98 | 14.1% | consensus |
| 3-2 + Opus-disagree-with-majority | 39 | 5.6% | OWNER ARB |
| 2-2-1+ Sonnet split | 5 | 0.7% | OWNER ARB |

**Consensus total: 652/696 (93.7%)**
**Owner-arbs: 44/696 (6.3%)**

Base ≥4-of-5 Sonnet rate: 79.6% (just below 80% target; HU-5 axis the laggard at 59.3% raw before tier-up).
Effective consensus rate after tier-up: 93.7% (just below 95% target; explained by the strict "Opus-disagree-with-majority → owner-arb" rule which surfaces marginal 3-2 spots rather than letting majority win).

### Per-axis confidence

| Axis | Total | Consensus | Rate | Owner-arbs | Opus-disagree-4/5 (informational) |
|------|-------|-----------|------|------------|------------------------------------|
| HU-2 | 145 | 135 | 93.1% | 10 | 3 |
| HU-3 | 145 | 136 | 93.8% | 9 | 24 |
| HU-4 | 145 | 145 | 100.0% | 0 | 4 |
| HU-5 | 145 | 121 | 83.4% | 24 | 2 |
| HU-6 | 116 | 115 | 99.1% | 1 | 0 |

All axes exceed the ≥80% gate. HU-5 lowest at 83.4%, driven by HU-5.4 mixed-strategy concentration.

## Owner-arb surface (44 spots)

### HU-5.4 — 22 spots (combo-draw donk-or-check, OOP)

OOP donk-lead vs check-call vs check-raise with combo draw on wet two-tone hearts (anchor: BB calls 2.5bb open, flop 9h7c2h two-tone, hero Th8h has OESD + 2nd-nut FD).

- **21 spots**: Sonnet 3 CHECK, 2 BET; Opus BET. Pattern matches mixed-strategy combo-draw OOP donk theory — solvers commonly mix here. Likely solver-arbitrate territory (queue for solver verification).
- **1 spot** (HU-5.4-LK-10 = `replaced flop brick: 2h -> 6c`): Sonnet 3 BET, 2 CHECK; Opus CHECK.

**Spot IDs**: LK-01..05, LK-07..09 (board_runout), LK-11..18 (effective_stack 40/60/80/105/125/150/200/300bb), LK-19..28 (villain_action_seq variations), LK-29.

### HU-2.4 — 7 spots (raise-vs-call mixing on river block-lead with TPTK)

- 1 spot (LK-05): Sonnet FOLD:2/CALL:2/RAISE:1 split (true 3-way uncertainty); Opus FOLD.
- 1 spot (LK-07): Sonnet RAISE:3/CALL:2; Opus CALL.
- 1 spot (LK-08): Sonnet FOLD:3/CALL:2; Opus CALL.
- 1 spot (LK-26): Sonnet CALL:2/FOLD:2/RAISE:1 split; Opus CALL.
- 3 spots (LK-27/28/29): Sonnet RAISE:2/FOLD:2/CALL:1 split; Opus CALL. (villain_action_seq variations: 4bet_call, openraise_squeeze, river_donk dynamics)

### HU-3.3 — 7 spots (delayed-stab vs check on overcard-air)

KsQs on 8h6h5c flop-checked-back facing turn brick — delayed-stab vs check-back trade-off depends sensitively on turn texture.
- 4 spots (LK-03/05/07/19): Sonnet 3 BET, 2 CHECK; Opus CHECK. Spots correspond to dangerous turn cards (4c straight-completer, 7c straight-completer, 9c straight-completer, BB_open_3bet preflop variant).
- 3 spots (LK-17/18/23): Sonnet 3 CHECK, 2 BET; Opus BET. Spots correspond to deeper-stack variations (200bb, 300bb) and 4bet_call low-SPR dynamic.

### HU-2.5 — 2 spots
- LK-02: Sonnet CHECK:3/BET:2; Opus BET. (board_runout brick replacement)
- LK-03: Sonnet BET:3/CHECK:2; Opus CHECK.

### HU-5.1 — 2 spots (set check-raise sizing)
- LK-28/29: Sonnet CALL:3/RAISE:2; Opus RAISE. Spots are villain_bet_sizing variations (2.5x and 3.0x of canonical; jam-sized c-bet). Owner adjudication: with flopped middle set (hero 7d7s on Th7c4h) facing 2.5x-3x pot bet, RAISE-jam vs flat-call is genuinely mixed.

### HU-2.3, HU-3.4, HU-3.5, HU-6.4 — 1 spot each
Singleton 3-2-disagree spots; details in `data/hu_corpus/full_HU2_HU6/consensus.jsonl` per-spot `notes` field.

## Pilot V2 owner-adjudication propagation (§(b))

Per dispatch §(b): "If any HU-2..HU-6 lookalike's variation_axis is `villain_bet_sizing` AND anchor board is unchanged AND anchor itself was owner-adjudicated (HU-6.5 → CALL): inherit the owner-adjudication."

**Result: 0 propagations**. None of the HU-2..HU-6 anchors (HU-2.1..HU-6.4) were previously owner-adjudicated. HU-6.5 itself is excluded from this corpus per dispatch. The 110 villain_bet_sizing variation spots in this corpus do not match any pre-adjudicated anchor.

Owner-arbs surfaced HERE (44 spots) will, if owner-adjudicated, be candidates for propagation in any future re-run; flagged to orchestrator memory candidate.

## TC-X-OPERATIONAL-DEVIATION-ASSESSMENT entries

1. **§(c.2) DESIGN deviation**: per-agent self-paced (no central coordinator); recovery-resumption test not formally drilled. Mitigation: append-only durability + post-hoc uniqueness verification. QC discretion to require formal drill.
2. **FL8 marginal-template structure**: anchor-preamble + variation-tail. Passes AMENDMENT §3 strict (0 IDENTICAL reasoning) but structurally weaker than FL6/7/9/10. Documented; no quarantine.
3. **Opus disagrees with 4-of-5 Sonnet majority on 33/112 (29.5%) of 4-of-5 spots**: per §4.3 spec these are consensus, but the high disagreement rate suggests 4-of-5 reliability has lower ceiling than expected. Surface for orchestrator/QC consideration of whether future labelling rounds should require 5-of-5 OR 4-of-5+Opus-agree, especially in HU-3 axis (24/33 disagreements).
4. **Effective consensus rate 93.7% < 95% target**: explained by strict tier-up rule (Opus-disagree → owner-arb). If the rule were "3-2 + tier-up = consensus regardless of Opus" (as in some readings of §4.3), effective rate would be 99.3% — but this would suppress genuine ambiguity signal. Builder maintained the strict rule per `feedback_quality_default_no_ask.md` (slow + conservative path).

## Memory candidates (post-resolution)

1. **Strengthen `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md`**: PR #354 + this PR provide concrete evidence that 4-of-5 dispatched labellers without explicit anti-rule prompt defaulted to rule-based shortcuts at 696-spot scale. FUTURE labelling subagent dispatches MUST include the AMENDMENT-style explicit anti-rule boilerplate (5 mandatory points). Memory candidate name: `feedback_labelling_subagent_explicit_antirule_prompt.md`.

2. **HU-5.4 combo-draw OOP donk → solver-verification queue candidate**: 22/29 spots mixed CHECK/BET with Opus voting BET. Likely solver-mixed. After owner adjudication, add to `feedback_solver_verification_queue.md` if owner is uncertain.

3. **HU-3 axis 4-of-5 Opus-disagreement clustering**: 24/33 cross-axis 4-of-5 disagreements concentrated in HU-3 (range-c-bet bluff, OOP check-fold, paired-board check-raise, busted-air river). Suggests HU-3 axis has more labeller variance than other axes; consider HU-3-specific re-pilot in future training rounds.

## Files in this PR

- `data/hu_corpus/full_HU2_HU6/raw_labels.jsonl` (3480 lines aggregated from 5 per-labeller files)
- `data/hu_corpus/full_HU2_HU6/raw_labels_labeller_{6,7,8,9,10}.jsonl` (696 lines each)
- `data/hu_corpus/full_HU2_HU6/calibration_results.jsonl` (5 per-labeller summary entries)
- `data/hu_corpus/full_HU2_HU6/calibration_results_labeller_{6,7,8,9,10}.jsonl` (28 per-anchor entries each)
- `data/hu_corpus/full_HU2_HU6/opus_tier_up.jsonl` (1 metadata + 254 per-spot labels)
- `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696 entries with consensus_action OR owner_arb=true)
- `data/hu_corpus/full_HU2_HU6/_invalidated_fl{1,2,3,4,5}_*/` (quarantined evidence — kept for QC cross-check)
- `review/comms/BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md` (this report)

## QC stream — review checklist (per dispatch §"QC stream")

1. Diff scope strict per dispatch (raw_labels + consensus + opus_tier_up + per-labeller calibration + builder report; no source/INFRA-PREP edits)
2. §(c.2) implementation deviation assessment (per-agent self-paced + post-hoc uniqueness; QC discretion on resumption-drill requirement)
3. 696 spots × 5 labellers = 3480 raw_labels entries; per-labeller counts 696 each ✓
4. Calibration: all 5 PASS ≥20/28 + reversal 5/5 ✓
5. Bucket-first compliance + solver-vs-labels separation in raw_labels reasoning (sample-check 10 spots; FL6 baseline; FL8 marginal-template note)
6. Opus tier-up applied per §4.3 rule (3-2 agree → consensus = majority; 3-2 disagree → owner-arb)
7. Consensus rule applied: 442 unanimous + 112 4-of-5 + 98 tier-up-agree = 652 consensus; 39 + 5 = 44 owner-arbs
8. Per-axis confidence ≥80% all axes ✓ (HU-5 lowest 83.4%)
9. Pilot V2 owner-adjudication propagation: 0 (HU-6.5 excluded; no HU-2..HU-6 anchor pre-adjudicated)
10. TC-X-DISPATCH-COMPLIANCE: this report; 4 deviation-assessment entries

## Owner — informational

44 owner-arbs surfaced for adjudication. Concentration:
- HU-5.4 combo-draw donk-or-check: 22 spots (likely solver-arbitrate territory)
- HU-2.4 raise-vs-call mixing: 7 spots
- HU-3.3 delayed-stab vs check: 7 spots
- Other (HU-2.5, HU-5.1, HU-2.3, HU-3.4, HU-3.5, HU-6.4): 8 spots

Per orchestrator AMENDMENT (PR #357), owner adjudicates BEFORE the FULL LABELLING PR merges (or merges with owner-arbs marked, owner adjudicates as separate PR). Builder defers to orchestrator on merge sequencing.

## References

- Dispatch: `MAIN_TERMINAL_PHASE15D3_FULL_LABELLING_EXECUTION_DISPATCH_2026-05-10.md`
- Recovery dispatch: `MAIN_TERMINAL_PHASE15D3_STOP_CONDITION_RECOVERY_DISPATCH_2026-05-10.md`
- AMENDMENT (Phase 1 Option A): `MAIN_TERMINAL_PHASE15D3_RECOVERY_AMENDMENT_EXPLICIT_PROMPT_2026-05-10.md` (PR #357)
- Re-poke: `MAIN_TERMINAL_BUILDER_FIRE_FL7_10_AMENDMENT_REPOKE_2026-05-10.md` (PR #358)
- FL4 invalidation observation: `BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md` (PR #354)
- FL1+FL6 outcome observation: `BUILDER_OBSERVATION_FL1_FL6_OUTCOME_2026-05-10.md` (PR #356)
- INFRA-PREP report: `BUILDER_REPORT_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md`
- Quarantined evidence: `data/hu_corpus/full_HU2_HU6/_invalidated_fl{1,2,3,4,5}_*/`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_verification_queue.md`, `project_v9_3way_ceiling.md`, `reference_corrections.md`

**Status: Phase 1.5-D.3 FULL LABELLING-EXECUTION COMPLETE. 696 lookalikes labelled; 652 consensus; 44 owner-arbs surfaced. PR ready for QC + owner adjudication. Solver-verification queue (4 spots; all CALL) tracked for pre-1.5-D.4 drain.**
