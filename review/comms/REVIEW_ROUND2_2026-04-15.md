---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Owner + Builder
re: Review of Round 2 deliverables (cross-check, Track 2, Fix 1, Track 4 prep, batch2)
status: REVIEW — all four deliverables accepted; trainer/eval rewrite proceeds
---

# Round 2 Review

## Acceptance summary

| Deliverable | Verdict |
|---|---|
| Track 3.5 cross-check | ACCEPT — Branch C → B call is correct per directive |
| Track 2 dtype guard | ACCEPT — clean test-first, 16/16 |
| Track 2 eval run | CORRECTLY BLOCKED — stop-protocol honored |
| Fix 1 BP generators | ACCEPT — good discipline on the in-place regeneration vs full generator run |
| Track 4 prep | ACCEPT — 10 MW-miss hands extracted with full features |
| Batch2 disposition | ACCEPT — out of scope, justified |

## Cross-check numbers — context

`street` rank 20/108 triggers Branch B per directive, and that is the call
we honour. But the full picture reads **less alarming** than a bare "rank
20" suggests:

- Combined `street` + `hero_position` gain share: **1.26%** of total —
  well under even the Branch A 5% threshold.
- `attn_street` / `attn_hero_position` gain: **zero each**. The model
  never split on the attention-gated versions. If ANOMALY-A at path 5
  (silent-zero) had caused the model to learn a corrupted street signal,
  we would expect the attention mirror to have absorbed some gain too.
  It didn't.
- `street` has 95 splits at 0.0075 gain-per-split — coarse partitioning
  feature, not high-signal. Top-10 features range from 0.004 to 0.164
  gain-per-split; `street` sits at the low end of that range.
- Top-10 distribution is healthy (equity_margin 15%, attn_pot_odds 13%,
  facing_bet 9.8%, etc.). Usual suspects at the top — no signs of the
  model leaning on a mis-encoded column.

Interpretation: the loader path is most likely path 2 (NaN-as-missing)
or path 3 (proper mapping), not path 5 (silent-zero). But this remains
indirect — the trainer recovery is the direct answer.

## Track 2 eval BLOCKED call — the right move

Builder correctly refused to improvise a 108-feature inference wrapper
with `attn_*=1` + legal-action masking to produce numbers that would
"compete" with the 72.5% / 80.0% baseline. Writing a new eval path and
publishing results from it would have muddied Gate 7. Stop-protocol
honored.

## Fix 1 caveats — logged, not blocking

Three caveats flagged by builder:
1. `v2_2_training.csv` left corrupted per directive — correct.
2. `hand_sequence_validator` strictness + batch4 count mismatch prevent
   full `generate_all()` runs. Pre-existing, not introduced by Fix 1.
3. Hardcoded `/home/rupertbeytell/...` paths replaced with
   `__file__`-relative derivations. Good cleanup. This is the kind of
   portability fix that should land alongside the primary work — no
   objection.

## Decision

**Builder executes the v2.2 trainer + 108-feature eval rewrite now.**
Does not wait. Does not need owner action to start.

Reasoning in MAIN_TERMINAL_UPDATE_2026-04-15-d.md.
