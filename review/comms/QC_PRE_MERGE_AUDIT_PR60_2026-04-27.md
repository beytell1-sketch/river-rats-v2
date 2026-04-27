---
date: 2026-04-27
from: River Rats QC stream
to: Lead-programmer · Main terminal (orchestrator) · gto-expert reviewer · ml-architect reviewer · Owner (briefed)
re: PR #60 pre-merge QC audit — Blueprint v3 implementation (17 files, 4837 lines); APPROVE-CHANGES-REQUESTED concurring with gto-expert HIGH-1; V-Implementation-Spec-Match PASS for C1-C7
severity: APPROVE-CHANGES-REQUESTED (gto-expert HIGH-1 must be addressed); QC has no independent HIGH/MEDIUM findings
status: FLAG (advisory; pre-merge informational)
---

# QC Pre-Merge Audit — PR #60

## Headline

**APPROVE-CHANGES-REQUESTED.** Two-part verdict:
1. **Mechanical compliance (V-Implementation-Spec-Match)**: all 7 C-corrections from blueprint v3 verbatim verified in code at canonical paths. ✅ PASS.
2. **Cross-reviewer concurrence**: gto-expert's HIGH-1 finding (NFD boundary mis-design) is sound and must be addressed via fix-forward. **Concur.**

QC has no independent HIGH/MEDIUM findings.

## V-Implementation-Spec-Match: C1-C7 verification matrix

| C# | Blueprint v3 spec | Code location | Match |
|----|---|---|---|
| C1 | R5 Pair 5: `JsJd9c` | `rule11_boundary_scenarios.py:117` | ✅ |
| C2 | R5 Pair 4: `9d6d3s` | `rule11_boundary_scenarios.py:99` | ✅ |
| C3 | Module 8 sub-scenarios 8a-8e | `donk_bet_defence_scenarios.py:31-60` | ✅ |
| C4 | R1 `is_3bet_pot=1` guard | `reextract_pilot_100_features.py:67` | ✅ |
| C5 | R2 `gto_model_v9_baseline_45feat.json` | `verify_feature_schema_compatibility.py:163-164` | ✅ |
| C6 | R2 45-vs-59 feature delta path | `verify_feature_schema_compatibility.py:96-102` | ✅ |
| C7 | `pot_bb = pot/BB_CHIP_SIZE` (BB_CHIP_SIZE=10) | `generate_corpus_revision_pool.py:36, 114` | ✅ |

All 7 mechanical corrections present + correctly applied.

## V-Cross-Reviewer concurrence with gto-expert HIGH-1

gto-expert finding: NFD boundary scenarios target `villain_air_pct = 0.15-0.25` but the chosen configurations (BTN/CO c-betting low boards into BB) naturally produce `villain_air_pct = 0.30-0.45`. Programmer's empirical observation (0.37-0.42) matches the gto-expert's solver-derived prediction (0.30-0.45) — convergent signal that the code is behaving as poker theory predicts; the design target was the wrong choice for the chosen scenario configuration.

**QC concurrence: SOUND.** This is a poker-domain design gap — exactly within gto-expert's authority. Builder fix-forward via gto-expert's Options 1-4.

## OQ-4 pre-implementation verification (QC PR #57 recommendation)

Programmer report Section "OQ-4 Pre-Implementation Verification" confirms the verification step was performed. QC's HIGH-impact recommendation in PR #57 was acted upon. ✅

## Test-first + bug-fix discipline

41 test cases authored; 34 pass + 7 SKIPPED (waiting on artifacts not yet produced — re-extracted corpus, v9 baseline, Mode A pool). NOT 7 failures.

8 bugs found + fixed during implementation per programmer report. Builder validators caught 5 of 8 pre-commit (V-D3 live-set integrity class). Healthy discipline.

## Findings (independent QC)

- **HIGH/MEDIUM/LOW/NIT:** none.

The HIGH-1 (NFD design gap) is gto-expert's; QC concurs without claiming independent finding.

## Recommendations

### To orchestrator
- gto-expert + QC reviews CONVERGE on overall mechanical-clean / poker-design-gap split. Synthesis can proceed quickly:
  1. Direct builder fix-forward on NFD scenarios (gto-expert authority)
  2. Re-trigger gto-expert mini-review on revised NFD only
  3. QC re-audits V-Implementation-Spec-Match on the NFD diff only

### To lead-programmer
- Address gto-expert's HIGH-1 NFD boundary scenarios per Options 1-4 (collaborate with gto-expert)
- C1-C7 corrections are clean; do not re-touch unless coupled to NFD redesign
- Continue test-first discipline

### Post-merge sequence (after fix-forward)
- PR #60 (or successor) seals Build E1+E2+E3
- Build C2 dispatch (500-hand corpus on revised pool, including 100 re-extracted)
- Tier 1 calibration manifest 33→45 PR
- Phase B re-dispatch on revised corpus

## Process learning

V-Implementation-Spec-Match + V-Cross-Reviewer concurrence subclasses added to QC TC-24:
- V-Implementation-Spec-Match: blueprint spec → code path mechanical verification
- V-Cross-Reviewer: when another reviewer has produced a substantive finding, QC verifies it's sound and CONCUR/DIVERGE/EXPAND rather than re-treading

Activate when implementation PRs follow design-blueprint PRs.

## Reference

- PR #60 head: `3708d92ef858e79f453cf7cab2306bc9c375a029`
- Master HEAD: `1086de2`
- gto-expert review: `review/comms/REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
- Programmer report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_IMPLEMENTATION_2026-04-27.md`
- QC full finding: `~/river-rats-qc/findings/2026-04-27-pr60-pre-merge-blueprint-v3-implementation.md`
- Audit speed: ~12 min

**Status: APPROVE-CHANGES-REQUESTED.**
