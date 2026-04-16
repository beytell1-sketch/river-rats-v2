---
date: 2026-04-16
from: Programmer (Track D, Phase 1.4)
to: v2.3 backlog (post-ship cleanup)
re: PA_Board* upstream pool serialisation defect
status: TICKET (record-keeping; not a current sprint work item)
references:
  - review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-f.md §1 (cleanup ticket directive)
  - review/comms/PHASE_1_4_CURATED_DELIVERY_2026-04-16.md (PA_Board3 disposition)
  - review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md (sibling Fix 1)
  - river-rats-core/situation_factory.py:85-119 (normalise_situation guard)
  - river-rats-core/situation_factory.py:377-388 (Fix 1 num_opponents validator)
priority: post-v2.3-ship cleanup, unless another v2.3 track needs PA_Board* data
owner: unassigned (no current blockee)
---

# PA_Board* Pool Defect — Cleanup Ticket

## Defect

The PA_Board* records in `training-data/3way_combined_350.jsonl` exhibit
two systemic serialisation issues:

1. **`street` is a single-char encoding** (`'f'` / `'t'` / `'r'`) instead
   of the canonical full-string (`'flop'` / `'turn'` / `'river'`) or
   integer (`0` / `1` / `2`) encoding accepted by
   `situation_factory.normalise_situation()`.
   - `normalise_situation` raises `KeyError: unknown street string 'f'`
     to fail loudly rather than silently coerce (ANOMALY-A guardrail).

2. **`num_opponents` encodes the table size, not the villain count.**
   E.g. `num_opponents=2` paired with `villain_positions=['CO']` (length
   1). This trips the Fix-1 validator at
   `situation_factory.py:377-388`:
   `len(spec.villain_positions) < num_opponents_declared` →
   `ValueError`.

## Scope

All 79 PA_Board* records in `training-data/3way_combined_350.jsonl`
exhibit BOTH defects:

```
PA_Board* total records: 79
  street single-char: 79
  num_opponents > len(villain_positions): 79
```

Sample (first 5):
```
PA_Board1_Ac8d3s_h1: street='f', num_opponents=2, villain_positions=['CO']
PA_Board1_Ac8d3s_h2: street='f', num_opponents=2, villain_positions=['CO']
PA_Board1_Ac8d3s_h3: street='f', num_opponents=2, villain_positions=['CO']
PA_Board1_Ac8d3s_h4: street='f', num_opponents=2, villain_positions=['CO']
PA_Board1_Ac8d3s_h5: street='f', num_opponents=2, villain_positions=['CO']
```

The intended semantics on each record's `num_opponents` is unclear
without re-running the source generator: it could mean "table size
including hero" (= 1 villain truly active, hero + villain) OR "intended
3-way pot but villain-position list dropped a seat at serialisation."
Disambiguation is part of the fix.

## Fix target

Normalise at the serialisation boundary, mirroring Fix 1 from the BP
generator diagnosis:

1. Identify the upstream PA_Board* generator (likely a `prepare_*` /
   `generate_*` script in `review/` or `river-rats-core/`; not searched
   in this ticket's scope).
2. Audit whether `num_opponents` semantics is "table size" or "villain
   count" — fix the generator to emit the canonical "villain count"
   semantics (consistent with d-series and BP-series).
3. Pipe every record through `normalise_situation()` before
   `json.dumps`, so `street` becomes integer (`0` / `1` / `2`).
4. Re-extract the affected pool. Diff old vs new on the 79 records to
   confirm only the two fields changed.
5. Add a regression test under
   `river-rats-core/tests/test_pa_board_serialisation.py` (new file,
   one-shot) that round-trips a PA_Board* record through
   `normalise_situation` + `build_situation` and asserts no exceptions.

## Impact / blast radius

- v2.2 training: PA_Board* records were ingested via the existing
  `3way_combined_350.jsonl` pipeline. Whether v2.2 actually trained on
  them depends on the assemble script's filtering — if it dropped
  records that failed the validator, v2.2 has lost those 79 hands. If
  it passed validation under an older lax codepath, v2.2 may have
  trained on records with `num_opponents=2` but only one true villain,
  potentially mislabelling the seat semantics.
- v2.3: The single PA_Board3 candidate that surfaced as a curated
  row-6 nut-blocker hand was DROPPED. v2.3 supplement is unaffected
  (umbrella absorbs predicate coverage).
- v2.4+: Any future track that wants to surface PA_Board* curated
  candidates needs the fix landed first.

## Priority

**Post-v2.3-ship cleanup** unless another v2.3 track surfaces a need
for PA_Board* data. Currently no track depends on this. Track D
(curated nut-blocker) was the only prospective consumer and has been
re-scoped to 3 hands without PA_Board3.

## Owner

Unassigned. Log against the v2.3 backlog. When the next person picks
this up, they should:

1. Read `BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md` Fix 1 first —
   identical pattern, identical fix shape.
2. Identify the PA_Board* generator (file search for `'PA_Board'` in
   `river-rats-core/` and `review/`).
3. Apply the two-field fix and regenerate.
4. Diff old vs new pool, push regenerated `3way_combined_350.jsonl`
   (or a v2 of it).
5. Close this ticket.
