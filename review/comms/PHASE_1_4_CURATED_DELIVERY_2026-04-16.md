---
date: 2026-04-16
from: Programmer (Track D, Phase 1.4)
to: Main terminal (reviewer/orchestrator)
re: Track D curated nut-blocker staging — FINAL: 3 curated staged, PA_Board3 dropped per owner
status: DELIVERED
directive: review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-e.md §1 (commit 10247b6)
owner_resolution: review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-f.md §1 (drop PA_Board3)
cleanup_ticket: review/comms/TICKET_PA_BOARD_POOL_DEFECT_2026-04-16.md (post-v2.3-ship backlog)
---

# Phase 1.4 Curated Nut-Blocker Staging — FINAL

## Summary

Per owner directive `MAIN_TERMINAL_UPDATE_2026-04-16-f.md §1`, the Track D
curated row 6-7 allocation scales from 4 → 3 hands. `PA_Board3_Jh8h4h_h6`
is dropped due to systemic PA_Board* pool defects (see cleanup ticket).
The remaining 3 cleanly-staged curated hands are delivered.

Supplement net total: 420 → **398**. UMBRELLA (268 hands) absorbs the
residual Section 2 predicate coverage for nut-blocker drawing shapes.
Phase 7 backup clause (factory sub-pattern on nut-blocker semi-bluff)
remains available if drawing-signal regression surfaces post-validation.

## Per-hand delivery

All 3 records were located in their expected source pools, stripped of
label fields, piped through `normalise_situation()` from
`river-rats-core/situation_factory.py`, tagged with `_curated_source`,
and written to the split JSONLs by street.

| # | sid | Source pool | Row | Draw | Blocker | num_opp / len(villain_positions) | normalise_situation | Output JSONL |
|---|-----|-------------|-----|------|---------|----------------------------------|---------------------|--------------|
| 1 | `d1983_BTN_turn` | `training-data/3way_combined_350.jsonl` | 7 (turn) | flush / 9 | YES (Ad on Jd7dKh2c, nut FD on two-tone-d) | 2 / 2 | OK (street 'turn'→1, hero_position 'BTN'→3) | `v23_curated_draw_turn.jsonl` |
| 2 | `BP7_06` | `training-data/factory_batch5_situations.jsonl` | 7 (turn) | flush / 9 | YES (Ah on Qh9d5h7c, nut FD) | 2 / 2 | OK (already numeric: street=1, hero_position=2) | `v23_curated_draw_turn.jsonl` |
| 3 | `d5620_BTN_flop` | `training-data/3way_combined_350.jsonl` | 6 (flop) | straight / 8 | LIKELY (AdQs broadway draw, A-blocker, on JsKsKd) | 2 / 2 | OK (street 'flop'→0, hero_position 'BTN'→3) | `v23_curated_draw_flop.jsonl` |

Label-stripping verified: no record carries `expert_action`, `action`,
`oracle_action`, `adjusted_action`, `expert_confidence`,
`expert_reasoning`, `difficulty`, `key_factors`, `factor_conflicts`,
`alternatives_considered`, or `label_source`. Labels will be assigned
by Phase 4 production labelling.

## Deliverable status

| Artefact | State |
|---|---|
| `training-data/v23_curated_draw_flop.jsonl` | DELIVERED (1 record: `d5620_BTN_flop`) |
| `training-data/v23_curated_draw_turn.jsonl` | DELIVERED (2 records: `d1983_BTN_turn`, `BP7_06`) |
| `review/comms/PHASE_1_4_CURATED_DELIVERY_2026-04-16.md` | THIS FILE |
| `review/comms/TICKET_PA_BOARD_POOL_DEFECT_2026-04-16.md` | Cleanup ticket — post-v2.3-ship backlog |
| Commit / push | Pending (Task 1 commit follows this delivery update) |

## PA_Board3 disposition

Dropped per owner directive. PA_Board* pool has systemic defects:
- `street='f'|'t'|'r'` (single char) instead of full `'flop'|'turn'|'river'`
- `num_opponents` set to table size, not villain count
  (e.g. `num_opponents=2` with `villain_positions=['CO']`)

Patching one record does not fix the pool and would create undocumented
drift. Cleanup tracked in
`review/comms/TICKET_PA_BOARD_POOL_DEFECT_2026-04-16.md` (record-keeping
only; not a work item for this sprint).

## Net supplement math (final)

Build plan §1.2 original rows 6+7 target: **25** curated hands.
MAIN_TERMINAL_UPDATE-e decision: accept 4 confirmed, umbrella absorbs rest.
MAIN_TERMINAL_UPDATE-f decision: accept 3 confirmed (PA_Board3 dropped).

- Phase 1 supplement generated: 483 (factory) + 3 (curated) = **486**
- Phase 1 supplement net (post-dedupe): 385 (factory net) + 3 (curated)
  = **388** (vs MAIN_TERMINAL_UPDATE-e target of 389; Δ −1 hand, ~0.25%).
- Overall v2.3 supplement target: 420 net → **398 net** (Δ −22, ~5%).
  Same order of magnitude as owner's −5% class-balance acceptance window.

## Build plan §1.2 update (rows 6-7)

Per MAIN_TERMINAL_UPDATE-f §1: "3 confirmed nut-blocker curated hands
staged; `PA_Board3_Jh8h4h_h6` dropped per PA_Board* upstream defect
(see TICKET_PA_BOARD_POOL_DEFECT_2026-04-16). UMBRELLA absorbs predicate
coverage."

## Sequencing

Phase 3 calibration gate is now unblocked: 483 factory + 3 curated =
486 Phase 1 hands available for Phase 2 assembly QA (already PASS) and
Phase 3 calibration gate launch.
