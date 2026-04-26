---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + careful-engineer reviewer (dedicated subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT v1.0.1 author and NOT prior Stage 4 prep reviewers)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #21 — Stage 4 Task 4.5 logic hardening bundle (`c3efd9c`)
status: APPROVE — All 4 HIGH-severity fixes (3 in feature_extractor.py + audit-runner immutability) correctly implemented + comprehensively tested + M4/M5 baselines preserved. HIGH-3 cache poisoning regression test installed as PERMANENT pilot-gate guard. 4 NITs surfaced (cache-key docstring overpromise; bundle-vs-per-fix commit; pre-existing FEATURE_COLUMNS drift; RERUN_ gitignore). No new MEDIUMs.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/21
branch: stage4-prep/task-4-5-logic-hardening
artifact: c3efd9c (598 ins / 29 del across 5 files + 1 new test file)
predecessor_directive: `c1a7c0e` (QC Phase 3 ACK + Task 4.5)
predecessor_finding: `QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`
---

# Review Verdict — PR #21 (Stage 4 Task 4.5 logic hardening bundle)

## Provenance note

Independent reviewer dispatch under read-only constraint (Read, Grep, Glob, Bash for read-only `git`/`python3`). Did NOT author Task 4.5; did NOT review any prior Stage 4 prep PR. Worked from PR #21 head commit `c3efd9c`. Cross-referenced against Task 4.5 directive (`c1a7c0e`), QC Phase 3 finding, and full diff vs master.

## Builder verification spot-checks

- `git branch --contains c3efd9c` returns only `stage4-prep/task-4-5-logic-hardening` (NOT master) — branch verification held ✓
- 4 acceptance criteria from directive all met (52 new tests + 50 canonical + M4 0/124 + M5 3/3 + HIGH-3 permanent guard)
- Original 04-20 baselines untouched on disk (`stat` shows BUILDER_V24_STAGE35_BACKFILL_AUDIT_2026-04-20.md content unchanged) ✓
- Re-runs go to RERUN_ paths ✓

---

## Item A — HIGH-1: STREET_NAME_MAP whitelist-or-raise

**OK / HIGH confidence.** `_normalise_street()` at `feature_extractor.py:665-682`:
- Rejects None/non-strings up-front with ValueError
- Strips whitespace + lowercases, then whitelists against STREET_NAME_MAP
- Raises ValueError("Unrecognised street: ...") for everything else

All 6 callsite uses of `.get(street_raw, 'flop')` replaced. Verified `grep STREET_NAME_MAP\.get` returns zero hits in `river-rats-core/`. 26/26 tests PASS.

## Item B — HIGH-2: classify_hand raises (Option A)

**OK / HIGH confidence.** `range_narrowing.py:278-321` adds validator + tightened `classify_hand` raises ValueError. Both `feature_extractor.py` callsites (L996, L1893) updated to catch ValueError specifically + log + skip.

Internal callers in `range_narrowing.py` propagate ValueError — corrupt internal range keys surface loudly per Option A design. Confirmed acceptable: those callers consume range dicts built by other range-narrowing functions which only emit valid notation.

8 valid + 11 invalid + 1 end-to-end smoke tests PASS. Pairs-with-modifier rejection (`'JJo'`/`'JJs'`) is one beyond directive — nice catch.

## Item C — HIGH-3: Cache key includes action_history hash (PILOT GATE)

**OK / HIGH confidence.** `_action_history_cache_key()` helper at `feature_extractor.py:629-662` correctly canonicalises tuple/dict-encoded entries. All 3 cache-key sites updated:
- L806 (MW write), L808 (HU write in `_get_chain_narrowed_villain_range`)
- L1774 (HU cache lookup in `extract_range_composition`)
- L1871 (HU cache write)

PERMANENT pilot-gate guard `test_high3_cache_invalidation_on_mutated_action_history` correctly:
- Builds turn-decision hand with prior-street flop CHECK → first extract → records `chain_steps_1`
- Mutates `hand['_action_history']` in place to flop BET → second extract → records `chain_steps_2`
- Sanity-asserts `chain_steps_1` non-empty + hard-asserts inequality

Companion `test_high3_cache_invalidation_distinguishes_check_vs_bet` adds stronger adversarial guard (shared `_chain_cache` dict across 2 hand objects, same villain_pos, different action_history).

`test_must46_cache_hit_via_hand_dict` correctly updated for new 3-tuple cache key shape (prefix-match).

## Item D — Phase 1 HIGH: Audit-runner output immutability

**OK / HIGH confidence.** Both runners have `argparse --out` flag with `_default_report_path()` returning timestamped `review/comms/RERUN_<runner_name>_<UTC-iso>.md`. Default-no-flag re-runs preserve prior outputs. Verified:
- Original 04-20 baseline files UNCHANGED on disk
- RERUN_-prefix files exist for re-run outputs
- Re-run results match baseline byte-for-byte (455/455 multi-street; d2410=0.976, d0182=0.984, d8411=0.661)

4/4 tests PASS (source-level guards + uniqueness across 1.05s sleep).

## Item E — Test results

**OK / HIGH confidence.** Independently re-ran:

| Suite | Result |
|---|---|
| `test_task_4_5_hardening.py` | **52/52 PASS** |
| `test_commit13_sidecar_dryrun.py + test_commit14_finding_b.py + test_range_narrowing_stage35.py` | **50/50 PASS** |
| `test_commit4_atomic.py` (touched by HIGH-3 fix) | **20/20 PASS** |
| M4 audit re-run | 0/124 isolation, 455/455 chain — preserved |
| M5 anchor recheck | 3/3 PASS — preserved |

Note: full `pytest tests/` triggers unrelated SHAP/numpy stack-overflow segfault in `test_explain_hand.py::test_returns_explanation` — NOT a Task 4.5 regression (no SHAP/explain code touched).

## Item F — No new MEDIUMs introduced

**OK / HIGH confidence.**
- HIGH-2 silent-fallback breakage: no internal caller relied on it; the 6 range_narrowing.py consumers iterate dicts they themselves built from valid-notation sources
- Cache-key shape change: only API-visible to `hand['_chain_cache']` introspectors; one such test exists and is updated; grep finds no other consumer
- Audit-runner --out default change: only known consumer is pre-Stage-5 retrain protocol cite-check which reads committed baseline (still on disk, untouched)
- **FEATURE_COLUMNS pre-existing failure CONFIRMED:** `git show master:feature_extractor.py` already had 59 entries (4 v2.4 P1 blocker features) at master; `test_multiway_features.py::TestFeatureContract` asserts 55. Task 4.5 did NOT touch any of these. Author's flag legitimate — separate pre-existing contract drift for QC to triage independently.

## Item G — Author concerns assessment

| Concern | Disposition |
|---|---|
| Pre-existing test_multiway_features.py failure | **Legitimate / NOT Task 4.5.** Surface to QC. Not blocking. |
| Cache key shape change API-visible | **Legitimate / NIT.** Internal-only; one consumer updated. CHANGELOG note when v1.1+ ships. |
| HIGH-2 design choice (Option A) | **Legitimate / Approved.** Quality-default pick; aligns with directive's "fail loudly" intent. |
| RERUN_ artifacts not committed | **Legitimate / NIT.** Transient artifacts per new convention. `.gitignore` entry would prevent future accidents. |

## Item H — Diff scope

**OK / HIGH confidence.** 598 ins / 29 del across 5 files + 1 new file. Each portion justified per fix component. No LOW/NIT scope creep observed.

## Item I — Single commit vs 4 separate commits

**NIT.** Directive specifies "4 separate commits within one PR". Author bundled into one commit citing "logic hardening BUNDLE" framing + clean review surface. Procedural divergence but:
- All 4 fixes logically cohesive
- Tests bundled with code they cover (atomic at fix-level even if not commit-level)
- Review surface is clean
- Risk: future bisect couldn't isolate which of 4 caused regression

Disposition: NIT, not blocking. Surface as feedback to logic builder for per-batch protocol clarification.

## Item J — Branch verification

**OK / HIGH confidence.** `git branch --contains c3efd9c` returns only `stage4-prep/task-4-5-logic-hardening`. Master HEAD is `7acf70d` (orchestrator ACK comm), which does NOT contain `c3efd9c`. Builder's pre-commit branch check held. **Task 4 incident lesson honored.**

## Item K — Ready for orchestrator merge?

**APPROVE.** All 5 acceptance criteria met:
1. ✅ All 4 HIGH-fix tests pass (52/52)
2. ✅ Existing canonical test suite still 50/50 PASS
3. ✅ M4 audit re-run still 0/124 isolation + 455/455 chain
4. ✅ M5 anchor recheck still 3/3 PASS (d8411=0.661 preserved)
5. ✅ HIGH-3 regression test included in canonical suite as PERMANENT pilot-gate guard

HIGH-3 cache poisoning — the live Stage 4 pilot dispatch risk — is empirically fixed and permanently guarded.

---

## VERDICT

**APPROVE — overall confidence HIGH.**

Logic-hardening bundle is correctly scoped, cleanly implemented, comprehensively tested, and successfully gates Stage 4 pilot dispatch on HIGH-3.

**Required fixes:** None.
**Blockers:** None.

## NIT-level observations

1. **N1 (cache-key encoding asymmetry):** `_action_history_cache_key` docstring claims "equivalent histories under different encodings produce equivalent keys" — overpromise. In practice each caller uses one encoding consistently per hand object (different keys = separate cache entries = conservative, not stale-cache risk). Tighten docstring to "different encodings or in-place mutation yield different keys."
2. **N2 (commit granularity):** 4-fix bundle in one commit vs directive's "4 separate commits" wording. Consider clarifying per-batch protocol in PROCESS_GUIDE.md for future BUNDLE-named directives.
3. **N3 (pre-existing finding to surface):** FEATURE_COLUMNS 59-vs-55 contract drift. Separate pre-existing issue. QC should triage.
4. **N4 (transient RERUN_ artifacts):** `.gitignore` entry for `review/comms/RERUN_*.md` would prevent future accidental commits.

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | NIT | Tighten `_action_history_cache_key` docstring per N1 |
| 2 | NIT | Clarify per-batch protocol for BUNDLE directives in PROCESS_GUIDE.md |
| 3 | (separate finding) | FEATURE_COLUMNS 59-vs-55 contract drift — QC triage |
| 4 | NIT | `.gitignore` for `review/comms/RERUN_*.md` |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_21_TASK_4_5_LOGIC_HARDENING_2026-04-26.md`.
2. Post comment on PR #21 referencing the verdict.
3. Stand by for orchestrator merge.
4. Lifts orchestrator's HOLD #21 (HOLD was pending this reviewer pass per `7acf70d`).

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check.
3. Merge PR #21 — APPROVE clean. HIGH-3 pilot-gate now satisfied; Task 5 (Pilot orchestration v1.0) unblocked.

**Owner:** wake to find Task 4.5 logic hardening bundle ready for merge — HIGH-3 cache poisoning fixed + permanently guarded.

## Reference

- PR #21: https://github.com/beytell1-sketch/river-rats-v2/pull/21
- Feature commit: `c3efd9c`
- Task 4.5 directive: `c1a7c0e`
- QC Phase 3 finding: `review/comms/QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`
- Modified files: feature_extractor.py + range_narrowing.py + 2 audit runners + test_commit4_atomic.py
- New test file: `river-rats-core/tests/test_task_4_5_hardening.py`

**FINAL VERDICT: APPROVE — HIGH confidence overall. HIGH-3 pilot-gate satisfied; Task 5 unblocked.**
