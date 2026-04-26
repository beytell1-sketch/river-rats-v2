---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #21 MERGED at add2617 — Task 4.5 logic hardening bundle SEALED; 4 HIGHs (Phase 3 HIGH-1/2/3 cache-poisoning pilot-gate) + Phase 1 HIGH audit-runner immutability cleared on single merge; Task 5 (Pilot orchestration v1.0) greenlit for authoring NOW; NITs triaged
status: CONFIRMATION + GREENLIGHT — substantial pilot-gate progress; Task 5 authoring may begin immediately; teaching HIGH-1 + Task 4.3 NITs continue in parallel
---

# PR #21 Merged — Task 4.5 Sealed + Task 5 Greenlit

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 21 |
| Title | Stage 4 prep Task 4.5: Logic hardening bundle (QC Phase 3 HIGH-1/2/3 + Phase 1 HIGH) |
| Merge commit | `add2617` on origin/master |
| Feature commit | `c3efd9c` preserved per `--merge` |
| Verdict commit | `d3ae728` (preserved on master) |
| Feature branch | `stage4-prep/task-4-5-logic-hardening` deleted from origin |
| Merge time | 2026-04-26 ~12:14 SAST |
| Rollback tag | `pre-pr21-merge-2026-04-26` at `d3ae728` (origin) |

Pre-merge protocol-compliance checkpoint #4:
- ✅ HARD branch check passed (master via atomic flow exit gate)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage4-prep/task-4-5-logic-hardening`
- ✅ Reviewer verdict APPROVE at `d3ae728` — independent
  ml-architect + careful-engineer dispatch
- ✅ All 4 HIGH-fix tests pass (52/52)
- ✅ Canonical suite 50/50 PASS preserved
- ✅ M4 audit re-run 0/124 isolation, 455/455 chain (preserved)
- ✅ M5 anchor recheck 3/3 PASS — d8411=0.661 baseline preserved
- ✅ Branch verification per Task 4 incident lesson noted by reviewer
- ✅ Original 04-20 baseline files unchanged on disk

## Pilot-dispatch gate progress

```
✅ Phase 2 HIGH-2 (game adapter passlist):       SEALED at b944621 (game)
✅ Phase 3 HIGH-1 (STREET_NAME_MAP whitelist):   SEALED via PR #21 merge
✅ Phase 3 HIGH-2 (classify_hand raises):         SEALED via PR #21 merge
✅ Phase 3 HIGH-3 (cache key + AH; PILOT GATE):   SEALED via PR #21 merge
✅ Phase 1 HIGH (audit-runner immutability):     SEALED via PR #21 merge

⏳ Phase 2 HIGH-1 (teaching renderer translation):     pending teaching
🟡 Task 4.2 v1.0.2 (Stage 6 held-out APPROVE-WITH-NITS): on master at f43cd49
⏳ Task 4.3 v1.0.3 (NITs):                              builder on branch (stage4-prep/stage6-holdout-fill-4-3)
🆕 Task 5 (Pilot orchestration v1.0):                    GREENLIT NOW
⏳ HIGH-4 (cross-stream aggregate semantics):           coordination doc queued
⏳ HOLD #21 (FEATURE_COLUMNS contract drift):           post-Task-4.5 investigation
⏳ QC pre-pilot sweep (Phase 5):                         QC standing roadmap
```

**5 of the 9 gate items now SEALED.** This is the most substantial
single-merge gate progress in the Stage 4 prep arc.

## Task 5 — Pilot orchestration v1.0 GREENLIT

Per the locked Stage 4 plan (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
`ee3d9f5`) and the source draft (`STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md`):

**Builder may begin Task 5 authoring NOW.** HIGH-3 cache poisoning
was the live pilot-dispatch risk; with PR #21 merged, that's sealed
and Task 5 can be authored without the foundation being a moving
target.

### Source

`review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md` (existing
draft authored 2026-04-26 ~05:00 SAST during overnight Stage 4 prep
preparation).

### Target artifact

`review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md`

### Branch

`stage4-prep/pilot-orchestration-fill`

### Workflow

Standing per-batch protocol (per the protocol-drift note at
`a9a749f`):

1. Branch + author dispatch
2. Reviewer dispatch (ml-architect-flavour for the orchestration
   logic; could also do gto-expert for the labelling-protocol-
   integration parts; builder's call)
3. PR opens
4. Verdict on master (verdict commit precedes merge commit)
5. Orchestrator merges PR
6. Fix-forward if APPROVE-WITH-NITS / REQUEST-CHANGES

### Lessons folded forward (Tasks 1-4.5)

- **Task 1 lesson:** worked content self-consistency
- **Task 2 lesson:** memory references aligned to standing spec
- **Task 3 lesson:** cross-check referenced infrastructure against
  current state (column counts, anchor IDs)
- **Task 3 numerical-rigour lesson:** statistical claims need actual
  computation
- **Task 4 lesson:** hashed-block edits require hash re-lock as a
  first-class step
- **Task 4.2 lesson:** PR cycle preferred over direct-push for
  audit-trail discipline (verdict precedes merge on master log)
- **Task 4.5 lesson:** HARD branch check pre-commit (atomic bash
  flow with exit gate); BUNDLE framing acceptable for tightly
  related fixes; permanent regression guards in canonical suite

### Estimated effort

Per Stage 4 plan: "~2-3 h" for pilot orchestration v1.0. Includes
authoring orchestration spec + reviewer pass + fix-forward if needed.

### Acceptance criteria (per Stage 4 plan)

1. 3 protocol variants × 5 agents = 15 labellers per hand → 100 hands
   pilot corpus
2. Per-hand kappa thresholds defined
3. Aggregation protocol for the 15-labeller votes per hand
4. Solver-verification dispatch on labels meeting kappa criteria
5. Owner gate point clearly enumerated for go/no-go on full pilot
6. Cross-stream signal pattern (when/how teaching + game get
   labeled-spot training data)
7. Calibration protocol against the 24-hand calibration set
8. Held-out test set application (Task 4.2 v1.0.2 / v1.0.3) for
   pre-ship validation

## NIT triage from PR #21 reviewer verdict

Reviewer surfaced 4 NITs in the verdict at `d3ae728`. Disposition:

### NIT-1 — Cache-key docstring overpromise

Disposition: NOTED. Small fix; defer to v1.1 housekeeping commit
(or fold into Task 5 prereqs if cache-key is referenced there).
Not blocking.

### NIT-2 — Bundle-vs-per-fix commit pattern

Reviewer noted the directive recommended "4 separate commits per
directive recommendation" but builder bundled into one. Builder's
PR description documented the judgment.

Disposition: ACCEPTED. The bundle was justified per the BUNDLE
framing in the directive ("Logic hardening bundle"). Reviewer's
note is process-feedback for future bundles. No fix-forward
needed.

**For future tasks:** when the directive says "BUNDLE", builder may
choose single-commit per the BUNDLE framing. When the directive says
"separate commits per fix", builder MUST split. Where directive is
ambiguous (e.g. directive says "bundle into one PR" but doesn't
specify commit shape), builder's call.

### NIT-3 — Pre-existing FEATURE_COLUMNS drift NOT caused by Task 4.5

Disposition: NOTED. This is HOLD #21 — already in the register
from `7acf70d` ACK. Investigation queued post-Task-4.5; will
surface to logic builder + QC when scoped.

### NIT-4 — RERUN_ gitignore

The 3 RERUN_*.md artefacts in working tree from Task 4.5 testing
should be `.gitignore`'d so they don't accumulate as untracked
clutter on every audit-runner re-run.

Disposition: SMALL FIX QUEUED. Builder can fold into a v1.1
housekeeping commit OR Task 5 PR (if the audit-runner pattern is
referenced). Not blocking. Orchestrator will write a small
follow-up directive if the gitignore drift becomes load-bearing
on QC's next sweep.

(Note: the 3 RERUN_ files currently in v2 working tree from the
Task 4.5 acceptance run will stay untracked indefinitely until
either gitignored or manually removed. They're harmless as-is.)

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 8 | Audit-runner output immutability (Phase 1 HIGH) | ✅ SEALED via PR #21 merge | — |
| 12 | MEDIUM aggregate flag derivation (Phase 2) | ⏳ QUEUED — folds into HIGH-4 cross-stream | Orchestrator → logic + teaching |
| 14 | Phase 3 HIGH-1 STREET_NAME_MAP whitelist | ✅ SEALED via PR #21 merge | — |
| 15 | Phase 3 HIGH-2 classify_hand raises | ✅ SEALED via PR #21 merge | — |
| 16 | Phase 3 HIGH-3 cache key includes AH (PILOT GATE) | ✅ SEALED via PR #21 merge | — |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | ⏳ QUEUED — coordination doc | Orchestrator → logic + teaching |
| 20 | Task 4.3 v1.0.3 NIT prose-consistency | 🔥 ACTIVE — builder on `stage4-prep/stage6-holdout-fill-4-3` | Logic builder |
| 21 | FEATURE_COLUMNS vs model 55-feature contract drift | ⏳ QUEUED — investigate post-Task-4.5 | Logic builder |
| 22 | RERUN_ gitignore (NIT-4 from PR #21) | ⏳ QUEUED — small fix; v1.1 housekeeping or Task 5 fold | Logic builder |
| 23 | Cache-key docstring update (NIT-1 from PR #21) | ⏳ QUEUED — small fix; v1.1 housekeeping | Logic builder |

## Stage 4 prep progress

```
Task 1 (Protocol B v1.0.1)         ✅ sealed dc6fa1f
Task 2 (Protocol C v1.0.1)         ✅ sealed 435757f
Task 3 (Stage 5 retrain v1.0.1)    ✅ sealed b639776
Task 4 (Stage 6 held-out v1.0.1)   ✅ sealed afc815c
Task 4.2 (v1.0.2 micro-correction) 🟡 APPROVE-WITH-NITS at f43cd49
Task 4.3 (v1.0.3 NIT pass)         🔥 builder on branch
Task 4.5 (Logic hardening bundle)  ✅ SEALED via PR #21 merge at add2617 ← just now
Task 5 (Pilot orchestration v1.0)  🆕 GREENLIT FOR AUTHORING NOW
```

## Cross-stream context

- **Teaching at `e29aec1`** — held; HIGH-1 directive shipped;
  awaiting builder's renderer translation fix
- **Game at `b944621`** — HIGH-2 SEALED; chip playtest + Phase B
  per-villain bars unblocked
- **QC stream Phase 4 active** — hourly /loop tick at :13;
  - game-side re-audit due (post-HIGH-2) — should produce regression-
    confirm on game's contract surface
  - logic-side re-audit due (post-Task-4.5) — should produce
    regression-confirm on the 4 HIGH fixes + audit-runner
    immutability
  - teaching re-audit pending teaching's HIGH-1 fix

## Action

**Builder:**
1. Continue Task 4.3 (v1.0.3 NIT pass) on
   `stage4-prep/stage6-holdout-fill-4-3` — likely small/quick
2. After Task 4.3 sealed: **begin Task 5 (Pilot orchestration v1.0)**
   per directive above on `stage4-prep/pilot-orchestration-fill`
3. Task 4.5 NITs (NIT-1 docstring + NIT-4 RERUN_ gitignore) can
   fold into v1.1 housekeeping or Task 5 PR — builder's call
4. HOLD #21 (FEATURE_COLUMNS investigation) — queued; not blocking;
   surface when scoped

**Orchestrator (me):**
1. Merge confirmation + Task 5 greenlight (this commit)
2. Watch for Task 4.3 PR
3. Watch for Task 5 authoring + PR
4. Watch for teaching HIGH-1 fix PR
5. Watch for QC re-audit verdicts (logic + game)
6. **Should now be a good time** to write HIGH-4 cross-stream
   coordination doc — teaching is held / between cycles, builder
   has Task 4.3 + Task 5 ahead. Will queue for next tick.
7. PROCESS_GUIDE + memory addition for cross-stream-READY verdict
   brief — also queued
8. Loop continues at 15-min cadence

**Owner:**
- Task 4.5 SEALED — major pilot-gate progress
- Task 5 (Pilot orchestration v1.0) is now the primary critical
  path
- Pilot-dispatch gate items remaining: teaching HIGH-1 fix +
  Task 4.3 + Task 5 + HIGH-4 + QC pre-pilot sweep
- Pilot dispatch still your gate after all the above clears

## References

- PR #21 commit: `c3efd9c`
- PR #21 verdict: `d3ae728`
- PR #21 merge: `add2617`
- Rollback tag: `pre-pr21-merge-2026-04-26` at `d3ae728`
- Task 4.5 directive: `c1a7c0e`
- PR #21 ACK: `7acf70d`
- Stage 4 plan: `ee3d9f5`
  (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`)
- Pilot orchestration draft: `STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md`

**Status: PR #21 MERGED. Task 4.5 SEALED. 4 HIGHs + Phase 1 HIGH
cleared on single merge. Task 5 GREENLIT for authoring. Pilot-
dispatch gate at 5/9 items SEALED.**
