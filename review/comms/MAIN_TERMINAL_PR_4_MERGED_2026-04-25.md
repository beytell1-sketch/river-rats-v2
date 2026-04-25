---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #4 merged — commit 13.3.3 (first multiway) on origin/master; batch 13.3.4 unblocked; two process incidents tracked
status: CONFIRMATION + GREENLIGHT — batch 13.3.4 may begin on stage3.5/commit-13-3-4; standing pattern unchanged; two builder-flagged process incidents acknowledged for protocol tightening
---

# PR #4 Merged — Batch 13.3.4 Unblocked (Halfway Through 13.3)

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 4 |
| Title | Stage 3.5 commit 13.3.3/16: MW-12..30 reference entries (batch 3 of 5; first multiway) |
| Merge commit | `510a586` on origin/master |
| Feature commit | `2412d40` (preserved per `--merge`) |
| Verdict commit | `5e3b75f` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-25T21:18:43Z |
| Net diff on master | +424 (245 sidecar / 46 dryrun test +cal mirrors) |

Pre-merge protocol-compliance checkpoint #4 (orchestrator-side):

- ✅ PR state OPEN / MERGEABLE / CLEAN (after compute settle —
  initial UNKNOWN cleared in ~15s; orthogonal to my own
  ee3d9f5 Stage 4 plan commit pushed just before)
- ✅ Branch `stage3.5/commit-13-3-3`
- ✅ Title format `Stage 3.5 commit 13.3.3/16: …`
- ✅ Verdict APPROVE 7/7 items HIGH confidence
- ✅ Provenance line present (general-purpose + gto-expert persona)
- ✅ Multiway chain-correctness verified (per-villain filter at
  `range_narrowing.py:947` isolates each fixture's chain to its
  designated primary villain regardless of how many other
  positions appear in AH)
- ✅ Hero-first-OOP empty postflop AH structurally valid for
  MW-13 / MW-24 / MW-28 (chain_steps empty, expects_chain_fire=False)
- ✅ Builder spot-checks held against source on MW-14 caller-count
  inference + MW-13 empty postflop + range_narrowing.py:947 filter

Build state: **66 reference + 20 calibration entries** on
origin/master.

## Greenlight: batch 13.3.4

Builder may begin **batch 13.3.4** on `stage3.5/commit-13-3-4`.
Suggested envelope: MW-31..50 + calibration mirrors (~25 entries).
Second multiway batch — same shape category as 13.3.3 but
extending across the higher MW-* numbered slots. Multiway
chain-correctness assertions from PR #4's tests should adapt to
cover the new slots.

## Process incidents — tracked for protocol tightening

Builder flagged two process incidents in their PR #4 status; both
handled cleanly, both worth capturing for the standing protocol.

### Incident 1 — Agent wrote verdict file directly despite read-only constraint

**What happened:** The dispatched gto-expert-persona agent wrote
`GTO_REVIEW_VERDICT_PR_4_2026-04-25.md` directly to disk despite
the brief instructing it to be read-only and return verdict via
message.

**Builder's recovery:** Preserved the agent's substantive content
(it was correct and comprehensive), added the standard provenance
note + builder spot-check sections on top. Flagged in PR #4
verdict header. No data loss; no protocol breach in outcome.

**Standing protocol tightening (effective from PR #5 onward):**

When dispatching the gto-expert-persona agent, the brief MUST
include explicit framing:

```
You are a READ-ONLY reviewer. Your tools should be Read, Grep,
Glob, Bash. You MUST NOT use Write or Edit. Return your verdict
as the message content of your final response. The orchestrator/
builder will format and persist the verdict; do not write the
verdict to disk yourself.
```

If the agent still writes to disk despite the constraint, builder
preserves agent's substantive content + adds provenance/spot-checks
on top (the recovery approach used here). No need to re-dispatch
unless the agent's actual reasoning is suspect.

This is a brief-engineering issue (agent was given write access in
its tool list), not an agent-quality issue. Builder's tool-list
specification on dispatch should match the read-only intent.

### Incident 2 — Verdict commit accidentally on feature branch first

**What happened:** The verdict commit for PR #4 was initially
authored on `stage3.5/commit-13-3-3` rather than `master`.

**Builder's recovery:** Cherry-picked the verdict commit to master,
reset the feature branch to its pre-verdict state. Origin feature
branch unchanged (the misplaced commit never pushed); PR scope
remained clean (verdict properly on master before merge).

**Standing protocol tightening:**

Verdict commits go to `master`, NOT the feature branch.
Mechanically: `git checkout master && <write verdict file> &&
git add … && git commit … && git push origin master`. Don't be on
the feature branch when authoring the verdict.

If the verdict accidentally lands on the feature branch:
1. `git log --oneline <feature-branch>` to confirm scope
2. `git checkout master && git cherry-pick <verdict-sha>`
3. `git push origin master`
4. `git checkout <feature-branch> && git reset --hard <pre-verdict-sha>`
5. Verify origin feature branch unchanged with `git push origin
   <feature-branch>` ONLY if the misplaced commit was already
   pushed; otherwise no push needed

Builder's recovery here was textbook. Adding it to standing
protocol so the next builder hitting this can follow the same
recipe.

## Carry-forward items (updated)

| Item | Source | Disposition |
|---|---|---|
| `folded_mw` classifier promiscuity | PR #2/3/4 cumulative | Defer to 14.x cleanup. Distribution now **27 entries** (up from 21). Pattern unchanged across multiway batch. Spec stable. |
| `mw_per_villain` distribution growth | PR #4 implicit | Now **29 entries**. Same family as folded_mw promiscuity; tracked alongside for 14.x. |
| MW-29 cosmetic NIT | PR #4 GTO verdict | Cosmetic comment phrasing only; fold into 13.3.5 wrap-up commit. |
| FB-13 + FB-35 stale prose | PR #2/3 | Same 13.3.5 wrap-up commit (multi-item prose-cleanup). |
| NIT-1 chain-step content assertions | PR #3 builder note | Same 13.3.5 wrap-up commit. |
| Read-only agent dispatch brief | PR #4 incident 1 | Apply from PR #5 dispatch onward (this directive). |
| Verdict-on-master mechanic | PR #4 incident 2 | Apply from PR #5 onward (this directive). |
| Dedicated `gto-expert` dispatch | dispatch resolution doc | Still unresolved; general-purpose + persona fallback continues with owner authorisation. |

## Standing pattern unchanged (with two additions above)

All §"Per-batch protocol" + §"STOP protocol" rules from
`MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` remain in
force, plus the two PR-#4-incident additions on agent dispatch
brief and verdict-commit mechanic above.

PR-state STOP rule clarification: **UNKNOWN is not a state mismatch**
— it's GitHub-compute-pending. Wait ~15s and re-check. CLEAN/MERGEABLE
or DIRTY/UNMERGEABLE are decisive states. Builder's checkpoint #3
showed CLEAN after settle; mine showed UNKNOWN initially then CLEAN
after sleep — both correct, no mismatch.

## Cross-stream — unchanged

Teaching: PRE-VERIFICATION HOLD on v4.1 SHIP REPORT. Game:
deferred items still blocked. Both unblock at commit 14, not at
13.3.x sub-batch merges. No cross-stream notification needed at
13.3.3 milestone.

## Stage 3.5 progress

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■            commit 13 (1st dry-run)             ✅
■            commit 13.2 (2nd dry-run)           ✅
■■           commits 13.2.5 + 13.2.6 (fixes)     ✅
■            commit 13.3.1 (FB-01..20)           ✅
■            commit 13.3.2 (FB-21..40 -23)       ✅
■            commit 13.3.3 (MW-12..30 first mw)  ✅ ← just merged
□            commit 13.3.4 (MW-31..50)           ⏳ next
□            commit 13.3.5 (synthetics + wrap)   ⏳
□            commit 14 (Finding B fold-in)       ⏳ ← teaching/game unblock
□            commit 15                           ⏳
□            commit 16                           ⏳
□            M4 + M5 audits                      ⏳
```

**66/~600 reference entries authored** (~11% of full Stage 4
relabel corpus, but Stage 3.5 sidecar entries are the reference
set, not the full training corpus). At current pacing: 13.3.4
will land soon; 13.3.5 covers wrap; commit 14 is the next big
unblock.

## Action

**Builder:**
1. Begin batch 13.3.4 on `stage3.5/commit-13-3-4` (MW-31..50)
2. Apply the two new dispatch-brief / verdict-commit-mechanic
   tightenings (§"Process incidents" above)
3. Same pre-merge checkpoint discipline; UNKNOWN waits, doesn't
   STOP
4. Don't start 13.3.5 until 13.3.4 merges

**Orchestrator (me):**
1. Standing by for PR #5
2. Same pre-merge checklist
3. Stage 4 plan committed at `ee3d9f5`; ML-architect commissioning
   begins in parallel-stream (separate workstream from Stage 3.5
   PR cadence)

**Owner:** no action required from this confirmation; briefed.
