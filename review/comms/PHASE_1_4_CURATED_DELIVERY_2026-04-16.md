---
date: 2026-04-16
from: Programmer (Track D, Phase 1.4)
to: Main terminal (reviewer/orchestrator)
re: Track D curated nut-blocker staging — BLOCKED on 1 of 4 candidates (stop condition tripped)
status: BLOCKED
directive: review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-e.md §1 (commit 10247b6)
---

# Phase 1.4 Curated Nut-Blocker Staging — BLOCKED

## Summary

Of the 4 owner-accepted nut-blocker candidates, **3 pass pre-flight
validation and 1 fails two independent stop conditions**. Per the task
spec:

> - If `normalise_situation` round-trip fails on any record — STOP
>   (would be a Fix 1 regression).
> - If a record's `num_opponents` doesn't match `len(villain_positions)`
>   — STOP (would fail the Phase 1 validator on copy).

The failing hand is `PA_Board3_Jh8h4h_h6`. No staging files were
written; no commit is pending. The task is BLOCKED on owner direction
for how to resolve this one candidate before any curated row 6/7
JSONLs can ship.

## Per-hand pre-flight

All 4 records were located in their expected source pools.

| # | sid | Source pool | Street (row) | Draw | Blocker | num_opp / len(villain_positions) | normalise_situation | Verdict |
|---|-----|-------------|--------------|------|---------|----------------------------------|---------------------|---------|
| 1 | `d1983_BTN_turn` | `training-data/3way_combined_350.jsonl` | turn (row 7) | flush / 9 | YES (Ad on Jd7dKh2c, Ace-d on two-tone-d) | 2 / 2 ✅ | OK (street='turn'→1, hero_position='BTN'→3) | READY |
| 2 | `PA_Board3_Jh8h4h_h6` | `training-data/3way_combined_350.jsonl` | flop (row 6) | flush / 9 | YES (Ah on Jh8h4h monotone-h) | 2 / 1 ❌ | FAIL: `KeyError: unknown street string 'f'` | **BLOCKED (2 conditions)** |
| 3 | `BP7_06` | `training-data/factory_batch5_situations.jsonl` | turn (row 7) | flush / 9 | YES (Ah on Qh9d5h7c, nut FD) | 2 / 2 ✅ | OK (already numeric: street=1, hero_position=2) | READY |
| 4 | `d5620_BTN_flop` | `training-data/3way_combined_350.jsonl` | flop (row 6) | straight / 8 | LIKELY (AdQs nut broadway draw, A-blocker) | 2 / 2 ✅ | OK (street='flop'→0, hero_position='BTN'→3) | READY |

## Why PA_Board3_Jh8h4h_h6 fails

Two independent stop-condition trips on the source-pool record:

### Trip 1: `normalise_situation` round-trip fails

The source record encodes `street: 'f'` (single character) at the
top level. `normalise_situation()` in
`river-rats-core/situation_factory.py:85-119` only accepts the full
strings `{'flop','turn','river'}` or canonical integers; it raises
`KeyError` on anything else to fail loudly rather than silently
coerce (ANOMALY-A guardrail, Fix 1).

```
KeyError: normalise_situation: unknown street string 'f';
          expected one of ['flop', 'river', 'turn']
```

Note: the record *also* carries `feat_dict.street = 0` (numeric,
correct), but `normalise_situation` reads the top-level `street`
field, not `feat_dict.street`.

### Trip 2: `num_opponents` vs `len(villain_positions)` mismatch

The record has `num_opponents: 2` but `villain_positions: ['CO']`
(length 1). This trips the validator in
`river-rats-core/situation_factory.py:377-388`:

```python
if len(spec.villain_positions) < num_opponents_declared:
    raise ValueError(
        f"villain_positions has {len(spec.villain_positions)} seats "
        f"but num_opponents={num_opponents_declared}. ..."
    )
```

1 < 2 → `ValueError` at `build_situation()` time.

### Upstream pattern

I spot-checked the PA family in `3way_combined_350.jsonl`: **all 30+
PA_Board* records exhibit the same encoding** (`num_opponents=2`,
single-villain `villain_positions`). It looks like the PA-series pool
emitted `num_opponents` as total players at the table (hero+villains)
rather than number of villains. The Phase 1.4 candidate filter
predicate (`num_opponents == 2  # i.e. 3-way pot (hero + 2 villains)`)
admitted these records on the field value, even though the seat list
says otherwise. Candidate doc line 183 acknowledges the 1-villain
seat list but still tagged the row as "row 6 (flop)" under the 3-way
filter.

This is an upstream data-consistency issue, not a downstream
programmer error — but it cannot be resolved by mutating the source
pool (task constraint: "Do NOT modify source JSONLs").

## What was NOT done

- **No JSONLs staged.** `training-data/v23_curated_draw_flop.jsonl`
  and `training-data/v23_curated_draw_turn.jsonl` were not written.
  The task deliverable is "4 hands"; producing a 3-hand artefact
  unilaterally would be scope drift (the same anti-pattern the
  directive flagged for widening and factory-generating).
- **No commit, no push.** Nothing to push until the full 4-hand set
  is validated or owner re-scopes.
- **No substitution.** Per stop condition: "STOP, report (don't
  substitute another hand)."

## Options for owner decision

1. **Drop PA_Board3 to 3 curated hands.** Scale rows 6+7 from 4 → 3.
   Supplement total 420 → 398 (vs −21 originally). Umbrella still
   absorbs the residual coverage per MAIN_TERMINAL_UPDATE-e §1.
   Programmer stages `d5620_BTN_flop`, `d1983_BTN_turn`, `BP7_06`
   on next directive.
2. **Accept a PA_Board3 fixup.** Owner authorises a one-line
   correction on the copy (not the source): set `street='flop'`
   and either drop `num_opponents` to 1 or patch
   `villain_positions` with the intended second villain. The source
   pool remains untouched. This is a Programmer edit on a curated
   copy, not a source-pool mutation — but it reaches into the
   semantic meaning of the record (2-way vs 3-way pot) and should
   be owner-signed-off before execution.
3. **Substitute from the remaining 12 NO-blocker candidates** in
   `V23_CURATED_CANDIDATES_2026-04-16.md`. The directive explicitly
   forbade widening the filter, so this would require an owner
   override — not recommended.

Recommendation: Option 1 (drop to 3). Cleanest. The PA encoding
problem is systemic (30+ PA records with the same shape) so a
case-by-case fixup on one hand sets a bad precedent. Umbrella
absorbs the residual coverage and the Phase 7 backup clause remains
available if a drawing-signal gap surfaces.

## Backup clause

Per MAIN_TERMINAL_UPDATE-e §1 Phase 7 backup: if Phase 7 validation
surfaces an identifiable drawing-signal gap (v2.3 regresses on
semi-bluff BET while improving on made-hand BET), a factory
sub-pattern in `generate_factory_batch6.py` can be added targeting
nut-blocker semi-bluff shape. Noted — not triggered now.

## Net supplement math (if owner picks Option 1)

Build plan §1.2 original rows 6+7 target: **25** curated hands.
MAIN_TERMINAL_UPDATE-e decision: accept 4 confirmed, umbrella
absorbs rest.
If PA_Board3 is dropped: **3** curated hands land.

- Phase 1 supplement generated: 483 (factory) + 3 (curated) = **486**
- Phase 1 supplement net (post-dedupe): 385 (factory net) + 3 (curated)
  = **388** (vs the MAIN_TERMINAL_UPDATE-e target of 389, and the
  build-plan original of 410 net).
- Delta from target: −1 hand (~0.25%). Negligible class-balance
  impact, same order as the owner's −5% acceptance.

## Deliverable status

| Artefact | State |
|---|---|
| `training-data/v23_curated_draw_flop.jsonl` | NOT WRITTEN (blocked) |
| `training-data/v23_curated_draw_turn.jsonl` | NOT WRITTEN (blocked) |
| `review/comms/PHASE_1_4_CURATED_DELIVERY_2026-04-16.md` | THIS FILE |
| Commit / push | Pending owner direction |

## Next programmer action

Await owner direction on the 3 options above. On option-1 approval
I can stage the 3 ready hands, update the supplement math in the
build plan, and push in a single commit within ~5 min.
