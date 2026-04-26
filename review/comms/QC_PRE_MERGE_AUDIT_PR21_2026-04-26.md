---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: PR #21 pre-merge QC audit — Task 4.5 logic hardening bundle; CONVERGED APPROVE on all 4 spec-fixes; 1 MEDIUM follow-up + 3 NITs surfaced (non-blocking; v1.1 candidates); recommend merge
status: FLAG (advisory; pre-merge informational; orchestrator's dispatched reviewer makes the merge call)
severity: CONVERGED PASS / MEDIUM (advisory v1.1) / NIT (defer)
multi-expert verdict: CONVERGED APPROVE — both agents recommend merge
PR head: c3efd9cd83d5883598aea94b239db151c6f199da
full finding: ~/river-rats-qc/findings/2026-04-26-pr21-pre-merge-task4-5.md
---

# QC Pre-Merge Audit — PR #21 (Task 4.5)

## Headline

**APPROVE.** PR #21 cleanly satisfies all 4 fix-specs from QC Phase 1 + Phase 3 findings. Multi-expert pair (spec-vs-implementation + adversarial framings) **CONVERGED APPROVE**. Recommend merge — Stage 4 pilot dispatch gate clears 1 step closer.

QC ran a pre-merge audit because:
- Pre-merge review is cheaper than post-hoc fix-forward (per QC's TC-10 pre-merge variant intent)
- Orchestrator's reviewer hadn't dispatched yet (PR #21 is OPEN with HOLD #21 pending reviewer)
- This PR is the bundled response to 4 of QC's HIGH findings → comprehensive review appropriate

## Per-fix one-line summary

| Fix | Spec match | Empirical | NITs |
|-----|------------|-----------|------|
| HIGH-1 STREET_NAME_MAP whitelist-or-raise | IMPROVED (did both: extended map + helper) | PASS — case-insensitive, whitespace-tolerant, all rejection patterns work | none |
| HIGH-2 classify_hand raises | IMPROVED (Option A + JJo/JJs guard) | PASS — 13 valid notations classify, 13 invalid raise | 1 NIT (`AhAh` accepted); 1 MEDIUM (indirect propagation via `narrow_to_*` — out of Task 4.5 scope) |
| HIGH-3 cache key + AH (PILOT GATE) | IMPROVED (canonicalises tuple AND dict encodings) | PASS — 3-call mutation produces 3 distinct results; adversarial monkey-patch reproduces pre-fix poisoning | 1 NIT (nested mutable inner types unhashable) |
| Phase 1 audit-runner --out | EXACT (Option A as specced) | PASS — 4 tests including 1.05s sleep collision-check | 2 NITs (1s timestamp resolution; --out doesn't validate against original baseline path) |

## Test results (independently verified by both agents)

- `test_task_4_5_hardening.py` (new): **52/52 PASS**
- Canonical 3-file suite: **50/50 PASS**
- `test_commit4_atomic.py`: **20/20 PASS** (includes updated `test_must46_cache_hit_via_hand_dict` for new 3-tuple cache key shape; assertion strength preserved)
- `test_multiway_features.py::TestFeatureContract`: 3 PRE-EXISTING failures, NOT introduced by Task 4.5 (verified by both agents via comparison against master pre-PR)

## Multi-expert convergence (TC-15 fourth demonstration)

CONVERGED APPROVE on the 4 spec-fixes themselves. Adversarial framing surfaced additional NITs that spec-comparison didn't reach (1 MEDIUM + 3 NITs). Same protocol-diversity outcome as Phases 1/2/3.

| Aspect | Agent #1 spec-vs-impl | Agent #2 adversarial |
|--------|------------------------|----------------------|
| Merge recommendation | APPROVE (clean) | APPROVE-WITH-NITS |
| HIGH-1/2/3 + Phase 1 spec match | All PASS / IMPROVED | All break attempts handled cleanly |

## MEDIUM finding (advisory, NOT blocking Task 4.5)

**HIGH-2 indirect propagation gap.** Agent #2 SOLO finding: `range_narrowing.py:601, 673, 778` (`narrow_to_betting_range/checking/continuing`) call `classify_hand(hand, board)` WITHOUT try/except. These are invoked from `narrow_by_action_history` which is called from `feature_extractor.py:825` and `:1794` — neither callsite has a try/except wrapper.

If an audit/pilot script loads a corrupted opp_range from disk, the corrupted key reaches `narrow_to_betting_range` → ValueError propagates UP past the explicit-classify-hand try/except guards (the ones Task 4.5 just hardened) and crashes the entire feature extraction.

PR's "log + skip" defense applies to the EXPLICIT classify_hand callsites that this PR updated, NOT the indirect narrowing-chain path. Limited to corrupt-on-disk audit/pilot scenarios; not a production-path issue (logic's internal range generation produces well-formed combos).

**Recommended fix (v1.1 follow-up):** add `try/except ValueError as exc: logging.warning + skip` wrapper around the `narrow_to_*` calls OR around `narrow_by_action_history` callsites in `feature_extractor.py:825, 1794`. Either closes the gap.

**Disposition:** explicitly out-of-scope for Task 4.5 per directive. Schedule for v1.1 hardening pass or post-pilot housekeeping.

## NITs (defer to v1.1+; non-blocking)

- HIGH-2: `classify_hand('AhAh', board)` accepted (duplicate specific card not rejected by `_is_valid_hand_notation`). Not a regression.
- HIGH-3: `_action_history_cache_key` doesn't flatten mutable inner values; TypeError if a future caller adds list/dict-typed `amount` field.
- Phase 1: timestamp 1s resolution can collide on rapid back-to-back runs (<1s). PR's own test sleeps 1.05s implicitly acknowledges this. Worth a 1-line millisecond suffix or PID disambiguator.
- Code style: `import logging` inline at lines 998, 1895 of feature_extractor.py; module-top import would be cleaner but harmless.

## Pilot dispatch gate progress (per orchestrator c1a7c0e)

- ✅ Phase 2 HIGH-2 game-side adapter passlist (sealed at game `26fdf57`)
- ⏳ Phase 2 HIGH-1 teaching-side renderer translation (pending teaching builder)
- 🟡 Phase 1 HIGH + Phase 3 HIGH-1/2/3 logic-side (Task 4.5): READY FOR MERGE per this audit; gate clears on merge
- ⏳ HIGH-4 cross-stream coordination on §3.7 aggregate semantics (orchestrator-led; not gating Task 4.5)

After Task 4.5 merges + teaching HIGH-1 fix lands → all 3 cross-stream HIGH fixes shipped → pilot dispatch gate has progressed from 1/3 to 3/3 cross-stream HIGH fixes.

Remaining gate criteria after Task 4.5 + teaching HIGH-1 land:
- Task 5 (Pilot orchestration v1.0) — still queued (Task 4.5 is the gate)
- All 5 prep tasks sealed
- QC pre-pilot sweep clean

## Test class implications

- TC-10 audit-trail integrity **pre-merge variant** — first-run; demonstrated value (compact, focused, surfaces issues BEFORE reviewer dispatch)
- TC-15 multi-expert convergence — fourth demonstration; consistent protocol-diversity outcome
- Adding incident #17 candidate (out-of-scope-related propagation gap pattern) to QC's library

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr21-pre-merge-task4-5.md`
- PR #21: https://github.com/beytell1-sketch/river-rats-v2/pull/21
- Orchestrator Task 4.5 directive: `MAIN_TERMINAL_QC_PHASE3_ACK_TASK4_5_DIRECTIVE_2026-04-26.md` (`c1a7c0e`)
- Phase 1 + 3 findings: `~/river-rats-qc/findings/2026-04-26-{audit-trail-pr5-pr9,commit14-arch-stress}.md`

**Status: QC pre-merge audit COMPLETE. CONVERGED APPROVE. No blocking findings. Orchestrator's dispatched reviewer makes the formal merge call.**
