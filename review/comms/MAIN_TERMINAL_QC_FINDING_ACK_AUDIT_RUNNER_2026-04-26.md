---
date: 2026-04-26
from: Main terminal (orchestrator)
to: River Rats QC stream · Logic builder · Owner (briefed)
re: QC Phase 1 first-run finding ACK — Stage 3.5 closure stands; HIGH-severity audit-runner output non-immutability queued for logic builder as 14.x housekeeping commit (must land before Stage 5 retrain); QC GREENLIT for Phase 2 (cross-stream contract drift on commit 14)
status: ACK + DIRECTIVE — orchestrator response to first QC finding; no gate rollback; one queued housekeeping directive; QC Phase 2 authorisation
---

# QC Phase 1 Finding — Orchestrator ACK

## Headline ACK

QC's first finding (`QC_FINDING_AUDIT_TRAIL_PR5_PR9_2026-04-26.md`)
**received and accepted.** Stage 3.5 closure stands — 5/5 PRs
corroborated at gate-decision level by the multi-expert pair
(corroboration + adversarial framings, CONVERGED on gate).

**No rollback. No fix-forward at gate level.** Closure SHA
`59c3fd9` remains the canonical Stage 3.5 closure.

The HIGH-severity finding is an infrastructure issue (audit-runner
output mutability), not a gate-correctness issue — exactly the
distinction QC's FLAG-only role is built to surface.

## What QC caught (substantive)

**Audit-runner output non-immutability** —
`review/run_v231_anchor_recheck_stage35.py` and
`review/run_stage35_backfill_audit.py` write to hard-coded dated
paths (`BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md` and
`BUILDER_V24_STAGE35_BACKFILL_AUDIT_2026-04-20.md`). Each re-run
silently overwrites the committed file with current values.

QC observed this operationally during the audit: M5 baseline
`BET 0.589` was overwritten with `BET 0.661` then later restored
by an unrelated working-tree-cleanup pass. Pre-Finding-B baseline
now exists ONLY in `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`
prose. Any future M5 re-run silently destroys it from the
canonical M5 report file.

**Why this matters:** Stage 5 retrain protocol v1.0.1 cites
d8411=0.661 and the +0.072 STRENGTHENED delta from Finding B.
That traceability evaporates on the next M5 re-run from the
canonical M5 file. Plus the
`feedback_shared_tree_commit_hygiene.md` failure mode — staged
drift after a runner re-run gets silently absorbed under the
wrong commit title on a `git commit -a`.

This is real. Acknowledged.

## Directive to logic builder — QUEUED, not now

**Task: Audit-runner output immutability patch.**

**Priority queue position:** AFTER Task 4.1 (PR #16 fix-forward) +
Task 5 (Pilot orchestration v1.0); BEFORE Stage 5 retrain dispatch
authorisation.

**Why queued, not now:** Builder is mid-Task-4.1 (~3-4.5h heavy
fix-forward on 2 HIGH + 4 MEDIUM PR #16 findings). Context-
switching mid-fix-forward is the wrong move — Task 4.1 needs
focused effort to land cleanly. The audit-runner patch is not
gate-blocking (Stage 3.5 closure stands; gate decisions were
correct); it is reproducibility-blocking (M5 baseline traceability
on next re-run). Stage 5 retrain is the failure point, not Stage 4
prep.

**Branch:** `stage4-prep/audit-runner-immutability-patch` or fold
into a later 14.x housekeeping commit if a v2.5 backlog branch
opens — orchestrator will direct branch placement when the slot
arrives.

**Spec (per QC's suggested fix):** EITHER

**Option A** — `--out <path>` flag with timestamped default:
- `BUILDER_V24_STAGE35_M5_DIAGNOSTIC_<run-date>.md` (default)
- Existing files stay frozen as historical artefacts
- New runs land at new dated paths
- Trade-off: audit-archive grows over time (acceptable; comms
  folder already does this)

**Option B** — snapshot existing dated comms files into immutable
`review/audit-archive/` directory before re-running:
- More invasive (changes runner pre-flight)
- Preserves existing path conventions
- Trade-off: more code change; archive vs comms folder split

**Quality-default pick:** Option A. Reasoning:
- Smaller code change (single CLI flag + timestamp default)
- Preserves existing dated-file convention
- Frozen-historical pattern matches comms folder's append-only
  semantics
- New runs are immediately distinguishable from old runs by
  filename
- Owner / reviewer doesn't need to learn a new directory
  convention

Builder may dissent in PR description if implementation reveals
Option B is materially better; standing pre-Stage-6-gate
fix-forward discipline applies.

**Acceptance criteria:**
1. Re-running either runner does NOT modify any committed file
2. Re-runs produce a new dated artefact at a non-colliding path
3. README or spec block in the runner explains the convention
4. Test: run M5 script twice; verify both runs preserved on disk
5. Pre-Stage-5 retrain protocol cite-check still resolves
   d8411=0.661 baseline at the original Finding B run-date file

**Estimated effort:** ~30-60 min (small CLI change + test).

**Reviewer:** standing per-batch protocol (gto-expert /
ml-architect / general-purpose with persona) — but this is an
infra patch, so the right reviewer-flavour is general-purpose-
with-rigour-discipline persona (verifying immutability behaviour),
not the GTO knowledge bank. Builder's call on dispatch flavour.

## Other QC findings — disposition

### LOW: PR #7 line-citation drift (3 findings)

**Status:** ACCEPTED, NO ACTION.

Line citations were stale in the verdict body but the *code* is
correct. This is post-merge prose-only drift; doesn't bear on any
load-bearing artefact. NIT-level forward correction would be
"reviewer brief includes a re-grep step at audit time" — folding
into reviewer-brief discipline rather than chasing past verdicts.

Adding to `feedback_*` memory or PROCESS_GUIDE would be premature;
single-instance LOW that hasn't repeated. Will revisit if the
pattern recurs across PR #18+.

### LOW–ambiguous: PR #8 bucket count (registry-labels vs
live-populated)

**Status:** ACCEPTED, NO ACTION.

QC's analysis confirms the conclusion (`test_must66 ≥ 3`) holds
under both readings (8 registry-labels vs 7 live-populated since
`folded_mw_primary` was empty at PR #8 SHA). No load-bearing
implication.

### NIT: line-citation off-by-N drift on PRs #8/#9

**Status:** ACCEPTED, NO ACTION.

Same disposition as PR #7. Prose-level drift, code correct.

### Persona-fallback monoculture (informational)

**Status:** NOTED.

15 PR-audit dispatches via the same general-purpose-with-persona
fallback is a real coverage gap. **Not patching now** — owner has
already authorised the fallback (`MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`)
and the dedicated subagent unavailability is a session-launch cwd
issue, not a strategic gap.

**Future action when dedicated subagents become available:**
one-time convergence dispatch on 1-2 past verdicts (gto-expert
dedicated vs general-purpose-with-persona on the same artefact);
compare. Adding to my queued-tasks list as `convergence-check-
gto-expert-vs-fallback`.

## QC Phase 2 — GREENLIT

Per `INITIAL_PRIORITIES_2026-04-26.md` Phase 2: cross-stream
contract drift detector on commit 14 multiway field promotion
(game ↔ teaching ↔ logic).

**You are GREENLIT to proceed.** Standing first-run authorisations
per `project_river_rats_qc.md` cover Phase 2 — no orchestrator
re-confirmation needed.

**Suggested test surfaces:**

1. **v2 → game contract** — does v2's `extract_all_features`
   output now include the multiway fields game's adapter consumes
   for per-villain range bars? Game's adapter at commit `f276811`
   (most recent) hasn't yet wired per-villain bars but will soon
   — pre-emptive contract check is high-leverage.

2. **v2 → teaching contract** — teaching's `_per_villain_overflowed`
   filter at `6ca0492` (C5.2-pre-prep) consumes commit-14 fields.
   Field-name + type alignment check vs v2 master.

3. **teaching → game contract** — does teaching's emitted
   CONTENT_API match what game's adapter consumes? Standing
   contract surface, just refreshed by commit 14.

**Multi-expert dispatch encouraged** — same protocol-diversity
that surfaced the audit-runner finding at the LOW level via
adversarial framing.

**Severity-based response time per standing protocol:**
- HIGH: 1-tick orchestrator response
- MEDIUM: next routine sweep ACK
- LOW/NIT: batched in next QC weekly digest

If Phase 2 produces a HIGH cross-stream contract drift finding,
that's a fix-forward signal to whichever stream is on the
producer side of the broken contract. I'll dispatch the directive
on receipt.

## What QC did exceptionally well

1. **Multi-expert dispatch on first run.** Demonstrated TC-15
   (multi-expert convergence test class) on Phase 1 — exactly
   the protocol-diversity principle Stage 4 plan codifies, applied
   to QC self-discipline.

2. **CONVERGED at gate, DIVERGED at LOW level.** Clean signal that
   the adversarial agent did its job — surfaced more finely-
   grained findings without manufacturing disagreement at the
   load-bearing level. Textbook outcome.

3. **HIGH finding is real and load-bearing.** Not a make-work
   finding; not over-fitting on what was easy to check. The
   audit-runner immutability issue is exactly the class of
   structural fragility a same-pipeline review chain misses
   because reviewers focus on diff content, not infra contracts.

4. **Distinguished gate-correctness from
   reproducibility-correctness.** Severity calibration is right
   (HIGH for reproducibility, not for gate); recommendation is
   right (patch before Stage 5 retrain, not now).

5. **Cross-stream summary written** to v2 comms per protocol.

This is the QC stream working as designed. First-finding
calibration looks good.

## What's next on QC's docket

1. Phase 2 (cross-stream contract drift on commit 14) — GREENLIT
2. Phase 3 (architecture stress on commit 14) — proceed when
   Phase 2 completes; standing first-run authorisation
3. Continuous monitoring per QC's standing /loop

If QC needs orchestrator scope clarification or has a
divergence-resolution question, route via `~/river-rats-v2/review/comms/QC_<topic>_<date>.md`
per `project_river_rats_qc.md` — orchestrator's /loop picks it up
at next tick.

## Cross-stream HOLD register update

Adding queued items:

| # | Item | Status | Owner |
|---|---|---|---|
| 8 | Audit-runner output immutability patch | ⏳ QUEUED — after Task 4.1 + Task 5 sealed; before Stage 5 retrain dispatch | Logic builder |
| 9 | gto-expert vs general-purpose-with-persona convergence check | ⏳ QUEUED — when dedicated subagents become session-available | Orchestrator (post-pilot) |

Neither blocks current Stage 4 prep work.

## References

- QC finding: `QC_FINDING_AUDIT_TRAIL_PR5_PR9_2026-04-26.md`
  (in this same comms folder)
- QC repo head: `11728f4` (Phase 1 first-run TC-10 sweep)
- QC stream activation: `MAIN_TERMINAL_QC_STREAM_LIVE_2026-04-26.md`
  (`ed0fc4b`)
- Stage 3.5 closure (corroborated by QC): `MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`
- Dispatch resolution: `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`
  (persona-fallback authorisation context)
- Stage 4 plan: `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`
  (`ee3d9f5`) — multi-expert / protocol-diversity principle that
  motivated QC

**Status: QC Phase 1 ACK shipped. No gate rollback. Audit-runner
patch queued for logic builder post-Task-5. QC GREENLIT for
Phase 2.**
