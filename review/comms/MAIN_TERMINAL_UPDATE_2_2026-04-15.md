---
date: 2026-04-15
from: Main terminal
to: Builder terminal
re: Response to BUILDER_STATUS_2026-04-15.md — approvals, direction, Track 2 GO
status: DIRECTIVE
---

# Main Terminal Update #2 — Response to Builder Status

Builder, thanks for the clean Track 3.5 work and honest
BLOCKED-ambiguity report. Reviewed. Here's direction.

## Track 3.5 — Owner deliberating, partial proceed authorised

Full owner response is being drafted at
`review/comms/OWNER_UPDATE_TRACK35_BLOCKED_2026-04-15.md` —
owner needs to check local machines for the v2.2 training
script and decide on the training-impact verdict.

**In the meantime, you are authorised to:**

1. **Apply Fix 1 to BP generators** — normalise `street` and
   `hero_pos` at serialisation boundary. Use the `normalise_situation`
   helper from your report (§4 Fix 1 option a). Apply to all 5
   generators under `review/generate_factory_*.py`.

2. **Regenerate affected JSONLs** with the fix. Target:
   `training-data/factory_batch*_situations.jsonl` updated in
   place so the pre-training schema test passes.

3. **Do NOT regenerate `v2_2_training.csv`** — leave the current
   corrupted CSV alone for now. It's the evidence of the
   ANOMALY-A. Owner may want to keep it for comparison. Fix
   propagates forward (to any v2.3 assembly), not backward.

4. **Do NOT retrain v2.2.** Gate 7 is still owner's decision.

5. **Pytest schema test is now a pre-flight gate** — wire
   `test_training_data_encoding.py` so it must pass before any
   future training script runs. This protects v2.3.

Owner will make the separate decision on recovering the v2.2
trainer and the Gate 7 ship question. Your job for now is to
fix the upstream generators so v2.3 starts from clean data
regardless of how the v2.2 question resolves.

## Track 5 — Confirmed no-op, thank you

Line-by-line verification against blueprint + regression test
passing is exactly the right approach. Batch2 line drift: you
were correct to stop. Architecture Expert should either confirm
batch2 needs a separate fix spec OR explicitly mark it as
out-of-scope for v2.3 (since batch2 hasn't contributed new
situations recently).

**Action:** Architecture Expert produces a 1-paragraph
disposition: "batch2 needs X" or "batch2 is out of scope
because Y." Commit to `review/comms/BATCH2_DISPOSITION_2026-04-15.md`.
If the conclusion is "out of scope," we're done with Track 5
entirely.

## Track 2 — GO

**Launch now.** Don't wait for additional approval. The
protocol does allow proactive execution when the work is
owner-preapproved and not blocked.

Run FB-40 and MW-50 through the hardened harness from Track 1.
Expected outcomes:

- FB-40: 72.5% should stand (29/40 hands)
- MW-50: 80.0% should stand (40/50 hands, same miss set as
  prior — 1 swap from d2920 / d4534)

**Watch for:**

- Any accuracy delta > 0 on either test set means the hardened
  harness changed behaviour — flag it
- Any hand that changes prediction vs the earlier report should
  be documented in the per-hand comparison

**Deliverable:** `review/comms/EVAL_RERUN_HARDENED_2026-04-15.md`
with per-hand comparison and verdict (stand vs changed).

## Track 4 — Stay HELD

Builder is correct to hold. Track 4's bias diagnosis depends
on knowing whether the model saw corrupt features. Until owner
decides on Track 3.5 training-impact verdict, don't start
Track 4.

**Exception:** you CAN do a "feature extraction prep" pre-pass
— re-extract features for all 10 MW misses using
`extract_all_features()` and stage them for Track 4 analysis.
This is data prep, not analysis. When Track 4 is unblocked,
the data is ready.

## Track 6 — Stay HELD

Correct. Depends on Track 4 output.

## Summary of what to do now

| Action | When |
|---|---|
| Apply Fix 1 to BP generators (normalise at serialisation) | Start now |
| Regenerate `factory_batch*_situations.jsonl` | After Fix 1 |
| Re-run pytest schema test — must pass | After regeneration |
| Architecture Expert batch2 disposition | Start now (parallel) |
| Launch Track 2 (FB-40 / MW-50 re-eval) | Start now (parallel) |
| Feature extraction prep for Track 4 hands | Start now (parallel) |
| Commit and push after EACH deliverable | Always |

## Commit discipline reminder

You've been doing this right since the restart — keep it up.
Push after every commit. Don't batch. Prior session's pattern
of local-only commits caused recovery work.

## Communication checks

I'll write any further direction to:
`review/comms/MAIN_TERMINAL_UPDATE_<N>_<date>.md`

You keep writing status to:
`review/comms/BUILDER_STATUS_<date>.md` (update in place for
same-day status, OR new file per day)

Deliverables go to topically-named files.

---

**Builder: proceed with the 6 actions above. Report progress
when each deliverable lands. Owner is deliberating Track 3.5
training-impact verdict in parallel; separate update to
follow.**
