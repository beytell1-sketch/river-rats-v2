---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: PR #47 pre-merge QC audit — v3.2 protocol revision (Path A bundled Fix 1+2+3); APPROVE (clean); all vectors PASS; A.4 reversal-gate fixes empirically traceable
status: FLAG (advisory; pre-merge informational)
severity: APPROVE / no findings
PR head: 621567e2619cf8fee54c544da8bd9a1df9909e5e
full finding: ~/river-rats-qc/findings/2026-04-26-pr47-pre-merge-v3-2-protocol-revision.md
---

# QC Pre-Merge Audit — PR #47 (v3.2 protocol revision)

## Headline

**APPROVE.** PR #47 cleanly addresses A.4 HARD HALT empirical failures + A.8 F-S5 audit MEDIUM in single bundled revision. All 3 fixes textually present + empirically motivated. v3.1 preserved as historical record. Design ↔ pilot byte-equivalence preserved on Protocol B edits.

## Vector results

| Vector | Result | Note |
|--------|--------|------|
| V-PathA-1 v3.2 file at canonical path | ✅ PASS | 845 lines new |
| V-PathA-2 Fix 1 paired-board CHECK exception | ✅ PASS | Rule 11 line 669+ with EXCEPT clauses + decision rule + carve-outs |
| V-PathA-3 Fix 2 villain_air_pct ≥ 0.20 threshold | ✅ PASS | OVERRIDE section line 758+ matches solver-corrected MW-30 anchor |
| V-PathA-4 Fix 3 F-S5 phantom feature replaced | ✅ PASS | hand-class proxy from bucket + preflop construction; no phantom feature |
| V-PathA-5 v3.1 preserved | ✅ PASS | `git ls-tree` returns blob unchanged |
| V-PathA-6 hash transitions | ✅ N/A | v3.2 new file; Protocol B edits no existing sidecar to update |
| V-X1 design ↔ pilot byte-equivalence | ✅ PASS | identical Range-mass axis text in both files |
| V-X4 carryforward claim verification | ✅ N/A | references forward-pointing not closure-overclaim |

## Empirical traceability

**Fix 1 → d3688 (KdTd4s, 2-tone-flush board OOP) + d9556 (5s6d6h, paired board)** — both A.4 failures. Rule 11 EXCEPT clauses cover both fixture surfaces.

**Fix 2 → MW-39 (Kh8h3d, villain_air_pct=0.05)** — A.4 failure. 0.20 threshold prevents nut-FD raise on low-fold-equity spots; matches `feedback_solver_findings.md` MW-30 CALL anchor.

**Fix 3 → A.8 F-S5-1/F-S5-2 phantom feature** — `hero_top_pair_plus_pct` removed; replaced with `bucket + prior_actions`-based hand-class proxy.

## Cross-build pattern consistency

Builder cites: "preserves design ↔ pilot byte-equivalence pattern from Build A/B verbatim-inlining". Confirmed — both Protocol B files +15/-3 identical edits.

## Multi-expert verdict

SOLO + concrete-finding-driven. Bundled PR with empirically-traced fixes; pre-emptive vector scoping sufficient.

## Recommendation

**APPROVE merge.** No findings. After merge: Pilot Orchestrator re-runs A.4 with parallel Sonnet+Opus on v3.2 to verify d3688/d9556/MW-39 PASS reversal gate. Phase B dispatches if both lanes PASS.

## Process learning

- Empirical-failure → static-audit → bundled-protocol-fix loop working as designed
- TC-15 multi-expert convergence on identical failures revealed upstream cause; fix delivered; next test verifies
- Multi-layer review chain (A.4 calibration + A.8 static + QC HIGH-2 fix surface) all converged on same protocol/KB deficiency

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr47-pre-merge-v3-2-protocol-revision.md`
- PR #47: https://github.com/beytell1-sketch/river-rats-v2/pull/47
- Path A directive: `MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (`24494eb`)
- A.7 HALT: `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (`b2de857`)

**Status: APPROVE. Recommend merge.**
