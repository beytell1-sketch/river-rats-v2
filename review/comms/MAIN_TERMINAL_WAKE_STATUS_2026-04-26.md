---
date: 2026-04-26 (~05:10 SAST)
from: Main terminal (orchestrator)
to: Owner (read first on wake)
re: Single-page wake-status snapshot — what landed overnight, what's ready for review, what's stalled, what to do first
status: NAVIGATIONAL — orientation aid; nothing requires immediate action
---

# Wake-Up Status — 2026-04-26

## TL;DR (3 lines)

1. **Stage 3.5 is 15/16 commits done.** Commits 14 + 15 merged
   overnight cleanly. Commit 16 (delayed_probe HU-only predicate)
   has scope-doc but no PR yet — builder appears stalled ~3h.
2. **Cross-stream unblocks fired** for teaching HOLD #5 + game
   per-villain range bars after commit 14 landed; both held
   pending downstream execution.
3. **5 Stage 4 design DRAFTs ready for review** at convenience.
   Pilot dispatch is your gate; nothing executes without your
   greenlight on Stage 4 execution.

## What landed overnight

| Time | Commit | What |
|---|---|---|
| 22:06 | `8480b56` | PR #5 merged (commit 13.3.4 — second multiway batch) |
| 22:30 | `fdec54b` | (earlier — already done before sleep) PR #3 merged 13.3.2 |
| 22:56 | `5007a41` | PR #6 merged (commit 13.3.5 — final 13.3 wrap) — **commit 13.3 sealed** |
| 23:34 | `b0ef6c5` | PR #7 merged (commit 14 — Finding B fold-in) — **cross-stream unblock fired** |
| 00:03 | `a9b6301` | PR #8 merged (commit 15 — folded_mw classifier split) |
| 02:14 | `66a06c0` | Builder scope-doc for commit 16 (last v2 master HEAD) |

Plus 5 Stage 4 design DRAFTs at `4d939f1` + `362e70b`:
- `protocol_b_composition_first_v0_1_DRAFT.md`
- `protocol_c_adversarial_elimination_v0_1_DRAFT.md`
- `STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md`
- `STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md`
- `STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md`

Plus 4 rollback tags on origin:
`stage3.5-pre-13-3-4-merge`, `stage3.5-pre-13-3-5-merge`,
`stage3.5-pre-14-merge`, `stage3.5-pre-15-merge`.

## Stage 3.5 progress

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■■■■■        commits 13 / 13.2 / 13.2.5/6 / 13.3.1-5  ✅
■            commit 14 (Finding B fold-in)       ✅
■            commit 15 (folded_mw split)         ✅
□            commit 16                           🟡 builder stalled? (scope doc 02:14, no PR by 05:10)
□            M4 + M5 audits                      ⏳
```

## What's ready for your review (read at convenience)

**Tier 1 — substantive drafts (gto-expert + ml-architect content fill needed):**
1. `prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md` (351 lines)
2. `prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md` (342 lines)
3. `review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md` (225 lines)
4. `review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` (205 lines)
5. `review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md` (284 lines)

All marked DRAFT v0.1. All `[GTO-EXPERT REVIEW NEEDED]` and
`[ML-ARCHITECT REVIEW NEEDED]` flags throughout.

**Tier 2 — milestone confirmations (skim):**
- `MAIN_TERMINAL_OVERNIGHT_PROGRESS_2026-04-26.md` (02:00 snapshot)
- `MAIN_TERMINAL_PR_5_MERGED_2026-04-26.md` (PR #5 merge)
- `MAIN_TERMINAL_PR_7_MERGED_COMMIT15_GREENLIGHT_2026-04-26.md`
  (commit 14 merge + cross-stream unblock)
- `MAIN_TERMINAL_PR_8_MERGED_COMMIT16_GREENLIGHT_2026-04-26.md`
  (commit 15 merge)
- `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md`
  (cross-stream notification to teaching)

**Tier 3 — context (skip unless needed):**
- `BUILDER_COMMIT15_SCOPE_2026-04-26.md` (builder's scope reasoning)
- `BUILDER_COMMIT16_SCOPE_2026-04-26.md` (builder's commit 16 plan)
- `~/river-rats-game/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-26-a.md`
  (cross-stream to game)

## What's stalled

**Commit 16 PR not yet opened.** Builder posted scope-doc at 02:14
saying they'd author commit 16 (delayed_probe HU-only predicate
tightening + 2 NITs). At 05:10 SAST, no PR #9 exists. ~3 hours
without progress.

Possible causes (no anomaly comms surfaced):
- Builder's /loop session went idle/closed
- Builder hit complexity in delayed_probe predicate work
- Builder taking thorough slow/quality time

**No BLOCKED comms.** No STOP-protocol triggers. Orchestrator
discipline = wait + watch.

## Cross-stream HOLD register

| # | Item | Status |
|---|---|---|
| 1 | Stage 3.5 commit 16 + M4/M5 | ⏳ stalled on commit 16 |
| 2 | nut_flush_block hero-side | ✅ CLEARED 04-24 |
| 3 | C5 fixture swap real rows F3/F4 | 🟡 unblocked-pending-teaching-execution (3-gate rule) |
| 4 | Orchestrator pre-Stage-6 gate | ⏳ pending (waits for #1) |
| 5 | Commit 14 multiway field promotion | ✅ CLEARED 04-26 (PR #7 merge) |
| 6 | Teaching Path B (range_position_desc) | ⏳ pending (separate trigger) |

## What to do on wake (recommended order)

1. **5 min:** read this doc + scan v2 origin/master git log (5 commits)
2. **2 min:** check builder terminal — is /loop alive? Any pending
   work? If session is dead, restart from `~/river-rats-v2/` and
   nudge to commit 16 authoring.
3. **5 min:** check teaching terminal — is /loop alive? If yes, has
   it surfaced "begin C5.2?" Confirm/deny. If no, paste loop
   activation block + confirm C5.2 begin.
4. **5 min:** check game terminal — is anyone there? Phase A is
   their workstream now (no orchestrator dependency).
5. **30+ min:** read 5 Stage 4 DRAFTs at convenience; revise/
   approve/reject each.
6. **Decision:** authorise commission of gto-expert + ml-architect
   agents to fill in DRAFT poker/ML-judgment specifics. Authorisation
   path: paste a brief from each draft into the relevant builder
   terminal (logic for ml-architect; teaching for gto-expert if
   teaching session has it; or a fresh agent dispatch).

## Loop status

Orchestrator loop alive at 60-min cadence. Next tick 05:44 / 06:44
(multiple stale schedules in queue from cadence transitions).
Will continue ticking until you stop or session ends.

## Memory updates

- `feedback_quality_default_no_ask.md`: strengthened with explicit
  "applies to my own open questions in proposals" addendum
- `feedback_shared_tree_commit_hygiene.md`: added hard pre-commit
  branch verification recipe + recovery procedure (after two
  misplaced-commit incidents)

## Reference (paths)

```
~/river-rats-v2/
  review/comms/
    MAIN_TERMINAL_*_2026-04-26.md         ← orchestrator overnight
    BUILDER_*_2026-04-26.md               ← builder scope docs
    GTO_REVIEW_VERDICT_PR_[5-8]_*.md      ← per-PR verdicts
    STAGE[4-6]_*_DRAFT_2026-04-26.md      ← Stage 4/5/6 DRAFTs
  prompts/stage4_drafts/
    protocol_b_*.md
    protocol_c_*.md

~/river-rats-game/review/comms/
  MAIN_TERMINAL_TO_GAME_2026-04-26-a.md   ← game cross-stream

~/river-rats-teaching/
  review/comms/                            ← (held; no new since 0b6d4d3)
```

Sleep well; this is the orchestrator's last big artifact before
your wake. Next ticks will continue but this is the navigation hub.
