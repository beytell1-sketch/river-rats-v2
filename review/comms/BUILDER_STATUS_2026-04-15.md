---
date: 2026-04-15
from: Builder terminal (restarted)
to: Main terminal / Owner
re: Tier 1 status — Track 3.5 BLOCKED-ambiguity, Track 5 NO-OP, Track 4 held
status: AWAITING DIRECTION on Track 3.5 blocker
---

# Builder Status — Post Restart

## Summary

Restarted builder, cloned repo to `/home/rupert/river-rats-v2/`,
read all required files (CLAUDE.md, SESSION_STATE, HRP_INVESTIGATION,
DIRECTIVE_POST_HRP, REVIEW_PARALLEL_TRACKS, MAIN_TERMINAL_UPDATE,
TRAINING_DATA_AUDIT, BP_GENERATOR_DEFECT_DIAGNOSIS). Pulled main
terminal updates (Tracks 1+3 already committed by main terminal,
Track 3.5 added as BLOCKING).

Launched Tier 1 tracks 3.5 and 5 in parallel.

## Track 3.5 — ANOMALY-A verification — BLOCKED-AMBIGUITY (commit `498e076`)

**Conclusion: cannot definitively confirm v2.2 training corruption.**

Confirmed:
- BP-series factory generators emit `street` and `hero_pos` as Python
  strings; d-series emits numeric. Phase 3.5H assembly merged both
  into `v2_2_training.csv` without normalising.
- Audit understated scope: `hero_position` has the same mixed encoding
  (185 string / 200 numeric, same BP-row set). `villain_position` is
  clean.
- Test-first deliverable shipped:
  `river-rats-core/tests/test_training_data_encoding.py` (3 fail / 1
  pass on current CSV; will pass once BP generators normalise at
  serialisation).

**Blocker:** the script that produced `v2_2_model.json` is not in git.
`river-rats-core/train_model.py` cannot be the v2.2 trainer (wrong
CSV, wrong feature count, `float()` coercion would crash on 'flop').
Three plausible loader behaviours remain (NaN-as-missing / explicit
mapping / silent-zero); cannot distinguish without recovering the
script.

**Worst-case (silent-zero):** 99 turn+river BP rows (25.7% of training)
relabelled as flop — consistent with observed MW bucket-first CHECK
bias. Not diagnostic.

**Owner decision needed:**
1. Accept BLOCKED-ambiguity and proceed Track 4 under worst-case
   assumption?
2. Recover or rewrite the v2.2 training script into `river-rats-core/`
   before Track 4?
3. Other?

Severity HIGH per investigator. See
`review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md` for full report.

## Track 5 — BP generator fix — NO-OP (already applied)

All four blueprint fixes were already implemented in a prior session.
Verified line-by-line against blueprint:
- Fix 1 (`situation_factory.py` validator + `num_opponents` field):
  present at expected lines
- Fix 2 (batch3, batch4 metadata fields): present
- Fix 3 (batch5 covered by validator): confirmed
- Fix 4 (`labelling_agent._normalise_flat_situation`): present, called
  in `prepare_batches()`
- Tests: `test_situation_factory.py` 3/3 pass including the
  villain-count-mismatch regression test

**Full pytest suite:** 1036 passed, 128 skipped, 11 failed. All 11
failures are missing-model-artefact issues in
`test_oracle_router.py` / `test_attention_experiments.py` (e.g.,
`gto_model_v8_hu.json`) — preexisting infra, unrelated to Track 5.

**Minor blocker:** `generate_factory_batch2.py` structure differs from
blueprint (1309 lines, no `SituationSpec`-based loop at cited
location). Per stop protocol, did not improvise. Blueprint section 7
itself marks batch2 as LOW priority — recommend Architecture Expert
confirm if this needs a separate fix spec or can be dropped.

Working tree clean, no commit needed.

## Track 2 — FB-40 / MW-50 re-eval — READY TO LAUNCH

Independent of Track 3.5 blocker. Can launch now. Will use Track 1's
hardened harness on FB-40 + MW-50 to confirm 72.5% / 80.0% stand.
Holding for owner go-ahead per "incremental review" protocol, or
proceeding now if no objection.

## Track 4 — MW miss bias deep-dive — HOLDING

Per `MAIN_TERMINAL_UPDATE_2026-04-15.md`, Track 4 holds until 3.5
completes. With 3.5 BLOCKED-ambiguity, Track 4 stays held pending
owner decision above.

## Track 6 — Track A scope corrections — HOLDING

Depends on Track 4.

## Tier 1 / Tier 2 status

| Track | Status | Tier |
|---|---|---|
| 1 Harness hardening | ✅ done (b5d84b5) | 1 |
| 3 Training audit | ✅ done (8e77e05) | 1 |
| 3.5 ANOMALY-A | ⚠️ BLOCKED-ambiguity (498e076) | 1 |
| 5 BP generator fix | ✅ no-op (already applied) | 1 |
| 2 FB-40 re-eval | 🟡 ready to launch | 2 |
| 4 MW bias deep-dive | ⏸️ held on 3.5 | 2 |
| 6 Scope corrections | ⏸️ held on 4 | 2 |

## Awaiting

1. Owner direction on Track 3.5 blocker (3 options above)
2. Go-ahead to launch Track 2 in parallel (or proceed without
   explicit approval — protocol allows)

I will check `review/comms/MAIN_TERMINAL_UPDATE_*` periodically for
new direction.
