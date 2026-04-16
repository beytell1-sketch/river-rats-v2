---
date: 2026-04-16
from: Builder
to: Main terminal / Owner
re: Round 5 status — Phase 1 + Track B + Track C complete; Track D flagged BLOCKED
status: 2 ITEMS NEED OWNER ATTENTION
---

# Builder Status #5 — Phase 1 Round

5 commits this round.

| Commit | Track | Result |
|---|---|---|
| `c28c35e` + `fd89387` | A: Phase 1 generation | ✅ 483/483 hands, 0 validator failures |
| `3dfc35f` | B: v3 labeller prompt | ✅ 912 lines, override clause verbatim |
| `63c684b` | C: calibration exam update | ✅ 23/28 + 4 new anchors + Group D registry |
| `b51b22f` | D: curated-draw filter | ⚠️ **BLOCKED** — only 16 candidates (<20 floor) |

## Track A — Phase 1 generation: COMPLETE

| Bucket | BP | OS target | Generated | Clean |
|---|---:|---:|---:|---:|
| MM_IP_TURN | 30 | 38 | 38 | 38 |
| MM_IP_FLOP | 15 | 19 | 19 | 19 |
| MM_OOP_TURN | 20 | 25 | 25 | 25 |
| SM_IP_TURN | 20 | 25 | 25 | 25 |
| SM_IP_RIVER | 15 | 19 | 19 | 19 |
| MON_CHECKED | 15 | 19 | 19 | 19 |
| RAISE_VALUE | 20 | 25 | 25 | 25 |
| PROT_DANGER | 16 | 20 | 20 | 20 |
| PFR_CONT | 20 | 25 | 25 | 25 |
| UMBRELLA | 214 | 268 | 268 | 268 |
| **Total** | **385** | **483** | **483** | **483** |

- Validator failures: **0/483** (`num_opponents` validator clean)
- Schema preflight: **0 errors** across all 10 JSONLs
- UMBRELLA predicate compliance: **268/268 (100%)**
- Tests: 4/4 pass (test-first)

Key design notes from generator:
- UMBRELLA restricted to turn/river (flop cannot satisfy `villain_checked_back=1`)
- UMBRELLA villain_positions reordered so non-opener is primary villain → satisfies `villain_range_capped=1`
- RAISE_VALUE OOP-hero uses turn check-raise (OOP flop impossible — hero is earliest seat)
- Hand-strength tiers anchored to `hand_evaluator.evaluate_hand().category`

Deliverables: `review/generate_factory_batch6.py`, 10 `training-data/v23_*.jsonl`, `PHASE_1_GENERATION_REPORT_2026-04-16.md`.

## Track B — v3 labeller prompt: COMPLETE

`prompts/gto_labeller_v3.md` (912 lines), additive from v2 — nothing removed.

- **Override clause verbatim** at lines 304–311 in new section "BET-Decision Guidance — Stream B.2 Override Clause" (between Reasoning Protocol and Enriched Output). Inside `### Override clause (verbatim — do not paraphrase)` subsection.
- Wording matches directive-f §2.2 and scope §2 (no discrepancy).
- Negative-control guidance lists each precondition failure case explicitly (Phase 3.5 Criterion 1 negative control).
- 4 §3 additions tagged: `[v3 addition §3.A]`, `§3.B`, `§3.C`, `§3.D`.
- DO NOT Rule 10 (compressed-SPR CHECK default) + Rule 11 (HRP=0.00 artifact).
- Step 3 enhancement: BET-with-medium-or-better-checked-to action added.
- Calibration Notes: 3 v2 reversal anchors retained + 4 new MW anchors added.
- New Pass 2 Review section requires `[v3 addition ...]` citation on overrides.
- Output schema extended: new `override_clause_fired` boolean; feature_attention mandatory-features list extended to 7 override-clause features when clause fires.

## Track C — calibration exam: COMPLETE

`river-rats-core/calibration_exam.py` updated, 10/10 tests pass.

- Threshold: **23/28** standard + **100% reversal hands**
- 4 new anchors:
  - **Reversal:** `d2410_CO_turn`, `d3178_CO_river` (Stream B.2 predicate)
  - **Standard:** `d8886_BB_flop`, `d8963_HJ_turn` (mixed-zone)
  - All 4 sourced from canonical labelled JSONL (not hardcoded), all `expert_action=BET`
- **Group D:** 1 confirmed reversal (`d3688_BB_flop`) ingested via extensible `GROUP_D_REVERSAL_HANDS` registry
- Tests cover hand count, threshold, reversal rule, single-reversal-failure, full-pass scenario, anchor sourcing

**FLAG (non-blocking, owner attention):** Diagnostic test set doc names only `d3688` for Group D; the remaining 4 hands are "owner-nominated, TBD." Registry is extensible — additional hands added there auto-ingest into reversal set with no code change. Phase 3 calibration cannot run until Group D is finalised.

## Track D — curated-draw filter: BLOCKED

Stop condition tripped per build plan §1.4 (<20 floor on candidate count).

- **16 candidates** matched the filter (target was rows 6+7 = 25 hands; ~30 candidate target for spot-check)
- **9 from `3way_combined_350.jsonl`, 7 from `factory_batch5_situations.jsonl`**
- **Nut-blocker YES/LIKELY: 4/16 (25%)** — target was ≥50%
  - YES: d1983_BTN_turn, PA_Board3_Jh8h4h_h6, BP7_06
  - LIKELY: d5620_BTN_flop
- Row split: 10 flop / 6 turn
- Draw types: flush-only 9, straight-only 4, combo 3

**Data quality flag:** all 7 BP-batch5 candidates have `action=CALL` with `to_call=0` — malformed. Marked as "treat as unlabelled" for Pass 1/2.

**Owner decision needed (3 options per agent):**
1. Accept 16 candidates, scale rows 6–7 target down (15 → ~10 net per row)
2. Widen filter (permit `is_made_hand=1` weak-pair+draw or `facing_bet>0` semi-bluff-raise)
3. Source additional 3-way check-through spots from another pool

Deliverable: `review/comms/V23_CURATED_CANDIDATES_2026-04-16.md` ready for owner async spot-check.

## Updated phase grid

| Phase | Status |
|---|---|
| 0 Pre-flight | ✅ GO |
| 1 Generation (factory) | ✅ 483 hands clean |
| 1.4 Curated (rows 6-7) | ⚠️ BLOCKED on owner decision (16 < 20) |
| 1.5 Solver-sourced (row 11) | 🟡 owner-led, async |
| 2 Assembly QA | 🟡 ready (after curated resolved) |
| 3 Calibration | 🟡 ready (waiting on Group D finalisation + v3 prompt smoke test) |
| 3.5 Pilot review | ⏸️ gated on Phase 3 |
| 4 Production labelling | ⏸️ gated on Phase 3.5 |

## Items needing owner attention

1. **Track D curated-draw scope decision** — 16 vs 20+ candidates; pick widening strategy or accept reduced target
2. **Group D reversal hand finalisation** — 4 owner-nominated TBD hands needed before Phase 3 calibration can run

## What builder can do without further direction

- Phase 2 Assembly QA dry-run on the 10 generated JSONLs (validate combined schema, dedupe, check predicate splits)
- Wait on Track D + Group D before proceeding into Phase 3

I'll hold here pending owner direction on the two flagged items. Phase 1 main generation is otherwise green and committed.

Standing by.
