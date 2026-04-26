---
date: 2026-04-26
from: V-X2 partial-fold lookup agent (orchestrator-dispatched)
to: Main terminal (orchestrator)
re: Phase A.5 fixture source verification — do existing v2.3 calibration constants contain partial-fold MW fixtures?
status: LOOKUP
---

# V-X2 Phase A.5 fixture source — partial-fold content check

## Summary

NONE of the 12 hands referenced by `GROUP_D_REVERSAL_HANDS` (5 hands) and the
non-Group-D members of `GTO_REVERSAL_HANDS` (`MW-30`, `MW-33`, `MW-50`,
`d2410_CO_turn`, `d3178_CO_river`) carry explicit "fold" entries in a
`prior_actions` field that `_villain_pos_raw` could be tested against. The
9 d-prefixed canonical JSONL records use a hero-only `prior_actions` schema
(zero "fold" tokens across the entire 401-record canonical pool), and the
3 MW-NN hands have no JSONL record at all — their action history lives only
as prose in `BATCH2_8_HAND_DESIGNS.md`. Eight of those MW prose blocks do
narrate a villain folding (4-way preflop → 3-way postflop), but it is
unstructured text, not a `prior_actions` list entry that `_villain_pos_raw`
selection logic can consume.

## Per-hand results

| situation_id     | num_opponents | has_fold_in_prior_actions | action_sequence_summary |
|------------------|---------------|---------------------------|-------------------------|
| d3688_BB_flop    | 2             | no                        | `prior_actions=['preflop: BB call']` (hero-only); villain_positions=[HJ, BTN]; flop, no facing bet |
| d4312_CO_turn    | 2             | no                        | `prior_actions=['preflop: CO raise', 'flop: CO check']` (hero-only); villain_positions=[BTN, BB]; turn |
| d9556_BB_flop    | 2             | no                        | `prior_actions=['preflop: BB call']` (hero-only); villain_positions=[UTG, BTN]; flop |
| d2074_BTN_turn   | 2             | no                        | `prior_actions=['preflop: BTN call', 'flop: BTN check']` (hero-only); villain_positions=[HJ, BB]; turn |
| d5466_CO_flop    | 2             | no                        | `prior_actions=['preflop: CO raise']` (hero-only); villain_positions=[BTN, BB]; flop |
| d2410_CO_turn    | 2             | no                        | `prior_actions=['preflop: CO raise', 'flop: CO check']` (hero-only); villain_positions=[BTN, BB]; turn (predicate-matching anchor: villain_checked_back=1) |
| d3178_CO_river   | 2             | no                        | `prior_actions=['preflop: CO raise', 'flop: CO check', 'turn: CO check']` (hero-only); villain_positions=[BTN, BB]; river |
| MW-30            | 2             | n/a (no JSONL record)     | Prose only in BATCH2_8_HAND_DESIGNS.md: "CO opens, BTN calls, SB calls, BB (hero) calls. Flop KJ6r: CO bets 35, BTN calls, **SB folds**. Hero faces bet+call." Started 4-way preflop, SB folds on flop → 3-way live |
| MW-33            | 2             | n/a (no JSONL record)     | Prose only: "CO opens, BTN calls, SB calls, BB (hero) calls. Flop 873r: CO bets 40, BTN calls, **SB folds**. Hero facing bet+call with set." 4-way preflop → 3-way live (SB folded flop) |
| MW-50            | 2             | n/a (no JSONL record)     | Prose only: "CO opens, BTN calls, SB calls, BB (hero) calls. Flop J84r: CO bets, BTN raises, **SB folds**, BB calls. Turn 5: CO calls. BTN bets 90 into 220." 4-way preflop → 3-way live, multi-street with one fold |

### Schema confirmation
- Across the entire canonical labelled JSONL pool (`test_set_50_labelled.jsonl`
  + `3way_combined_350.jsonl`, 401 records total), `prior_actions` contains
  zero "fold" tokens. The schema is hero-only.
- `villain_positions` always lists 2 live opponents (consistent with the
  "live 3-way only" pool description for `3way_situations_10k.jsonl`).
- MW-30/33/50 have no JSONL representation; they enter the calibration exam
  via `_parse_action_history_prose()` parsing of the markdown design file
  (`river-rats-core/calibration_exam.py:114-128`).

## Recommendation for orchestrator

**Recommend Build D (synthetic partial-fold fixture file).** The existing
v2.3 calibration constants do not provide any usable partial-fold MW
fixtures for Phase A.5 because:

1. **d-prefixed hands carry hero-only `prior_actions`** — even where a
   preflop fold mathematically must have occurred to reach a 3-way live
   postflop spot from a 4-way+ pool, the JSONL records do not encode
   villain fold entries. Pointing `_villain_pos_raw` at these hands
   exercises the live-2-villain selection path, NOT the partial-fold
   live-vs-folded discrimination path the test is meant to cover.
2. **MW-30/33/50 have no JSONL `prior_actions` at all** — only markdown
   prose. They cannot serve as a `_villain_pos_raw` test fixture without
   first being lifted into a structured schema.
3. **The canonical pool is uniformly fold-free in `prior_actions`** — 0
   fold entries across 401 records. There is no nearby corpus to mine.

A purpose-built 5-hand synthetic fixture file (Build D) is the cleanest
path: each hand carries a `prior_actions` list with one explicit "fold"
entry (some `<position>: fold`) plus at least one still-live villain in
`villain_positions`, designed specifically so the test asserts
`_villain_pos_raw` selects a live opponent, not the folded one.

If the orchestrator wants to AVOID a new synthetic file, the only
alternative is to retrofit `prior_actions` on MW-30/33/50 by parsing the
existing markdown prose (which already narrates a fold). But this is a
schema migration touching the prose-parser and the MW reference loader —
larger surface area than 5 synthetic fixtures, and it would tangle Phase
A.5 with a refactor of the MW ingestion path.

### Files inspected
- `/home/rupertbeytell/river-rats-v2/river-rats-core/calibration_exam.py` (constants definitions, lines 73-97; canonical-record loader lines 138-156)
- `/home/rupertbeytell/river-rats-v2/training-data/test_set_50_labelled.jsonl` (4 of 9 d-prefixed hands)
- `/home/rupertbeytell/river-rats-v2/training-data/3way_combined_350.jsonl` (5 of 9 d-prefixed hands)
- `/home/rupertbeytell/river-rats-v2/design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` (MW-30 lines 404-432, MW-33 lines 484-502, MW-50 lines 849-867)
