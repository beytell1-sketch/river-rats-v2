---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #2 merged — commit 13.3.1 on origin/master; batch 13.3.2 unblocked; carry-forward items tracked
status: CONFIRMATION + GREENLIGHT — batch 13.3.2 may begin on stage3.5/commit-13-3-2; 14.x cleanup item logged; standing pattern unchanged
---

# PR #2 Merged — Batch 13.3.2 Unblocked

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 2 |
| Title | Stage 3.5 commit 13.3.1/16: FB-01..20 reference entries (batch 1 of 5) |
| Merge commit | `091de4c` on origin/master |
| Feature commit | `04a1181` (preserved per `--merge`) |
| Verdict commit | `31559ae` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-25T20:00:31Z |
| Net diff on master | +305 / -1 (sidecar additions + dryrun test +41) |

Pre-merge protocol-compliance checkpoint #4 (orchestrator-side):

- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch naming `stage3.5/commit-13-3-1` (matches directive)
- ✅ Title format `Stage 3.5 commit 13.3.1/16:…`
- ✅ Verdict APPROVE 7/7 items HIGH confidence
- ✅ Provenance line present (general-purpose + gto-expert persona,
  owner-authorised fallback, recorded honestly per discipline)
- ✅ Item D rationale acceptable (chain code unaffected; deferring
  classifier-promiscuity to 14.x is reasoned, not a punt)
- ✅ NIT-3 scoped out of PR; flagged for separate prose-fix commit

Merge executed via `gh pr merge 2 --merge --delete-branch`.

## Greenlight: batch 13.3.2

Builder may begin authoring **batch 13.3.2** on
`stage3.5/commit-13-3-2`. Suggested envelope (from §"Recommended
batch composition" of `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md`):

> FB-21..40 minus FB-23 + their calibration mirrors (~25 entries)

Builder may re-shape within the ~25-entries-per-PR envelope per the
parent directive's permission. If shape-category clustering argues
for adjustment, note rationale in the PR description.

## Standing pattern unchanged

All §"Per-batch protocol" + §"STOP protocol" rules from
`MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` remain in force
verbatim. In particular: `gh pr view <N> --json state` at all four
checkpoints; verdict provenance line in every verdict comms doc;
don't start 13.3.3 until 13.3.2 merges.

## Carry-forward items (tracked, not re-triggered)

These are logged so they don't fall off the radar. None are
13.3.2 prerequisites; none gate batch authoring.

| Item | Source | Disposition |
|---|---|---|
| `folded_mw` classifier promiscuity (Item D from PR #2 verdict) | GTO PR #2 | Defer to commit 14.x cleanup. Fix-spec: split `folded_mw` into `folded_mw_primary` vs `folded_mw_offvillain` based on `villain_pos in fold_positions`. Carries through 13.3.2..5 unchanged because FB-* shape distribution stays similar. Orchestrator picks this up when commit 14 design lands. |
| FB-13 `_FB_ACTION_HISTORY:760` stale prose ("bet-and-call" vs JSONL action_string showing direct fold) — NIT-3 from PR #2 | GTO PR #2 | Separate prose-fix commit. Doc-only, can land any time outside the 13.3 sequence; orchestrator suggests folding into the same prose-cleanup commit as any other stale annotations surfaced during 13.3.2..5 batches. Builder discretion on timing. |
| GTO dispatch via dedicated `gto-expert` subagent | `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` | Still unresolved. General-purpose + persona fallback continues with owner authorisation. If builder restarts session from `~/river-rats-v2/` cwd at any point, switch back to dedicated agent and note switchover in next verdict doc. |

## Cross-stream — unchanged

Teaching: PRE-VERIFICATION HOLD on v4.1 SHIP REPORT. Commit 14
remains the unblock for HOLD #3 / #5.

Game: deferred items (per-villain range bars, range_position_desc
rename) still blocked on commit 14 + teaching Path B respectively.

No cross-stream notification needed at 13.3.1 milestone — these
streams unblock at commit 14, not at 13.3.x sub-batch merges.

## Action

**Builder:**
1. Begin batch 13.3.2 on `stage3.5/commit-13-3-2`
2. Apply standing per-batch protocol verbatim
3. Don't start 13.3.3 until 13.3.2 merges

**Orchestrator (me):**
1. Standing by for PR #3
2. Same pre-merge checklist on PR #3 verdict
3. Track carry-forward items into commit 14 design discussion

**Owner:** no action; briefed via this doc.
