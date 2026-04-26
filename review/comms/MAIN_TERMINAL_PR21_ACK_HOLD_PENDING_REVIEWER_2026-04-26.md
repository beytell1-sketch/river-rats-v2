---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #21 Task 4.5 logic hardening bundle ACK at c3efd9c — substantial work landing; 160/160 tests pass; 4 author concerns surfaced for tracking; holding merge pending independent reviewer verdict per standing per-batch protocol; new HOLD #21 added for FEATURE_COLUMNS contract drift (test_multiway_features pre-existing failure)
status: ACK + HOLD — PR #21 acknowledged; merge awaits reviewer APPROVE; author concerns triaged
---

# PR #21 ACK + Hold Pending Reviewer

## Headline

PR #21 opened at `c3efd9c` (single comprehensive commit) per the
Task 4.5 directive at `c1a7c0e`. Substantial work — 4 HIGH-severity
fixes + Phase 1 HIGH audit-runner immutability bundled cleanly.

**Status: HOLD pending independent reviewer verdict.** Per standing
per-batch protocol, merge waits for reviewer APPROVE. Builder has
the dispatch step in flight per PR description ("Independent
reviewer pass (will dispatch in this PR cycle)").

Returning to the standing PR pattern after the Task 4.2 direct-push
divergence — good discipline restoration.

## Test-results acknowledgment

| Suite | Result |
|-------|--------|
| Canonical (test_commit13_sidecar_dryrun + test_commit14_finding_b + test_range_narrowing_stage35) | **50/50 PASS** |
| New (test_task_4_5_hardening) | **52/52 PASS** |
| Broader sweep (commit4_atomic + blocker + action_history_bridge + commit10/11) | **108/108 PASS** |
| **Combined** | **160/160 PASS** |
| M4 audit re-run | **0/124 isolation violations; 455/455 chain activity** ✓ |
| M5 anchor recheck | d2410=0.976 ✓; d0182=0.984 ✓; **d8411=0.661** ✓ (Stage 5 retrain baseline preserved) |

**The d8411=0.661 baseline preservation is a key Phase 1 HIGH
acceptance.** With audit-runner immutability now landed, this baseline
is no longer at risk of silent overwrite on next M5 re-run. The
RERUN_*_2026-04-26T09-44-20Z.md output files written by the new
default-output convention demonstrate the immutability behaviour
empirically (original 2026-04-20 baseline files preserved).

## What's strong about this PR

1. **HARD branch check verified pre-commit.** Builder explicitly
   documented `git branch --show-current = stage4-prep/task-4-5-logic-hardening`
   per the Task 4 incident lesson. Direct application of the
   `feedback_shared_tree_commit_hygiene.md` discipline. Good.

2. **Permanent pilot-gate guard for HIGH-3.** The cache invalidation
   regression test (`test_high3_cache_invalidation_on_mutated_action_history`)
   is in the canonical suite. This is the load-bearing Stage 4 pilot
   gate per the directive — making it permanent (not a one-shot
   verification) means future cache-key refactors can't silently
   reintroduce poisoning.

3. **Option A on HIGH-2** (`classify_hand` raises on bad input).
   Internal callers propagate; corrupt-key bugs surface loudly.
   Quality default — silent classification of malformed input was
   the original problem. Right call.

4. **`_normalise_street()` helper for HIGH-1.** Case-insensitive
   whitelist + raise-on-unrecognised. 14 valid forms + 12 invalid
   tested. Both narrow (single-char `f`) and wide (full-word `flop`)
   conventions accepted. Pilot agents / retrain scripts using either
   convention won't trip.

5. **Audit-runner `--out` flag + timestamped default.** Default
   filename pattern is `RERUN_<runner_name>_<UTC-iso>.md` — clean,
   unambiguous, sortable. Prior 2026-04-20 baseline files preserved.
   Stage 5 retrain protocol cite-check on d8411=0.661 still
   resolves.

6. **Single comprehensive commit per directive's "logic hardening
   BUNDLE" framing.** Reviewer recommendation was "4 separate
   commits" but bundled is acceptable per the BUNDLE framing — clean
   review surface; atomic merge property preserved. Builder's
   judgment call documented in PR description.

## Author concerns triage

### Concern 1 — Pre-existing FEATURE_COLUMNS contract drift (NEW HOLD)

Builder reports 3 failing tests in `test_multiway_features.py::TestFeatureContract`:
> "FEATURE_COLUMNS has 4 extra items (`nut_flush_block` etc) vs the
> model's 55-feature contract."

**Disposition:** This is a SEPARATE finding worthy of investigation
post-Task-4.5. Adding as **HOLD #21** in the register.

- Severity: requires investigation. Could be:
  - (a) FEATURE_COLUMNS has correct content; model's 55-feature
    contract is stale → update model contract
  - (b) Model's 55-feature contract is correct; FEATURE_COLUMNS has
    extra items that should be removed
  - (c) Intentional drift (FEATURE_COLUMNS is a superset; model
    consumes a subset) → document the distinction
- Owner: Logic builder
- Sequencing: investigate post-Task-4.5 merge; depending on finding,
  may be a small fix (option a or b) OR a documentation pass (c)
- QC implication: surface to QC Phase 4 monitoring; if the FEATURE_COLUMNS
  vs model contract drift is real, it's a contract-drift class of bug
  that QC's TC-03 should flag on next sweep

**Not blocking Task 4.5 acceptance** per directive criterion 2
(canonical suite 50/50 passes; FEATURE_COLUMNS contract test isn't
in canonical suite).

### Concern 2 — Cache key shape API-visible

Builder flagged: cache key changed from 2-tuple `(kind, position)` to
3-tuple `(kind, position, ah_hash)`. One test in
`test_commit4_atomic.py::test_must46_cache_hit_via_hand_dict`
inspected the 2-tuple shape directly; updated.

**Disposition:** TRACKING NOTE. Internal-only data structure. No
external consumers. The shape change is a side-effect of the HIGH-3
fix; documented in HOLD register.

### Concern 3 — HIGH-2 design choice (Option A: raise vs Option B: skip)

Builder picked Option A (raise on bad input). Internal callers
propagate; corrupt-key bugs surface loudly.

**Disposition:** AGREED. This is the quality-default pick (loud
failure beats silent classification). Matches QC's recommendation
and the "no improvising" principle in the v2 CLAUDE.md anti-patterns.

### Concern 4 — RERUN_ artifacts NOT included in commit

Builder flagged: 3 timestamped audit-output files in `review/comms/`
from acceptance verification — NOT included in this commit (transient
artifacts per new convention).

**Disposition:** AGREED. The new immutability convention's whole
point is that re-runs produce timestamped artifacts that don't get
committed. They're verification evidence, not canonical state. The
canonical state is the runner code + the `--out` default pattern.
Builder's call to exclude is correct.

(Side note: those RERUN_ artifacts could be moved to a `.gitignore`
pattern if they accumulate. Not urgent.)

## What's pending on PR #21

1. **Independent reviewer dispatch by builder.** Per directive
   `c1a7c0e`: ml-architect-flavour reviewer; could be split for
   cache-key + classify-hand work. Builder's call on dispatch
   strategy.

2. **Reviewer verdict on master** (verdict commit precedes merge).
   Standing per-batch protocol applies.

3. **Orchestrator merge on APPROVE** via atomic bash flow with
   rollback tag (similar to PR #18 merge pattern).

4. **If APPROVE-WITH-NITS / REQUEST-CHANGES:** fix-forward via
   v1.0.1 of Task 4.5 per quality default.

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 8 | Audit-runner output immutability (Phase 1 HIGH) | 🟡 ON PR — folded into Task 4.5 PR #21 | Logic builder |
| 12 | MEDIUM aggregate flag derivation (Phase 2) | ⏳ QUEUED — Task 4.5 didn't include; folds into HIGH-4 cross-stream | Orchestrator → logic + teaching |
| 14 | Phase 3 HIGH-1 STREET_NAME_MAP whitelist | 🟡 ON PR — folded into Task 4.5 PR #21 | Logic builder |
| 15 | Phase 3 HIGH-2 classify_hand raises | 🟡 ON PR — folded into Task 4.5 PR #21 | Logic builder |
| 16 | Phase 3 HIGH-3 cache key includes AH (PILOT GATE) | 🟡 ON PR — folded into Task 4.5 PR #21 | Logic builder |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | ⏳ QUEUED — coordination doc | Orchestrator → logic + teaching |
| 20 | Task 4.3 v1.0.3 NIT prose-consistency | ⏳ QUEUED — directive issued at cb4ef48; awaiting builder | Logic builder |
| **21** | **FEATURE_COLUMNS vs model 55-feature contract drift** | **🆕 ACTIVE — investigate post-Task-4.5 merge** | **Logic builder** |

## Cross-stream context

- **Teaching at `e29aec1`** — held; HIGH-1 directive shipped; awaiting
  builder's renderer translation fix
- **Game at `b944621`** — HIGH-2 SEALED at 26fdf57; chip playtest +
  Phase B per-villain bars unblocked
- **QC stream Phase 4 active** — hourly /loop tick at :13;
  game-side re-audit due now after HIGH-2 seal
- **Other v2 PRs:** none open besides PR #21

## Pilot-dispatch gate progress

```
Phase 2 HIGH-1 (teaching renderer translation):  pending teaching fix
Phase 2 HIGH-2 (game adapter passlist):          ✅ SEALED at 26fdf57
Phase 3 HIGH-1/2/3 (Task 4.5):                   🟡 ON PR #21 — pending reviewer
Phase 1 HIGH (audit-runner immutability):        🟡 ON PR #21 (folded)
Task 4.2 v1.0.2 (Stage 6 held-out):              ON master at f43cd49
Task 4.3 v1.0.3 (NITs):                          directive issued; awaiting builder
Task 5 (Pilot orchestration):                    queued
HIGH-4 (cross-stream aggregate semantics):       coordination doc queued
```

PR #21 sealing brings 5 of the 9 gate items closer (Task 4.5 covers
4 HIGHs + audit-runner). Once reviewed + merged, gate looks like:

```
Phase 2 HIGH-1: pending
Phase 2 HIGH-2: ✅
Phase 3 HIGH-1/2/3: ✅ (post-PR-#21-merge)
Phase 1 HIGH: ✅ (post-PR-#21-merge)
Task 4.2: APPROVE-WITH-NITS at f43cd49
Task 4.3: pending
Task 5: pending
HIGH-4: pending
```

Substantial pilot-gate movement.

## Action

**Builder:**
1. Dispatch independent reviewer on PR #21 per standing pattern
   (ml-architect-flavour per directive `c1a7c0e`)
2. Surface verdict in `review/comms/` when it lands
3. Continue to Task 4.3 v1.0.3 NITs after Task 4.5 sealed (or
   inverse if priorities shift; builder's call)
4. **HOLD #21 (FEATURE_COLUMNS contract drift) is a queued
   investigation task** — not blocking; investigate post-Task-4.5
   merge

**Orchestrator (me):**
1. PR #21 ACK shipped (this commit)
2. Holding PR #21 merge pending reviewer verdict
3. Loop continues at 15-min cadence
4. On reviewer APPROVE → tag rollback + merge via atomic bash flow
5. On APPROVE-WITH-NITS / REQUEST-CHANGES → fix-forward directive
6. Watch teaching HIGH-1 fix PR + builder Task 4.3 PR

**Owner:**
- Stage 4 prep substantial movement: Task 4.5 PR #21 in review;
  PR #21 closes 4 HIGHs + Phase 1 HIGH on a single merge
- Pilot-dispatch gate: progress on 5 of 9 items via PR #21 + Task 4.5
  + game HIGH-2
- HOLD #21 surfaces a potentially load-bearing FEATURE_COLUMNS
  contract drift; investigation scoped post-Task-4.5

## References

- Task 4.5 directive: `c1a7c0e`
  (`MAIN_TERMINAL_QC_PHASE3_ACK_TASK4_5_DIRECTIVE_2026-04-26.md`)
- PR #21 commit: `c3efd9c`
- Phase 3 finding (origin of HIGH-1/2/3): `QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`
- Phase 1 finding (origin of audit-runner immutability):
  `QC_FINDING_AUDIT_TRAIL_PR5_PR9_2026-04-26.md`

**Status: PR #21 ACK'd; held pending reviewer verdict; HOLD #21
new for FEATURE_COLUMNS contract drift investigation.**
