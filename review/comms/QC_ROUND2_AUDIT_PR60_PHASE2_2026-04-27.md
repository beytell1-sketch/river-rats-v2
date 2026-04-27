---
date: 2026-04-27
from: River Rats QC stream
to: Lead-programmer · Main terminal (orchestrator) · gto-expert reviewer · ml-architect reviewer · Owner (briefed)
re: PR #60 Phase 2 round 2 QC audit — F1-F4 fix-forward verified; APPROVE (clean); TC-26 V-Integration-Trace first application validates curative
severity: APPROVE clean
status: FLAG (advisory; pre-merge informational)
---

# QC Round 2 Audit — PR #60 Phase 2 Fix-Forward (F1-F4)

## Headline

**APPROVE clean.** All 4 required fixes (F1-F4) properly applied + integration-verified. Test results: **43 passed + 7 skipped + 0 failed** (up from 34 in Phase 1). New TC-26 V-Integration-Trace vector class applied successfully on first real PR — first application **validates the curative** (incident #20 → TC-26).

## Vector results

| Vector | Result |
|--------|--------|
| V-Implementation-Spec-Match F1 (hand_dict short keys at line 133-149) | ✅ PASS |
| **V-Integration-Trace F1** (key-flow + executable test) | ✅ PASS |
| V-Implementation-Spec-Match F2 (N1 smoke field name) | ✅ PASS |
| V-Implementation-Spec-Match F3 (OOP gate 0.55-0.65 + IP gate 0.35-0.45) | ✅ PASS |
| V-Implementation-Spec-Match F4 (NFD T1-T5 turn-decision templates) | ✅ PASS |
| V-Integration-Trace output record (false positive guard) | ✅ PASS |

## V-Integration-Trace as designed (TC-26 first application)

The new TC-26 V-Integration-Trace vector class (added in QC PR #62 addendum, motivated by incident #20) applied successfully:

**F1 V-Integration-Trace check pattern**:
1. Mechanical match: short-form keys present at call site? ✅
2. Symbolic data-flow check: dict keys signature matches `extract_all_features` expected keys (`pos`, `h`, `b`, `st`, `fb`, `pot`, `tc`, `vp`)? ✅
3. Executable test: exercises fix path AND asserts prior bug is gone? ✅
   - `test_short_form_keys_accepted_by_extract_all_features` (positive)
   - `test_long_form_keys_cause_keyerror` (regression — confirms bug was real)

This is the canonical V-Integration-Trace pattern. Builder's test design (`test_long_form_keys_cause_keyerror`) independently mirrors it — convergence between QC vector design + builder test design = healthy alignment.

## False positive caught

When initially scanning, lines 164-184 of `generate_corpus_revision_pool.py` showed long-form keys (`hero_cards`, `hero_position`, `street`, etc.) which superficially looked like F1 fix incomplete. On closer reading, this is the OUTPUT RECORD `rec` schema (intentional — downstream consumers expect long-form keys in output JSONL). The F1 fix is on the INPUT to `extract_all_features` at lines 133-149, which uses short-form keys correctly.

V-Integration-Trace discriminator: **trace what gets passed to `extract_all_features` specifically, not what gets stored in output schema.**

## NITs (non-blocking)

- **NIT 1 (defensive code)**: bare `except Exception:` at `generate_corpus_revision_pool.py:154` could mask future exceptions if a different error type is introduced. Recommend tightening to `except (KeyError, ValueError, TypeError):`. Cleanup item for next iteration; not blocking.

- **NIT 2 (T5 ceiling)**: T5 NFD template documented as filtered by R4 gate (target 0.25 unreachable; range_analyzer 2-barrel self-filtering caps at ~0.21). T5 included as documented "ceiling data point". Boundary set effectively T1-T4. Recommend gto-expert mini-review on whether 4-template boundary set is acceptable, or whether T5 should be repurposed.

## Findings

- **HIGH/MEDIUM/LOW:** none
- **NIT:** 2 (above)

All 4 required fixes properly applied + integration-verified.

## Recommendations

### To orchestrator + round 2 reviewers (gto-expert + ml-architect + QC)
- **APPROVE merge.** All F1-F4 verified. No HIGH/MEDIUM findings. 2 NITs noted; non-blocking.

### To gto-expert (mini-review on T5 ceiling)
Confirm whether T5 should remain as documented ceiling data point or be replaced with another template (e.g. flop-decision spot to broaden coverage).

### Post-merge sequence
1. PR #60 merges (Build E1 + E2 + E3 sealed)
2. Build C2 dispatch (500-hand corpus on revised pool, 100 re-extracted + 400 new)
3. Tier 1 calibration manifest 33→45 PR
4. Phase B re-dispatch on revised corpus

QC pre-merge audits each via worktree → branch → PR pattern; **vectors paired V-Implementation-Spec-Match + V-Integration-Trace by default** (TC-26 standard).

## Process learning

TC-26 V-Integration-Trace activates whenever a PR's diff introduces a "fix prior bug" code path. Now part of standard QC pre-merge audit checklist. First application validates the curative (incident #20 → TC-26 → applied → caught the false positive correctly + verified the real fix).

## Reference

- PR #60 head (Phase 2): `0b97181d5e561a06ff203a14a5fa87cb2b44436b`
- Master HEAD: `6c1e2ab`
- Programmer Phase 2 report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- QC full finding: `~/river-rats-qc/findings/2026-04-27-pr60-phase2-pre-merge-fix-forward.md`
- Curative learning: `~/river-rats-qc/learning/{incident_pattern_library #20, test_class_registry TC-26, curative_additions_log entry #2}`
- Audit speed: ~10 min

**Status: APPROVE clean. F1-F4 fix-forward verified. TC-26 V-Integration-Trace first application = curative validated.**
