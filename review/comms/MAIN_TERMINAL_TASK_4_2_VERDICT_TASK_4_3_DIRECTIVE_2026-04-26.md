---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: Task 4.2 v1.0.2 reviewer verdict APPROVE-WITH-NITS at f43cd49 (post-hoc dispatch); v1.0.3 micro-correction directive — 3 NITs (1 newly-visible §12 tally duplicate + 2 pre-existing prose-lag); v1.0.2 hash-locked artifact OK for pilot use prerequisites pending; Stage 4 prep updated
status: VERDICT + DIRECTIVE — APPROVE-WITH-NITS; v1.0.3 dispatch per quality default; hash-lock + spec-block intact for pilot use; NITs are documentation-prose drift outside hashed block
---

# Task 4.2 Reviewer Verdict + Task 4.3 v1.0.3 Directive

## Reviewer verdict — APPROVE-WITH-NITS

Independent reviewer dispatched post-hoc by orchestrator on master at
`f43cd49` (per `a9a749f` ACK directive). Provenance: general-purpose
subagent acting as gto-expert (different subagent than v1.0 reviewer
at `9758a99` and v1.0.1 reviewer at `cc247ac`).

### Verdict summary

| Item | Result | Detail |
|------|--------|--------|
| H025 header | **PASS** | Header reads `94.2bb`; body reframe arrives at 94.2; pot odds 29.3% empirically validates as 29.28% (39 / (94.2+39)); FOLD conclusion preserved with intact rationale |
| Hash re-lock | **PASS** | Computed SHA256 = `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5` over 47652 bytes — exact match. Marker discipline preserved (1 literal pair). v1.0.1 hash `b775df2a...` preserved at line 288 + independently verified against `git show 3bbef9e:...` |
| Closure §6 tally | **PASS** | `5 HIGH / 3 MEDIUM / 2 LOW; 1 FOLD / 3 CHECK / 2 CALL / 3 BET / 1 RAISE` matches empirical re-count of the 10 sample IDs (HIGH = {007, 013, 028, 032, 049}, etc.) |
| Self-consistency grep `105.2` | **PASS** | Exactly 3 hits, all in changelog / historical-traceability prose; no leak into hand bodies or spec block |
| New HIGH/MEDIUM | **none** | No new substantive issues introduced |

### NITs (3 total)

**NIT-A (newly-visible after fix; same-class as v1.0.2's scoped fix):**
- Concern §12 at lines 1582-1586 still carries stale tally
  `Sample composition now: 0 → 1 FOLD, 2 CHECK, 3 CALL, 4 BET, 1 RAISE`
- Empirical truth is `1 FOLD / 3 CHECK / 2 CALL / 3 BET / 1 RAISE`
- v1.0.2 fixed §6 (canonical tally) but missed this duplicate location
- **Same class as the stale-pre-swap-count error v1.0.2 was scoped to fix**
- Severity: NIT (because §6 is canonical declaration; §12 is internal
  Concerns prose), but qualifies for v1.0.3 because it's a factual
  error in same class as the v1.0.2-scoped fix

**NIT-B (pre-existing version-prose lag):**
- Document title at line 37 still reads `# Stage 6 Held-Out Test Set v1.0.1`
- Line 50 says "This document is the v1.0.1 lock"
- Frontmatter `version: v1.0.2` is correct
- Cosmetic title-prose lag — was outside v1.0.2's surgical scope

**NIT-C (pre-existing version-prose lag):**
- Pre-eval prereq §1 at line 57 says "Hash matches v1.0.1 lock"
- Should generalise to "v1.0.x current lock" or update each revision
- Same class as NIT-B

### Pre-pilot use disposition (per reviewer)

> "Hash-locked artifact ready for pilot use? **YES** (subject to the
> standing pre-pilot prerequisites: solver verification on the 10-hand
> sample + owner final approval, both already enumerated in the file's
> review_chain)."

**v1.0.2 spec-block + hash-lock are intact** for pilot use. The 3 NITs
are documentation-prose drift OUTSIDE the hashed block; they do not
affect the spec-block lock or any hand-level label/rationale used for
evaluation.

### Reviewer's recommended NIT disposition

> "Bundle [NITs] into v1.1 calibration material per the standing
> orchestrator directive (alongside the 4 v1.0.1 deferred NITs)."

Reviewer suggests deferral to v1.1. Orchestrator's quality-default
disposition differs (see directive below) — this is one of those
edge cases where the reviewer's pragmatic recommendation and the
quality-default discipline diverge slightly.

## Orchestrator directive — Task 4.3 v1.0.3 micro-correction

### Quality default reasoning

`feedback_quality_default_no_ask.md` says: "Always recommend AND
execute the slow/quality path. Owner's answer is always 'do what's
best even if slower.' Don't ask between fast/loose vs slow/clean —
pick clean and proceed."

Reviewer's "defer to v1.1" is the fast path. Quality default is the
slow path (fix all 3 NITs in v1.0.3 micro-correction now).

The 3 v1.0.2 NITs are factual errors (especially NIT-A which is a
duplicate of the same-class error v1.0.2 was scoped to fix). They're
small and direct — single-line fixes per NIT. ~10-20 min total
builder time. Quality-default cleanly says: address them.

This differs from the v1.0.1 NIT deferral (which was correctly
deferred because those were poker-judgment-call kinds of issues —
H001 minor poker overstatement, H027 inline self-correction
artifact, etc., not factual errors). The v1.0.2 NITs are factual
prose-version errors — a different class.

### v1.0.3 scope (3 surgical fixes)

1. **NIT-A — Concern §12 tally consistency**
   - File: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` lines 1582-1586
   - Fix: change `Sample composition now: 0 → 1 FOLD, 2 CHECK, 3 CALL, 4 BET, 1 RAISE`
     to `Sample composition now: 1 FOLD / 3 CHECK / 2 CALL / 3 BET / 1 RAISE`
   - Verify: matches §6 canonical tally exactly

2. **NIT-B — Document title + line 50 lock-prose update**
   - File: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` lines 37 + 50
   - Fix: title `# Stage 6 Held-Out Test Set v1.0.1` → `# Stage 6 Held-Out Test Set v1.0.2`
   - Fix: line 50 "This document is the v1.0.1 lock" → "This document is the v1.0.2 lock"

3. **NIT-C — Prereq §1 hash-lock prose**
   - File: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` line 57
   - Fix: "Hash matches v1.0.1 lock" → "Hash matches v1.0.2 lock"
   - Or generalise to "v1.0.x current lock" — builder's call. The
     latter is more future-proof; the former is more specific. Either
     is fine.

### Hash-lock implications

**Critical check:** all 3 NIT fixes are OUTSIDE the hashed block
(lines 37, 50, 57, 1582-1586 are all prose / changelog / Concerns,
not inside HASHED-BLOCK-START to HASHED-BLOCK-END). **No hash
re-lock required for v1.0.3.** v1.0.2 hash `65cfbf26...` over 47652
bytes remains the canonical lock for the spec-block.

If during the fix the builder discovers any of these locations IS
inside the hashed block, STOP and report — that would change the
analysis (would require hash re-lock and bump to v1.0.3 of the
spec-block, not just prose).

### Workflow

**Standing per-batch protocol** (per the protocol-drift note at
`a9a749f`):

1. Branch: `stage4-prep/stage6-holdout-fill-4-3`
2. Self-edit the 3 lines + verify hash unchanged via recompute
3. Author commit
4. Reviewer dispatch (general-purpose with gto-expert persona;
   different subagent than the v1.0.2 reviewer just completed —
   I'll keep a list for cross-version dispatch hygiene)
5. PR opens
6. Verdict on master (verdict commit precedes merge commit)
7. Orchestrator merge

This time **no direct-push.** Even surgical 3-line fixes go through
the PR cycle for audit-trail discipline.

### Acceptance criteria

1. NIT-A: Concern §12 tally matches §6 tally exactly
2. NIT-B: title + line 50 say v1.0.2
3. NIT-C: prereq §1 says v1.0.2 (or v1.0.x current lock)
4. Hash recompute: `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
   unchanged at 47652 bytes (any change → STOP)
5. Reviewer APPROVE before pilot use
6. PR title: `Stage 4 prep Task 4.3: v1.0.3 NIT prose-consistency
   pass (NIT-A §12 + NIT-B/C version-prose)`

### Estimated effort

~15-30 min total (3 line-level fixes + hash verify + PR cycle).

### Sequencing — relative to Task 4.5

Task 4.5 (logic hardening bundle) is in flight on
`stage4-prep/task-4-5-logic-hardening`. Task 4.3 is independent
(different file, different scope, no dependencies). Builder can:

- (a) **Pause Task 4.5 to ship Task 4.3 first** — Task 4.3 is small
  and unblocks pilot use sealing
- (b) **Continue Task 4.5; Task 4.3 follows after Task 4.5 sealed** —
  Task 4.5 is heavier and takes longer; serialising avoids
  context-switching

**Quality-default pick: option (a) — Task 4.3 first.** Reasoning:
- Task 4.3 is small (~15-30 min); doesn't disrupt Task 4.5 momentum
- Task 4.3 unblocks pilot use sealing (v1.0.2 → v1.0.3 sealed)
- Task 4.5's heavy lift is better attacked with fresh context after
  a small win

If builder strongly prefers option (b), surface that — orchestrator
will defer to builder's context-budget judgment.

## Stage 4 prep progress (updated)

```
Task 1 (Protocol B v1.0.1)         ✅ sealed dc6fa1f
Task 2 (Protocol C v1.0.1)         ✅ sealed 435757f
Task 3 (Stage 5 retrain v1.0.1)    ✅ sealed b639776
Task 4 (Stage 6 held-out v1.0.1)   ✅ sealed afc815c
Task 4.2 (v1.0.2 micro-correction) 🟡 ON MASTER at f43cd49 — APPROVE-WITH-NITS verdict
Task 4.3 (v1.0.3 NIT pass)         🆕 directive issued — pilot-use seal gate
Task 4.5 (Logic hardening bundle)  🔥 in flight on stage4-prep/task-4-5-logic-hardening
Task 5 (Pilot orchestration)       ⏳ queued
```

## v1.0.2 hash-lock for pilot use

**Pilot evaluation can use v1.0.2 NOW** for any pre-flight that
doesn't require sealed canonical (e.g. solver verification on the
10-hand sample, prereq enumeration). Pilot DISPATCH still gates on:
- v1.0.3 sealed (NITs cleaned)
- Solver verification on 10-hand sample
- Owner final approval
- All Stage 4 prep tasks sealed
- Phase 2 HIGH-1/HIGH-2 fixes shipped (teaching + game)
- Phase 3 HIGH-1/2/3 fixes shipped (Task 4.5)
- Phase 1 HIGH (audit-runner immutability) shipped (Task 4.5)
- HIGH-4 cross-stream coordination resolved (separate)
- QC pre-pilot sweep clean

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 18 | v1.0.2 reviewer verdict + pilot-use sealing | 🔥 ACTIVE — verdict APPROVE-WITH-NITS; v1.0.3 directive issued | Orchestrator → builder |
| 20 | Task 4.3 v1.0.3 NIT prose-consistency pass | 🔥 ACTIVE — small surgical 3-line fix | Logic builder |

(Other HOLDs from `a9a749f` unchanged.)

## Cross-stream context

- **Teaching at `e29aec1`** — HIGH-1 directive shipped; awaiting
  builder's renderer translation fix
- **Game at `097a6a0`** — HIGH-2 directive shipped + chip integration
  ACK; awaiting builder's adapter passlist fix
- **QC stream** — three sweeps complete; HOLDs Phase 4 awaiting
  owner /loop activation
- **No open PRs**

## Action

**Builder:**
1. **Recommendation: Task 4.3 first** (~15-30 min), then resume Task 4.5
2. Standing per-batch protocol (PR + reviewer + merge — NO direct-push)
3. Surface in `review/comms/` when PR opens
4. After Task 4.3 sealed, return to Task 4.5 with fresh context

**Orchestrator (me):**
1. Verdict + directive shipped (this commit)
2. Watch for Task 4.3 PR
3. Watch for Task 4.5 PR
4. Watch for teaching HIGH-1 fix PR + game HIGH-2 fix PR
5. Loop continues at 15-min cadence

**Owner:**
- 4 + Task 4.2-as-APPROVE-WITH-NITS of 5+ Stage 4 prep tasks (now
  6 tasks total: 1, 2, 3, 4, 4.2, 4.3, 4.5, 5)
- v1.0.3 micro-correction unblocks v1.0.2 sealing for pilot use
- Pilot dispatch still gated on multi-pre-flight checklist above

## References

- Task 4.2 commit: `f43cd49`
- Task 4.2 ACK + reviewer dispatch: `a9a749f`
  (`MAIN_TERMINAL_TASK4_2_DIRECT_PUSH_ACK_REVIEWER_DISPATCHED_2026-04-26.md`)
- Task 4.2 directive: `aedc3fd`
  (`MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md`)
- Reviewer dispatch (background agent): completed 2026-04-26 (verdict
  body summarised in this comm; full per-item analysis preserved in
  this doc + the reviewer agent's transcript)
- Phase 3 ACK + Task 4.5: `c1a7c0e`
  (`MAIN_TERMINAL_QC_PHASE3_ACK_TASK4_5_DIRECTIVE_2026-04-26.md`)

**Status: v1.0.2 verdict APPROVE-WITH-NITS; hash-lock + spec-block
intact for pilot prerequisites; v1.0.3 directive issued for 3 NIT
surgical fixes; pilot-use sealing on v1.0.3 APPROVE.**
