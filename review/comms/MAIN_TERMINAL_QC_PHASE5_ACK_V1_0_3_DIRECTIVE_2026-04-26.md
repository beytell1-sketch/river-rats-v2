---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed; HIGH-severity 1-tick rule) · QC stream · Teaching builder
re: QC Phase 5 pre-pilot adversarial sweep ACK — 2 HIGH-severity findings caught spec-fitness gaps my prior "pilot gate effectively CLEAR" brief at 755b0f1 missed; v1.0.3 pilot orchestration spec fix-forward directive issued (~2-3h) to address HIGH-1 + HIGH-2 + 3 MEDIUMs; pilot dispatch authorization deferred until v1.0.3 sealed
status: ACK + DIRECTIVE + STATUS CORRECTION — my 755b0f1 brief was based on incomplete review; QC found real pilot-fitness gaps; pilot dispatch SHOULD wait for v1.0.3 fix; teaching HIGH-1 PR #1 reviewer dispatched separately
---

# QC Phase 5 ACK + v1.0.3 Directive + Status Correction

## Status correction — my 755b0f1 brief was wrong

I claimed at `755b0f1` that the pilot-dispatch gate was "effectively
CLEAR" pending only owner authorization + QC Phase 5 sweep. I based
that on:
- Empirical dependency analysis (correct: HIGH-1 doesn't affect pilot
  correctness)
- Logic-side gate items all sealed (correct)
- Reviewer + my own pre-merge protocol-compliance checkpoint #4
  (incomplete: those checked prose consistency + cross-references to
  other Stage 4 prep docs, but **not** against `calibration_exam.py`
  infrastructure code)

**QC's Phase 5 adversarial sweep found 2 HIGH-severity gaps the
same-pipeline review chain missed.** This is exactly the failure
mode the QC stream was created to surface. The "gate effectively
clear" claim was load-bearing on logic-side review which had already
shipped; it didn't account for spec-vs-infrastructure-code drift that
adversarial framing catches.

**Owner: do not authorize pilot dispatch until v1.0.3 lands.** The
gate is not clear; QC's findings are real pilot-fitness blockers.

**Total wait estimated: ~2-3h spec edit + reviewer cycle.** Roughly
the same as waiting for teaching HIGH-1 originally would have been.
So owner's instinct ("do we really need to wait for teaching?") was
correct — we don't wait for teaching. But we DO wait for QC's
spec-fitness findings.

## QC Phase 5 findings — disposition

### HIGH-1 (S-A12) — Primary-villain selection drives blocker NaN-flagging

**Surface:** 3-way pot, BB folds mid-flop, SB live through river. Pilot
labellers dispatching with `_villain_pos_raw='BB'` (folded primary)
get blockers all NaN-flagged. With `_villain_pos_raw='SB'` (live
primary), blockers populate correctly.

**Root cause:** HIGH-4 OR-derivation (monotone-True semantics)
documented at `c1a7c0e` + sealed at `d3fcd02`. NOT a regression — the
OR-derivation is correct. But pilot risk: spec doesn't guarantee
labellers select a live opponent as `_villain_pos_raw`. Stage 5
retrain feature regeneration on partial-fold MW training rows with
folded-primary loses blocker training signal.

**Fix (Option A, preferred):** v1.0.3 spec adds explicit rule:
> "On any multi-opponent hand where any opponent is live, designate a
> live (non-folded, non-overflowed) opponent as `_villain_pos_raw`."

Plus Phase A preflight assertion that verifies this rule is honored
on partial-fold MW fixtures.

**Effort:** ~30-45 min spec edit. No code change. No cross-stream
impact.

### HIGH-2 (S-X1) — Calibration manifest drift

**Surface:** Pilot orchestration spec v1.0.2 PRE-DISPATCH PREREQUISITES
rows #3 + #10 say:
- 24-hand calibration manifest
- "20/24 + all 3 GTO-reversal hands correct"

**`river-rats-core/calibration_exam.py` v2.3** says:
- `STANDARD_EXAM_SIZE = 28`
- `STANDARD_PASS_THRESHOLD = 23` → 23/28
- 5 GTO_REVERSAL_HANDS + 5 GROUP_D_REVERSAL_HANDS = 10 reversal hands
  with 100%-must-pass

Comms history (`PHASE_0_PREFLIGHT_2026-04-16.md`,
`BUILDER_STATUS_5_2026-04-16.md`) records v2.2→v2.3 threshold change.
**Stage 4 pilot spec was authored without folding that change in.**

**Why prior reviewers missed it:** orchestrator's gto-expert +
ml-architect dispatches checked prose consistency + cross-refs to
other Stage 4 prep docs. None cross-checked `calibration_exam.py`
infrastructure code. **This is the spec-vs-infrastructure-code drift
pattern (incident class).**

**Fix:** v1.0.3 spec reconciles Phase A pass criterion to v2.3
manifest. Refer to constants by name (`STANDARD_EXAM_SIZE`,
`STANDARD_PASS_THRESHOLD`, etc.) so future drift surfaces
inconsistency.

**Effort:** ~30-60 min spec edit. No code change. No cross-stream
impact.

### MEDIUMs to fold in (3 of 4)

- **S-X3:** `docs/LABELLING_PIPELINE.md` content stale (v1 prompt + v1.1
  KB + 24-hand exam mental model) — compounds HIGH-2. Refresh to v3.1
  prompt + 28-hand exam. ~15-30 min.
- **S-X4:** Highlighter prose-style protocol fingerprinting —
  anonymisation doesn't strip protocol-vocabulary tokens. Pre-Phase-C
  anonymisation step strips protocol-vocabulary tokens. ~30 min in
  pilot orch spec.
- **S-X10:** Cross-protocol firewall has no orchestrator-side audit
  (relies on labeller self-report). Post-Phase-B audit: scan label
  paths against dispatch records. ~30 min in pilot orch spec.

**S-A3 (cache-key dict-vs-tuple form difference)** — defer to v1.1
post-pilot housekeeping. Cache invariants tested empirically; this is
a strict-equivalence concern, not a pilot-fitness concern.

### LOWs (5 of 5) — defer to v1.1

All LOW findings (S-A2/A9 hand-notation duplicate-card; audit-runner
1s timestamp collision; S-X5/6/8/9 various) are non-pilot-affecting.
Defer to v1.1 / post-pilot housekeeping bundle.

## v1.0.3 Pilot Orchestration Spec Fix-Forward Directive

### Scope (5 surgical fixes)

1. **HIGH-1 (S-A12):** add `_villain_pos_raw` live-selection rule to
   spec. Specifically:
   - Add to PRE-DISPATCH PREREQUISITES (new row #16 or addendum):
     "Pilot labeller fixture preparation MUST select a live
     (non-folded, non-overflowed) opponent as `_villain_pos_raw` on
     any multi-opponent hand where any opponent is live."
   - Add to Phase A preflight: "Verify `_villain_pos_raw` selection
     rule is honored on partial-fold MW fixtures (5-hand sample)."

2. **HIGH-2 (S-X1):** reconcile Phase A pass criterion to
   `calibration_exam.py` v2.3:
   - Replace "20/24 + 3 GTO-reversal" → "23/28 + 10 reversal hands
     (5 GTO_REVERSAL + 5 GROUP_D_REVERSAL); 100%-must-pass on all
     reversal hands"
   - Refer to constants by name where possible:
     `STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`,
     `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS`
   - Update PRE-DISPATCH PREREQUISITES rows #3 + #10 accordingly

3. **MEDIUM (S-X3):** `docs/LABELLING_PIPELINE.md` refresh:
   - Update prompt-version reference: v1 → v3.1
   - Update KB-version reference: v1.1 → current (verify against
     `prompts/gto_labeller_v3.1.md` content)
   - Update calibration-exam reference: 24-hand → 28-hand
   - Cross-reference v2.3 `calibration_exam.py` constants

4. **MEDIUM (S-X4):** add anonymisation step to spec:
   - Insert pre-Phase-C step: "Highlighter input is the consensus
     action + per-protocol vote tally + aggregate reasoning text
     STRIPPED of protocol-vocabulary tokens (e.g. 'KB-driven',
     'composition-first', 'adversarial-elimination'); orchestrator
     applies token-strip before dispatching to highlighter."
   - Update Highlighter brief template accordingly

5. **MEDIUM (S-X10):** add post-Phase-B audit to spec:
   - "After Phase B completes, orchestrator runs cross-protocol
     firewall audit: scan label-output paths against dispatch
     records; flag any path-traversal where a labeller wrote outside
     `review/pilot_run_<date>/labels/protocol_<own_protocol>/agent_<own_slot>/`."

### NOT in scope for v1.0.3

- S-A3 cache-key strict-equivalence (defer v1.1)
- All 5 LOW findings (defer v1.1)
- HOLD #21 / #22 / #23 / #24 / #27 (post-pilot housekeeping)
- Teaching HIGH-1 (separate teaching critical-path; PR #1 in flight)

### Branch + workflow

- **Branch:** `stage4-prep/pilot-orchestration-fill-1-0-3`
- **Workflow:** standing per-batch protocol (PR + reviewer + merge)
- **Reviewer:** ml-architect-flavour or orchestration-engineering
  persona; different subagent than v1.0.1 / v1.0.2 reviewers

### Acceptance criteria

1. v1.0.3 spec adds `_villain_pos_raw` live-selection rule + Phase A
   preflight assertion (HIGH-1)
2. Phase A pass criterion reconciles to `calibration_exam.py` v2.3
   constants (HIGH-2)
3. `docs/LABELLING_PIPELINE.md` refresh shipped in same PR or
   sequenced immediately after (MEDIUM S-X3)
4. Anonymisation step added pre-Phase-C with token-strip rule
   (MEDIUM S-X4)
5. Post-Phase-B firewall audit added to orchestrator scope (MEDIUM
   S-X10)
6. Frontmatter bumped to v1.0.3 with full changelog citing each fix
7. Reviewer APPROVE before owner pilot-dispatch authorization

### Estimated effort

~2-3h total per QC's estimate (5 fixes + reviewer cycle).

## Pilot-dispatch gate (corrected)

```
✅ All Stage 4 prep tasks sealed
✅ All logic-side cross-stream HIGH fixes sealed
✅ Task 5 v1.0.2 NITs cleaned
✅ Stage 6 held-out hash-locked at 65cfbf26...
✅ Game HIGH-1 forward-compat (Phase B)
✅ QC Phase 5 sweep COMPLETE — 2 HIGH findings surfaced

⏳ Pilot orchestration v1.0.3 — fix-forward directive issued (~2-3h)
⏳ Owner pilot-dispatch authorization — final gate

Reclassified (still active, NOT blocking pilot):
- Teaching HIGH-1 (PR #1 in reviewer dispatch) — gates teaching C5.2
- HOLD #21/22/23/24/27 — v1.1 / post-pilot housekeeping
```

After v1.0.3 sealed:
- QC re-audits (Phase 6 candidate or post-fix re-sweep) — confirms
  HIGH-1 + HIGH-2 reconciled
- Owner authorizes pilot dispatch
- Pilot dispatches per v1.0.3 spec

## Teaching HIGH-1 PR #1 (parallel track)

Teaching opened HIGH-1 PR #1 at `b9e6c89` on
`teaching/v4-1-high-1-composition-translation`. Their session can't
dispatch the V3 reviewer (cwd-launch issue per their note). I
dispatched a general-purpose-with-V3-persona reviewer in the
background; verdict expected ~5-10 min.

If V3 reviewer APPROVE: orchestrator merges teaching's PR; teaching's
C5.2 unblocked. If APPROVE-WITH-NITS / REQUEST-CHANGES: fix-forward
to teaching builder.

This runs in parallel with logic builder's v1.0.3 spec work — they're
independent critical paths.

## Process-level lesson (memory candidate)

**Pre-merge review chains have a blind spot for spec-vs-infrastructure-code
drift.** All my dispatched reviewers + QC pre-merge audits checked
prose consistency + cross-refs to other Stage 4 prep docs. None
cross-checked actual infrastructure code (`calibration_exam.py`,
`prompts/gto_labeller_v3.1.md`, etc.) against the spec.

This is incident-class material. Will write a memory addition:
`feedback_spec_vs_infrastructure_code_drift.md` after this hot work
clears.

The corrective behavior for future spec authoring + reviewer dispatch:
- When a spec references infrastructure code (file paths, constant
  names, version numbers): reviewer must `git ls-tree` or `cat` the
  referenced file at master HEAD and verify the spec's claims.
- "Infrastructure" includes: test files, config files, prompt files,
  threshold constants, calibration data, version markers in
  filenames or frontmatter.
- This is a NEW reviewer-brief addition (same class as the
  cross-stream-READY tightening from Phase 2 ACK).

## QC Phase 5 disposition

QC's adversarial sweep ran exactly as designed. Multi-expert TC-15
sixth demonstration: CONVERGED on Layer 1 + invariants; DIVERGED on
Layer 2 HIGH findings (each agent surfaced unique high-leverage gap).

QC's recommendation table is the v1.0.3 fix-list (above). They've
explicitly said: "Pilot dispatch is owner-gated; QC's role is to
inform that decision." Their FLAG-only role is preserved.

After v1.0.3 sealed: QC may run a confirming re-sweep (post-fix
adversarial). Their call on whether re-sweep is justified.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 29 | Pilot orchestration v1.0.3 (HIGH-1 + HIGH-2 + 3 MEDIUMs) | 🔥 ACTIVE — directive issued | Logic builder |
| 30 | Teaching HIGH-1 PR #1 reviewer dispatch | 🔥 ACTIVE — V3 reviewer dispatched (background) | Orchestrator + Teaching |
| 31 | `feedback_spec_vs_infrastructure_code_drift.md` memory addition | ⏳ QUEUED — post-hot-work | Orchestrator |

## Action

**Logic builder:**
1. **Begin Task 5 v1.0.3 spec fix-forward** per directive above
   (~2-3h; 5 surgical fixes)
2. Standing per-batch protocol (PR + reviewer + merge — no direct-push)
3. Surface in `review/comms/` when PR opens
4. After v1.0.3 sealed: pilot dispatch unblocked from spec side

**Teaching builder:**
- HIGH-1 PR #1 in V3 reviewer dispatch (orchestrator-coordinated;
  background)
- Stand by for verdict; if APPROVE → orchestrator merges; if NITs →
  fix-forward
- C5.2 unblocked after PR #1 merge

**Orchestrator (me):**
1. Status correction + v1.0.3 directive shipped (this commit)
2. Teaching V3 reviewer in background; will land verdict shortly
3. On reviewer verdict: merge or fix-forward dispatch
4. On v1.0.3 PR: standing per-batch handling
5. Post-v1.0.3-merge: write `feedback_spec_vs_infrastructure_code_drift.md`
   memory + pre-pilot owner readiness brief CORRECTED
6. /loop continues at 15-min cadence

**Owner:**
- Pilot dispatch gate is NOT clear; QC found 2 real HIGH gaps
- v1.0.3 fix-forward in progress (~2-3h)
- Teaching HIGH-1 PR #1 in reviewer dispatch (independent track)
- After v1.0.3 sealed + (optionally) QC re-sweep: pilot-dispatch
  authorization is the next decision

## QC Phase 5 finding bundle (Path B)

QC's full Phase 5 sweep doc is in v2 working tree as
`QC_PHASE5_PRE_PILOT_SWEEP_2026-04-26.md` — bundling into this
commit per dual-path protocol Path B.

## References

- QC Phase 5 sweep: `QC_PHASE5_PRE_PILOT_SWEEP_2026-04-26.md` (in this
  commit)
- Pre-pilot brief (CORRECTED by this comm): `755b0f1`
  (`MAIN_TERMINAL_PRE_PILOT_OWNER_READINESS_BRIEF_2026-04-26.md`)
- Pilot orchestration spec v1.0.2 (current canonical):
  `STAGE4_PILOT_ORCHESTRATION_v1_0.md` (sealed via PR #29 at `b2fbf02`)
- Calibration infrastructure: `river-rats-core/calibration_exam.py`
  v2.3
- Phase 4 ticks log: `~/river-rats-qc/learning/coverage_map.md`

**Status: QC Phase 5 sweep ACK + status correction. v1.0.3 directive
issued (~2-3h). Pilot-dispatch gate NOT clear; v1.0.3 must seal
first. Teaching HIGH-1 PR #1 V3 reviewer dispatched in parallel.**
