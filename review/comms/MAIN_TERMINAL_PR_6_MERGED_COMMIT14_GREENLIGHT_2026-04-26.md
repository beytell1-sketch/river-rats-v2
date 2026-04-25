---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner · Teaching builder · Game builder
re: PR #6 merged — commit 13.3 COMPLETE (5/5 sub-batches done); commit 14 (Finding B fold-in) greenlit on stage3.5/commit-14; rollback tag stage3.5-pre-13-3-5-merge saved
status: CONFIRMATION + GREENLIGHT — Stage 3.5 commit 13.3 sealed; commit 14 may begin; cross-stream pre-notification (teaching + game unblock when commit 14 MERGES, not when it starts)
---

# PR #6 Merged — Commit 13.3 COMPLETE — Commit 14 Greenlit

## Milestone: Stage 3.5 commit 13.3 is DONE

All 5 sub-batches of commit 13.3 (the ~130-entry full lift) are now
on origin/master:

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■            commit 13 (1st dry-run)             ✅
■            commit 13.2 (2nd dry-run)           ✅
■■           commits 13.2.5 + 13.2.6 (fixes)     ✅
■            commit 13.3.1 (FB-01..20)           ✅
■            commit 13.3.2 (FB-21..40 -23)       ✅
■            commit 13.3.3 (MW-12..30 first mw)  ✅
■            commit 13.3.4 (MW-31..50 second mw) ✅
■            commit 13.3.5 (synthetics + wrap)   ✅ ← just merged (FINAL 13.3)
□            commit 14 (Finding B fold-in)       🆕 greenlit — NEXT
□            commit 15                           ⏳
□            commit 16                           ⏳
□            M4 + M5 audits                      ⏳
```

Reference + calibration + synthetic corpus is now sealed for
commit-14 onwards. Per PR #6 verdict: "13.3 corpus sufficiently
sealed for Stage 3.5 → commit 14 transition."

## PR #6 merge confirmation

| Field | Value |
|---|---|
| PR # | 6 |
| Title | Stage 3.5 commit 13.3.5/16: 13.3 wrap-up — 6 NITs cleaned + chain-step content assertions |
| Merge commit | `5007a41` on origin/master |
| Feature commit | `2e89479` (preserved per `--merge`) |
| Verdict commit | `beb37d6` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-25T22:56:43Z (SAST 00:56) |
| Rollback tag | `stage3.5-pre-13-3-5-merge` at `2105691` (origin) |
| NITs absorbed in 13.3.5 | FB-13 stale prose, FB-35 stale prose, MW-29 cosmetic, MW-50 cosmetic, NIT-1 chain-step content, PR-5 test-comment NIT |

Pre-merge protocol-compliance checkpoint #4 (orchestrator-side):

- ✅ HARD branch check: `git branch --show-current` = `master` (lesson
  applied; no misplaced commit incidents this session)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage3.5/commit-13-3-5`
- ✅ Title format `Stage 3.5 commit 13.3.5/16:…`
- ✅ Verdict APPROVE 7/7 items HIGH confidence (commit `beb37d6`)
- ✅ Provenance line present (general-purpose + gto-expert persona)
- ✅ All 6 carry-forward NITs from PRs #2-#5 absorbed in 13.3.5

## Greenlight: commit 14 (Finding B fold-in)

Builder may begin **commit 14** on `stage3.5/commit-14`. This is the
critical-path commit for cross-stream unblocking — teaching HOLD #5
+ game per-villain range bars both depend on it.

### Commit 14 scope (locked from prior plans)

Per `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`
+ `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` §"Commit 14
prep handoff":

**Code changes (~30 LoC in `feature_extractor.py`):**

In `extract_range_composition` (the wrapper that calls
`_get_chain_narrowed_villain_range` and populates `range_feats`):
copy three fields from `chain_meta` onto `range_feats`:

```python
range_feats['_per_villain_folded'] = chain_meta.get('per_villain_folded', {})
range_feats['_per_villain_composition'] = chain_meta.get('per_villain_composition', {})
range_feats['_per_villain_overflowed'] = chain_meta.get('per_villain_overflowed', {})
```

For `_per_villain_composition` specifically: derive per-opponent by
running the same partition-by-shape logic that produces
`villain_top_pair_plus_pct` etc., applied to that opponent's
narrowed range.

Composition per opponent (`Dict[str, Dict[str, float]]`):
```python
{
  'BB': {'tp_plus': 0.34, 'medium': 0.21, 'draw': 0.18, 'air': 0.27},
  'CO': {...},
  ...
}
```

**Tests (4 new):**

1. `test_must46_per_villain_folded_promoted_in_multiway` — verifies
   `_per_villain_folded` appears on features dict for 3-way+ hands
2. `test_must46_per_villain_composition_promoted_in_multiway` —
   same for `_per_villain_composition`; verifies composition triple
   sums to ≈1.0 per opponent
3. `test_must46_per_villain_overflowed_promoted_in_multiway` — same
   for `_per_villain_overflowed`
4. `test_must46_per_villain_empty_dict_in_HU` — regression: HU hands
   produce empty dicts for the three new keys (NOT missing keys —
   empty dicts so consumers don't NoneType-error)

**HU regression guards:**

HU code paths must continue producing the existing scalar villain
composition fields (`villain_top_pair_plus_pct` etc.) unchanged.
The `_per_villain_*` dicts on HU rows are EMPTY `{}`, not absent.

**PR #7 spec:**

| Field | Value |
|---|---|
| Branch | `stage3.5/commit-14` |
| Title | `Stage 3.5 commit 14/16: Finding B fold-in — multiway per-villain field promotion` |
| PR body | MUST include: |
| | • 3-line promotion diff |
| | • 4 new test names + scope |
| | • HU regression evidence (existing tests pass unchanged) |
| | • Cross-stream impact: "unblocks teaching HOLD #5" and "unblocks game per-villain range bars" |
| | • Reference to commit-14 spec doc(s) |

### Per-batch protocol (unchanged from PRs #2-#6)

1. Author batch on branch
2. Apply pre-commit branch check (HARD ABORT if not on `stage3.5/commit-14`)
3. Push branch + open PR
4. `gh pr view 7 --json state` checkpoint after create
5. Dispatch GTO reviewer (general-purpose + persona fallback continues)
6. Verdict to PR thread + commit verdict comms to master
7. `gh pr view 7 --json state` checkpoint pre-merge
8. Orchestrator merges with `--merge --delete-branch` after my checks
   (autonomous-merge per overnight directive)

## Cross-stream pre-notification (teaching + game)

**Important: commit 14 LANDING (merge to master) is the unblock
signal — NOT commit 14 starting.** Teaching's loop watches for the
commit 14 merge. Game's deferred items unblock at the same point.

I will write the formal cross-stream notifications when commit 14
MERGES:

- `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_<date>.md` — triggers
  teaching's C5.2 fixture swap process
- `MAIN_TERMINAL_TO_GAME_<date>-<letter>.md` — triggers game's
  per-villain range bars + range_position_desc rename consideration

Until then: teaching stays at PRE-VERIFICATION HOLD; game stays
deferred. No premature notifications.

## Carry-forward items (post-13.3 sealed)

| Item | Source | Disposition |
|---|---|---|
| `folded_mw` classifier promiscuity | PRs #2-#6 cumulative (32+ entries) | Defer to 14.x cleanup. The 13.3 corpus sealing means the pattern is now stable. Fix-spec at PR #2 verdict §D applies. |
| `mw_per_villain` distribution growth | PRs #4-#6 cumulative | Same family; 14.x. |
| MW-50 RAISE→BET normalisation | PR #5 verdict | Deferred to v2.5 (pre-existing, owner-authorised track). |
| Dedicated `gto-expert` dispatch path | dispatch resolution doc | Owner-authorised general-purpose + persona fallback continues across all PRs. |

## Stage 4 design DRAFTs status

5 drafts on origin/master from overnight work (`4d939f1` + `362e70b`
+ `2105691`):

- Protocol B (composition-first labelling)
- Protocol C (adversarial elimination labelling)
- Stage 5 multi-seed retrain protocol
- Stage 6 held-out test set construction
- Stage 4 pilot orchestration script

All marked DRAFT v0.1. Awaits owner review on wake + gto-expert /
ml-architect content fill-in. Pilot dispatch is owner gate.

## Action

**Builder:**
1. Begin commit 14 authoring on `stage3.5/commit-14`
2. Apply HARD pre-commit branch check (`if [ "$BRANCH" != "stage3.5/commit-14" ]; then ABORT`)
3. PR #7 per spec above
4. Dispatch GTO reviewer per per-batch pattern (provenance recorded
   honestly per fallback discipline)

**Orchestrator (me):**
1. PR #6 merge confirmed + commit 14 greenlit (this doc)
2. Loop continues at 60-min cadence (no PR open + waiting for builder
   to author commit 14)
3. When commit 14 PR (#7) opens: standing pre-merge checklist
4. When commit 14 MERGES: cross-stream notifications fire
5. After commit 14 merges: continue to commits 15, 16, M4, M5
6. Standing by for owner wake — review of overnight progress + Stage 4
   drafts

**Teaching:** continue HOLD. Loop will detect commit 14 merge + my
cross-stream notification + surface to owner-on-wake.

**Game:** continue deferred-items hold. Same trigger.

**Owner:** sleep / wake to read overnight progress note (`2105691`)
+ this confirmation + 5 Stage 4 drafts. No emergency.
