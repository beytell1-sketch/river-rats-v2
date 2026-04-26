---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #8 merged — commit 15 (classifier promiscuity cleanup — folded_mw split) on master; commit 16 greenlit; rollback tag stage3.5-pre-15-merge saved; only commit 16 + M4 + M5 remain in Stage 3.5
status: CONFIRMATION + GREENLIGHT — Stage 3.5 entering final cluster (commit 16 + M4 + M5 audits) before pre-Stage-6 gate fires
---

# PR #8 Merged — Commit 15 Sealed — Commit 16 Greenlit

## Stage 3.5 progress (post-PR-8)

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■■■■■        commits 13 / 13.2 / 13.2.5/6 / 13.3.1-5  ✅
■            commit 14 (Finding B fold-in)       ✅
■            commit 15 (folded_mw split)         ✅ ← just merged
□            commit 16                           🆕 greenlit — NEXT
□            M4 + M5 audits                      ⏳ post-commit-16
```

**Three items left in Stage 3.5: commit 16, M4 audit, M5 audit.**
Stage 3.5 closure + pre-Stage-6 gate fires after these clear.

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 8 |
| Title | Stage 3.5 commit 15/16: classifier promiscuity cleanup — folded_mw bucket split |
| Merge commit | `a9b6301` on origin/master |
| Feature commit | `d090743` (preserved per `--merge`) |
| Verdict commit | `488310f` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-26T00:03:51Z (SAST 02:03) |
| Rollback tag | `stage3.5-pre-15-merge` at `92db21f` (origin) |

Pre-merge protocol-compliance checkpoint #4:

- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage3.5/commit-15`
- ✅ Title format
- ✅ Verdict APPROVE 7/7 HIGH confidence
- ✅ Provenance line present (general-purpose + gto-expert persona)
- ✅ Verdict notes "stale-tree recovery confirmed clean" — shared-tree
  hygiene held during builder's authoring
- ✅ Builder scope-doc (`23d24d0`) properly invokes autonomous-advance
  directive + builder discretion per overnight authorisation

## Commit 15 substance — what shipped

Per the verdict + commit message: classifier promiscuity cleanup
on the `folded_mw` bucket. The 32+ entries that PR #2-#6 verdicts
flagged as `folded_mw` non-primary-villain folds (Item D from PR
#2) now correctly route to a split bucket distinguishing
"primary villain folded" (true sentinel territory) from
"non-primary villain folded" (HU-after-fold).

This was the Item D 14.x carry-forward; builder folded it into
commit 15 per the 14.x cleanup window opened by PR #7 merge.

Cosmetic NITs (per verdict): 2 minor items, deferred to commit 16
wrap or later. Non-blocking.

## Greenlight: commit 16

Builder may begin **commit 16** on `stage3.5/commit-16`. This is
the FINAL substantive Stage 3.5 commit before the M4/M5 audits.

[**COMMIT 16 SCOPE — TO BE SPECIFIED BY BUILDER:** per the same
disposition as commit 15: builder is the canonical authority on
commit 16 scope per the v24 stage3.5 blueprint docs. If clear:
author per blueprint. If unclear or commit-16-specific dependencies
emerge: surface via `BUILDER_COMMIT16_SCOPE_<date>.md` per builder
discretion + autonomous-advance directive.

Likely commit 16 candidates (one or more, builder's call):
- `mw_per_villain` distribution growth (29+ entries; same family
  as folded_mw, similar split pattern)
- Final integration tests against the new commit-14 multiway
  fields (now exercised in production code paths)
- 2 cosmetic NITs from PR #8 verdict (small, fold into 16 wrap)
- Any final Stage 3.5 cleanup not yet covered

Builder discretion. Autonomous-advance per owner directive.]

## Carry-forward items (post-commit-15)

| Item | Source | Disposition |
|---|---|---|
| `folded_mw` classifier promiscuity | PRs #2-#6 | ✅ CLEARED in commit 15 |
| `mw_per_villain` distribution growth | PRs #4-#6 | Likely commit 16 candidate |
| MW-50 RAISE→BET normalisation | PR #5 | Deferred to v2.5 (still pre-existing) |
| Cosmetic NITs (PR #8 verdict, 2 items) | PR #8 | Commit 16 wrap or later |
| Dedicated `gto-expert` dispatch | dispatch resolution | Owner-authorised general-purpose + persona fallback continues |

## Cross-stream — unchanged

Teaching: still at `0b6d4d3` (held — awaiting user confirmation
per 3-gate rule for C5.2 fixture swap). My earlier
`MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md` notification
fired the cross-stream unblock signal at the comms layer; teaching
loop will surface to user on next sweep + ask confirmation.

Game: at `021b302` (my notification — Phase A may be in design
work in their own repo / mockups; no commits to surface yet).

## Stage 4 design DRAFTs status

5 drafts on origin/master from earlier overnight. Awaits owner
review on wake + domain-expert content fill. Pilot dispatch is
owner gate.

## Action

**Builder:**
1. Begin commit 16 on `stage3.5/commit-16` (or surface scope via
   `BUILDER_COMMIT16_SCOPE_<date>.md`)
2. HARD pre-commit branch check
3. PR #9 per standing pattern

**Orchestrator (me):**
1. PR #8 merged + commit 16 greenlit (this doc)
2. Loop continues at 60-min cadence (or 30 min if PR #9 opens
   quickly)
3. When commit 16 PR opens → standing pre-merge checklist + merge
   on APPROVE
4. After commit 16 merges + M4 + M5 audits clean: pre-Stage-6
   gate fires

**Owner:** sleep / wake to read overnight progress note + Stage 4
drafts + commit 14/15 confirmations. No emergency.

## References

- `MAIN_TERMINAL_PR_7_MERGED_COMMIT15_GREENLIGHT_2026-04-26.md` —
  parent commit-14-merge confirmation
- `BUILDER_COMMIT15_SCOPE_2026-04-26.md` (`23d24d0`) — builder's
  scope-reading + autonomous-advance notice
- Stage 4 design drafts (Protocol B/C, Stage 5/6, Pilot
  orchestration) — `4d939f1`, `362e70b`
- `feedback_quality_default_no_ask.md`, `feedback_no_deadlines.md`
