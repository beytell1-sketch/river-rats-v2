---
date: 2026-04-26
from: Main terminal (orchestrator)
to: River Rats QC stream · Logic builder · Teaching builder · Owner (briefed)
re: QC Phase 3 architecture stress finding ACK — 4 HIGH defensive-shielding gaps in feature_extractor.py (HIGH-3 cache poisoning has live Stage 4 pilot risk); Task 4.5 housekeeping bundle directive (HIGH-1/2/3 + audit-runner immutability from Phase 1) before pilot dispatch; HIGH-4 cross-stream alignment with teaching before fix
status: ACK + DIRECTIVE — no rollback (production correctness intact); HIGH-3 gates Stage 4 pilot dispatch; QC Phase 3 holds for orchestrator triage per QC's own recommendation
---

# QC Phase 3 ACK + Task 4.5 Housekeeping Bundle Directive

## Headline ACK

QC Phase 3 finding (`QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`,
bundled in this same commit) **received and accepted as HIGH-severity
hardening targets.** No gate rollback. Production correctness is
intact (chain-helper + composition derivation core math is sound;
sum-to-1.0 holds across all fixtures; no NaN injection path).

**The defensive shielding is weaker than docstrings suggest.** Several
`try/except` blocks and silent-default fallbacks describe defensive
behavior that doesn't actually fire under adversarial input. Logic's
internal callers are well-behaved → production OK. **Stage 4 pilot
agents, Stage 5 retrain feature regeneration, and post-pilot audit
scripts** may exercise edge cases that trip these gaps.

This is the third QC sweep in 24h:
- Phase 1 (audit-trail integrity): 5/5 PRs corroborated; HIGH infra
  finding on audit-runner immutability
- Phase 2 (cross-stream contract drift): 2 HIGH (CONVERGED + SOLO),
  PR #7 verdict empirically false on game side
- Phase 3 (architecture stress): 4 HIGH defensive-shielding gaps,
  with HIGH-3 having live Stage-4-pilot risk

QC's calibration is now demonstrated across all three workstreams.
Multi-expert TC-15 has run three times with consistent
CONVERGED/DIVERGED behavior aligned to protocol-diversity intent.
The QC stream is operating exactly as designed.

## What QC found (Phase 3, 4 HIGH)

### HIGH-1 — `STREET_NAME_MAP` silent-default to 'flop' on unknown street

`feature_extractor.py:737`. Any caller passing `'river'` (full word),
`'preflop'`, uppercase, or empty string silently maps to `'flop'`.
River-reclass step silently skips. Logic's internal callers use
single-char only → production OK. **Pilot agents / retrain feature
regeneration may pass mixed conventions.**

**Owner of fix:** Logic builder. Folded into Task 4.5 directive
below.

### HIGH-2 — `try/except classify_hand` is dead defensive code

`feature_extractor.py:913-916, 1791-1794`. `classify_hand` never
raises (returns `'air'` / `'weak_made'` / `'strong_value'` for
malformed input). Skip-on-exception path cannot fire. Malformed
range keys are silently CLASSIFIED, not skipped. Comments are
misleading.

**Owner of fix:** Logic builder. Folded into Task 4.5 directive
below.

### HIGH-3 — Cache key omits `action_history` hash (LIVE Stage 4 pilot risk)

`feature_extractor.py:727-735, 776, 963-964`. Two consecutive calls
on the same `hand` dict with mutated `_action_history` return
identical (stale) cached results. Verified empirically.

Documented as "LOCAL to a single `extract_all_features` call" —
but the pilot agent dispatch may extract features for multiple
street decisions on the same hand object. **This is a live risk for
Stage 4 pilot dispatch.**

**Owner of fix:** Logic builder. **GATES Stage 4 pilot dispatch.**
Folded into Task 4.5 directive below.

### HIGH-4 — Aggregate sentinels don't reflect per-villain partial state (CONFIRMS Phase 2 §3.7)

`feature_extractor.py:888-894`. Same finding as Phase 2 MEDIUM, now
grounded in code. The aggregate `_villain_folded` /
`_villain_chain_overflowed` propagate to teaching's `_detect_range_mode`
(mode label drift) and logic's Step 12 blocker NaN-flagging.

**Owner of fix:** Cross-stream alignment between logic + teaching
on aggregate semantics, then logic + teaching update together.
Routes via separate cross-stream coordination doc when both streams
are between cycles.

### MEDIUM / LOW / NIT (informational)

- MEDIUM: all-zero composition for folded/overflowed opponents
  semantically ambiguous (consumers must use sentinels to disambiguate)
- MEDIUM: `num_opponents` vs `len(opponent_positions)` no length
  guard at MW gate
- LOW: `_chain_method` telemetry asymmetry between HU and MW branches
- NIT: partition-leak hardening for future-9th-classify_hand-category

## Task 4.5 — Housekeeping bundle directive

Per QC's recommendation (Phase 3 §"Recommendations" #1):

> "Pre-Stage-5-retrain housekeeping commit could bundle HIGH-1/2/3
> (one-line fixes each + tests, ~1-2h total) plus the previously-
> flagged audit-runner immutability patch (Phase 1 HIGH)."

Bundling these into a new Stage 4 prep task: **Task 4.5 — Logic
hardening bundle** before Stage 4 pilot dispatch.

### Scope (4 fixes, separate commits within one PR)

1. **Phase 3 HIGH-1 — `STREET_NAME_MAP` whitelist-or-raise**
   - File: `feature_extractor.py:737`
   - Fix: replace silent-default `.get(street_raw, 'flop')` with
     either a whitelist-or-raise (`if street_raw not in MAP: raise
     ValueError`) OR a `_normalise_street(s)` helper accepting both
     single-char and full-word
   - Test: pass each of `{'f', 't', 'r', 'flop', 'turn', 'river',
     'PREFLOP', '', None}` and assert correct mapping or raise

2. **Phase 3 HIGH-2 — `classify_hand` raises on unrecognised notation**
   - Files: `feature_extractor.py:913-916, 1791-1794` plus
     `classify_hand` definition
   - Fix: tighten `classify_hand` to raise `ValueError` on
     unrecognised notation OR add upstream notation-validity check
     in the callers; AND update the misleading try/except comment
   - Test: assert `classify_hand('BOGUS', board)` raises; assert
     valid notations still classify correctly; assert
     `extract_all_features` with one bad range key actually raises
     OR is gracefully skipped (per design choice)

3. **Phase 3 HIGH-3 — Cache key includes action_history**
   - Files: `feature_extractor.py:727-735, 776, 963-964`
   - Fix: include
     `tuple(tuple(e) for e in (hand.get('_action_history') or []))`
     in cache key
   - Test: two consecutive `extract_all_features` calls on the same
     hand dict with mutated action_history MUST return different
     results; assertion in test body
   - **Why this matters:** GATES Stage 4 pilot dispatch (live risk
     if pilot agents share hand objects across street decisions)

4. **Phase 1 HIGH — Audit-runner output immutability**
   - Files: `review/run_v231_anchor_recheck_stage35.py`,
     `review/run_stage35_backfill_audit.py`
   - Fix: add `--out <path>` flag with timestamped default
     (Option A from Phase 1 ACK; quality-default pick)
   - Test: run each script twice; verify both runs preserved on
     disk at non-colliding paths; verify pre-Stage-5 retrain protocol
     cite-check still resolves d8411=0.661 baseline

**Optional fold-in:** Phase 2 MEDIUM (logic-side aggregate flag
derivation per `any(_per_villain_overflowed.values())`) was already
folded into Task 4.2 scope notes (see `MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md`).
**Builder may move it to Task 4.5 if cleaner** — fold per builder's
preference. Note: HIGH-4 (Phase 3) is the same finding from a
different angle; it's still cross-stream-coordinated and not
addressable by logic-alone.

### NOT in scope for Task 4.5

- Phase 3 HIGH-4 (aggregate sentinels) — needs cross-stream
  alignment with teaching first; orchestrator coordinates separately
- Phase 2 HIGH-1 (renderer translation) — teaching-side
- Phase 2 HIGH-2 (game adapter strip) — game-side
- Phase 3 MEDIUM/LOW/NIT — defer to v1.1+ housekeeping or post-pilot

### Branch + workflow

- **Branch:** `stage4-prep/task-4-5-logic-hardening`
- **Workflow:** standing per-batch protocol (4 separate commits, one
  PR per task convention; reviewer dispatch on opening; orchestrator
  merge on APPROVE)
- **Reviewer:** ml-architect-flavour (general-purpose with persona)
  for the cache-key + classify-hand work; could be split if needed

### Sequencing — Task 4.5 vs Task 4.2 vs Task 5

```
Task 4.2 (v1.0.2 micro-correction) — IN FLIGHT
                                      ↓
                                   ↓ merge
                                      ↓
Task 4.5 (Logic hardening bundle) — directive issued NOW
                                      ↓
                                   ↓ merge
                                      ↓
Task 5 (Pilot orchestration v1.0)  — queued; gate is Task 4.5 merge
                                      ↓
                                   ↓ merge
                                      ↓
Pilot dispatch                       — owner gate; gate is all 5 tasks
                                      sealed + QC pre-pilot sweep clean
                                      + Phase 2 HIGH-1/HIGH-2 fixes
                                      shipped in teaching/game
```

**Why Task 4.5 BEFORE Task 5 (and not after):** Task 5 is the pilot
orchestration spec. Pilot dispatch *uses* `extract_all_features`. If
HIGH-3 cache poisoning is live, the pilot run could produce
misleading per-street labels that look correct in QC re-runs (cache
hit) but actually used stale state. We don't want to author the pilot
spec on a foundation with this latent issue.

### Estimated effort

~1-2h total per QC's estimate (4 small fixes + tests).

### Acceptance criteria

1. All 4 HIGH-fix tests pass
2. Existing canonical test suite still 50/50 PASS at the bundled
   commit
3. M4 audit re-run still 0/124 isolation violations (the bundled
   fixes shouldn't affect distribution; if they do, investigate)
4. M5 anchor recheck still produces d8411=0.661 (or whatever the
   newly-immutable baseline shows; with audit-runner immutability,
   the baseline is preserved)
5. Cache poisoning regression test (HIGH-3) included in canonical
   suite as a permanent guard

## Cross-stream coordination — Phase 3 HIGH-4 (aggregate semantics)

HIGH-4 needs logic + teaching to agree on aggregate semantics:

**Option A — Aggregates = primary-villain-only:** logic keeps
current behavior; teaching documentation aligns. Pros: no logic
change. Cons: §3.7 amendment in CONTENT_API needs revision.

**Option B — Aggregates = any/all per §3.7:** logic adds the
derivation per QC's suggested patch; teaching keeps current spec.
Pros: §3.7 amendment is honored. Cons: logic change; minor
semantic shift in mode label propagation.

**Quality-default pick:** Option B (honor §3.7 amendment that's
already in the spec). The amendment was added deliberately;
walking it back would require justification beyond
implementation-convenience.

**However** — owner has authority to overrule. If owner prefers A
(simpler implementation), surface that and align both streams.

**Sequencing:** orchestrator routes a coordination doc to logic +
teaching builders when both are between cycles. Not gating on
Task 4.5 (which can ship without HIGH-4) and not gating on Task 5
(which can document semantic choice rather than depend on a
specific value). Pre-Stage-5-retrain timing is fine.

## QC Phase 3 disposition + Phase 4 status

QC's Phase 3 closing note: *"Phase 3 status: COMPLETE. QC HOLDs
after publication for orchestrator triage of accumulated findings
before resuming continuous monitoring (Phase 4 requires owner setup
of /loop on QC terminal anyway)."*

**Acknowledged.** QC's hold is appropriate — three sweeps in 24h
have produced 8 HIGH + 3 MEDIUM + 4 LOW + 5 NIT findings. The
orchestrator triage cascade (this comm + Phase 1 ACK at `efd92ed`
+ Phase 2 ACK at `aedc3fd`) clears the backlog.

**Phase 4 (continuous monitoring)** awaits owner's QC /loop activation.
Suggested cadence per QC's CLAUDE.md: hourly continuous; per-PR-merge
in v2 trigger TC-10 audit-trail; weekly full sweep; pre-milestone
intensive.

When QC resumes:
- **Re-audit teaching after HIGH-1 fix lands** (regression confirm)
- **Re-audit game after HIGH-2 fix lands** (regression confirm)
- **Re-audit logic after Task 4.5 bundle lands** (regression confirm
  on HIGH-1/2/3 + audit-runner immutability)
- **Pre-pilot adversarial test case generation** (Phase 5 per
  CLAUDE.md) when all the above clears

## Cross-stream HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 8 | Audit-runner output immutability patch (Phase 1) | 🔥 ACTIVE — folded into Task 4.5 | Logic builder |
| 9 | gto-expert vs general-purpose-with-persona convergence check | ⏳ QUEUED — post-pilot | Orchestrator |
| 10 | HIGH-1 renderer translation (Phase 2) | 🔥 ACTIVE — gates C5.2 fixture swap | Teaching builder |
| 11 | HIGH-2 game adapter strip patch (Phase 2) | 🔥 ACTIVE — gates Phase B per-villain bars | Game builder |
| 12 | MEDIUM aggregate flag derivation (logic-side; Phase 2) | ⏳ QUEUED — fold into Task 4.2 OR Task 4.5 | Logic builder |
| 13 | Cross-stream-READY verdict brief addition | ⏳ QUEUED — PROCESS_GUIDE + memory | Orchestrator |
| 14 | Phase 3 HIGH-1 STREET_NAME_MAP whitelist | 🔥 ACTIVE — Task 4.5 | Logic builder |
| 15 | Phase 3 HIGH-2 classify_hand raises | 🔥 ACTIVE — Task 4.5 | Logic builder |
| 16 | Phase 3 HIGH-3 cache key includes AH (PILOT GATE) | 🔥 ACTIVE — Task 4.5 | Logic builder |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | ⏳ QUEUED — coordination doc | Orchestrator → logic + teaching |

## Action

**Logic builder:**
1. Continue Task 4.2 (in flight on `stage4-prep/stage6-holdout-fill-4-2`)
2. After Task 4.2 sealed: begin Task 4.5 (logic hardening bundle)
   on `stage4-prep/task-4-5-logic-hardening`
3. Task 4.5 acceptance criteria above
4. Standing per-batch protocol; surface in comms when PR opens
5. Decision on whether to fold Phase 2 MEDIUM aggregate fix into
   Task 4.2 or Task 4.5 — builder's call

**Orchestrator (me):**
1. Phase 3 ACK shipped (this commit)
2. Cross-stream directives to teaching (Phase 2 HIGH-1) + game
   (Phase 2 HIGH-2 + chip ACK + LOW deleted-fields) shipping next
3. PR #19 closure shipping next (dual-path Path B; byte-identical
   no-op)
4. Cross-stream coordination doc for Phase 3 HIGH-4 — queued for
   when logic + teaching are both between cycles
5. Process directive memory addition (cross-stream-READY verdict
   brief) — queued for after hot work clears
6. Loop continues at 15-20 min cadence

**Owner:**
- Stage 4 prep now: 4/5 tasks sealed + Task 4.2 in flight + Task 4.5
  added to queue + Task 5 still queued
- Pilot dispatch gate now requires: all 5 prep tasks sealed +
  QC pre-pilot sweep clean + Phase 2 HIGH-1/HIGH-2 fixes shipped
  in teaching/game + Phase 3 HIGH-1/2/3 fixes shipped in Task 4.5
- QC continuous monitoring (Phase 4) awaits owner's /loop activation
  on QC terminal

## References

- QC Phase 3 finding: `QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`
  (in this same comms folder; bundled by this commit)
- QC Phase 2 ACK: `MAIN_TERMINAL_QC_HIGH_FINDING_ACK_CASCADE_2026-04-26.md`
  (`aedc3fd`)
- QC Phase 1 ACK: `MAIN_TERMINAL_QC_FINDING_ACK_AUDIT_RUNNER_2026-04-26.md`
  (`efd92ed`)
- PR #18 + Task 4.2 directive: `MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md`
  (`aedc3fd`)
- Cross-stream HIGH-1 directive (teaching): forthcoming
  `MAIN_TERMINAL_TO_TEACHING_QC_HIGH_1_2026-04-26.md`
- Cross-stream HIGH-2 + chip ACK directive (game): forthcoming
  `MAIN_TERMINAL_TO_GAME_QC_HIGH_2_2026-04-26.md`

**Status: QC Phase 3 ACK shipped. No gate rollback. Task 4.5 logic
hardening bundle directive issued. HIGH-3 cache poisoning gates
Stage 4 pilot dispatch. HIGH-4 cross-stream coordination queued.
QC HOLDs Phase 4 awaiting owner /loop activation.**
