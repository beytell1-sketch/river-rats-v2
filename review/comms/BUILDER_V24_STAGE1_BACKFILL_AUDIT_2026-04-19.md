---
date: 2026-04-19
from: Builder
to: Main terminal / Owner
re: v2.4 P1 Stage 1 — backfill audit of new blocker features on existing training rows
status: AUDIT COMPLETE — results feed Stage 4 re-labelling scope
---

# v2.4 P1 Stage 1 — Backfill Audit

Computed `nut_flush_block` on all 579 training rows that have
hero + board cards accessible. `flush_draw_block_pct`,
`straight_draw_block_pct`, `nut_made_block_pct` require villain range
data which is reconstructed at feature-extraction time — these land in
Stage 4 when full re-extraction runs against the v3.2-labelled set.

## Row sources

```
{
  "pass1_final_labels_v23.jsonl": 468,
  "v23_air_check_3way_labelled.jsonl": 40,
  "v23_2_value_bet_3way_labelled.jsonl": 39,
  "pass1_final_labels_v23_call.jsonl": 32
}
```

## Distribution — `nut_flush_block`

```
Total rows: 579
nut_flush_block = 1:  65  (11.2%)
nut_flush_block = 0:  514  (88.8%)
```

## Sanity checks

```
nut_flush_block violations: 0
```

All sanity checks PASS.

## I1 ask (defensive bucket)

**Finding: the reviewer's literal predicate (`flush_draw_rank == 0
AND nut_flush_block == 1`) is empty by feature construction.**
`nut_flush_block = 1` requires hero to hold A-of-flush-suit, which
forces `flush_draw_rank = 14` for that suit (flush_draw_rank is
defined as hero's highest rank in the flush suit, returning 0 only
when hero holds 0 cards of the suit). So the literal conjunction is
always 0.

Re-interpreting per reviewer intent (hero has A-blocker but does NOT
have a flush draw — i.e., hero+board < 4 of suit):

```
nut_flush_block == 1 AND has_flush_draw == 0
Count: 36 / 579 = 6.22%
Threshold: 2.0%
Status: OK — above threshold. Defensive-bucket signal IS present in
existing training data.
```

Literal predicate preserved for reference:

```
flush_draw_rank == 0 AND nut_flush_block == 1
Count: 0 / 579 = 0.00%
(Empty by feature construction.)
```

**Flag to reviewer:** I1 ask wording should be updated to
`has_flush_draw == 0` (not `flush_draw_rank == 0`) for future
distribution checks on defensive-blocker coverage. The spirit of
the check is satisfied.

## Stage 1 completion

- [x] Revised plans committed (via BUILDER_V24_P1_SPEC_LOCKED + mods captured)
- [x] `blocker_features.py` implemented (4 features)
- [x] `feature_keys.py` + `feature_extractor.py` wired
- [x] 17 unit tests pass
- [x] v2.3.1 calibration-anchor gate still passes 5/5 (backward compat)
- [x] Backfill audit on `nut_flush_block` — distribution + sanity + I1 check

## Stage 2 preview

Next cycle opens KB §1.9 update: documenting defensive blocker direction
for v3.2 prompt feature_attention guidance. Reference existing
`feedback_concentration_effect.md` + `feedback_counter_example_balance.md`
memories.
