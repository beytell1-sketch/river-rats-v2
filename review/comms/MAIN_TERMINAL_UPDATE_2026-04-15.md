---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder terminal (restart)
re: Status + next actions — read this after SESSION_STATE_2026-04-15.md
status: DIRECTIVE — read and execute
---

# Main Terminal Update — 2026-04-15

## Purpose of this file

You cannot talk to me directly. This file is how I communicate
with you. Read it after `SESSION_STATE_2026-04-15.md`. It
contains:

1. What the prior builder session completed (and I recovered)
2. A new critical finding that reshapes priorities
3. Next actions in order

Check this folder regularly:
`review/comms/MAIN_TERMINAL_UPDATE_*.md` — I may write newer
updates.

---

## 1. Tracks 1 and 3 are committed

The prior builder session completed Track 1 and Track 3 but
stopped responding before committing. Main terminal recovered
and committed both:

- **Commit b5d84b5:** Track 1 harness hardening
  (`gto_model.py`, `reference_evaluator.py`,
  `tests/test_harness_feature_completeness.py`)
  - All 12 tests pass
  - `features_from_dict()` now raises `KeyError` on missing
    features — no more silent zeros
  - `_validate_feat_dict()` guard at evaluation boundary

- **Commit 8e77e05:** Track 3 training data audit
  (`review/comms/TRAINING_DATA_AUDIT_2026-04-15.md`)

**You do NOT need to redo Track 1 or Track 3.**

## 2. CRITICAL FINDING from Track 3: ANOMALY-A

The audit found that `street` is encoded inconsistently in
`training-data/v2_2_training.csv`:

- 52% of rows (200/385): float encoding (0/1/2)
- 48% of rows (185/385): string encoding ('flop'/'turn'/'river')

**If the v2.2 training pipeline coerced all values to float,
the 185 string rows were read as 0 (flop) regardless of their
actual street.** This would have corrupted the street feature
across half the training data.

This is a **bigger deal than the HRP test-harness bug.** HRP
was a test-time issue. ANOMALY-A, if confirmed, is a
TRAINING-time issue that affected the model itself.

Possible consequences if ANOMALY-A corrupted training:
- v2.2 model has fuzzy street understanding
- Part of the MW miss could be street confusion, not bucket-first bias
- Track 4 bias deep-dive may need to redo analysis with street
  corrected
- v2.3 supplement generation must confirm encoding consistency

## 3. NEW PRIORITY TRACK — before Track 4 proceeds

### Track 3.5: ANOMALY-A verification (NEW, BLOCKING)

**Who:** ML Architect (verify) + Programmer (test)

**What:**
1. Read `river-rats-core/train_model.py` (or wherever v2.2
   training actually ran) and determine how `street` is
   handled:
   - Is it cast to float? If yes, string rows → 0 silently
   - Is it one-hot encoded? If yes, string rows may be dropped
     or treated as a new category
   - Is it left as-is? If yes, pandas may have rejected strings
2. Check the ACTUAL training logs / feature matrix that was
   fed to XGBoost. Was `street` numeric throughout? Did
   string-encoded rows get reclassified, zeroed, or silently
   coerced?
3. Write a test that asserts training data has a consistent
   street encoding before training. Test-first, then fix
   upstream.

**Deliverables:**
- `review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md`
  - Root cause: which pipeline stage produced the mixed encoding
  - Training impact: did v2.2 train on correct or corrupted
    street values?
  - Scope of damage: if corrupted, how many predictions are
    affected?
  - Fix plan: how to prevent recurrence

**Constraint:**
- Do NOT retrain v2.2 yet — Gate 7 is still owner's decision
- Do NOT modify training data in place — fix should be in the
  generation/extraction pipeline
- Follow test-first protocol

**Why this is blocking:**
- Track 4 (MW miss bias deep-dive) analyses the model's errors
  assuming the model saw correct features. If street is
  corrupted, the "bucket-first CHECK bias" diagnosis may be
  partially or wholly wrong — the model might be confused
  about street, not passive.
- v2.3 scope depends on understanding the real v2.2 bias.

## 4. Reordered Tier 1 / Tier 2 from the parallel tracks directive

**NEW Tier 1 (start immediately):**
- ✅ Track 1: Harness hardening — DONE (b5d84b5)
- ✅ Track 3: Training data audit — DONE (8e77e05)
- 🆕 Track 3.5: ANOMALY-A verification — **START NOW, BLOCKING**
- Track 5: BP generator fix implementation — still queued

**NEW Tier 2 (after 3.5):**
- Track 4: MW miss bias deep-dive — HOLD until 3.5 completes
  (the bias diagnosis needs correct feature data to be valid)
- Track 2: FB-40 re-eval with hardened harness — can run any time
- Track 6: Track A scope corrections — still depends on Track 4

## 5. Commit protocol reminder

**Commit and push each track artifact as you complete it.**
Do not batch. Prior session completed work locally but did not
push — that's how we ended up needing this recovery.

After each deliverable:
```
git add <files>
git commit -m "Track N: ...<description>"
git push origin master
```

If `git push` fails with authentication error, STOP and
report BLOCKED in a new file at
`review/comms/BUILDER_BLOCKED_<date>.md`. Do NOT attempt to
work around push failures.

## 6. How to respond to me

You can't talk to me directly. I read comms files. Write your
reports to:

- `review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md` — Track 3.5 deliverable
- `review/comms/BUILDER_STATUS_2026-04-15.md` — any status update or question
- `review/comms/BUILDER_BLOCKED_<date>.md` — if blocked on auth or infrastructure

I check `ls -lt review/comms/ | head -10` periodically. Push
after every commit.

## 7. Gate 7 still pending

Owner has not yet run solver on the 10 MW misses
(`review/comms/SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html`).
All Tier 1 and Tier 2 work is Gate 7-independent. Keep going.

---

**Next action for you: Start Track 3.5 immediately. Follow
test-first → blueprint → implement. Commit and push when done.
Then move to Track 5 (generator fix) or Track 2 (FB-40 re-eval)
per normal Tier 2 sequencing.**
