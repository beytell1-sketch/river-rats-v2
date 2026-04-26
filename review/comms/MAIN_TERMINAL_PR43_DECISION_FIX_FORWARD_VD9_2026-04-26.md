---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed) · QC stream
re: PR #43 builder decision request — orchestrator decision: **fix-forward Build D v1.0.1 (V-D9 hash-lock determinism)**; PR #43 HOLDS until v1.0.1 ships clean
status: ORCHESTRATOR DECISION — quality-default fix-forward; same pattern as V-C13; ~10-15 min builder cycle
---

# PR #43 — Orchestrator Decision

## TL;DR

- **Fix-forward Build D v1.0.1** — builder adds `random.seed(SEED)`
  before `extract_all_features` MC equity calls; regenerates artifact;
  new SHA256
- PR #43 HOLDS — superseded by v1.0.1 PR; closes after v1.0.1 lands
- After v1.0.1 merge: V-X2 closed empirically; orchestrator writes
  Phase A.5 spec edit; pilot dispatch resumes

## V-D9 reasoning (determinism IS part of the contract)

The Build D directive (`MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`)
explicitly references the Build C v1.0 conventions to inherit, including:

> "SEED-driven determinism, hash-lock, disjointness verification
> methodology"

Build C used SEED=20260426 for selection; the same intent applies to
Build D's MC equity feature extraction.

**Builder's reviewer caught it correctly** — script omitted
`random.seed()` before `extract_all_features` MC equity calls. The
committed artifact's bytes are valid + self-consistent with the
lock (current SHA256 `c196fb82...513` matches the file), but
**re-derivation produces different bytes** — anyone re-running the
script gets different feat_dict values (because MC equity is
stochastic without a seed), producing different SHA256.

**The clean test from `feedback_spec_vs_infrastructure_code_drift.md`
(with existence-drift addendum):**

> "If someone implemented this spec verbatim at master HEAD, would
> it work?"

Current state answer: PARTIALLY. The artifact loads correctly for
Phase A.5 use; the lock SHA256 verifies the committed artifact. But
if someone re-runs the script (e.g., post-pilot-dispatch diagnostic,
or to regenerate after corruption, or for a future Build E that
inherits the conventions), they get a different SHA256 — breaking
the determinism + hash-lock contract.

This is the same incident class as V-C13 (corpus-content gap that
was real but ship-blocking-debatable). Per quality-default +
consistency with the V-C13 fix-forward decision: fix-forward.

## V-D9 fix-forward scope

Modify `scripts/build_phase_a5_partial_fold_fixtures.py`:
- Add `random.seed(SEED)` (or equivalent) BEFORE the loop that calls
  `extract_all_features` per fixture (or before the script's main
  generation block)
- If `extract_all_features` uses `numpy.random` internally, also
  `np.random.seed(SEED)`
- Verify by running the script twice in fresh sessions and confirming
  byte-identical output (ergo identical SHA256)

Regenerate:
- `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl` (new SHA;
  expected byte-different from `c196fb82...513`)
- `data/phase_a5_partial_fold_fixtures_2026-04-26.lock.json`
  (records new SHA256, references old SHA `c196fb82...` for
  traceability)

**Branch:** `stage4-pre-dispatch/phase-a5-partial-fold-fixtures-v1-0-1`
(NEW branch — don't push to existing PR #43 branch; orchestrator
policy on multi-version PRs, same as V-C13)

**Workflow:** PR #45 + dual/triple-reviewer audit + merge. Same
pattern as Build C v1.0.1.

**Estimated effort:** ~10-15 min builder cycle + ~10-15 min review
cycle = ~30 min total to clear V-D9.

## Audit-divergence note (V-D9 + meta-learning)

This is the **second TC-15 protocol-diversity divergence today**:

1. **Build B (PR #37):** builder + orch caught residual NIT (line
   1563 §Anti-patterns) that QC missed → QC added V-X4 curative
2. **Build D (PR #43):** builder caught determinism MED that QC
   missed → QC tick 47 added V-D9 curative

Per `project_river_rats_qc.md`, this is **exactly what TC-15
multi-expert protocol-diversity is supposed to surface**. The
divergent findings ARE the value — different framings catch
different classes of issue. Three additions to QC's learning
artefacts today (TC-23, V-X4, V-D9) is healthy adaptive growth, not
a sign of QC fragility.

**Reinforcement of `project_river_rats_qc.md`:** QC stream's
self-improvement loop is operating as designed. No corrective
feedback needed; the curatives ARE the corrective learning.

## QC PR #44 Path B bundle

QC's audit comm bundled into orch commit. Closing PR #44 as no-op
after this commit lands. QC's V-D vectors covered fixture quality +
diversity + disjointness + 59-feature contract — but their
checklist didn't include re-derivation determinism. V-D9 curative
will close that gap for future per-fixture / per-corpus audits.

## What about merging as-is + housekeeping the determinism later?

**Considered + rejected** because:
1. **Determinism IS in the directive** (not a v1.1 nice-to-have)
2. **V-C13 precedent** — that was also "non-blocking but real"; we
   went with fix-forward, same logic applies
3. **30 min total turnaround** is small enough that quality-default
   wins
4. **Sets clean expectations for future builds** — same protocol
   inheriting from Build C will inherit determinism rigor

## Workflow note ack — builder asked correctly

Builder flagged the MED + builder's reviewer marked non-blocking +
builder still asked orchestrator for decision per quality-default
pattern. **That's exactly the right escalation** — when the reviewer
says "non-blocking" but the principle is at stake, escalate to
orchestrator. Healthy team discipline.

## Pilot dispatch resume — updated dependency list

1. ✅ Build A — SEALED at 2ea67d0
2. ✅ Build B — SEALED at 3241413
3. ✅ Build C v1.0.1 — SEALED at 2a64e11
4. ⏸️ PR #43 (Build D v1.0) — HELD pending v1.0.1
5. 🔥 Build D v1.0.1 — V-D9 fix-forward (this directive)
6. 🔥 Phase A.5 spec edit — orchestrator-owned, post-Build-D-v1.0.1
   (~5-10 min)
7. PRE-DISPATCH gate re-check
8. Phase A.1-A7 preflight begins

**Total estimated time to pilot dispatch resume:** ~30-45 min from
now.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A | ✅ SEALED | Logic builder |
| 36 | Build B | ✅ SEALED | Logic builder |
| 37 | Build C v1.0 (PR #39) | ✅ CLOSED — superseded | Logic builder |
| 40 | Build C v1.0.1 (PR #41) | ✅ SEALED | Logic builder |
| 42 | Build D v1.0 (PR #43) | ⏸️ HELD — superseded by v1.0.1 | Logic builder |
| 43 | Build D v1.0.1 (V-D9 fix-forward) | 🔥 ACTIVE — directive issued | Logic builder |
| 41 | Phase A.5 spec edit | 🔥 QUEUED post-Build-D-v1.0.1 | Orchestrator |

## Action

**Logic builder:**
1. Take orchestrator decision: fix-forward Build D v1.0.1 (V-D9
   determinism)
2. Create branch `stage4-pre-dispatch/phase-a5-partial-fold-fixtures-v1-0-1`
3. Add `random.seed(SEED)` (and `np.random.seed(SEED)` if applicable)
   before `extract_all_features` MC equity calls
4. Regenerate artifact + lock
5. Verify by running script twice in fresh contexts; confirm
   byte-identical output
6. PR #45 with explicit V-D9 close note + new SHA256 + verification
   evidence
7. Standing per-batch protocol (PR + dual/triple-reviewer + merge)
8. Do NOT touch PR #43; closes as superseded after v1.0.1 lands
9. After v1.0.1 merges: surface
   `BUILDER_BUILDS_ABCD_COMPLETE_2026-04-26.md` (final builder signal
   before pilot dispatch resumes)

**Orchestrator (me):**
1. Decision directive shipped + QC PR #44 bundled (this commit)
2. Watch for PR #45 (Build D v1.0.1) drop (~10-15 min ETA)
3. Dispatch ml-architect or gto-expert reviewer at PR #45 open
4. After v1.0.1 merge: write Phase A.5 spec edit (~5-10 min)
5. Re-issue pilot dispatch directive (Phase A.1-A7 preflight resumes)

**QC stream:**
- Continue Layer 1+2 mode for PR #45 (Build D v1.0.1) audit
- V-D9 curative now in registry — re-run on v1.0.1 with determinism
  vector
- TC-15 multi-expert offer standing
- Same Path B bundle pattern

**Owner:**
- Build D MED (hash-lock determinism) is real
- Fix-forward decision: ~30-45 min total to clear
- Pilot dispatch resume contingent on Build D v1.0.1 + Phase A.5
  spec edit
- Sets clean precedent for any future Build E / corpus regen work

## References

- PR #43: `https://github.com/beytell1-sketch/river-rats-v2/pull/43`
- PR #44 (QC audit): `https://github.com/beytell1-sketch/river-rats-v2/pull/44`
- Builder reviewer verdict: `488373c`
- Build D directive: `fa280d6`
- V-C13 precedent (parallel decision): `MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md`
- Memory: `feedback_spec_vs_infrastructure_code_drift.md` (incl.
  existence-drift addendum)
- QC learning artefacts (3 additions today): TC-23, V-X4, V-D9

**Status: PR #43 HELD. Build D v1.0.1 fix-forward DIRECTIVE issued.
~30-45 min total to pilot dispatch resume.**
