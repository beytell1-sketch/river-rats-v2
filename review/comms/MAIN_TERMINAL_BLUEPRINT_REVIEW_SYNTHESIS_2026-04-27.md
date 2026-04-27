---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Architect (Phase 2.5 next dispatch) · ml-architect / gto-expert (reviews acknowledged) · QC stream
re: Blueprint review synthesis — three reviews converge APPROVE-WITH-NITS / APPROVE clean; quality-first defaults applied; architect Phase 2.5 dispatch next to update blueprint with required corrections
status: SYNTHESIS — decisions taken on quality-first defaults; PR #53 will be superseded by updated blueprint after architect Phase 2.5
---

# Blueprint review synthesis (PR #53)

## Three reviews summary

| Reviewer | Verdict | Key findings |
|----------|---------|--------------|
| ml-architect | APPROVE-WITH-NITS | Verified both root-cause bugs against master source line-by-line; required R1 (re-extract 100) + R2 (feature schema check); 3 nits |
| gto-expert | APPROVE-WITH-NITS | 5/7 scenario modules realistic; Module 4 truncation flagged; KB §1.7 + Rule 11 boundary cases GTO-meaningful; 5 missing patterns identified |
| QC | APPROVE clean | All 7 vectors PASS (V-Source-1/2/3/4 + V-X1 + V-X4 + V-Cn-action-distribution); concurs Path A or C; recommends Path A or C over Path B |

## Three-way convergence on Path A (re-extract existing 100 hands)

- **ml-architect (Q3):** re-extract required — corrupted SPR/PFA features create spurious feature split if mixed with corrected new 400 hands; 2-4 dev hours, no relabelling needed (labels tied to game state, not feature vectors)
- **QC (Cross-stream / scope concerns):** Path A or C preferable; Path B has real regime-distribution risk
- **gto-expert (Q7):** 100+400 mix manageable — consistent with Path A (re-extraction makes the mix valid; without it, gto-expert's "manageable" doesn't apply)

**Decision: ADOPT PATH A.** Three-way reviewer convergence + saves $15-25 valid labels + preserves 100 valid poker situations. Path C (discard) is wasteful; Path B (mix as-is) carries known regime-distribution contamination risk.

## Required fixes adopted (all 5 R-items)

All five required fixes from both specialist reviews are adopted as quality-first defaults:

| ID | From | Fix | Adoption reasoning |
|----|------|-----|--------------------|
| R1 | ml-architect | `scripts/reextract_pilot_100_features.py` — re-extract 100 with corrected BB-unit pot conversion + `_opener_position` propagation | Required for Path A; eliminates feature corruption |
| R2 | ml-architect | Pre-training feature schema compatibility check (warm-start base model columns ↔ 59-feature corpus contract) | Cheap insurance against silent feature schema drift; prevents downstream training corruption |
| R3 | gto-expert | Fix Module 4 (multi-street aggression) — extend truncated action histories to river for `villain_aggression_count=2` | Module 4 is currently broken; without R3 the MAGG pattern coverage stratum doesn't actually produce MAGG hands |
| R4 | gto-expert | Post-generation validation of NFD boundary hands' actual `villain_air_pct` (±0.03 tolerance) | Verifies KB §1.7 OVERRIDE boundary cases hit the actual threshold, not just the feature filter |
| R5 | gto-expert | Vary board textures across 5 Rule 11 boundary pairs (≥3 different textures) | Prevents Rule 11 boundary learning from latching to a single texture pattern; produces more general boundary signal |

## Scope additions adopted (2 of 5 gto-expert flagged patterns)

gto-expert flagged 5 patterns the blueprint missed; severity ratings:
- Pattern A (donk-bet defence): **MEDIUM** — adopt
- Pattern E (SB sandwich): **MEDIUM** — adopt
- Pattern B (turn/river check-raise response): LOW — defer to v2 corpus expansion
- Pattern C (river overbet response): LOW — defer
- Pattern D (blocker-driven bluff/fold): LOW — defer

**Decision: ADD 2 NEW SCENARIO MODULES** (donk-bet defence + SB sandwich) to the blueprint's 7 → 9 total. Defer the 3 LOW-severity patterns to a future v2 corpus expansion.

Reasoning: medium-severity gaps fill real role-asymmetries the corpus would otherwise miss (SB-as-hero is 3% of current corpus despite being a real position; donk-bet defence covers a common 3-way line v3.2 doesn't currently scaffold). Low-severity patterns are quality polish; they can be added in a future expansion without blocking initial Tier 2 build.

## Open question dispositions

### Blueprint Q1 (SPR unit consistency) — RESOLVED

Three-way reviewer convergence on Path A. No further owner decision needed; quality-first default chosen.

### Blueprint Q2 (v3.3 protocol revision timing) — DEFERRED PER QC

QC recommendation: wait for Build E source pool generation + sample inspection before committing to v3.3-needed/not-needed. If new corpus surfaces hand classes not covered by v3.2, surface as protocol revision proposal at that point.

**Adopted: defer v3.3 decision until Build E sample inspection.** Don't speculate; let the corpus tell us if v3.2 has gaps.

### Blueprint Q3 (Tier 1 as labelling gate) — INFORMATIONAL ONLY

QC recommendation: Tier 1 33→45 readiness should INFORM Tier 2 mass-labelling kickoff but not strictly gate it.

**Adopted: Tier 1 expansion runs in parallel with Tier 2 labelling, not as strict prerequisite.** Tier 1 is QC harness for protocol; Tier 2 is the training corpus. They're independent artifacts. If Tier 1 expansion surfaces v3.3-required gaps mid-way through Tier 2 labelling, we can pause Tier 2 and address. Better than blocking the critical path on the calibration set.

## Nits (folded into programmer phase, not blocking)

- ml-architect N1: SPR regression assertion in smoke test
- ml-architect N2: Pairwise correlation check (factory pool vs self-play pool)
- ml-architect N3: Forbidden fingerprints incremental update
- gto-expert recommendation: +1-2 MAGG FOLD calibration hands as part of Tier 1 expansion

## Next execution step: Architect Phase 2.5 dispatch

The blueprint at PR #53 needs updating to incorporate the 5 required fixes + 2 scope additions. Options weighed:
- (a) **Architect Phase 2.5 dispatch** — same architect agent updates blueprint cleanly. ~$15-20, 1-2 hours.
- (b) Merge PR #53 as-is and have lead-programmer apply corrections during implementation — risks programmer building to outdated spec; lower quality.
- (c) Reject PR #53 entirely — wasteful; the existing blueprint is 90% correct.

**Decision: Architect Phase 2.5.** The architect agent who wrote the original blueprint is best positioned to make the corrections coherently. Then PR #53 closes; updated blueprint goes through the same review cycle (ml-architect + gto-expert + QC). If reviews converge clean, blueprint merges and lead-programmer dispatches.

Sequencing:
```
PR #53 (current blueprint) → Architect Phase 2.5 (update with 5 R-items + 2 scope additions)
                                    ↓
                          Updated blueprint as new PR
                                    ↓
                  Reviews 2 (ml-architect + gto-expert + QC)
                                    ↓
                          Reviews converge → merge
                                    ↓
                          Lead-programmer dispatch implements
```

Adds one additional review cycle (~$25-30 + 1-2 hours wall-time) but ensures the spec is right before implementation. Quality-first default.

## What is NOT changing

- v3.2 protocol unchanged (v3.3 decision deferred)
- 500 Phase A labels at master `4bce49f` preserved (their feature dicts will be re-extracted via R1, but labels themselves stay)
- XGBoost architecture unchanged
- Tier 3 holdout untouched

## What IS changing (with this synthesis + Architect Phase 2.5)

- Path A re-extraction added to blueprint scope
- Module 4 action histories fixed (R3)
- NFD boundary validation step added (R4)
- Rule 11 boundary cases varied across textures (R5)
- 2 new scenario modules: donk-bet defence + SB sandwich
- Pre-training feature schema compatibility check (R2)
- Blueprint goes from 7 modules → 9 modules

## Cumulative cost

- Today's research + audits + reviews so far: ~$170
- Architect Phase 2.5: ~$15-20
- Reviews 2 (ml-architect + gto-expert + QC): ~$25-30
- **Synthesis-phase total: ~$210-220 / $200 cap**

Slight overage of the original Phase A pilot cap, well within original $700 pilot envelope. Worth flagging to owner that we'll cross $200 before lead-programmer dispatch; original cap was set for Phase A only and we've moved into a different (corpus revision) phase.

## References

- Synthesis upstream: `MAIN_TERMINAL_CORPUS_REVISION_SYNTHESIS_2026-04-27.md` (master `1a5f3e5`, PR #52)
- Blueprint under review: `BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md` (PR #53 head `e635d00`)
- ml-architect review: `REVIEW_ML_ARCHITECT_BLUEPRINT_PR53_2026-04-27.md`
- gto-expert review: `REVIEW_GTO_EXPERT_BLUEPRINT_PR53_2026-04-27.md`
- QC pre-merge audit: `~/river-rats-qc/findings/2026-04-27-pr53-pre-merge-blueprint-corpus-generation.md`
- Range-logic research decision: master `0f66298` (PR #51)
- Memory: `feedback_quality_default_no_ask.md` (always recommend AND execute slow/quality path)

**Status: SYNTHESIS COMPLETE. ARCHITECT PHASE 2.5 DISPATCH NEXT. PATH A + ALL 5 REQUIRED FIXES + 2 SCOPE ADDITIONS ADOPTED.**
