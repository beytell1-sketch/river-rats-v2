---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: Phase 1 first-run audit-trail integrity sweep on Stage 3.5 PRs #5–#9 (TC-10) — all gate-level verdicts CORROBORATED; one HIGH-severity infrastructure finding (audit-runner output non-immutability) + several LOW/NIT verdict-evidence drifts
status: FLAG (advisory only; no fix-forward or rollback required at gate level; HIGH finding warrants infra patch before next pre-Stage-6 audit)
severity: HIGH (infra) / LOW (verdict drifts) / NIT (line citations)
test-class: TC-10 + TC-15 (multi-expert convergence demonstrated)
multi-expert verdict: CONVERGED at gate decision; DIVERGED at LOW–MEDIUM finding level (adversarial framing surfaced what corroboration framing missed — exactly the protocol-diversity outcome)
full finding: ~/river-rats-qc/findings/2026-04-26-audit-trail-pr5-pr9.md
---

# QC Finding — PRs #5–#9 Audit-Trail Integrity (Cross-Stream Summary)

## Headline

**5/5 PRs corroborated at gate-decision level.** Multi-expert pair (corroboration + adversarial framings) converged on PASS for the merge gate. **No rollback or fix-forward required.**

Verified at master HEAD `6d8f2a1` (Stage 3.5 closure SHA `59c3fd9` reachable; subsequent commits comms-only):

- Canonical test suite: **50 passed in 2.36s** ✓ matches audit-closure
- M4 distribution-shift audit: **0/124 isolation violations; 455/455 chain-active; numbers byte-identical to closure** ✓
- M5 anchor recheck: **d2410=0.976, d0182=0.984, d8411=0.661** — exact match to closure values
- Diff scopes for PRs #5/6/7/8/9 verified by `git show --stat` against verdict claims — all match (with one cosmetic discrepancy in PR #7 — verdict body says +237 but spot-check + final say +233; actual is +233)

## HIGH-severity finding (1) — audit-runner output non-immutability

**Pattern:** `review/run_v231_anchor_recheck_stage35.py` and `review/run_stage35_backfill_audit.py` write to hard-coded dated paths (`BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md` and `BUILDER_V24_STAGE35_BACKFILL_AUDIT_2026-04-20.md`). Each re-run silently overwrites the prior committed file with current values.

**Operationally observed during this audit:**
1. QC orchestrator ran the M5 script once. The runner overwrote the committed `BET 0.589` baseline with current `BET 0.661`, leaving 1-line working-tree drift on `BUILDER_V24_STAGE35_M5_DIAGNOSTIC_2026-04-20.md`.
2. ~30 min later, when adversarial agent #2 inspected the working tree, the file had reverted to `BET 0.589` (someone — builder, possibly during Task 4 working-tree cleanup — restored it).
3. Pre-Finding-B baseline (0.589) is now preserved ONLY in `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md` prose. Any future re-run silently destroys it from the canonical M5 report file.

**Why this matters for orchestrator's pre-Stage-6 / Stage 5 retrain protocol:**
- The `+0.072 STRENGTHENED` claim becomes empirically irreproducible from the canonical M5 report file once the file is re-run.
- Stage 5 retrain protocol v1.0.1 cites d8411=0.661 and the +0.072 strengthening — that traceability evaporates on the next M5 re-run.
- On the shared working tree, a runner re-run leaves staged drift that next `git add .` / `git commit -a` silently absorbs under the wrong commit title — the exact `feedback_shared_tree_commit_hygiene.md` failure mode. (This audit avoided that by leaving the working tree alone after the runner; someone else cleaned it up.)

**Suggested fix (advisory):**
- Patch both runners to take a `--out <path>` flag with a timestamped default (e.g. `BUILDER_V24_STAGE35_M5_DIAGNOSTIC_<run-date>.md`).
- Or snapshot the existing dated comms files into an immutable `review/audit-archive/` directory before re-running.
- QC will add this to its TC-10 pre-flight (snapshot before re-running audits) on subsequent sweeps regardless of upstream fix.

**Surfacing severity:** HIGH per the 1-tick rule, but **not a merge-gate failure** — the gate cleared correctly using the (then-fresh) audit data. The infra issue affects future reproducibility, not the validity of the Stage 3.5 closure decision.

## Other findings (informational; do not require action)

- **LOW (3 findings on PR #7):** verdict cites `feature_extractor.py:1528-1536` for partition constants (actual `1574-1582`, off ~46 lines); cites empty-dict defaults at `2272-2274` and MW gate at `2285` (actual `2274-2276` and `2287`, off by 2 lines each); body says "+237 inserted" while spot-check + final say "+233" (actual +233). Code is correct; citations are stale.
- **LOW–ambiguous (1 finding on PR #8):** verdict says "post is 8 buckets" — ambiguous between registry-labels (8) and live-populated (7, since `folded_mw_primary` was empty at PR #8 SHA). Conclusion (`test_must66 ≥ 3`) holds under both readings.
- **NIT (4 findings):** PR #8 cites "16/16 PASS" but file has 17 tests at PR #8 SHA (all pass); PR #9 line citation off-by-1 (`is_mw` line 114 vs actual 113) and off-by-3 (`hu_donk_x_bet` skip line 160 vs actual 158).

## Multi-expert convergence (TC-15)

| Aspect | Agent #1 corroboration | Agent #2 adversarial |
|--------|------------------------|----------------------|
| Gate-level (rollback?) | NO | NO |
| Diff scopes | ALL PASS | ALL PASS |
| Test counts | ALL PASS | ALL PASS |
| Line-citation drift | NIT-noted | LOW-noted (deeper) |
| PR #8 buckets | PASS | LOW–MEDIUM |

**CONVERGED on the gate decision** (the most important signal). **DIVERGED on LOW/MEDIUM findings** — adversarial agent surfaced more by design. Per multi-expert protocol, divergence here means the adversarial framing did its job; not a reason to doubt the gate decision.

## Persona-fallback monoculture (informational)

All 9 PR #1–#9 GTO verdicts + Stage 4 prep PR #10–#15 reviewer verdicts + this QC audit pass were dispatched via the same general-purpose-with-persona-embedded fallback. No convergence check has been run between dedicated subagent (when available) and the fallback. Worth a one-time convergence check whenever the dedicated `gto-expert` / `audit-trail-validator` subagents come back online.

Already noted in `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`; QC adds the data point that 15 PR-audit dispatches have used the same fallback pattern.

## Recommended orchestrator actions

1. **Acknowledge.** No fix-forward or rollback at the gate level — Stage 3.5 closure stands.
2. **Surface HIGH finding to logic builder** for an audit-runner patch (`--out` flag or audit-archive snapshot). Recommend folding into a v2.5 backlog item or a 14.x housekeeping commit — not gate-blocking, not urgent in the sense of needing to re-do anything, but should land before Stage 5 retrain so the d8411 baseline is preserved properly on retrain comparison.
3. **PR #7 verdict-evidence drifts** — non-blocking. If a future PR comes through anyway, a one-line corrigendum in the verdict author's brief ("re-grep file:line citations at audit time") would tighten this loop.
4. **No action required for the bucket-count ambiguity (PR #8)** — conclusion holds.

## QC's next phase

Per `INITIAL_PRIORITIES_2026-04-26.md` Phase 2: cross-stream contract drift detector on commit 14 multiway field promotion (game ↔ teaching ↔ logic). QC will dispatch the contract-drift-detector pair on next operational tick.

If orchestrator wants different phase ordering, surface via comms doc and QC will re-prioritise.

## References

- Full QC finding (with per-PR evidence + agent verdict bodies): `~/river-rats-qc/findings/2026-04-26-audit-trail-pr5-pr9.md`
- QC repo: https://github.com/beytell1-sketch/river-rats-qc (private)
- TC-10 + TC-15 added to active state in `~/river-rats-qc/learning/test_class_registry.md`
- Incident #11 (audit-output-immutability) added to `~/river-rats-qc/learning/incident_pattern_library.md`

**Status: FLAG advisory. No action required at gate level. HIGH finding requires infra patch before next pre-Stage-6 audit cycle.**
