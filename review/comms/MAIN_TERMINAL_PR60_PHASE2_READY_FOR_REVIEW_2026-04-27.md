---
date: 2026-04-27
from: Main terminal (orchestrator)
to: gto-expert · ml-architect · QC stream · Owner (briefed)
re: PR #60 Phase 2 commit (0b97181) ready for round 2 review — F1-F4 applied; gto-expert NFD-diff + ml-architect re-test + QC paired V-Impl-Spec-Match + V-Integration-Trace
status: DIRECTIVE — round 2 review dispatch
---

# PR #60 Phase 2 ready for round 2 review

## What changed

Single Phase 2 commit on `programmer/blueprint-v3-implementation-2026-04-27` branch:

`0b97181` — "Phase 2 (F1-F4): fix Mode A SPR key names, N1 smoke test field, OOP gate bounds, NFD boundary redesign"

| Fix | File | Change |
|-----|------|--------|
| F1 | `river-rats-core/generate_corpus_revision_pool.py` `_generate_mode_a()` | hand_dict keys renamed long → short (`h`, `b`, `st`, `pos`, `tc`, `fb`, `vp`) to match `extract_all_features` schema. Pre-fix: silent KeyError → SPR ≈ 1.25 chip-unit. Post-fix: SPR ≈ 8.33 BB-unit. |
| F2 | `river-rats-core/tests/test_corpus_revision_v3.py` N1 smoke | `r.get('pot_bb', 0)` → `r.get('pot', 0)`. Test was permanently dormant; now actively guards SPR regression. |
| F3 | `scripts/build_corpus_revision_500_hand.py` `_verify_corpus()` | OOP gate tightened from `0.40-0.75` → `0.55-0.65` per spec; ip_pct `0.35-0.45` check added. |
| F4 | `river-rats-core/corpus_revision_scenarios/nfd_scenarios.py` | 5 boundary templates redesigned as turn-decisions per gto-expert spec. Old: BTN/CO c-bet on low boards → 0.37-0.42 air. New: turn-decisions where villain has bet two streets → range self-filtered → target 0.15-0.25 air band. |

## Round 2 review scope

### gto-expert (NFD-diff focused)

- Read `nfd_scenarios.py` head-state for the 5 redesigned boundary templates
- Verify each matches the spec from `REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md`:
  - 5 turn-decision action histories
  - Hero cards / villain positions / boards / turn cards as specified
  - Pot math reflects post-flop-bet turn pot (~20-22 BB)
- Verify R4 ±0.03 gate: at least 3 of 5 redesigned templates pass against their target
- Confirm 4 NFD CALL templates + 4 NFD RAISE templates were NOT touched (in scope: only boundary changes)
- Other modules (1-9 except NFD): no changes expected; just confirm

### ml-architect (re-test of F1/F2/F3)

- F1: generate small Mode A pool (≥20 deals), verify `feat_dict['spr']` distribution is BB-unit (mean in [4, 16], not 0.117-1.25)
- F2: confirm N1 smoke test now exercises the regression check (no longer dormant); pass with valid pool, flag if it can be tricked into a false-pass
- F3: synthetic corpus with 0.42 oop_pct should now FAIL the gate; 0.60 should pass; ip_pct path covered
- Existing 34 tests must remain green
- TC-26 V-Integration-Trace: trace F1 fix from input boundary (Mode A `_generate_mode_a` call) → `extract_all_features` consumption → output feat_dict spr value. Confirm fix value reaches consumer.

### QC stream (paired V-Impl-Spec-Match + V-Integration-Trace)

QC PR #62's TC-26 explicitly applies here — this is the first PR cycle after TC-26 was added. Run the new paired pattern:

- V-Implementation-Spec-Match (TC-24): F1-F4 mechanical landing in code at canonical paths
- V-Integration-Trace (TC-26): F1 fix flows input → extract_all_features → output (the exact failure mode TC-26 was created for)
- V-Cross-Reviewer concurrence: gto-expert NFD-diff + ml-architect F1-F3 re-test verdicts

QC's primary location: `~/river-rats-qc/findings/2026-04-27-pr60-phase2-paired-tc24-tc26.md` (or similar). Mirror to `review/comms/QC_PRE_MERGE_AUDIT_PR60_PHASE2_2026-04-27.md` per Path B pattern.

## Sequencing

```
gto-expert NFD-diff review (parallel)
ml-architect F1/F2/F3 re-test (parallel)
QC paired V-Impl-Spec-Match + V-Integration-Trace (parallel)
        ↓
Three reviews land in review/comms/
        ↓
Orchestrator round 2 synthesis
        ↓
Owner approval → merge PR #60
        ↓
[Build E1 / E2 / E3 / C2 / Tier 1 manifest sequence]
```

## What is NOT changing

- Blueprint v3 unchanged
- v3.2 protocol unchanged
- Mode B factory pool (111 records) unchanged

## References

- PR #60: https://github.com/beytell1-sketch/river-rats-v2/pull/60 (head `0b97181`)
- Phase 2 commit: `0b97181`
- Phase 1 baseline commit: `3708d92`
- Round 1 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
  - QC #61 + #62: master `0f77315` + `8a598e1`
- Round 1 synthesis: `review/comms/MAIN_TERMINAL_PR60_REVIEW_SYNTHESIS_2026-04-27.md` (master `6c1e2ab`)
- Blueprint v3: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` (master `1086de2`)

**Status: PR #60 PHASE 2 READY. Round 2 review dispatch in flight. Orchestrator will synthesize when all 3 reviews land.**
