---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Direction after Tier 1 — Track 2 authorised, Track 3.5 awaiting owner decision
status: DIRECTIVE
supersedes: n/a (adds to MAIN_TERMINAL_UPDATE_2026-04-15.md)
---

# Main Terminal Update — 2026-04-15 (b)

Companion to `REVIEW_TIER1_COMPLETE_2026-04-15.md`. Read that
first for the full review.

## Launch Track 2 now

Authorised. Do not wait further.

Scope per the original directive:
1. Run the Track 1 hardened harness on FB-40. Confirm or
   contradict 72.5% (29/40).
2. Run the hardened harness on MW-50. Confirm or contradict
   80.0% (40/50), including the d2920-in / d4534-out one-hand
   swap from the HRP re-extraction.
3. Per-hand comparison: old vs new harness prediction. Flag any
   hand whose prediction changes.

### Additional ask (not in the original directive)

While you're in the harness code: check whether the hardened
guard rejects string-where-numeric-expected on `street` /
`hero_position`. It probably doesn't (guard was designed for
missing keys, not wrong dtypes). If the FB-40 / MW-50 test
hands don't surface this because their own feat_dicts are
clean, that's fine — but please **add an explicit dtype check
to the guard** as a second-layer defence. Tiny addition, closes
the ANOMALY-A class of error at eval time.

Deliverable: `review/comms/EVAL_RERUN_HARDENED_2026-04-15.md`.

## Track 3.5 — awaiting owner decision

Three options summarised in the review. My recommendation
(Option 3 — hybrid) includes a quick feature-importance
cross-check on `street` / `hero_position` from
`v2_2_training_report.json`, **before** committing to
recover/rewrite the v2.2 trainer. That's a cheap call (~30 min)
and could collapse the ambiguity without labour.

**If owner selects Option 3, you may proceed with the
feature-importance cross-check without further direction** —
it is analysis only (no code changes, no model retraining).
Deliverable: `review/comms/V22_FEATURE_IMPORTANCE_XCHECK_2026-04-15.md`.

Otherwise hold Track 4 and Track 6 pending owner's call.

## Track 5 — accepted, minor follow-ups logged

- batch2 blueprint divergence: not worth a separate call unless
  v2.3 sources a hand from it. Log only.
- 11 preexisting pytest failures: not your fix. Log for
  future cleanup track.

## Commit discipline

Ongoing push protocol is working. Keep it up: one commit per
deliverable, push immediately.

## What I'm watching

- Track 2 deliverable
- Owner Track 3.5 decision
- Solver results (owner)
